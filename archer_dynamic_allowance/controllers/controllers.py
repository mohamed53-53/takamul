# -*- coding: utf-8 -*-
# from odoo import http


# class ArcherDynamicAllowance(http.Controller):
#     @http.route('/archer_dynamic_allowance/archer_dynamic_allowance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/archer_dynamic_allowance/archer_dynamic_allowance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('archer_dynamic_allowance.listing', {
#             'root': '/archer_dynamic_allowance/archer_dynamic_allowance',
#             'objects': http.request.env['archer_dynamic_allowance.archer_dynamic_allowance'].search([]),
#         })

#     @http.route('/archer_dynamic_allowance/archer_dynamic_allowance/objects/<model("archer_dynamic_allowance.archer_dynamic_allowance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('archer_dynamic_allowance.object', {
#             'object': obj
#         })
