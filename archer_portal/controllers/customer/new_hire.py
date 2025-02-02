from odoo import http,_
from odoo.exceptions import ValidationError
from odoo.http import request


class WebsiteCustomerHireRequest(http.Controller):

    @http.route('/customer-hire-registration/submit', type='http', auth="user", website=True, methods=['POST', 'GET'],
                csrf=False)
    def new_hire_request_submit(self, **kw):
     if not 'name' in kw or not 'email' in kw or not 'apply_job' in kw or not 'country_id' in kw or not 'project_id' in kw :
         raise ValidationError(_('Please Check Required fields'))
     else:
        obj_id = http.request.env['archer.customer.application'].sudo().create(kw)
        return request.render("archer_portal.customer_thankyou_page")


