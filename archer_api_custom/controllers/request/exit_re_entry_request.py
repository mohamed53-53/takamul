# -*- coding: utf-8 -*-
import functools
import json

from odoo.addons.archer_api_custom.controllers.helper.objects_map import handle_create_fcm_msg
from odoo.addons.archer_api_custom.controllers.common import validate_token
from odoo import http, tools,_
from odoo.http import request, Response


class ExitReEntryVisa(http.Controller):
    @validate_token
    @http.route("/api/requests/create_exit_re_entry_visa_request", methods=["POST"], type="json", auth="none", csrf=False)
    def create_exit_re_entry_visa_request(self, **kw):
        try:
            employee_id = request.env['hr.employee'].sudo().browse(kw['employee_id'])
            kw['project_id'] = employee_id.project_id.id
            kw['state'] = 'submit'
            if kw['purpose'] == 'business_trip':
                kw['expense_on_project'] = True
                kw['personal_vacation'] = False

            if kw['purpose']:
                kw['personal_vacation'] = True
                kw['expense_on_project'] = False

            exit_re_entry_visa_id = request.env['re.entry.visa'].sudo().create(kw)
            handle_create_fcm_msg(exit_re_entry_visa_id)

            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(True))

            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Failed Operation'))