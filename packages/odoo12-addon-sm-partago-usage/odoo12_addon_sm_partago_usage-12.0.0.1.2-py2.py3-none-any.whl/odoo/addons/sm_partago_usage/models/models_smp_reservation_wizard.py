# -*- coding: utf-8 -*-

from datetime import datetime,timedelta
import pytz
import json

from odoo import models, api,fields
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.addons.sm_connect.models.models_sm_carsharing_db_utils import sm_carsharing_db_utils
from odoo.addons.sm_partago_invoicing.models.models_reservation_calculator import reservation_calculator
from odoo.addons.sm_partago_db.models.models_smp_db_utils import smp_db_utils

def api_compute_reservation_params(parent, res):

  observations = ""
  start_time = datetime.strptime(str(res['startTime']).split('.')[0], '%Y-%m-%dT%H:%M:%S')
  end_time = datetime.strptime(str(res['endTime']).split('.')[0], '%Y-%m-%dT%H:%M:%S')

  fuel_consume = 0.0
  fuel_consume_watts = 0.0
  distance = 0
  tripinfo = res.get('tripInfo')
  if tripinfo:
    if tripinfo.get('effectiveStartTime'):
      effective_start_time = datetime.strptime(str(tripinfo['effectiveStartTime']).split('.')[0], "%Y-%m-%dT%H:%M:%S")

    else:
      effective_start_time = start_time

    if tripinfo.get('effectiveEndTime'):
      effective_end_time = datetime.strptime(str(tripinfo['effectiveEndTime']).split('.')[0], "%Y-%m-%dT%H:%M:%S")
    else:
      effective_end_time = end_time

    duration = (end_time - start_time).total_seconds() / 60.0
    effective_duration = (effective_end_time - effective_start_time).total_seconds() / 60.0

    charged_percentage = tripinfo.get('chargedPercentage') or 0.0
    discharged_percentage = tripinfo.get('dischargedPercentage') or 0.0
    fuel_consume = discharged_percentage - charged_percentage

    charged = tripinfo.get('chargedEnergy') or 0.0
    discharged = tripinfo.get('dischargedEnergy') or 0.0
    fuel_consume_watts = discharged - charged

    distance =tripinfo.get('distance') or 0
  
  final_fuel = 0.0
  end_status = res.get('endStatus')
  if end_status: 
    final_fuel = end_status.get('fuel_level') or 0.0


  current_car = res.get('carId') or -1
  credits = res.get('credits') or 0.0
  price = res.get('price') or 0.0

  return {
    'observations': observations,
    'start_time': start_time,
    'end_time': end_time,
    'effective_start_time': effective_start_time,
    'effective_end_time': effective_end_time,
    'duration': duration,
    'effective_duration': effective_duration,
    'current_car': current_car,
    'fuel_consume': fuel_consume,
    'fuel_consume_watts': fuel_consume_watts,
    'final_fuel_level': final_fuel,
    'credits': credits,
    'price': price,
    'used_mileage': distance
  }

def update_reservation_compute(comp, res_params):
  udata = {
    'observations': res_params['observations'],
    'startTime': res_params['start_time'],
    'endTime': res_params['end_time'],
    'effectiveStartTime': res_params['effective_start_time'],
    'effectiveEndTime': res_params['effective_end_time'],
    'duration': res_params['duration'],
    'effectiveDuration': res_params['effective_duration'],
    'initial_fuel_level': 0.0,
    'final_fuel_level': res_params['final_fuel_level'],
    'fuel_consume': res_params['fuel_consume'],
    'fuel_consume_watts': res_params['fuel_consume_watts'],
    'fuel_consume_invoiced': res_params['fuel_consume_invoiced'],
    'used_mileage': res_params['used_mileage'],
    'observations': res_params['observations'],
    'usage_mins_invoiced': res_params['usage_mins'],
    'non_usage_mins_invoiced': res_params['non_usage_mins'],
    'extra_usage_mins_invoiced': res_params['extra_usage_mins'],
    'current_car': res_params.get('current_car'),
    'credits': res_params.get('credits'),
    'price': res_params.get('price'),
    'compute_cancelled': res_params['compute_cancelled']
  }

  if res_params.get('carconfig_id'):
    udata['carconfig_id'] = res_params['carconfig_id']
  if res_params.get('related_company'):
    udata['related_company'] = res_params['related_company']
  if res_params.get('member_id'):
    udata['member_id'] = res_params['member_id']

  comp.write(udata)


