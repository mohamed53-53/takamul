""" Initialize Hr Employee """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class HrEmployee(models.Model):
    """
        Inherit Hr Employee:
         -
    """
    _inherit = 'hr.employee'

    penalty_ids = fields.One2many(
        'employee.penalty',
        'employee_id'
    )
    utility_deduction_ids = fields.One2many(
        'employee.deduction',
        'employee_id', domain=[('type', '=', 'utilities')]
    )
    other_deduction_ids = fields.One2many(
        'employee.deduction',
        'employee_id', domain=[('type', '=', 'other')]
    )
