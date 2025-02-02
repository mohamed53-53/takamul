'''
Created on Jan 25, 2021

@author: Zuhair Hammadi
'''
from odoo import models, fields, api, _
from itertools import groupby

class AccountCOC(models.Model):
    _name = 'account.coc'
    _inherit = ['approval.record', 'mail.thread', 'mail.activity.mixin']
    _description = 'Certification of Completion'
        
    WRITE_STATES = {
        'draft': [('readonly', False)],
    }
            
    name = fields.Char('Number', required = True, readonly=True, default = lambda self : _('New'), copy = False)
    purchase_order_id = fields.Many2one('purchase.order', 'Purchase Order', readonly = True, states=WRITE_STATES)     
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, readonly = True, states=WRITE_STATES, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    line_ids = fields.One2many('account.coc.line', 'coc_id', copy = True, readonly = True, states=WRITE_STATES)
    notes = fields.Text()
    
    company_id = fields.Many2one('res.company', 'Company', required=True, readonly = True, states=WRITE_STATES, default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, readonly = True, states=WRITE_STATES, default=lambda self: self.env.company.currency_id.id)    
        
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', tracking=True)
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')

    user_id = fields.Many2one(
        'res.users', string='Purchase Representative', index=True, tracking=True,
        default=lambda self: self.env.user, check_company=True)
    
    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    department_id = fields.Many2one('hr.department', default = lambda self : self.env.user.employee_ids.department_id)
    
    date = fields.Date(required = True, default = fields.Date.today)    
    
    invoice_id = fields.Many2one('account.move', readonly = True, string='Vendor Bill', copy = False)

    @api.depends('line_ids.price_total')
    def _amount_all(self):
        for record in self:
            amount_untaxed = amount_tax = 0.0
            for line in record.line_ids:
                line._compute_amount()
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            record.update({
                'amount_untaxed': record.currency_id.round(amount_untaxed),
                'amount_tax': record.currency_id.round(amount_tax),
                'amount_total': record.currency_id.round(amount_untaxed + amount_tax),
            })
        
    @api.model_create_multi
    @api.returns('self', lambda value:value.id)
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(self._name)
        
        return super(AccountCOC, self).create(vals_list)
    
    @api.onchange('purchase_order_id')
    def _onchange_purchase_order_id(self):
        if self.purchase_order_id:
            for name in ['partner_id','currency_id','company_id','notes']:
                self[name] = self.purchase_order_id[name]
                
            account_analytic_id = self.mapped('purchase_order_id.order_line.account_analytic_id')
            if len(account_analytic_id)==1:
                self.account_analytic_id = account_analytic_id

            self.line_ids = False
            
            for line in self.purchase_order_id.order_line:
                vals = { name: line[name] for name in ['sequence','name','account_analytic_id','analytic_tag_ids','price_unit','taxes_id','product_id','product_uom','display_type'] }
                vals.update({
                    'coc_id' : self.id,
                    'purchase_line_id' : line.id,
                    'product_qty' : max(line.qty_received - line.qty_coc,0),
                    'received_date' : self.date
                    })
                self.line_ids.new(vals)
        elif self.line_ids:
            self.line_ids = False
                        
    def action_create_invoice(self):
        self = self.filtered(lambda record: not record.invoice_id and record.state =='approved')      
        invoices =   self.env['account.move']
        for key, records_list in groupby(self, key = lambda record: (record.company_id, record.currency_id, record.partner_id)):
            records = self.browse()
            for record in records_list:
                records += record
            company_id, currency_id, partner_id = key
            AccountMove = self.env['account.move'].with_context(default_move_type = 'in_invoice', 
                                                                default_company_id = company_id.id,
                                                                default_currency_id = currency_id.id).with_company(company_id.id)
            vals = {
                'partner_id' : partner_id.id,
                'move_type' : 'in_invoice',
                'journal_id' : AccountMove._get_default_journal().id,
                'currency_id' : currency_id.id,
                'fiscal_position_id' : records.purchase_order_id.fiscal_position_id[:1].id or partner_id.with_company(company_id.id).property_account_position_id.id,
                'invoice_line_ids' : []
                }
            for line in records.mapped('line_ids'):
                vals['invoice_line_ids'].append((0,0, line._prepare_account_invoice_line()))
            invoice = AccountMove.create(vals)
            records.write({'invoice_id' : invoice.id})
            invoices += invoice
            
        action = self.env.ref("account.action_move_in_invoice_type").read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        
        return action