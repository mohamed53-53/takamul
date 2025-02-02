# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class HrLoan(models.Model):
    _name = 'hr.loan'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']
    _description = "Loan Request"

    def _compute_loan_amount(self):
        total_paid = 0.0
        for loan in self:
            for line in loan.loan_lines:
                if line.paid:
                    total_paid += line.amount
            balance_amount = loan.loan_amount - total_paid
            loan.total_amount = loan.loan_amount
            loan.balance_amount = balance_amount
            loan.total_paid_amount = total_paid

    name = fields.Char(string="Loan Name", default="/", readonly=True, help="Name of the loan")
    date = fields.Date(string="Date", default=fields.Date.today(), readonly=True, help="Date")
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, help="Employee")
    department_id = fields.Many2one('hr.department', related="employee_id.department_id", readonly=True,
                                    string="Department", help="Employee")
    installment = fields.Integer(string="No Of Installments", help="Number of installments")
    payment_date = fields.Date(string="Payment Start Date", required=True, default=fields.Date.today(), help="Date of "
                                                                                                             "the "
                                                                                                             "paymemt")
    loan_lines = fields.One2many('hr.loan.line', 'loan_id', string="Loan Line", index=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True, help="Company",
                                 default=lambda self: self.env.company,
                                 states={'draft': [('readonly', False)]})
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, help="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id)
    job_position = fields.Many2one('hr.job', related="employee_id.job_id", readonly=True, string="Job Position",
                                   help="Job position")
    loan_amount = fields.Float(string="Loan Amount", required=True, help="Loan amount")
    total_amount = fields.Float(string="Total Amount", store=True, readonly=True, compute='_compute_loan_amount',
                                help="Total loan amount")
    balance_amount = fields.Float(string="Remaining Amount", store=True, compute='_compute_loan_amount',
                                  help="Remaining amount")
    total_paid_amount = fields.Float(string="Total Paid Amount", store=True, compute='_compute_loan_amount',
                                     help="Total paid amount")

    state = fields.Selection([], string="State", default='draft', track_visibility='onchange', copy=False, )

    @api.model
    def create(self, values):
        # loan_count = self.env['hr.loan'].search_count(
        #     [('employee_id', '=', values['employee_id']), ('state', '=', 'approve'),
        #      ('balance_amount', '!=', 0)])
        # if loan_count:
        #     raise ValidationError(_("The employee has already a pending installment"))
        # else:
        values['name'] = self.env['ir.sequence'].get('hr.loan.seq') or '/'
        res = super(HrLoan, self).create(values)
        return res

    def compute_installment(self):
        """This automatically create the installment the employee need to pay to
        company based on payment start date and the no of installments.
            """
        for loan in self:
            loan.loan_lines.unlink()
            date_start = datetime.strptime(str(loan.payment_date), '%Y-%m-%d')
            amount = loan.loan_amount / loan.installment
            for i in range(1, loan.installment + 1):
                self.env['hr.loan.line'].create({
                    'date': date_start,
                    'amount': amount,
                    'employee_id': loan.employee_id.id,
                    'loan_id': loan.id})
                date_start = date_start + relativedelta(months=1)
            loan._compute_loan_amount()
        # if self.original_loan_id and self.env.context.get('reschedule'):
        #     return {
        #         'context': self.env.context,
        #         'name': _('Reschedule Loan'),
        #         'res_model': 'hr.loan',
        #         'view_mode': 'form',
        #         'view_type': 'form',
        #         'view_id': self.env.ref('ohrms_loan.reschedule_loan_form_view').id,
        #         'res_id': self.id,
        #         'type': 'ir.actions.act_window',
        #         'target': 'new',
        #     }


    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    def action_reject(self, reason=None):
        self.write({'state': 'rejected'})
        if reason:
            self.message_post(body=reason, subject="Reject Reason")


    def unlink(self):
        for loan in self:
            if loan.state not in ('draft', 'cancel'):
                raise UserError(
                    'You cannot delete a loan which is not in draft or cancelled state')
        return super(HrLoan, self).unlink()


class InstallmentLine(models.Model):
    _name = "hr.loan.line"
    _description = "Installment Line"

    date = fields.Date(string="Payment Date", required=True, help="Date of the payment")
    employee_id = fields.Many2one('hr.employee', string="Employee", help="Employee")
    amount = fields.Float(string="Amount", required=True, help="Amount")
    amount_rel = fields.Float()
    paid = fields.Boolean(string="Paid", help="Paid")
    loan_id = fields.Many2one('hr.loan', string="Loan Ref.", help="Loan")
    payslip_id = fields.Many2one('hr.payslip', string="Payslip Ref.", help="Payslip")
    is_last_installment = fields.Boolean(compute="check_last_installment", store=True)

    @api.depends('loan_id')
    def check_last_installment(self):
        for rec in self:
            dates = rec.loan_id.loan_lines.mapped('date')
            if dates:
                if rec.date == max(dates):
                    rec.is_last_installment = True
                else:
                    rec.is_last_installment = False
            else:
                rec.is_last_installment = False

    def action_show_details(self):
        view = self.env.ref('ohrms_loan.loan_line_wizard')
        return {
            'name': _('Loan Line Details'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'loan.line.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {'default_old_amount': self.amount, 'default_amount': self.amount,
                        'default_loan_line_id': self.id,
                        'default_loan_id': self.loan_id.id}
        }

    @api.onchange('amount')
    def onchange_amount(self):
        for rec in self:
            rec.amount_rel = rec.amount


class HrEmployee(models.AbstractModel):
    _inherit = "hr.employee.base"

    def _compute_employee_loans(self):
        """This compute the loan amount and total loans count of an employee.
            """
        self.loan_count = self.env['hr.loan'].search_count([('employee_id', '=', self.id)])

    loan_count = fields.Integer(string="Loan Count", compute='_compute_employee_loans')
