from odoo import api, fields, models
from odoo.exceptions import  ValidationError


class SalaryBreakDown(models.Model):
    _name = 'salary.breakdown'
    _rec_name = 'name'

    name = fields.Char()
    rate = fields.Float()
    is_experience_rule = fields.Boolean(string="")


class SalaryBreakDownLine(models.Model):
    _name = 'salary.breakdown.line'

    applicant_id = fields.Many2one(comodel_name="hr.applicant",)
    salary_breakdown_id = fields.Many2one(comodel_name="salary.breakdown",)
    num_experience_years = fields.Float()
    have_rule = fields.Boolean(string="")
    is_experience_rule = fields.Boolean()
    salary_breakdown_rate = fields.Float()
    subtotal = fields.Float(compute="compute_subtotal",store=True)

    @api.constrains('num_experience_years')
    def check_num_experience_years(self):
        for rec in self:
            if rec.num_experience_years > 5:
                raise ValidationError("Experience Years Should be <= 5 !")

    @api.depends('salary_breakdown_id','num_experience_years',
                 'is_experience_rule','have_rule','num_experience_years')
    def compute_subtotal(self):
        for rec in self:
            if rec.have_rule:
                if rec.is_experience_rule:
                    rec.subtotal = rec.salary_breakdown_rate * rec.num_experience_years
                else:
                    rec.subtotal = rec.salary_breakdown_rate
            else:
                rec.subtotal = 0

