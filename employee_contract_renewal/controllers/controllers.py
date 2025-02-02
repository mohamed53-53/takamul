# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeContractRenewal(http.Controller):
#     @http.route('/employee_contract_renewal/employee_contract_renewal', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_contract_renewal/employee_contract_renewal/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_contract_renewal.listing', {
#             'root': '/employee_contract_renewal/employee_contract_renewal',
#             'objects': http.request.env['employee_contract_renewal.employee_contract_renewal'].search([]),
#         })

#     @http.route('/employee_contract_renewal/employee_contract_renewal/objects/<model("employee_contract_renewal.employee_contract_renewal"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_contract_renewal.object', {
#             'object': obj
#         })
