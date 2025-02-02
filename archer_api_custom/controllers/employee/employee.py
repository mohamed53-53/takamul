import functools
import json

from odoo.addons.archer_api_custom.controllers.common import validate_token
from odoo import http, tools
from odoo.http import request, Response


class Employee(http.Controller):
    @validate_token
    @http.route("/api/employee/profile", methods=["POST"], type="json", auth="none", csrf=False)
    def api_employee_profile(self, **kw):
        try:

            if request.httprequest.accept_languages:
                lang=request.httprequest.accept_languages
            else:
                lang = 'en_US'

            user = request.env['res.users'].with_context(lang=str(lang)).sudo().browse(request.session['uid'])
            if user.employee_id:
                vals = {
                    "profile_source": 'employee' or None,
                    "en_name": user.employee_id.name or None,
                    "ar_name": user.employee_id.arabic_name or None,
                    "work_email": user.employee_id.work_email or None,
                    "mobile_phone": user.employee_id.mobile_phone or None,
                    "work_phone": user.employee_id.work_phone or None,
                    "department_id": user.employee_id.department_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
                    "manager_id": user.employee_id.parent_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
                    "depart_mngr_id": user.employee_id.coach_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
                    "work_location_id": user.employee_id.work_location_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
                    "job_id": user.employee_id.job_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
                    "gender": user.employee_id.gender or None,
                    "birthday": user.employee_id.birthday or None,
                    "country_id": user.employee_id.country_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
                    "identification_id": user.employee_id.identification_id or None,
                    "passport_id": user.employee_id.passport_id or None,
                    "marital": user.employee_id.marital or None,
                    "emergency_contact": user.employee_id.emergency_contact or None,
                    "emergency_phone": user.employee_id.emergency_phone or None,
                    'join_date': user.employee_id.contract_id.date_start or None
                }
            else:
                vals = {
                    "profile_source": 'user' or None,
                    "en_name": user.partner_id.name or None,
                    "ar_name": None,
                    "work_email": user.partner_id.email or None,
                    "mobile_phone": user.partner_id.phone or None,
                    "work_phone": None,
                    "department_id": None,
                    "manager_id": None,
                    "depart_mngr_id": None,
                    "work_location_id": None,
                    "job_id": None,
                    "gender": None,
                    "birthday": None,
                    "country_id": user.partner_id.country_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
                    "identification_id": None,
                    "passport_id": None,
                    "marital": None,
                    "emergency_contact": None,
                    "emergency_phone": None,
                    'join_date': None
                }
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(vals, indent=4, sort_keys=True, default=str),
            )
            return json.loads(response.data)

        except Exception as ex:
            raise Exception(ex)
