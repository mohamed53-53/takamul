from odoo import models, fields, api


class HrStructureRule(models.Model):
    _inherit = 'hr.salary.rule'

    is_social_rule = fields.Boolean(string='Social Rule')


class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    # @api.model
    # def _get_default_rule_ids(self):
    #     rules = super(HrPayrollStructure, self)._get_default_rule_ids()
    #     return rules.append((0, 0, {
    #             'name': _('GOSI'),
    #             'sequence': 210,
    #             'code': 'GOSI',
    #             'category_id': self.env.ref('hr_payroll.ALW').id,
    #             'condition_select': 'python',
    #             'condition_python': 'result = employee.country_id.code == "SA" and employee.is_insured == True',
    #             'amount_select': 'code',
    #             'amount_python_compute': 'result = contract.env["hr.payslip"].get_gosi_amount(employee, payslip, categories.ALW)',
    #         }))


class ContractInherit(models.Model):
    _inherit = 'hr.payslip'

    # is_insured = fields.Boolean(default=False)
    #
    # basic_insurance_salary = fields.Monetary(string="Basic Insurance Salary")
    # variable_insurance_salary = fields.Monetary(string="Variable Insurance Salary")
    # employee_share_insurance = fields.Monetary(string="Employee Share Insurance")
    # company_share_insurance = fields.Monetary(string="Company Share Insurance",)

    def get_employee_gosi_amount(self, employee, payslip, alw):
        if employee and employee.is_insured:
            bs = payslip.paid_amount + alw
            if employee.employee_age < 60:
                social_insurance = self.env['social.insurance'].search(
                    [('company_id', '=', payslip.company_id.id), ('age_above_60', '=', False)], limit=1)
            else:
                social_insurance = self.env['social.insurance'].search(
                    [('company_id', '=', payslip.company_id.id), ('age_above_60', '=', True)], limit=1)

            employee_share_basic = social_insurance.employee_basic * bs / 100
            if employee_share_basic < social_insurance.employee_min_limit_basic:
                employee_share_basic = social_insurance.employee_min_limit_basic
            elif employee_share_basic > social_insurance.employee_max_limit_basic:
                employee_share_basic = social_insurance.employee_max_limit_basic
            return employee_share_basic

        return 0.0

    def get_company_gosi_amount(self, employee, payslip, alw):
        if employee and employee.is_insured:
            bs = payslip.paid_amount + alw
            if employee.employee_age < 60:
                social_insurance = self.env['social.insurance'].search(
                    [('company_id', '=', payslip.company_id.id),('age_above_60','=',False)], limit=1)
            else:
                social_insurance = self.env['social.insurance'].search(
                    [('company_id', '=', payslip.company_id.id), ('age_above_60', '=', True)], limit=1)

            company_share_basic = social_insurance.company_basic * bs / 100

            if company_share_basic < social_insurance.company_min_limit_basic:
                company_share_basic = social_insurance.company_min_limit_basic
            elif company_share_basic > social_insurance.company_max_limit_basic:
                company_share_basic = social_insurance.company_max_limit_basic

            # employee_share_basic = social_insurance.employee_basic * bs / 100
            # company_share_basic = social_insurance.company_basic * bs / 100

            return company_share_basic

        return 0.0
