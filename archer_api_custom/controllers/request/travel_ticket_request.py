import functools
import json

from odoo.addons.archer_api_custom.controllers.helper.objects_map import handle_create_fcm_msg
from odoo.addons.archer_api_custom.controllers.common import validate_token
from odoo import http, tools,_
from odoo.http import request, Response


class TravelTicket(http.Controller):
    @validate_token
    @http.route("/api/requests/create_travel_ticket_request", methods=["POST"], type="json", auth="none", csrf=False)
    def create_travel_ticket_request(self, **kw):
        try:
            employee_id = request.env['hr.employee'].sudo().browse(kw['employee_id'])
            others_vals = []

            if kw['other_travelers']:
                if kw['other_travelers_ids']:
                    for trav in kw['other_travelers_ids']:
                        others_vals.append((0, 0, {
                            "traveler_name": trav["traveler_name"],
                            "relation": trav["relation"]
                        }))
            kw['other_travelers_ids'] = others_vals if others_vals else False
            kw['state'] = 'submit'
            ticket_request = request.env['travel.tickets'].sudo().create(kw)
            handle_create_fcm_msg(ticket_request)
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(True))
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))
