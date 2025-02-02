from odoo import http
from odoo.http import request


class GeneralController(http.Controller):

    @http.route('/general/set_web_login', type='json', auth='public', csrf=False)
    def set_web_login(self, user_id, flag):
        user = request.env['res.users'].browse(user_id)
        if user :
            user.sudo().write({'web_login':flag})
            return True
        else:
            return False