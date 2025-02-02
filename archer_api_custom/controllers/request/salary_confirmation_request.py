# -*- coding: utf-8 -*-
import json

from odoo.addons.archer_api_custom.controllers.helper.objects_map import handle_create_fcm_msg
from odoo.addons.archer_api_custom.controllers.common import validate_token

from odoo import http,_
from odoo.http import request, Response


class SalaryConfirmationRequest(http.Controller):
    @validate_token
    @http.route("/api/requests/create_salary_confirmation_request", methods=["POST"], type="json", auth="none", csrf=False)
    def create_salary_confirmation_request(self, **kw):
        try:
            employee_id = request.env['hr.employee'].sudo().browse(kw['employee_id'])
            kw['project_id'] = employee_id.project_id.id
            kw['state'] = 'submit'
            salary_confirmation_request_id = request.env['salary.confirmation'].sudo().create(kw)
            handle_create_fcm_msg(salary_confirmation_request_id)
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(True))
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Failed Operation'))