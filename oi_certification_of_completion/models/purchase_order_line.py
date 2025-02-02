'''
Created on Jan 27, 2021

@author: Zuhair Hammadi
'''
from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    coc_line_ids = fields.One2many('account.coc.line', 'purchase_line_id')
    qty_coc = fields.Float("COC Qty", compute = '_calc_qty_coc', digits='Product Unit of Measure', compute_sudo=True, store=True)
    qty_received_method = fields.Selection(selection_add=[('coc', 'Certification of Completion')])
        
    @api.depends('coc_line_ids.product_qty', 'coc_line_ids.state')
    def _calc_qty_coc(self):
        for record in self:
            record.qty_coc = sum(record.coc_line_ids.filtered(lambda line : line.state not in ['draft','rejected']).mapped('product_qty'))
        
    @api.depends('product_id', 'order_id.coc_ok')
    def _compute_qty_received_method(self):
        super(PurchaseOrderLine, self)._compute_qty_received_method()
        for line in self.filtered(lambda l: not l.display_type):            
            if line.product_id.type == 'service' and line.order_id.coc_ok:
                line.qty_received_method = 'coc'
            
    @api.depends('qty_coc')
    def _compute_qty_received(self):
        super(PurchaseOrderLine, self)._compute_qty_received()
        for line in self:
            if line.qty_received_method == 'coc':
                line.qty_received = line.qty_coc            