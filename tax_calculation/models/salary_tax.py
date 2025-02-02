# -*- coding: utf-8 -*-
from __future__ import division
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError
from odoo.addons.hr_payroll.models.browsable_object import BrowsableObject, InputLine, WorkedDays, Payslips


class SalaryTax(models.Model):
    _inherit = 'hr.payslip'

    tax_rule_ids = fields.Many2many(comodel_name="salary.tax.rule", string="Tax Computation",
                                    relation='hr_tax_rule_rel', compute='_onchange_tax_employee_id')
    tax_amount = fields.Float(string="Tax Amount", required=False, )
    payslip_tax_type = fields.Selection(string="Tax Type", help="Compute Tax For Employee On Payslip",
                                        selection=[('annual', 'Annually'), ('month', 'Monthly'), ], required=False,
                                        default='month')
    is_apply_tax = fields.Boolean(string="Apply Tax",compute="check_apply_tax")

    @api.depends('employee_id')
    def check_apply_tax(self):
        for pay in self:
            if pay.employee_id.contract_id.apply_tax:
                pay.is_apply_tax = True
            else:
                pay.is_apply_tax = False

    @api.onchange('employee_id')
    def _onchange_tax_employee_id(self):
        taxes = self.env['salary.tax.rule'].search([]).ids
        self.tax_rule_ids = taxes

    @api.model
    def create(self, vals):
        res = super(SalaryTax, self).create(vals)
        taxes = self.env['salary.tax.rule'].search([]).ids
        res.tax_rule_ids = taxes
        return res

    def compute_sheet(self):
        for payslip in self:
            tot_amount = 0.0
            total_tax = 0.0
            total_discount = 0.0
            print("===================emp",payslip.employee_id.contract_id)
            if payslip.employee_id.contract_id.apply_tax:
                number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
                # delete old payslip lines
                payslip.line_ids.unlink()
                # set the list of contract for which the rules have to be applied
                # if we don't give the contract, then the rules to apply should be for all current contracts of the employee
                contract_ids = payslip.contract_id.ids or \
                               self.get_contract(payslip.employee_id, payslip.date_from, payslip.date_to)
                lines = [(0, 0, line) for line in payslip._get_payslip_lines()]
                for line in lines:
                    rule_data = self.env['hr.salary.rule'].browse(line[2]['salary_rule_id'])
                    if rule_data.taxable:
                        tot_rule = float(line[2]['amount']) * float(line[2]['quantity']) * float(line[2]['rate']) / 100.0
                        tot_amount += tot_rule
                tot_amount = tot_amount * 12
                if tot_amount:
                    if self.env.user.company_id.payslip_tax_minimum_salary == 0:
                        raise ValidationError(_("Please set Payslip Tax Minimum Salary"))
                    if self.env.user.company_id.payslip_tax_minimum_salary_force == 0:
                        raise ValidationError(_("Please set Payslip Tax Minimum Force"))
                    tot_amount = tot_amount - self.env.user.company_id.payslip_tax_minimum_salary
                    if tot_amount <= self.env.user.company_id.payslip_tax_minimum_salary_force:
                        for line in payslip.tax_rule_ids:
                            if not line.level == str(len(payslip.tax_rule_ids)):
                                if tot_amount > (line.amount_to - line.amount_from):
                                    total_tax += line.total_tax
                                    tot_amount -= (line.amount_to - line.amount_from)

                                elif tot_amount <= (line.amount_to - line.amount_from):
                                    tax_level = tot_amount * (line.tax_rate / 100)
                                    total_tax += tax_level
                                    total_discount = total_tax * (line.tax_exemption / 100)
                                    break
                                else:
                                    if tot_amount < line.amount_from:
                                        tax_level = tot_amount * (line.tax_rate / 100)
                                        total_tax += tax_level
                                        total_discount = total_tax * (line.tax_exemption / 100)
                                        break
                            else:
                                tax_level = tot_amount * (line.tax_rate / 100)
                                total_tax += tax_level
                                total_discount = total_tax * (line.tax_exemption / 100)
                                break
                    else:
                        for line in payslip.tax_rule_ids:
                            if line.force_amount_to > tot_amount > line.force_amount_from:
                                total_tax = tot_amount * (line.tax_rate / 100)
                                total_discount = total_tax * (line.tax_exemption / 100)

                tax_amount = total_tax - total_discount
                taxes = self.env['res.config.settings'].search([])
                if taxes:
                    for tax in taxes[-1]:
                        if tax.payslip_tax_type == 'month':
                            payslip.write({'tax_amount': round(tax_amount / 12), 'payslip_tax_type': 'month'})
                        else:
                            payslip.write({'tax_amount': round(tax_amount), 'payslip_tax_type': 'annual'})
                else:
                    payslip.write({'tax_amount': round(tax_amount / 12), 'payslip_tax_type': 'month'})

                payslip.write({'line_ids': lines, 'number': number})

        return super(SalaryTax, self).compute_sheet()

    # def _get_payslip_lines(self):
    #     def _sum_salary_rule_category(localdict, category, amount):
    #         if category.parent_id:
    #             localdict = _sum_salary_rule_category(localdict, category.parent_id, amount)
    #         localdict['categories'].dict[category.code] = localdict['categories'].dict.get(category.code, 0) + amount
    #         return localdict
    #
    #     self.ensure_one()
    #     result = {}
    #     rules_dict = {}
    #     worked_days_dict = {line.code: line for line in self.worked_days_line_ids if line.code}
    #     inputs_dict = {line.code: line for line in self.input_line_ids if line.code}
    #
    #     employee = self.employee_id
    #     contract = self.contract_id
    #     journal_currency = self.env.company.currency_id
    #     if self.journal_id and self.journal_id.currency_id:
    #         journal_currency = self.journal_id.currency_id
    #     localdict = {
    #         **self._get_base_local_dict(),
    #         **{
    #             'categories': BrowsableObject(employee.id, {}, self.env),
    #             'rules': BrowsableObject(employee.id, rules_dict, self.env),
    #             'payslip': Payslips(employee.id, self, self.env),
    #             'worked_days': WorkedDays(employee.id, worked_days_dict, self.env),
    #             'inputs': InputLine(employee.id, inputs_dict, self.env),
    #             'employee': employee,
    #             'contract': contract
    #         }
    #     }
    #     for rule in sorted(self.struct_id.rule_ids, key=lambda x: x.sequence):
    #         localdict.update({
    #             'result': None,
    #             'result_qty': 1.0,
    #             'result_rate': 100})
    #         if rule._satisfy_condition(localdict):
    #             amount_currency, qty, rate = rule._compute_rule(localdict)
    #             amount = amount_currency
    #             if rule.currency_id and rule.currency_id.id != journal_currency.id:
    #                 quantity = rule.currency_id._get_conversion_rate(rule.currency_id, journal_currency,
    #                                                                  self.company_id, self.date_from)
    #                 amount = quantity * amount_currency
    #             #check if there is already a rule computed with that code
    #             previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
    #             #set/overwrite the amount computed for this rule in the localdict
    #             tot_rule = amount * qty * rate / 100.0
    #             localdict[rule.code] = tot_rule
    #             rules_dict[rule.code] = rule
    #             # sum the amount for its salary category
    #             localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
    #             # create/overwrite the rule in the temporary results
    #             result[rule.code] = {
    #                 'sequence': rule.sequence,
    #                 'code': rule.code,
    #                 'name': rule.name,
    #                 'note': rule.note,
    #                 'salary_rule_id': rule.id,
    #                 'contract_id': contract.id,
    #                 'employee_id': employee.id,
    #                 'amount': amount,
    #                 'amount_currency': amount_currency,
    #                 'quantity': qty,
    #                 'rate': rate,
    #                 'slip_id': self.id,
    #             }
    #     return result.values()


class PayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    currency_id = fields.Many2one('res.currency', string='Currency', related="salary_rule_id.currency_id",
                                  help="The optional other currency if it is a multi-currency entry.")
    company_currency_id = fields.Many2one(related='company_id.currency_id', readonly=True)
    amount_currency = fields.Monetary(string="Amount Currency", currency_field="currency_id")
    amount = fields.Monetary(digits='Payroll', currency_field="company_currency_id")

    # @api.depends('slip_id.journal_id', 'quantity', 'rate', 'amount')
    # def adjust_line_currency(self):
    #     print(self)
    #     for line in self:
    #         journal_currency = self.env.company.currency_id
    #         if line.slip_id.journal_id and line.slip_id.journal_id.currency_id:
    #             journal_currency = line.slip_id.journal_id.currency_id
    #         line.amount_currency = line.amount
    #         if line.currency_id and line.currency_id.id != journal_currency.id:
    #             quantity = line.currency_id._get_conversion_rate(line.currency_id, journal_currency,
    #                                                              line.slip_id.company_id, line.slip_id.date_from)
    #             line.amount = quantity * line.amount_currency