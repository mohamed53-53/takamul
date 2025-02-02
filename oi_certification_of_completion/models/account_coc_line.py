'''
Created on Jan 25, 2021

@author: Zuhair Hammadi
'''
from odoo import models, fields, api
from odoo.tools.misc import get_lang

class AccountCOCLine(models.Model):
    _name = 'account.coc.line'
    _order = 'coc_id, sequence, id'
    _description = 'Certification of Completion Line'
    
    coc_id = fields.Many2one('account.coc', required = True, ondelete = 'cascade', index = True)
    state = fields.Selection(related='coc_id.state', store=True, readonly=True)
    currency_id = fields.Many2one(related='coc_id.currency_id', store=True, readonly=True)
    company_id = fields.Many2one(related='coc_id.company_id', store=True, readonly=True)
    partner_id = fields.Many2one(related='coc_id.partner_id', store=True, readonly=True)
    
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Text(string='Description', required=True)
    
    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')    
    
    purchase_line_id = fields.Many2one('purchase.order.line')
    po_product_qty = fields.Float(string='Item Quantity', related='purchase_line_id.product_qty', readonly = True)
    po_price_unit = fields.Float(string='Item Unit Price', related='purchase_line_id.price_unit', readonly = True)
    po_price_subtotal = fields.Monetary(string='Item Amount', related='purchase_line_id.price_subtotal', readonly = True)
    
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)

    taxes_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])
    
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)])
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_qty = fields.Float(string='Received Quantity', digits='Product Unit of Measure', required=True)
    product_uom_qty = fields.Float(string='Total Received Quantity', compute='_compute_product_uom_qty', store=True)    
    
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")    
    
    processed_quantity = fields.Float(string='Processed Quantity', digits='Product Unit of Measure', compute = '_calc_processed', store = True)
    processed_price_subtotal = fields.Monetary(string='Processed Amount', store=True, compute = '_calc_processed')    
    
    received_date = fields.Date(required = True, string='Date Received')
    
    _sql_constraints = [
        ('accountable_required_fields',
            "CHECK(display_type IS NOT NULL OR (product_id IS NOT NULL AND product_uom IS NOT NULL))",
            "Missing required fields on accountable Certification of Completion line."),
        ('non_accountable_null_fields',
            "CHECK(display_type IS NULL OR (product_id IS NULL AND price_unit = 0 AND product_uom_qty = 0 AND product_uom IS NULL))",
            "Forbidden values on non-accountable Certification of Completion line"),
    ]
    
    @api.depends('purchase_line_id')
    def _calc_processed(self):
        for record in self:            
            coc_line_ids = record.purchase_line_id.coc_line_ids.filtered(lambda line : line.state not in ['draft', 'rejected']) - record
            record.processed_quantity = sum(coc_line_ids.mapped('product_qty'))
            record.processed_price_subtotal = sum(coc_line_ids.mapped('price_subtotal'))
    
    @api.depends('product_qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                vals['price_unit'],
                vals['currency_id'],
                vals['product_qty'],
                vals['product'],
                vals['partner'])
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    @api.depends('product_uom', 'product_qty', 'product_id.uom_id')
    def _compute_product_uom_qty(self):
        for line in self:
            if line.product_id and line.product_id.uom_id != line.product_uom:
                line.product_uom_qty = line.product_uom._compute_quantity(line.product_qty, line.product_id.uom_id)
            else:
                line.product_uom_qty = line.product_qty


    def _prepare_compute_all_values(self):
        # Hook method to returns the different argument values for the
        # compute_all method, due to the fact that discounts mechanism
        # is not implemented yet on the purchase orders.
        # This method should disappear as soon as this feature is
        # also introduced like in the sales module.
        self.ensure_one()
        return {
            'price_unit': self.price_unit,
            'currency_id': self.coc_id.currency_id,
            'product_qty': self.product_qty,
            'product': self.product_id,
            'partner': self.coc_id.partner_id,
        }

    def _get_product_purchase_description(self, product_lang):
        self.ensure_one()
        name = product_lang.display_name
        if product_lang.description_purchase:
            name += '\n' + product_lang.description_purchase

        return name
        
    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
        product_lang = self.product_id.with_context(
            lang=get_lang(self.env, self.partner_id.lang).code,
            partner_id=self.partner_id.id,
            company_id=self.company_id.id,
        )
        self.name = self._get_product_purchase_description(product_lang)

        self._compute_tax_id()

    def _compute_tax_id(self):
        for line in self:
            fpos = line.coc_id.purchase_order_id.fiscal_position_id or line.coc_id.partner_id.with_company(line.company_id.id).property_account_position_id
            # If company_id is set in the order, always filter taxes by the company
            taxes = line.product_id.supplier_taxes_id.filtered(lambda r: r.company_id == line.coc_id.company_id)
            line.taxes_id = fpos.map_tax(taxes) if fpos else taxes

    def _get_computed_account(self):
        self.ensure_one()
        self = self.with_company(self.company_id.id)

        fiscal_position = self.coc_id.purchase_order_id.fiscal_position_id or self.coc_id.partner_id.property_account_position_id
        accounts = self.product_id.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)
        return accounts['expense']

    
    def _prepare_account_invoice_line(self):
        self.ensure_one()

        if self.currency_id == self.company_id.currency_id:
            currency = False
        else:
            currency = self.currency_id

        return {
            'name': self.purchase_line_id and '%s: %s' % (self.purchase_line_id.order_id.name, self.name) or self.name,
            'currency_id': currency and currency.id or False,
            'purchase_line_id': self.purchase_line_id.id,
            'product_uom_id': self.product_uom.id,
            'product_id': self.product_id.id,
            'price_unit': self.price_unit,
            'quantity': self.product_qty,
            'partner_id': self.partner_id.id,
            'analytic_account_id': self.account_analytic_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'tax_ids': [(6, 0, self.taxes_id.ids)],
            'display_type': self.display_type,
            'account_id' : self._get_computed_account().id
        }
    