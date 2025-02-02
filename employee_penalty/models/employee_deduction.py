""" Initialize Employee bonuses """
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class OtherType(models.Model):
    _name = 'other.deduction.type'

    name = fields.Char()
    code = fields.Char()


class EmployeeDeduction(models.Model):
    _name = 'employee.deduction'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Employee Deduction'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one(
        'hr.employee',
        default=lambda self: self.env['hr.employee'].search(
            [('parent_id', '=', self.env.uid)], limit=1),
    )
    department_id = fields.Many2one('hr.department', related='employee_id.department_id')
    job_id = fields.Many2one('hr.job', related='employee_id.job_id')
    type = fields.Selection(selection=[('utilities', 'Utilities'), ('other', 'Other')], default="other")
    other_type_id = fields.Many2one(comodel_name="other.deduction.type", )
    type_code = fields.Char(related='other_type_id.code', store=True)
    amount_type = fields.Selection(string="Type", selection=[('percentage', 'Percentage'), ('amount', 'Amount')],
                                   default="amount")
    amount = fields.Float(string="Amount",  required=False)
    deduction_amount = fields.Float(string="Amount", compute="compute_deduction_amount")
    date = fields.Date(default=fields.Date.today())
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    move_id = fields.Many2one(comodel_name="account.move", string="journal Entry")
    reason = fields.Text()
    note = fields.Text()
    deducted = fields.Boolean(readonly=1)
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submit'),
         ('approve', 'Approved')],
        default='draft',
        string='Status'
    )
    payslip_id = fields.Many2one('hr.payslip', string="Payslip", readonly=True)

    @api.depends('amount', 'amount_type')
    def compute_deduction_amount(self):
        for rec in self:
            if rec.amount_type == 'percentage':
                rec.deduction_amount = rec.employee_id.contract_id.wage * rec.amount / 100
            else:
                rec.deduction_amount = rec.amount

    def action_submit(self):
        self.write({
            'state': 'submit'
        })

    def action_approve(self):
        self.write({
            'state': 'approve'
        })

    def action_set_draft(self):
        """ Action Set Draft Approve """
        self.write({
            'state': 'draft'
        })
