# -*- coding: utf-8 -*-
# from odoo import http


# class ArcherEmployeeEvaluation(http.Controller):
#     @http.route('/archer_employee_evaluation/archer_employee_evaluation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/archer_employee_evaluation/archer_employee_evaluation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('archer_employee_evaluation.listing', {
#             'root': '/archer_employee_evaluation/archer_employee_evaluation',
#             'objects': http.request.env['archer_employee_evaluation.archer_employee_evaluation'].search([]),
#         })

#     @http.route('/archer_employee_evaluation/archer_employee_evaluation/objects/<model("archer_employee_evaluation.archer_employee_evaluation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('archer_employee_evaluation.object', {
#             'object': obj
#         })
