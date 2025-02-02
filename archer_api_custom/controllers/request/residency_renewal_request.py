import functools
import json

from odoo.addons.archer_api_custom.controllers.helper.objects_map import handle_create_fcm_msg
from odoo.addons.archer_api_custom.controllers.common import validate_token
from odoo import http, tools,_
from odoo.http import request, Response


class ResedincyRenewal(http.Controller):
    @validate_token
    @http.route("/api/requests/create_residency_renewal_request", methods=["POST"], type="json", auth="none", csrf=False)
    def create_residency_renewal_request(self, **kw):
        try:
            employee_id = request.env['hr.employee'].sudo().browse(kw['employee_id'])
            # residency_id = request.env['residency.residency'].sudo().browse(kw['residency_id'])
            kw['project_id'] = employee_id.project_id.id
            kw['employee_position'] = employee_id.job_id.id
            kw['request_type'] = 'residency_renewal'
            kw['state'] = 'submit'
            kw['employee_renewal_id'] = employee_id.id
            kw['renewal_project_id'] = employee_id.project_id.id
            kw['residency_type'] = 'employee'
            kw['nationality'] = employee_id.country_id.id
            kw['gender'] = employee_id.gender
            kw['religion'] = employee_id.religion
            kw['date_of_birth'] = employee_id.birthday
            residency_renewal_id = request.env['residency.issuance'].sudo().create(kw)
            handle_create_fcm_msg(residency_renewal_id)
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(True))

            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))


    @validate_token
    @http.route("/api/requests/get_employee_residency_renewal_request", methods=["POST"], type="json", auth="none", csrf=False)
    def get_employee_residency_renewal_request(self, **kw):
        try:
            domain = [('request_type', '=', 'residency_renewal'), ('employee_id', '=', kw['employee_id'])]
            if 'request_id' in kw:
                domain.append(('id', '=', kw['request_id']))
            residency_issuance_id = request.env['residency.issuance'].sudo().search(domain)
            json_list = []
            for res in residency_issuance_id:
                vals = {
                    "id": res.id or None,
                    "sequence": res.sequence or None,
                    "residency_id": res.residency_id.mapped(lambda r: {'id': r.id, 'name': r.name, 'residency_type': r.residency_type}) or None,
                    "sponsor_name": res.sponsor_name or None,
                    "sponsor_phone": res.sponsor_phone or None,
                    "sponsor_address": res.sponsor_address or None,
                    "name": res.name or None,
                    "arabic_name": res.arabic_name or None,
                    "relation": res.relation or None,
                    "nationality": res.nationality.mapped(lambda n: {'id': n.id, 'name': n.name}) or None,
                    "religion": res.religion or None,
                    "date_of_birth": res.date_of_birth or None,
                    "job_title": res.job_title or None,
                    "state": res.state or None,
                    "gender": res.gender or None,
                }
                if res.state == 'approve':
                    vals.update({'issued_residency': {
                        "expiration_date_in_hijri": res.expiration_date_in_hijri or None,
                        "number": res.number or None,
                        "serial_number": res.serial_number or None,
                        "re_job_title": res.re_job_title or None,
                        "place_of_issuance": res.place_of_issuance or None,
                        "issuance_date": res.issuance_date or None,
                        "expiration_date": res.expiration_date or None,
                        "arrival_date": res.arrival_date or None,
                    }})
                json_list.append(vals)
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(json_list,indent=4, sort_keys=True, default=str))
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))
