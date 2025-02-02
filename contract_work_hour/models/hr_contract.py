""" Initialize Hr Contract """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class HrContract(models.Model):
    """
        Inherit Hr Contract:
         -
    """
    _inherit = 'hr.contract'

    no_month_days = fields.Float()
    hour_value = fields.Float()
    day_value = fields.Float(compute='_compute_day_value')
    workday_hours = fields.Float(default=8)

    # @api.depends('hour_value', 'workday_hours')
    # def _compute_day_value(self):
    #     """ Compute day_value value """
    #     for rec in self:
    #         rec.day_value = rec.hour_value * rec.workday_hours

    @api.depends('wage', 'no_month_days','workday_hours')
    def _compute_day_value(self):
        """ Compute day_value value """
        for rec in self:
            wage = 0
            for line in rec.rule_ids.filtered(lambda r: r.rule_id.is_social_rule):
                wage += line.total_value
            if not wage:
                wage = rec.wage
            rec.day_value = wage / rec.no_month_days if rec.no_month_days > 0 else 0
            rec.hour_value = wage / rec.no_month_days / rec.workday_hours if rec.no_month_days > 0 else 0


