from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
import numpy as np

class ContractInherit(models.Model):
    _inherit = 'hr.contract'

    @api.model
    def create(self, vals):
        contracts = super(ContractInherit, self).create(vals)
        open_contracts = contracts.filtered(
            lambda c: c.state == 'draft')
        for contract in open_contracts.filtered(lambda c: c.employee_id):
            project_id = contract.employee_id.project_id
            matched_grade_line = project_id.salary_constraint_ids.filtered(lambda g: g.grade_id == contract.employee_id.grade_id)
            if matched_grade_line and contract.wage:
                range = np.arange(matched_grade_line.basic_salary_min, matched_grade_line.basic_salary_max)
                if contract.wage not in range:
                    raise ValidationError(_('You can not enter "Wage" out of range basic salary min-max value.'))
        return contracts

    def write(self, vals):
        res = super(ContractInherit, self).write(vals)
        for contract in self.filtered(lambda c: c.employee_id):
            project_id = contract.employee_id.project_id
            matched_grade_line = project_id.salary_constraint_ids.filtered(
                lambda g: g.grade_id == contract.employee_id.grade_id)
            if matched_grade_line and contract.wage:
                range = np.arange(matched_grade_line.basic_salary_min, matched_grade_line.basic_salary_max)
                if contract.wage not in range:
                    raise ValidationError(_('You can not enter "Wage" out of range basic salary min-max value.'))
        return res

    def move_to_running(self):
        for rec in self:
            # emp_contracts = self.search([
            #     ('id', '!=', rec.id), ('state', '=', 'open'), ('employee_id', '=', rec.employee_id.id),
            #     ('date_start', '<=', rec.date_start), ('date_end', '>=', rec.date_start),
            # ])
            # print("emp_contracts>>>>", emp_contracts)
            # if emp_contracts:
            #     raise ValidationError("Contract for this Employee already exists in Running stage.")
            # else:
            rec.state = 'open'
