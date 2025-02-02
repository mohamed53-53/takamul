# -*- coding: utf-8 -*-
import functools
import json

from odoo.addons.archer_api_custom.controllers.helper.objects_map import handle_create_fcm_msg
from odoo.addons.archer_api_custom.controllers.common import validate_token
from odoo import http, tools,_
from odoo.exceptions import ValidationError
from odoo.http import request, Response


class SalaryTransferRequest(http.Controller):
    @validate_token
    @http.route("/api/requests/create_salary_transfer_request", methods=["POST"], type="json", auth="none", csrf=False)
    def create_salary_transfer_request(self, **kw):
        try:
            employee_id = request.env['hr.employee'].sudo().browse(kw['employee_id'])
            kw['project_id'] = employee_id.project_id.id
            kw['state'] = 'submit'
            if employee_id.is_locked and not 'bank_clearance_letter' in kw:
                raise ValidationError(_('Clearance Letter is required'))
            if 'iban_number' in kw and 're_enter_iban_number' in kw:
                if kw['iban_number'] != kw['re_enter_iban_number']:
                    raise ValidationError(_('IBAN and IBAN Confirmation not matched'))
                elif not employee_id.international_bank:
                    if len(kw['iban_number']) != 24:
                        raise ValidationError(_('IBAN must be 24 characters'))
                    if kw['iban_number'][:2] != 'SA':
                        raise ValidationError(_('IBAN must start with SA'))
                elif employee_id.international_bank :
                    if len(kw['iban_number']) != 34:
                        raise ValidationError(_('IBAN must be 34 characters'))
            salary_transfer_id = request.env['salary.transfer'].sudo().create(kw)
            handle_create_fcm_msg(salary_transfer_id)
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(True))
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))