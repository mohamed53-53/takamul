from odoo import models, fields


class HrLeaveType(models.Model):
    _name = 'hr.employee.leave.type'

    name = fields.Char(string='name', required=True)

class HRLeave(models.Model):
    _inherit = 'hr.leave.type'

    leave_type_ids = fields.Many2many(comodel_name='hr.employee.leave.type')