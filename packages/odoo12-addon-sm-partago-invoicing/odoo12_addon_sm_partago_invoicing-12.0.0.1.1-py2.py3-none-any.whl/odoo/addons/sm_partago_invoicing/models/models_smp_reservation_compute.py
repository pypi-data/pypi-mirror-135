# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _
from datetime import datetime
from odoo.addons.sm_partago_invoicing.models.models_reservation_calculator import reservation_calculator
from odoo.addons.sm_maintenance.models.models_sm_resources import sm_resources

class smp_reservation_compute(models.Model):
  _inherit = 'smp.sm_reservation_compute'
  _name = 'smp.sm_reservation_compute'

  # invoice_report_id = fields.Many2one('sm.invoice_report', string=_("Related invoice report"))
  report_reservation_compute_id = fields.Many2one('smp.sm_report_reservation_compute', string=_("Report"))

  compute_invoiced = fields.Boolean(string=_("Compute invoiced"))
  compute_forgiven = fields.Boolean(string=_("Compute forgiven"))

  usage_mins_tariff = fields.Float(string=_("Used mins (Tariff)"))
  non_usage_mins_tariff = fields.Float(string=_("Not used mins (Tariff)"))
  extra_usage_mins_tariff = fields.Float(string=_("Extra used mins (Tariff)"))
  usage_mins_nontariff = fields.Float(string=_("Used mins (NONtariff)"))
  non_usage_mins_nontariff = fields.Float(string=_("Not used mins (NONtariff)"))
  extra_usage_mins_nontariff = fields.Float(string=_("Extra used mins (NONtariff)"))
  total_usage_mins_tariff = fields.Float(string=_("Total used mins (tariff-invoice)"))
  total_usage_days_tariff = fields.Float(string=_("Total used days (tariff-invoice)"))
  total_usage_mins_invoiced = fields.Float(string=_("Total used mins (NONtariff-invoice)"))
  total_usage_days_invoiced = fields.Float(string=_("Total used days (NONtariff-invoice)"))
  fuel_consume_invoiced = fields.Float(string=_("Fuel consume (invoice)"))
  used_mileage_invoiced = fields.Float(string=_("Used mileage (invoice)"))

  related_invoice_lines = fields.One2many(comodel_name='account.invoice.line',
    inverse_name='related_reservation_compute_id',
    string=_("Related invoice lines"),
    domain=[('invoice_report_id','=',False)])

  related_invoice_lines_amount_total_cs = fields.Float(string=_("Related invoice lines amount total (Carsharing)"),
    compute="_get_related_invoice_lines_amount_total_cs",store=False)
  related_invoice_lines_amount_total_teletacs = fields.Float(string=_("Related invoice lines amount total (Teletacs)"),
    compute="_get_related_invoice_lines_amount_total_teletacs",store=False)
  reporting_rating_minutes = fields.Float(string=_("Reporting rating minutes"),
    compute="_get_reporting_rating_minutes",store=True)
  reporting_rating_hours = fields.Float(string=_("Reporting rating hours"),
    compute="_get_reporting_rating_hours",store=True)

  @api.depends('related_invoice_lines')
  def _get_related_invoice_lines_amount_total_cs(self):
    for record in self:
      amount_total = 0
      for line in record.related_invoice_lines:
        if line.line_type in ['cs_default','cs_extra']:
          amount_total += line.price_subtotal_signed
      record.related_invoice_lines_amount_total_cs = amount_total

  @api.depends('related_invoice_lines')
  def _get_related_invoice_lines_amount_total_teletacs(self):
    amount_total = 0
    for record in self:
      for line in record.related_invoice_lines:
        if line.line_type in ['cs_teletac']:
          amount_total += line.price_subtotal_signed
      record.related_invoice_lines_amount_total_teletacs = amount_total

  @api.depends('total_usage_mins_invoiced','total_usage_days_invoiced','total_usage_days_tariff','total_usage_mins_tariff')
  def _get_reporting_rating_minutes(self):
    for record in self:
      add_times = False
      # we have time tariffs
      if record.total_usage_days_tariff > 0 or record.total_usage_mins_tariff > 0:
        add_times = True
      else:
        # No time tariffs and money for the non-tariff values
        if record.related_invoice_lines_amount_total_cs > 0:
          add_times = True
      if add_times:
        record.reporting_rating_minutes = record.total_usage_mins_invoiced + record.total_usage_days_invoiced *600

  @api.depends('reporting_rating_minutes')
  def _get_reporting_rating_hours(self):
    for record in self:
      record.reporting_rating_hours = record.reporting_rating_minutes / 60

  def get_analytic_account(self):
    company = self.env.user.company_id
    analytic_account = company.notfound_car_analytic_account_id

    # find a better analytic account for line
    cs_carconfig = self.get_cs_carconfig_obj()
    if cs_carconfig:
      analytic_account = cs_carconfig.analytic_account_id

    return analytic_account

  def get_teletac_analytic_account(self):
    company = self.env.user.company_id
    analytic_account = company.notfound_teletac_analytic_account_id

    # find a better analytic account for line
    cs_carconfig = self.get_cs_carconfig_obj()
    if cs_carconfig:
      analytic_account = cs_carconfig.teletac_analytic_account_id

    return analytic_account

  @api.multi
  def mark_as_forgiven(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        computes = self.env['smp.sm_reservation_compute'].browse(self.env.context['active_ids'])
        if computes.exists():
          for compute in computes:
            compute.write({'compute_forgiven': True})

    return sm_resources.getInstance().get_successful_action_message(self, _('Mark as forgiven done successfully'),
      self._name)

  def apply_min_reservation_time_restriction(self):
    min_reservation_time = 60
    if self.total_usage_mins_tariff == 0 and self.total_usage_days_tariff == 0:
      if self.total_usage_days_invoiced == 0 and self.total_usage_mins_invoiced < min_reservation_time:
        self.write({'total_usage_mins_invoiced':min_reservation_time})

  @api.multi
  def mark_as_toinvoice(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        computes = self.env['smp.sm_reservation_compute'].browse(self.env.context['active_ids'])
        if computes.exists():
          for compute in computes:
            compute.write({
              'compute_forgiven': False,
              'compute_invoiced': False
            })

    return sm_resources.getInstance().get_successful_action_message(self, _('Mark as toInvoice done successfully'),
      self._name)


  @api.multi
  def update_reporing_values_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        computes = self.env['smp.sm_reservation_compute'].browse(self.env.context['active_ids'])
        if computes.exists():
          for compute in computes:
            compute._get_reporting_rating_minutes()

    return sm_resources.getInstance().get_successful_action_message(self, _('Calculate value done successfully'),
      self._name)

  def compute_invoice_report_tariff_time_quantities(self, tariff_model):
    prices = tariff_model.get_prices(self.cs_carconfig_id)
    tariff_day_price = prices['day_price'].product_tmpl_id.list_price
    tariff_min_price = prices['min_price'].product_tmpl_id.list_price
    return self.total_usage_mins_tariff * tariff_min_price + self.total_usage_days_tariff * tariff_day_price

  def compute_invoice_report_nontariff_time_quantities(self, tariff_model):
    prices = tariff_model.get_prices(self.cs_carconfig_id)
    tariff_day_price = prices['day_price'].product_tmpl_id.list_price
    tariff_min_price = prices['min_price'].product_tmpl_id.list_price
    return self.total_usage_mins_invoiced * tariff_min_price + self.total_usage_days_invoiced * tariff_day_price

  def compute_invoice_report_km_quantities(self, tariff_model):
    prices = tariff_model.get_prices(self.cs_carconfig_id)
    tariff_km_price = prices['kms_price'].product_tmpl_id.list_price
    return self.used_mileage_invoiced * tariff_km_price

  def decouple_mins_between_tariff_and_non(self, total_mins, tariff_avals, start_datetime, end_datetime):
    decoupled = {}
    if tariff_avals:
      tariff_avals_mins = self.check_mins_in_tariff(tariff_avals, start_datetime, end_datetime)
      decoupled['tariff'] = tariff_avals_mins
      decoupled['nontariff'] = total_mins - tariff_avals_mins
    else:
      decoupled['tariff'] = 0
      decoupled['nontariff'] = total_mins
    return decoupled

  def check_mins_in_tariff(self, avals_txt, start_datetime, end_datetime):
    mins = 0

    avals = self.prepare_tariff_avals(avals_txt)

    start_initial = {'day': start_datetime.weekday(
    ), 'hour': start_datetime.strftime("%H:%M")}
    end_initial = {'day': end_datetime.weekday(
    ), 'hour': end_datetime.strftime("%H:%M")}

    num_weeks = 0
    if start_datetime.isocalendar()[1] != end_datetime.isocalendar()[1]:
      num_weeks = end_datetime.isocalendar(
      )[1] - start_datetime.isocalendar()[1]

    # TODO: control different years!!!!
    if num_weeks > 0:
      start = start_initial
      start_week = {
        'day': 0,
        'hour': '00:00'
      }
      end_week = {
        'day': 6,
        'hour': '23:59'
      }
      i = 1
      mins = mins + self.check_mins_in_tariff_in_week(avals, start, end_week)

      while i < num_weeks:
        mins = mins + self.check_mins_in_tariff_in_week(avals, start_week, end_week)
        i = i + 1

      mins = mins + self.check_mins_in_tariff_in_week(avals, start_week, end_initial)
    else:
      mins = self.check_mins_in_tariff_in_week(
        avals, start_initial, end_initial)

    return mins

  def check_mins_in_tariff_in_week(self, avals, start, end):
    mins = 0

    for aval_key in avals:
      interval_start = {
        'day': avals[aval_key]['start_day'],
        'hour': avals[aval_key]['start_hour']
      }
      interval_end = {
        'day': avals[aval_key]['end_day'],
        'hour': avals[aval_key]['end_hour']
      }
      if self.week_time_compare(start, '>', interval_start) and self.week_time_compare(start, '<',
        interval_end) and self.week_time_compare(end, '>', interval_start) and \
        self.week_time_compare(end, '<', interval_end):
        mins = mins + self.week_time_diff(start, end)
      else:
        if self.week_time_compare(start, '>', interval_start) and self.week_time_compare(start, '<',
          interval_end):
          mins = mins + self.week_time_diff(start, interval_end)
        else:
          if self.week_time_compare(end, '>', interval_start) and self.week_time_compare(end, '<',
            interval_end):
            mins = mins + self.week_time_diff(interval_start, end)
          else:
            if self.week_time_compare(start, '<', interval_start) and self.week_time_compare(end, '>',
              interval_end):
              mins = mins + self.week_time_diff(interval_start, interval_end)

    return mins

  def prepare_tariff_avals(self, avals_txt):
    aval_dict = {}
    i = 0
    days = avals_txt.split('+')
    for day in days:
      day_range = day.split('-')
      start = day_range[0].split(' ')
      end = day_range[1].split(' ')
      aval_dict[i] = {
        'start_day': self.get_weekday(start[0]),
        'start_hour': start[1],
        'end_day': self.get_weekday(end[0]),
        'end_hour': end[1]
      }
      i = i + 1
    return aval_dict

  def get_weekday(self, day_str):
    if day_str == 'Mon':
      return 0
    if day_str == 'Tue':
      return 1
    if day_str == 'Wed':
      return 2
    if day_str == 'Thu':
      return 3
    if day_str == 'Fri':
      return 4
    if day_str == 'Sat':
      return 5
    if day_str == 'Sun':
      return 6

  def week_time_compare(self, time1, case, time2):
    if case == '<':
      if time1['day'] <= time2['day']:
        if time1['day'] == time2['day']:
          if datetime.strptime(str(time1['hour']), '%H:%M') <= datetime.strptime(str(time2['hour']), '%H:%M'):
            return True
        else:
          return True
    if case == '>':
      if time1['day'] >= time2['day']:
        if time1['day'] == time2['day']:
          if datetime.strptime(str(time1['hour']), '%H:%M') >= datetime.strptime(str(time2['hour']), '%H:%M'):
            return True
        else:
          return True

    return False

  def week_time_diff(self, start, end):
    compute = True
    mins = 0
    i = start['day']
    if i <= end['day']:
      while compute:
        if i != end['day']:
          mins = mins + 24 * 60
          i = i + 1
        else:
          rest = (datetime.strptime(
            str(end['hour']), '%H:%M') - datetime.strptime(str(start['hour']), '%H:%M')).total_seconds() / 60.00
          mins = mins + rest
          compute = False
    return mins

  def autoforgive_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        selected_reservations = self.env['smp.sm_reservation_compute'].browse(self.env.context['active_ids'])
        if selected_reservations.exists():
          for reserv in selected_reservations:
            if reserv.cs_user_type in ['promo','maintenance']:
              reserv.write({'compute_forgiven':True})

  def update_reservation_compute(self, res_params):
    udata = {
      'used_mileage_invoiced': res_params['used_mileage_invoiced'],
      'usage_mins_tariff': res_params['usage_mins_tariff'],
      'non_usage_mins_tariff': res_params['non_usage_mins_tariff'],
      'extra_usage_mins_tariff': res_params['extra_usage_mins_tariff'],
      'usage_mins_nontariff': res_params['usage_mins_nontariff'],
      'non_usage_mins_nontariff': res_params['non_usage_mins_nontariff'],
      'extra_usage_mins_nontariff': res_params['extra_usage_mins_nontariff'],
      'total_usage_mins_invoiced': res_params['invoice_mins_nontariff'],
      'total_usage_days_invoiced': res_params['invoice_days_nontariff'],
      'total_usage_mins_tariff': res_params['invoice_mins_tariff'],
      'total_usage_days_tariff': res_params['invoice_days_tariff'],
      'applied_tariff_id': res_params['applied_tariff_id']
    }

    self.write(udata)

  @api.model
  def compute_report_invoice_vals(self, tariff):
    effectiveStartTime = datetime.strptime(str(self.effectiveStartTime), "%Y-%m-%d %H:%M:%S")
    startTime = datetime.strptime(str(self.startTime), "%Y-%m-%d %H:%M:%S")

    effectiveEndTime = datetime.strptime(str(self.effectiveEndTime), "%Y-%m-%d %H:%M:%S")
    endTime = datetime.strptime(str(self.endTime), "%Y-%m-%d %H:%M:%S")

    res_params = {
      'applied_tariff_id': tariff['tariff_id']
    }

    # Calculate real start for computation
    if effectiveStartTime < startTime:
      real_start = effectiveStartTime
    else:
      real_start = startTime

    # Calculate real end for computation
    if effectiveEndTime < endTime:
      real_end = effectiveEndTime
    else:
      real_end = endTime

    decoupled_mins = self.decouple_mins_between_tariff_and_non(self.usage_mins_invoiced, tariff['tariff_aval'],
      real_start, real_end)
    res_params['usage_mins_tariff'] = decoupled_mins['tariff']
    res_params['usage_mins_nontariff'] = decoupled_mins['nontariff']

    # not used mins
    if endTime >= effectiveEndTime:
      decoupled_mins = self.decouple_mins_between_tariff_and_non(self.non_usage_mins_invoiced,
        tariff['tariff_aval'], effectiveEndTime, endTime)
      res_params['non_usage_mins_tariff'] = decoupled_mins['tariff']
      res_params['non_usage_mins_nontariff'] = decoupled_mins['nontariff']
      res_params['extra_usage_mins_tariff'] = 0
      res_params['extra_usage_mins_nontariff'] = 0

    else:
      decoupled_mins = self.decouple_mins_between_tariff_and_non(self.extra_usage_mins_invoiced,
        tariff['tariff_aval'], endTime, effectiveEndTime)
      res_params['extra_usage_mins_tariff'] = decoupled_mins['tariff']
      res_params['extra_usage_mins_nontariff'] = decoupled_mins['nontariff']
      res_params['non_usage_mins_tariff'] = 0
      res_params['non_usage_mins_nontariff'] = 0

    # Calculate days and minutes
    # fallback values
    company = self.env.user.company_id
    percentage_not_used = 1
    percentage_extra = 1
    kms_included_day = 200
    kms_included_hour = 30

    if company:
      percentage_not_used = company.percentage_not_used / 100
      percentage_extra = company.percentage_extra_minutes_cost / 100
      kms_included_day = company.maxim_kms_per_day
      kms_included_hour = company.maxim_kms_per_hour

    total_mins_reservation_tariff = res_params['usage_mins_tariff'] + percentage_not_used * res_params[
      'non_usage_mins_tariff'] + percentage_extra * res_params['extra_usage_mins_tariff']
    rvals = reservation_calculator.decouple_reservation_days_and_mins(total_mins_reservation_tariff)
    res_params['invoice_days_tariff'] = rvals['days']
    res_params['invoice_mins_tariff'] = rvals['mins']

    total_mins_reservation_nontariff = res_params['usage_mins_nontariff'] + percentage_not_used * res_params[
      'non_usage_mins_nontariff'] + percentage_extra * res_params['extra_usage_mins_nontariff']
    rvals = reservation_calculator.decouple_reservation_days_and_mins(total_mins_reservation_nontariff)
    res_params['invoice_days_nontariff'] = rvals['days']
    res_params['invoice_mins_nontariff'] = rvals['mins']

    # mileage_consume
    total_invoice_days = res_params['invoice_days_tariff'] + res_params['invoice_days_nontariff']
    total_invoice_mins = res_params['invoice_mins_tariff'] + res_params['invoice_mins_nontariff']

    used_mileage_invoiced = self.used_mileage - (kms_included_day * total_invoice_days) - (
      kms_included_hour * reservation_calculator.get_hours_from_minutes(total_invoice_mins))
    if used_mileage_invoiced < 0:
      used_mileage_invoiced = 0
    res_params['used_mileage_invoiced'] = used_mileage_invoiced

    self.update_reservation_compute(res_params)
    self.apply_min_reservation_time_restriction()

smp_reservation_compute()
