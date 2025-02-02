from . import models
from odoo.api import Environment, SUPERUSER_ID
from odoo.tools.sql import set_not_null

def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    
    for requisition in env['purchase.requisition'].search([('requester_id','=', False)]):
        requisition.write({'requester_id' :  requisition.create_uid.employee_ids[:1].id})
        
    env['purchase.requisition'].flush()
    set_not_null(cr, env['purchase.requisition']._table, 'requester_id')
