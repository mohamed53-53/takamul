# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeePromotion(http.Controller):
#     @http.route('/employee_promotion/employee_promotion', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_promotion/employee_promotion/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_promotion.listing', {
#             'root': '/employee_promotion/employee_promotion',
#             'objects': http.request.env['employee_promotion.employee_promotion'].search([]),
#         })

#     @http.route('/employee_promotion/employee_promotion/objects/<model("employee_promotion.employee_promotion"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_promotion.object', {
#             'object': obj
#         })
