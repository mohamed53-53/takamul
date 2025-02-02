# -*- coding: utf-8 -*-
import base64
import json

from odoo.addons.archer_api_custom.controllers.common import validate_token

from odoo import http,_
from odoo.http import request, Response


class SalaryIdentificationRequest(http.Controller):
    @validate_token
    @http.route("/api/requests/create_salary_identification_request", methods=["POST"], type="json", auth="none", csrf=False)
    def create_salary_identification_request(self, **kw):
        try:
            employee_id = request.env['hr.employee'].sudo().browse(kw['employee_id'])
            kw['project_id'] = employee_id.project_id.id
            kw['state'] = 'done'
            salary_identification_request_id = request.env['salary.identification'].sudo().create(kw)
            data = {
                'request_id': salary_identification_request_id.id
            }
            pdf_report = request.env.ref('archer_employee_request.action_report_salary_identification').sudo()._render_qweb_pdf(salary_identification_request_id.id,data=data)[0]
            salary_identification_request_id.e_stamp = base64.b64encode(pdf_report).decode()
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(base64.b64encode(pdf_report).decode()))
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))