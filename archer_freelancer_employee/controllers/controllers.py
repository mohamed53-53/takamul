# -*- coding: utf-8 -*-
# from odoo import http


# class ArcherFreelancerEmployee(http.Controller):
#     @http.route('/archer_freelancer_employee/archer_freelancer_employee', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/archer_freelancer_employee/archer_freelancer_employee/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('archer_freelancer_employee.listing', {
#             'root': '/archer_freelancer_employee/archer_freelancer_employee',
#             'objects': http.request.env['archer_freelancer_employee.archer_freelancer_employee'].search([]),
#         })

#     @http.route('/archer_freelancer_employee/archer_freelancer_employee/objects/<model("archer_freelancer_employee.archer_freelancer_employee"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('archer_freelancer_employee.object', {
#             'object': obj
#         })
