# -*- coding: utf-8 -*-
# from odoo import http


# class PayrollAmendment(http.Controller):
#     @http.route('/payroll_amendment/payroll_amendment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payroll_amendment/payroll_amendment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('payroll_amendment.listing', {
#             'root': '/payroll_amendment/payroll_amendment',
#             'objects': http.request.env['payroll_amendment.payroll_amendment'].search([]),
#         })

#     @http.route('/payroll_amendment/payroll_amendment/objects/<model("payroll_amendment.payroll_amendment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payroll_amendment.object', {
#             'object': obj
#         })
