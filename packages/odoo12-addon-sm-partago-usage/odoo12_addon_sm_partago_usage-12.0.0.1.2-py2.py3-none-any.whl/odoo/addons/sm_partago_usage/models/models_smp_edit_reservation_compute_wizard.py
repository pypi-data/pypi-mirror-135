# -*- coding: utf-8 -*-

from datetime import datetime
import pytz

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils



class sm_edit_reservation_compute_wizard(models.TransientModel):
  _name = "smp.sm_edit_reservation_compute_wizard"

  def get_default_startTime(self):
    current_reservation = self.get_context_current_reservation()
    if current_reservation:
      return current_reservation.startTime
    return False
    
  def get_default_effectiveStartTime(self):
    current_reservation = self.get_context_current_reservation()
    if current_reservation:
      return current_reservation.effectiveStartTime
    return False
    
  def get_default_endTime(self):
    current_reservation = self.get_context_current_reservation()
    if current_reservation:
      return current_reservation.endTime
    return False
    
  def get_default_effectiveEndTime(self):
    current_reservation = self.get_context_current_reservation()
    if current_reservation:
      return current_reservation.effectiveEndTime
    return False

  startTime = fields.Char(string='Start Time', readonly=False, default=get_default_startTime)
  effectiveStartTime = fields.Char(string='Effective Start Time', readonly=False, default=get_default_effectiveStartTime)
  endTime = fields.Char(string='End Time', readonly=False, default=get_default_endTime)
  effectiveEndTime = fields.Char(string='Effective End Time', readonly=False, default=get_default_effectiveEndTime)

  def get_context_current_reservation(self):
    try:
      active_reservation_id = self.env.context['active_id']
    except:
      active_reservation_id = False
    return  self.env['smp.sm_reservation_compute'].browse(active_reservation_id)

  def return_utc_time(self,datetime_data):
    mad_tz = pytz.timezone('Europe/Madrid')
    utc_tz = pytz.timezone('UTC')
    
    dt = datetime.now()
    
    if datetime_data:
      dt = datetime.strptime(str(datetime_data), "%Y-%m-%d %H:%M:%S")

    # Localizing the datetimes to the current timezone
    mad_time = mad_tz.localize(dt)

    # Localizing the datetimes to the UTC standard
    utc_time = mad_time.astimezone(utc_tz)

    # Setting up the fields in the wizard view
    print("UTC_TIME")
    print(utc_time)
    return utc_time

  @api.multi
  def create_request(self):
    self.modify_dates()
    return True
        
  @api.model
  def modify_dates(self):

    st = datetime.strptime(str(self.startTime), "%Y-%m-%d %H:%M:%S")
    efst = datetime.strptime(str(self.effectiveStartTime), "%Y-%m-%d %H:%M:%S")
    et = datetime.strptime(str(self.endTime), "%Y-%m-%d %H:%M:%S")
    efet = datetime.strptime(str(self.effectiveEndTime), "%Y-%m-%d %H:%M:%S")

    # --- NOT IN USE --- #
    mad_tz = pytz.timezone('Europe/Madrid')
    utc_tz = pytz.timezone('UTC')
    
    utc_time_st = utc_tz.localize(st)
    utc_time_efst = utc_tz.localize(efst)
    utc_time_et = utc_tz.localize(et)
    utc_time_efet = utc_tz.localize(efet)

    # Convert time zone
    mad_time_st = utc_time_st.astimezone(mad_tz)
    mad_time_efst = utc_time_efst.astimezone(mad_tz)
    mad_time_et = utc_time_et.astimezone(mad_tz)
    mad_time_efet = utc_time_efet.astimezone(mad_tz)
    # --- NOT IN USE --- #

    current_reservation = self.get_context_current_reservation()

    if current_reservation:
      current_reservation.write({
        'startTime': st,
        'effectiveStartTime': efst,
        'endTime': et,
        'effectiveEndTime': efet,
        'ignore_update': True,
      })
      
    return True
