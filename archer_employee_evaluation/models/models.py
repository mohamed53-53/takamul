# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class archer_employee_evaluation(models.Model):
#     _name = 'archer_employee_evaluation.archer_employee_evaluation'
#     _description = 'archer_employee_evaluation.archer_employee_evaluation'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
