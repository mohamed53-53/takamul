# -*- coding: utf-8 -*-
import functools
import json

from odoo.addons.archer_api_custom.controllers.helper.objects_map import handle_create_fcm_msg
from odoo.addons.archer_api_custom.controllers.common import validate_token
from odoo import http, tools,_
from odoo.http import request, Response


class VisitVisaAttestationRequest(http.Controller):
    @validate_token
    @http.route("/api/requests/create_visit_visa_request", methods=["POST"], type="json", auth="none", csrf=False)
    def create_visit_visa_request(self, **kw):
        try:
            employee_id = request.env['hr.employee'].sudo().browse(kw['employee_id'])
            kw['project_id'] = employee_id.project_id.id
            kw['state'] = 'submit'
            visit_visa_id = request.env['visit.visa.attestation'].sudo().create(kw)
            handle_create_fcm_msg(visit_visa_id)
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(True))
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))