class sm_reservation_wizard(models.TransientModel):
  _name = "smp.sm_reservation_wizard"

  from_q_date = fields.Date(string=_("From"))
  till_q_date = fields.Date(string=_("Till"))
  update_only_car = fields.Boolean(string=_("Update only car"))

  @api.multi
  def create_request(self):
    self.ensure_one()
    self.compute_reservations(self,self.from_q_date,self.till_q_date,update_only_car=self.update_only_car)
    return True

  @staticmethod
  def compute_reservations(parent,from_q=False,till_q=False,update_only_car = False,update_self=False):
    now_date = datetime.now()
    comp = False
    if from_q:
      from_q = from_q.strftime('%Y-%m-%d') + "T00:00:00.00"
    else:
      from_q = now_date.strftime('%Y-%m-%d') + "T00:00:00.00"
    if till_q:
      till_q = till_q.strftime('%Y-%m-%d') + "T00:00:00.00"
    else:
      # tomorrow_date = datetime.now()+ timedelta(days=+1)
      till_q = now_date.strftime('%Y-%m-%d') + "T00:00:00.00"
    app_db_utils = smp_db_utils.get_instance(parent)
    reservations_data_grouped = app_db_utils.get_app_reservations_by_group(parent,from_q,till_q)
    if reservations_data_grouped:
      for reservations_data in reservations_data_grouped.values():
        for reservation in reservations_data:
          res_params = api_compute_reservation_params(parent, reservation)
          res_id = reservation.get("id")
          # If comp exists it means we are trying to update a reservation
          if update_self:
            # We only update the parameter's reservation and nothing else
            if parent.name == res_id:
              comp = parent
          else:
            comp = sm_utils.get_create_existing_model(parent.env['smp.sm_reservation_compute'],
              [('name', '=', res_id)],{'name': res_id, 'compute_invoiced': False,
              'compute_forgiven': False, 'ignore_update': False})
          if comp:
            if update_only_car:
              comp.write({
                'current_car' : res_params['current_car']
              })
            else:
              if not comp.ignore_update and not comp.compute_invoiced and not comp.compute_forgiven:

                cs_person_index = reservation.get("personId")
                if cs_person_index:
                  member = parent.env['res.partner'].search([('cs_person_index', '=', cs_person_index)])
                  if member.exists():
                    res_params['member_id'] = member.id
                    if member.parent_id:
                      res_params['related_company'] = member.parent_id.name
                  else:
                    res_params['observations'] += _("Partner not found for cs_person_index = " + str(reservation.get('personId')) + "And name = " + str(reservation.get('person')) + "\n")
                
                carconfig = reservation.get("resourceId")
                carconfig = parent.env['smp.sm_car_config'].search([('name', '=', carconfig)])
                if carconfig:
                  res_params['carconfig_id'] = carconfig.id
                res_params['compute_cancelled'] = reservation.get('isCancelled')

                res_params['fuel_consume_invoiced'] = 0
                
                new_calculated_attributes = reservation_calculator.get_general_values(res_params,'list')

                res_params['usage_mins'] = new_calculated_attributes['usage_mins']
                res_params['non_usage_mins'] = new_calculated_attributes['non_usage_mins']
                res_params['extra_usage_mins'] = new_calculated_attributes['extra_usage_mins']

                update_reservation_compute(comp, res_params)

          # on each iteration we reset comp for being setup again
          comp = False