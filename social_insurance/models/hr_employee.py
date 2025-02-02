from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
import datetime


class Employee(models.Model):
    _inherit = 'hr.employee'

    is_insured = fields.Boolean(string="Is Insured", readonly=True)
    social_insurance_number = fields.Char(string="Number",)
    status = fields.Selection([
        ('in', 'Insured'),
        ('out', 'Outsource'),
    ])
    insurance_start_date = fields.Date(string="Start Date",readonly=True)
    insurance_end_date = fields.Date(string="End Date", )
    gosi_id = fields.Many2one(comodel_name='gosi.hire', string='Related GOSI')
    time_off_days = fields.Float(string="Annual Leave Days", )
    time_off_months = fields.Float(string="No. Of Months", default=11)
    monthly_balance = fields.Float(compute="compute_monthly_balance", store=True, reverse="set_monthly_balance",
                                   readonly=False)
    monthly_balance_value = fields.Float(string="Monthly Balance Value", compute="compute_time_off_day_value")

    @api.depends('time_off_months', 'time_off_days')
    def compute_monthly_balance(self):
        for rec in self:
            if rec.time_off_months > 0:
                rec.monthly_balance = rec.time_off_days / rec.time_off_months
            else:
                rec.monthly_balance = 0

    @api.depends('monthly_balance', 'contract_id.day_value')
    def compute_time_off_day_value(self):
        for rec in self:
            rec.monthly_balance_value = rec.contract_id.day_value * rec.monthly_balance

    def set_monthly_balance(self):
        print("Set Monthly Balance")

    @api.onchange('project_id')
    def _onchange_project_id(self):
        self.project_owner_id = self.project_id.owner_id.id
