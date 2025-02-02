from odoo import models, fields, api


class HrContract(models.Model):
    _inherit = 'hr.contract'
    structure_type_id = fields.Many2one('hr.payroll.structure.type', string="Salary Structure Type", )
    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', related='project_id.analytic_account_id')

    @api.depends('project_id')
    @api.onchange('project_id')
    def get_structure_type_domain(self):
        return {'domain': {'structure_type_id': [('project_ids', 'in', self.project_id.id)]}}


class HrStructureType(models.Model):
    _inherit = 'hr.payroll.structure.type'
    project_ids = fields.Many2many(comodel_name='project.project', required=True, readonly=False)


class HrStructure(models.Model):
    _inherit = 'hr.payroll.structure'
    project_ids = fields.Many2many(comodel_name='project.project', related='type_id.project_ids', readonly=False)


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'
    project_ids = fields.Many2many(comodel_name='project.project', related='struct_id.project_ids', readonly=False)
