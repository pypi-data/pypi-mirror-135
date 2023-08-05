class smp_usage_utils(object):

  __instance = None

  @staticmethod
  def get_instance():
    if smp_usage_utils.__instance is None:
      smp_usage_utils()
    return smp_usage_utils.__instance

  def __init__(self):
    if smp_usage_utils.__instance is not None:
      raise Exception("This class is a singleton!")
    else:
      smp_usage_utils.__instance = self

  def get_reservation_from_cc_and_start(self,parent,cc,start):
    if start and cc:
      reservation_name = cc + '/'+str(start.strftime("%Y%m%d-%H%M"))
      existing_r = parent.env['smp.sm_reservation_compute'].search([
        ('name','=',reservation_name)
      ])
      if existing_r.exists():
        return existing_r[0]
      existing_cc = parent.env['smp.sm_car_config'].search([('name','=',cc)])
      if existing_cc.exists():
        existing_r = parent.env['smp.sm_reservation_compute'].search([
          ('carconfig_id','=',existing_cc[0].id),
          ('startTimechar','=',start.strftime("%Y-%m-%d %H:%M:%S"))
        ])
        if existing_r.exists():
          return existing_r[0]
    return False