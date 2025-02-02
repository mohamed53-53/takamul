# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError

class Loan(models.Model):
    _inherit = 'hr.loan'

    is_rescheduled = fields.Boolean(string="IS Rescheduled ?", )
    loan_type_id = fields.Many2one(comodel_name="loan.type")

    def action_submit(self):
        for rec in self:
            active_loans = self.search([('employee_id', '=', rec.employee_id.id), ('balance_amount', '>', 0),
                                        ('state', '=', 'approve')])
            if active_loans:
                raise ValidationError("Employee Cannot Have More Than One Active Loan !!!")
            rec.write({'state': 'waiting_approval_1'})

    @api.onchange('employee_id', 'loan_amount', 'installment')
    def onchange_employee_loan(self):
        for rec in self:
            active_loans = self.search([('employee_id', '=', rec.employee_id.id), ('balance_amount', '>', 0),
                                        ('state', '=', 'approve')])
            if active_loans:
                raise ValidationError("Employee Cannot Have More Than One Active Loan !!!")
            if rec.employee_id and rec.employee_id.contract_id and rec.employee_id.project_id:
                loan_installments = rec.employee_id.project_id.max_loan_installments
                loan_amount = (rec.employee_id.project_id.max_loan_percentage / 100 * rec.employee_id.contract_id.rule_ids.filtered(lambda m: m.rule_id.code == 'BASIC').total_value)
                if rec.employee_id.contract_id.date_end and (((rec.employee_id.contract_id.date_end.year - fields.Date.today().year) * 12) + rec.employee_id.contract_id.date_end.month - fields.Date.today().month) <= loan_installments:
                    loan_installments = (((rec.employee_id.contract_id.date_end.year - fields.Date.today().year) * 12) + rec.employee_id.contract_id.date_end.month - fields.Date.today().month)
                if rec.installment > loan_installments:
                    raise ValidationError("Employee Can Have A Maximum Installments Of %s" % loan_installments)
                if rec.loan_amount > loan_amount:
                    raise ValidationError("Employee Can Have A Maximum Loan Amount Of %s" % loan_amount)
                if not rec.installment:
                    rec.installment = loan_installments

    @api.constrains('loan_amount','employee_id.contract_id.basic_salary')
    def check_loan_type(self):
        wage = 0
        for line in self.employee_id.contract_id.rule_ids.filtered(lambda r: r.rule_id.code == 'BASIC'):
            wage += line.total_value
        if not wage:
            wage = self.employee_id.contract_id.wage


class LoanLine(models.Model):
    _inherit = 'hr.loan.line'

    def action_installment_reschedule(self):
        if self.paid:
            raise exceptions.ValidationError('Can not reschedule paid installment !')
        view = self.env.ref('ohrms_loan.loan_line_wizard')
        return {
            'name': _('Installment Reschedule'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'loan.line.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {
                'default_old_amount': self.amount,
                'default_new_date': self.date,
                'default_amount': self.amount,
                'default_loan_line_id': self.id,
                'default_loan_id': self.loan_id.id
            }
        }
