'''
Created on Oct 3, 2018

@author: Admin
'''
from odoo import models, api, fields


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"
    
    @api.model
    def _user_id_domain(self):
        return [('groups_id','=', self.env.ref('purchase.group_purchase_user').id),('id','!=','1')]
    
    user_id = fields.Many2one('res.users', domain = _user_id_domain, default = None)
    requester_id = fields.Many2one('hr.employee', string="Requester",default=lambda self: self.env.user.employee_ids[:1],required=True, copy = False)
