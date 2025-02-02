# -*- coding: utf-8 -*-
# from odoo import http


# class ArcherVendorCoc(http.Controller):
#     @http.route('/archer_vendor_coc/archer_vendor_coc', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/archer_vendor_coc/archer_vendor_coc/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('archer_vendor_coc.listing', {
#             'root': '/archer_vendor_coc/archer_vendor_coc',
#             'objects': http.request.env['archer_vendor_coc.archer_vendor_coc'].search([]),
#         })

#     @http.route('/archer_vendor_coc/archer_vendor_coc/objects/<model("archer_vendor_coc.archer_vendor_coc"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('archer_vendor_coc.object', {
#             'object': obj
#         })
