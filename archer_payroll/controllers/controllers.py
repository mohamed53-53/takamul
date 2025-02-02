# -*- coding: utf-8 -*-
# from odoo import http


# class ArcherPayroll(http.Controller):
#     @http.route('/archer_payroll/archer_payroll', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/archer_payroll/archer_payroll/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('archer_payroll.listing', {
#             'root': '/archer_payroll/archer_payroll',
#             'objects': http.request.env['archer_payroll.archer_payroll'].search([]),
#         })

#     @http.route('/archer_payroll/archer_payroll/objects/<model("archer_payroll.archer_payroll"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('archer_payroll.object', {
#             'object': obj
#         })
