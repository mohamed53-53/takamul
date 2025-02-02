from odoo import fields, models, api,_


class HrExpenseConstraint(models.Model):
    _name = 'hr.expense.constraint'

    name = fields.Char(string="Name", required=True)
    constraint_ids = fields.One2many('hr.expense.constraint.list', 'constraint_id', string="Constraints")


class HrExpenseConstraints(models.Model):
    _name = 'hr.expense.constraint.list'

    constraint_id = fields.Many2one('hr.expense.constraint', string="Constraint")
    product_id = fields.Many2one('product.template', string="Service", required=True)
    grade_id = fields.Many2one('hr.grade', string="Grade", required=True)
    max_amount = fields.Float(string="Margin", required=True)
    period = fields.Selection([
        ('monthly', _('Monthly')),
        ('annually', _('Annually')),
    ], string='Period', required=True)
