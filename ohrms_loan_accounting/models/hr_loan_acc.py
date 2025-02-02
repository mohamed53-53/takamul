# -*- coding: utf-8 -*-
import time
from odoo import models, api, fields
from odoo.exceptions import UserError


class HrLoanAcc(models.Model):
    _inherit = 'hr.loan'

    employee_account_id = fields.Many2one('account.account', string="Loan Account")
    treasury_account_id = fields.Many2one('account.account', string="Treasury Account")
    journal_id = fields.Many2one('account.journal', string="Journal")

    state = fields.Selection([])

    def action_loan_pay(self):
        unpaid_amount = sum([line.amount for line in self.loan_lines if not line.paid])
        return {
            'context': {'default_unpaid_amount': unpaid_amount,
                        'default_loan_id': self.id},
            'name': 'Pay Loan',
            'res_model': 'register.loan.payment',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('ohrms_loan_accounting.register_loan_payment_form').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def action_approve(self):
        """This create account move for request.
            """


        if self.state == 'waiting_approval_1':
            loan_approve = self.env['ir.config_parameter'].sudo().get_param('account.loan_approve')
            contract_obj = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
            if not contract_obj:
                raise UserError('You must Define a contract for employee')
            elif not self.loan_lines:
                raise UserError('You must compute installment before Approved')
            elif loan_approve:
                self.write({'state': 'waiting_approval_2'})


            if not self.employee_account_id or not self.treasury_account_id or not self.journal_id:
                raise UserError("You must enter employee account & Treasury account and journal to approve ")
            if not self.loan_lines:
                raise UserError('You must compute Loan Request before Approved')
            timenow = time.strftime('%Y-%m-%d')
            for loan in self:
                amount = loan.loan_amount
                loan_name = loan.employee_id.name
                reference = loan.name
                journal_id = loan.journal_id.id
                debit_account_id = loan.employee_account_id.id
                credit_account_id = loan.treasury_account_id.id
                debit_vals = {
                    'name': loan_name,
                    'account_id': debit_account_id,
                    'journal_id': journal_id,
                    'date': timenow,
                    'partner_id': loan.employee_id.address_home_id.id,
                    'debit': amount > 0.0 and amount or 0.0,
                    'credit': amount < 0.0 and -amount or 0.0,
                    'loan_id': loan.id,
                }
                credit_vals = {
                    'name': loan_name,
                    'account_id': credit_account_id,
                    'journal_id': journal_id,
                    'partner_id': loan.employee_id.address_home_id.id,
                    'date': timenow,
                    'debit': amount < 0.0 and -amount or 0.0,
                    'credit': amount > 0.0 and amount or 0.0,
                    'loan_id': loan.id,
                }
                vals = {
                    'narration': loan_name,
                    'ref': reference,
                    'journal_id': journal_id,
                    'partner_id': loan.employee_id.address_home_id.id,
                    'date': timenow,
                    'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
                }
                move = self.env['account.move'].create(vals)
                move.post()
            super(HrLoanAcc, self).action_approve()
        elif self.state == 'waiting_approval_2':
            if not self.employee_account_id or not self.treasury_account_id or not self.journal_id:
                raise UserError("You must enter employee account & Treasury account and journal to approve ")
            if not self.loan_lines:
                raise UserError('You must compute Loan Request before Approved')
            timenow = time.strftime('%Y-%m-%d')
            for loan in self:
                amount = loan.loan_amount
                loan_name = loan.employee_id.name
                reference = loan.name
                journal_id = loan.journal_id.id
                debit_account_id = loan.employee_account_id.id
                credit_account_id = loan.treasury_account_id.id
                debit_vals = {
                    'name': loan_name,
                    'account_id': debit_account_id,
                    'journal_id': journal_id,
                    'date': timenow,
                    'partner_id': loan.employee_id.address_home_id.id,
                    'debit': amount > 0.0 and amount or 0.0,
                    'credit': amount < 0.0 and -amount or 0.0,
                    'loan_id': loan.id,
                }
                credit_vals = {
                    'name': loan_name,
                    'account_id': credit_account_id,
                    'journal_id': journal_id,
                    'date': timenow,
                    'partner_id': loan.employee_id.address_home_id.id,
                    'debit': amount < 0.0 and -amount or 0.0,
                    'credit': amount > 0.0 and amount or 0.0,
                    'loan_id': loan.id,
                }
                vals = {
                    'narration': loan_name,
                    'ref': reference,
                    'journal_id': journal_id,
                    'partner_id': loan.employee_id.address_home_id.id,
                    'date': timenow,
                    'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
                }
                move = self.env['account.move'].create(vals)
                move.post()
            super(HrLoanAcc, self).action_approve()
            # if self.original_loan_id:
            #     for line in self.original_loan_id.loan_lines:
            #         line.paid = True
           
            return True
        elif self.state == 'draft':
            self.write({'state':'waiting_approval_1'})
    def _compute_loan_amount(self):
        total_paid = 0.0
        for loan in self:
            for line in loan.loan_lines:
                total_paid += line.paid_amount
            balance_amount = loan.loan_amount - total_paid
            loan.total_amount = loan.loan_amount
            loan.balance_amount = balance_amount
            loan.total_paid_amount = total_paid


class HrLoanLineAcc(models.Model):
    _inherit = "hr.loan.line"

    paid_amount = fields.Float(string="Paid Amount", required=False, )

    def action_paid_amount(self):
        """This create the account move line for payment of each installment.
            """
        timenow = time.strftime('%Y-%m-%d')
        for line in self:
            if line.loan_id.state != 'approve':
                raise UserError("Loan Request must be approved")
            amount = line.amount - line.paid_amount
            loan_name = line.employee_id.name
            reference = line.loan_id.name
            journal_id = line.loan_id.journal_id.id
            debit_account_id = line.loan_id.treasury_account_id.id
            credit_account_id = line.loan_id.employee_account_id.id
            debit_vals = {
                'name': loan_name,
                'account_id': debit_account_id,
                'journal_id': journal_id,
                'partner_id': line.loan_id.employee_id.partner_id.id,
                'date': timenow,
                'debit': amount > 0.0 and amount or 0.0,
                'credit': amount < 0.0 and -amount or 0.0,
            }
            credit_vals = {
                'name': loan_name,
                'account_id': credit_account_id,
                'journal_id': journal_id,
                'date': timenow,
                'partner_id': line.loan_id.employee_id.partner_id.id,
                'debit': amount < 0.0 and -amount or 0.0,
                'credit': amount > 0.0 and amount or 0.0,
            }
            vals = {
                'narration': loan_name,
                'ref': reference,
                'journal_id': journal_id,
                'partner_id': line.loan_id.employee_id.partner_id.id,
                'date': timenow,
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
            }
            move = self.env['account.move'].create(vals)
            move.post()
            line.paid_amount = amount
        return True


class HrPayslipAcc(models.Model):
    _inherit = 'hr.payslip'



    @api.onchange('employee_id')
    def do_employee_loan(self):
        employee = self.employee_id
        date_from = self.date_from
        date_to = self.date_to
        payslip_input_type_id = self.env.ref('ohrms_loan.hr_payslip_input_type_loan')
        if date_from and date_to and employee and payslip_input_type_id:
            lon_obj = self.env['hr.loan'].search([('employee_id', '=', employee.id), ('state', '=', 'approved')])
            print(lon_obj,'<=====')
            total_loan = 0.0
            lst_loans = []
            for loan in lon_obj:
                for loan_line in loan.loan_lines:
                    if date_from <= loan_line.date <= date_to and not loan_line.paid:
                        total_loan += loan_line.amount - loan_line.paid_amount
                        lst_loans.append((6, 0, loan_line.ids))
            updated = False
            x = lst_loans
            if self.input_line_ids:
                for input_line in self.input_line_ids:
                    if payslip_input_type_id == input_line.input_type_id:
                        input_line.amount = total_loan
                        input_line.loan_line_id = lst_loans
                        updated = True
            if not updated:
                self.input_line_ids = [(0, 0, {
                    'input_type_id': payslip_input_type_id.id,
                    'loan_line_id': lst_loans,
                    'amount': total_loan,
                })]
                print(' self.input_line_ids', self.input_line_ids)
    @api.onchange('employee_id', 'struct_id', 'contract_id', 'date_from', 'date_to')
    def _onchange_employee(self):
        super(HrPayslipAcc, self)._onchange_employee()
        employee = self.employee_id
        date_from = self.date_from
        date_to = self.date_to
        payslip_input_type_id = self.env.ref('ohrms_loan.hr_payslip_input_type_loan')

        if date_from and date_to and employee and payslip_input_type_id:
            lon_obj = self.env['hr.loan'].search([('employee_id', '=', employee.id), ('state', '=', 'approved')])
            print(lon_obj,'<=====')
            total_loan = 0.0
            lst_loans = []
            for loan in lon_obj:
                for loan_line in loan.loan_lines:
                    if date_from <= loan_line.date <= date_to and not loan_line.paid:
                        total_loan += loan_line.amount - loan_line.paid_amount
                        lst_loans.append((6, 0, loan_line.ids))
            updated = False
            x = lst_loans
            if self.input_line_ids:
                for input_line in self.input_line_ids:
                    if payslip_input_type_id == input_line.input_type_id:
                        input_line.amount = total_loan
                        input_line.loan_line_id = lst_loans
                        updated = True
            if not updated:
                self.input_line_ids = [(0, 0, {
                    'input_type_id': payslip_input_type_id.id,
                    'loan_line_id': lst_loans,
                    'amount': total_loan,
                })]
                print(' self.input_line_ids', self.input_line_ids)
    def action_payslip_done(self):
        for line in self.input_line_ids:
            if line.loan_line_id:
                line.loan_line_id.action_paid_amount()
                if line.amount >= line.loan_line_id.amount:
                    line.loan_line_id.paid = True
                    line.loan_line_id.paid_amount = line.amount
                line.loan_line_id.loan_id._compute_loan_amount()
        return super(HrPayslipAcc, self).action_payslip_done()
