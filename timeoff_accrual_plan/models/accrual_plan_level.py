from odoo import api, fields, models


class AccrualPlanLevel(models.Model):
    _inherit = 'hr.leave.accrual.level'

    action_with_unused_accruals = fields.Selection(
        [('postponed', 'Transferred to the next year (Days)'),
         ('postponed_amount', 'Transferred to the next year (Amount)'),
         ('lost', 'Lost')],
        string="At the end of the calendar year, unused accruals will be",
        default='postponed', required='True')

    max_postponed_days = fields.Integer(string="Max. Transferred days", required=False, )
    max_postponed_amount = fields.Float(string="Max. Transferred amount", required=False, )


class Project(models.Model):
    _inherit = 'project.project'

    action_with_unused_accruals = fields.Selection(
        [('postponed', 'Transferred to the next year (Days)'),
         ('postponed_amount', 'Transferred to the next year (Amount)'),
         ('lost', 'Lost')],
        string="At the end of the calendar year, unused accruals will be",
        default='postponed', required='True')
    no_of_allocation_days = fields.Integer(string="No. Of Days", default=0)
