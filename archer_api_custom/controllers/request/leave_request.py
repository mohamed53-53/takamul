# -*- coding: utf-8 -*-
import functools
import json

from odoo.addons.archer_api_custom.controllers.helper.objects_map import handle_create_fcm_msg
from odoo.addons.archer_api_custom.controllers.common import validate_token
from odoo import http, tools,_
from odoo.http import request, Response


class LeaveRequest(http.Controller):
    @validate_token
    @http.route("/api/requests/create_leave_request", methods=["POST"], type="json", auth="none", csrf=False)
    def create_leave_request(self, **kw):
        try:
            employee_id = request.env['hr.employee'].sudo().browse(kw['employee_id'])
            kw['project_id'] = employee_id.project_id.id
            kw['leave_current_balance'] = employee_id.monthly_balance
            kw['state'] = 'submit'
            leave_request_id = request.env['leave.request'].sudo().create(kw)
            handle_create_fcm_msg(leave_request_id)
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(True))
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Failed Operation'))

    @validate_token
    @http.route("/api/requests/get_leave_type", methods=["POST"], type="json", auth="none", csrf=False)
    def get_leave_type_by_employee(self, **kw):
        try:
            employee_id = request.env['hr.employee'].sudo().browse(kw['employee_id'])
            json_list = [{
                'name': leave_type.name,
                'id': leave_type.id,
                'allow_extend': leave_type.employee_requests,
            } for leave_type in employee_id.project_id.leave_type_ids]
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(json_list, indent=4, sort_keys=True, default=str))
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Failed Operation'))