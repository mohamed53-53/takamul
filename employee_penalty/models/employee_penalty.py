""" Initialize Employee penalty """
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning

class EmployeePenalty(models.Model):
    """
        Initialize Employee Penalty:
         -
    """
    _name = 'employee.penalty'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Employee Penalty'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one(
        'hr.employee',
        default=lambda self:self.env['hr.employee'].search(
        [('user_id', '=', self.env.uid)], limit=1),
    )
    pin = fields.Char(related="employee_id.pin")
    penalty_amount = fields.Float(
        compute='_compute_penalty_amount'
    )
    penalty_type = fields.Selection(
        [('hour', 'Hour'),
         ('day', 'Day'),
         ('fixed', 'Fixed')],
        default='hour',
    )
    date = fields.Date(default=fields.Date.today())
    penalty_value = fields.Float()
    contract_id = fields.Many2one(
        'hr.contract',
        related='employee_id.contract_id'
    )
    reason = fields.Html()
    deducted = fields.Boolean(
        readonly=1
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('hr_specialist', 'HR Specialist'),
         ('approve', 'Hr Director Approved'),
         ('cancel', 'Canceled')],
        default='draft',
        string='Status'
    )

    def action_hr_specialist_approve(self):
        self.write({
            'state': 'hr_specialist'
        })

    def action_approve(self):
        """ Action Second Approve """
        # hr_accounting = self.env.ref('employee_bonuses.Allowances_accounting_review_group').users
        # for user in hr_accounting:
        #     self.env['mail.activity'].sudo().create({
        #         'res_id': self.id,
        #         'res_model_id': self.env['ir.model'].search([('model', '=', 'employee.penalty')], limit=1).id,
        #         'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
        #         'user_id': user.id,
        #     })
        self.write({
            'state': 'approve'
        })

    def action_set_draft(self):
        """ Action Set Draft Approve """
        self.write({
            'state': 'draft'
        })

    def action_cancel(self):
        """ Action Cancel """
        self.write({
            'state': 'cancel'
        })

    @api.depends('penalty_type', 'contract_id', 'penalty_value')
    def _compute_penalty_amount(self):
        """ Compute penalty_amount value """
        for rec in self:
            if rec.penalty_type == 'hour':
                rec.penalty_amount = rec.penalty_value * rec.contract_id.day_value/8 if rec.contract_id.day_value > 0 else 0
            if rec.penalty_type == 'day':
                rec.penalty_amount = rec.penalty_value * rec.contract_id.day_value if rec.contract_id.day_value > 0 else 0

            if rec.penalty_type == 'fixed':
                rec.penalty_amount = rec.penalty_value

