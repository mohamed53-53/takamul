from odoo import models, fields, api
from odoo.osv import expression


class HrPayslipEmployee(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    project_id = fields.Many2one('project.project')
    empl_type = fields.Selection(selection=[('full', 'Full Time'), ('part', 'Part Time')], string='Employee Type')

    @api.depends('department_id', 'project_id')
    def _compute_employee_ids(self):
        for wizard in self:
            domain = wizard._get_available_contracts_domain()
            if wizard.project_id:
                domain = expression.AND([
                    domain,
                    [('project_id', '=', self.project_id.id)]
                ])
            if wizard.empl_type:
                domain = expression.AND([
                    domain,
                    [('empl_type', '=', self.empl_type)]
                ])
            if wizard.department_id:
                domain = expression.AND([
                    domain,
                    [('department_id', 'child_of', self.department_id.id)]
                ])
            wizard.employee_ids = self.env['hr.employee'].search(domain)

        #         <xpath expr="//field[@name='rule_ids']/tree/field[@name='rule_id']" position="before">
        #             <field name="date"/>
        #         </xpath>
        #             def get_employee_rule_amount(self, employee, contract, rule, date_from, date_to):
        # contract_rule = contract.rule_ids.filtered(lambda r: r.rule_id.id in rule and r.employee_id.id == employee.id)
        # if contract_rule:
        #     percent = 1
        #     if date_from and date_to:
        #         if date_from <= contract_rule.date <= date_to:
        #             last_day_in_month = date.today().replace(day=calendar.monthrange(date.today().year, date.today().month)[1])
        #             percent = ((date_to - contract_rule.date).days + 1) / int(last_day_in_month.day)
        #         if percent == 1:
        #             total_value = contract_rule.total_value
        #             if contract.date_start < date_from:
        #                 last_payslips = self.env['hr.payslip'].search([('employee_id', '=', employee.id),
        #                                                                ('date_from', '!=', date_from),
        #                                                                ('date_to', '!=', date_to),
        #                                                                ('state', '!=', 'cancel')])
        #                 if not last_payslips:
        #                     last_day_in_month = contract.date_start.replace(
        #                         day=calendar.monthrange(contract.date_start.year, contract.date_start.month)[1])
        #                     last_month_percent = ((last_day_in_month - contract.date_start).days + 1) / int(last_day_in_month.day)
        #                     total_value += contract_rule.total_value * last_month_percent
        #             return total_value
        #         elif percent < 1:
        #             total_value = contract_rule.total_value * percent
        #             history_contract_rule = contract.history_rule_ids.filtered(
        #                 lambda r: r.rule_id.id in rule and r.date_history == contract_rule.date)
        #             total_value += (history_contract_rule.total_value * (1 - percent))
        #             return total_value
        #         else:
        #             return 0.0
        #     else:
        #         if contract_rule.value_type == 'percent':
        #             return (contract.wage * contract_rule.value) / 100
        #         elif contract_rule.value_type == 'amount':
        #             return contract_rule.value
        #         else:
        #             return 0.0
        # return 0.0
