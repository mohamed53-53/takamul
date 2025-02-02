from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    project_id = fields.Many2one("project.project")
    project_owner_id = fields.Many2one(related="project_id.owner_id")


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    project_ids = fields.Many2many(comodel_name="project.project", relation="department_project_rel",
                                   column1="project_id", column2="department_id", string="Projects")


class HrContract(models.Model):
    _inherit = 'hr.contract'

    @api.depends('project_id', 'employee_id')
    def set_project_analytic(self):
        for rec in self:
            if rec.project_id:
                rec.analytic_account_id = rec.project_id.analytic_account_id.id
            elif rec.employee_id and rec.employee_id.project_id:
                rec.analytic_account_id = rec.employee_id.project_id.analytic_account_id.id
            else:
                rec.analytic_account_id = False

    def compute_group_admin(self):
        for rec in self:
            if self.env.user.has_group('hr_contract.group_hr_contract_manager'):
                rec.is_admin = True
            else:
                rec.is_admin = False

    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    project_id = fields.Many2one("project.project", related="employee_id.project_id")
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account',
                                          related="project_id.analytic_account_id", store=True)
    is_admin = fields.Boolean(string="", compute="compute_group_admin")
    project_owner_id = fields.Many2one(related="project_id.owner_id")
