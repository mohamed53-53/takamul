# -*- coding: utf-8 -*-
# from odoo import http


# class ArcherRecruitment(http.Controller):
#     @http.route('/archer_recruitment/archer_recruitment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/archer_recruitment/archer_recruitment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('archer_recruitment.listing', {
#             'root': '/archer_recruitment/archer_recruitment',
#             'objects': http.request.env['archer_recruitment.archer_recruitment'].search([]),
#         })

#     @http.route('/archer_recruitment/archer_recruitment/objects/<model("archer_recruitment.archer_recruitment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('archer_recruitment.object', {
#             'object': obj
#         })
