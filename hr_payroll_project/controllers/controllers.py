# -*- coding: utf-8 -*-
# from odoo import http


# class HrPayrollProject(http.Controller):
#     @http.route('/hr_payroll_project/hr_payroll_project', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_payroll_project/hr_payroll_project/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_payroll_project.listing', {
#             'root': '/hr_payroll_project/hr_payroll_project',
#             'objects': http.request.env['hr_payroll_project.hr_payroll_project'].search([]),
#         })

#     @http.route('/hr_payroll_project/hr_payroll_project/objects/<model("hr_payroll_project.hr_payroll_project"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_payroll_project.object', {
#             'object': obj
#         })
