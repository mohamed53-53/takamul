from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProjectExpenseConstraints(models.Model):
    _name = 'project.expense.constraint.list'


    product_id = fields.Many2one(comodel_name="product.template", string='Service', required=True)
    grade_id = fields.Many2one(comodel_name='hr.grade', string="Grade", required=True)
    max_amount = fields.Float(string="Max Amount", required=True)
    period = fields.Selection([
        ('monthly', 'Monthly'),
        ('annually', 'Annually'),
    ], string='Period', required=True)
    project_request_id = fields.Many2one(comodel_name="project.request")
    project_id = fields.Many2one(comodel_name="project.project")
    service_ids = fields.Many2many('product.template', related='project_request_id.service_ids')



class SalaryConstraints(models.Model):
    _name = 'salary.constraint'

    grade_id = fields.Many2one(comodel_name='hr.grade', string="Grade")
    basic_salary_min = fields.Float(string="Basic Salary Min", required=True)
    basic_salary_max = fields.Float(string="Basic Salary Max", required=True)
    project_request_id = fields.Many2one("project.request")
    project_id = fields.Many2one(comodel_name="project.project")


    @api.depends('grade_id', 'basic_salary_min', 'basic_salary_max')
    @api.onchange('grade_id', 'basic_salary_min', 'basic_salary_max')
    def _onchange_basic_salary(self):
        for rec in self:
            if rec.basic_salary_max != 0 :
                if rec.basic_salary_min > rec.basic_salary_max:
                    rec.basic_salary_max = rec.basic_salary_min
                    raise ValidationError(_('Basic Salary Max must be greater then Basic Salary Min '))

    @api.depends('grade_id')
    @api.onchange('grade_id')
    def onchange_grade_id(self):
        exsist_items = self.project_request_id.salary_constraint_ids.grade_id
        if exsist_items:
            domain = {
                'domain': {'grade_id': [('id', 'not in', exsist_items.ids)]}}
            return domain
