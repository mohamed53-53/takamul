from odoo import models, fields, api


class PettyCashPaymentRegister(models.TransientModel):
    _name = 'account.coc.payment.register'

    coc_id = fields.Many2one(comodel_name='account.coc')
    payment_date = fields.Date(string="Payment Date", required=True, default=fields.Date.context_today,)
    amount = fields.Monetary(currency_field='currency_id', store=True, readonly=False, required=True)
    company_id = fields.Many2one(comodel_name='res.company', readonly=True,store=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name='res.currency', related='company_id.currency_id')
    partner_id = fields.Many2one(comodel_name='res.partner', string="Responsible", store=True, copy=False, ondelete='restrict', )
    journal_id = fields.Many2one(comodel_name='account.journal', domain=[('type', 'in', ['bank','cash'])], required=True,)
    available_partner_bank_ids = fields.Many2many(
        comodel_name='res.partner.bank',
        compute='_compute_available_partner_bank_ids',
    )
    payment_method_line_id = fields.Many2one('account.payment.method.line', string='Payment Method',
                                             readonly=False, store=True, copy=False,
                                             compute='_compute_payment_method_line_id',
                                             domain="[('id', 'in', available_payment_method_line_ids)]",
                                             )
    available_payment_method_line_ids = fields.Many2many('account.payment.method.line',
                                                         compute='_compute_payment_method_line_fields')
    hide_payment_method_line = fields.Boolean(
        compute='_compute_payment_method_line_fields',
        help="Technical field used to hide the payment method if the selected journal has only one available which is 'manual'")
    payment_method_id = fields.Many2one(
        related='payment_method_line_id.payment_method_id',
        string="Method",
        tracking=True,
        store=True
    )
    partner_bank_id = fields.Many2one('res.partner.bank', string="Recipient Bank Account",
                                      readonly=False, store=True, tracking=True,
                                      compute='_compute_partner_bank_id',
                                      domain="[('id', 'in', available_partner_bank_ids)]",
                                      check_company=True)

    @api.depends('available_payment_method_line_ids')
    def _compute_payment_method_line_id(self):
            available_payment_method_lines = self.available_payment_method_line_ids

            if self.payment_method_line_id in available_payment_method_lines:
                self.payment_method_line_id = self.payment_method_line_id
            elif available_payment_method_lines:
                self.payment_method_line_id = available_payment_method_lines[0]._origin
            else:
                self.payment_method_line_id = False

    @api.depends('available_partner_bank_ids', 'journal_id')
    def _compute_partner_bank_id(self):
            self.partner_bank_id = self.available_partner_bank_ids[:1]._origin
    @api.depends('partner_id', 'company_id',)
    def _compute_available_partner_bank_ids(self):
                self.available_partner_bank_ids = self.partner_id.bank_ids \
                    .filtered(lambda x: x.company_id.id in (False, self.company_id.id))._origin
    @api.depends('journal_id')
    def _compute_payment_method_line_fields(self):
            self.available_payment_method_line_ids = self.journal_id._get_available_payment_method_lines('outbound')
            if self.payment_method_line_id.id not in self.available_payment_method_line_ids.ids:
                self.hide_payment_method_line = False
            else:
                self.hide_payment_method_line = len(self.available_payment_method_line_ids) == 1 and self.available_payment_method_line_ids.code == 'manual'

    def action_confirm_payment(self):
        self.ensure_one()
        payment = self.env['account.payment'].create({
            'payment_type': 'outbound',
            'partner_type': 'customer',
            'amount': self.amount,
            'date': fields.Date.today(),
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'journal_id': self.journal_id.id,
            'payment_method_line_id': self.journal_id.outbound_payment_method_line_ids[0].id,
            'ref': 'Vendor COC %s'%self.coc_id.name,
            'for_petty_cash':True,
            'vendor_coc_id':self.coc_id.id,
            'analytic_account_id':self.coc_id.project_id.analytic_account_id.id,
        })
