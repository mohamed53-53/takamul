import json

from odoo import SUPERUSER_ID
from odoo.exceptions import AccessError
from odoo.http import Response, request


def jsonfy_response(data):
    Response.status = str(200)
    response = Response(
        status=200,
        content_type="application/json; charset=utf-8",
        headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
        response=data)
    return json.loads(json.dumps(response.response, indent=4, sort_keys=True, default=str))

def get_next_approve(obj):
    a_list = request.env['approval.config'].sudo().search([('model_id.name', '=', obj._name)], order='sequence').mapped('state')
    items = json.loads(obj.workflow_states)
    index = json.loads(obj.workflow_states).index(obj.state)+1
    next_item =items[index]
    return next_item

