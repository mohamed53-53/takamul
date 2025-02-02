from odoo import api, fields, models

class HrGrade(models.Model):
    _name = "hr.grade"

    name = fields.Char(string='Grade', copy=False, required=True, tracking=True)
    is_assign_to_employee = fields.Boolean()
    
    

