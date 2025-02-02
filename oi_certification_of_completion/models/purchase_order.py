'''
Created on Jan 27, 2021

@author: Zuhair Hammadi
'''
from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    coc_ok = fields.Boolean("Certification of Completion", help="Enable employee to invoiced the PO")
    coc_ids = fields.One2many('account.coc','purchase_order_id')
    coc_count = fields.Integer(compute = '_calc_coc_count')
    
    @api.depends('coc_ids')
    def _calc_coc_count(self):
        for record in self:
            record.coc_count = len(record.coc_ids)
                        
    def action_view_coc(self):
        action = self.env.ref("oi_certification_of_completion.action_account_coc").read()[0]
        action['context'] = {
            'default_purchase_order_id' : self.id
            }
        if len(self.coc_ids) > 1:
            action['domain'] = [('purchase_order_id', 'in', self.ids)]
        else:
            form_view = [(False, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = self.coc_ids.id
        
        return action