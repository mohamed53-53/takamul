from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class HrStructureRule(models.Model):
    _inherit = 'hr.salary.rule'

    is_dynamic = fields.Boolean(string='Dynamic Rule')

    @api.depends('is_dynamic')
    @api.onchange('is_dynamic')
    def onchange_is_dynamic(self):
        if self.is_dynamic and self.code:
            self.amount_select = 'code'
            self.amount_python_compute = 'result = contract.get_employee_rule_amount(employee, contract,"{rule}", payslip.date_from, payslip.date_to)'.format(rule=self.code)
        elif self.is_dynamic and not self.code:
            self.is_dynamic = False
            return {'warning': {'message': _('Please Set Code First')}}
        else:
            self.amount_select = 'fix'
            self.amount_python_compute = False
