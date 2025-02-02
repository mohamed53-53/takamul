from odoo import models, fields, _, api
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    for_petty_cash = fields.Boolean(string='For Petty Cash')
    request_id = fields.Many2one(comodel_name='archer.petty.cash.request', string='Source Request')
    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', string='Analytic Account')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('chief', 'Chief Finance Operation'),
        ('validate', 'Validate'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Status',
        default='draft', compute='compute_move_id_state')
    is_submit = fields.Boolean(defalt=False)
    chief_approve = fields.Selection(selection=[('approve', 'Approve'), ('reject', 'Reject')], defalt=False)
    validate_approve = fields.Selection(selection=[('approve', 'Approve'), ('reject', 'Reject')], defalt=False)
    reject_uid = fields.Many2one(comodel_name='res.users', string='Reject By')
    reject_date = fields.Date(string='Reject Date')

    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    @api.model
    def _after_approval_states(self):
        return [('posted', 'Posted'), ('cancel', 'Cancelled')]

    def action_reject(self, reason=None):
        self.write({'state': 'rejected'})
        if reason:
            self.message_post(body=reason, subject="Reject Reason")

    def action_approve_chief(self):
        self.chief_approve = 'approve'

    def action_payment_submit(self):
        self.is_submit = True
        self.chief_approve = False
        self.validate_approve = False

    def compute_move_id_state(self):
        for rec in self:

            if not rec.chief_approve and rec.is_submit  and rec.move_id.state not in ['cancel','posted']:
                rec.state = 'chief'
            elif rec.chief_approve == 'approve' and rec.is_submit and not rec.validate_approve and rec.move_id.state not in ['cancel','posted']:
                rec.state = 'validate'
            elif rec.chief_approve == 'reject' or rec.is_submit == 'reject' or rec.move_id.state == 'cancel':
                rec.state = 'cancel'
            else:
                rec.state = rec.move_id.state

    def unlink(self):
        for rec in self:
            if rec.for_petty_cash:
                rec.request_id.write({'state': 'fin_approve'})
        return super(AccountPayment, self).unlink()

    def action_post(self):
        if self.for_petty_cash:
            self.request_id.write({'paid_amount': self.amount, 'payment_state': 'paid', 'state': 'approved'})
        return super(AccountPayment, self).action_post()

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        ''' Prepare the dictionary to create the default account.move.lines for the current payment.
        :param write_off_line_vals: Optional dictionary to create a write-off account.move.line easily containing:
            * amount:       The amount to be added to the counterpart amount.
            * name:         The label to set on the line.
            * account_id:   The account on which create the write-off.
        :return: A list of python dictionary to be passed to the account.move.line's 'create' method.
        '''
        self.ensure_one()
        write_off_line_vals = write_off_line_vals or {}

        if not self.outstanding_account_id:
            raise UserError(_(
                "You can't create a new payment without an outstanding payments/receipts account set either on the company or the %s payment method in the %s journal.",
                self.payment_method_line_id.name, self.journal_id.display_name))

        # Compute amounts.
        write_off_amount_currency = write_off_line_vals.get('amount', 0.0)

        if self.payment_type == 'inbound':
            # Receive money.
            liquidity_amount_currency = self.amount
        elif self.payment_type == 'outbound':
            # Send money.
            liquidity_amount_currency = -self.amount
            write_off_amount_currency *= -1
        else:
            liquidity_amount_currency = write_off_amount_currency = 0.0

        write_off_balance = self.currency_id._convert(
            write_off_amount_currency,
            self.company_id.currency_id,
            self.company_id,
            self.date,
        )
        liquidity_balance = self.currency_id._convert(
            liquidity_amount_currency,
            self.company_id.currency_id,
            self.company_id,
            self.date,
        )
        counterpart_amount_currency = -liquidity_amount_currency - write_off_amount_currency
        counterpart_balance = -liquidity_balance - write_off_balance
        currency_id = self.currency_id.id

        if self.is_internal_transfer:
            if self.payment_type == 'inbound':
                liquidity_line_name = _('Transfer to %s', self.journal_id.name)
            else:  # payment.payment_type == 'outbound':
                liquidity_line_name = _('Transfer from %s', self.journal_id.name)
        else:
            liquidity_line_name = self.payment_reference

        # Compute a default label to set on the journal items.

        payment_display_name = self._prepare_payment_display_name()

        default_line_name = self.env['account.move.line']._get_default_line_name(
            _("Internal Transfer") if self.is_internal_transfer else payment_display_name['%s-%s' % (self.payment_type, self.partner_type)],
            self.amount,
            self.currency_id,
            self.date,
            partner=self.partner_id,
        )

        line_vals_list = [
            # Liquidity line.
            {
                'name': liquidity_line_name or default_line_name,
                'date_maturity': self.date,
                'amount_currency': liquidity_amount_currency,
                'currency_id': currency_id,
                'debit': liquidity_balance if liquidity_balance > 0.0 else 0.0,
                'credit': -liquidity_balance if liquidity_balance < 0.0 else 0.0,
                'partner_id': self.partner_id.id,
                'account_id': self.outstanding_account_id.id,
            },
            # Receivable / Payable.
            {
                'name': self.payment_reference or default_line_name,
                'date_maturity': self.date,
                'amount_currency': counterpart_amount_currency,
                'currency_id': currency_id,
                'debit': counterpart_balance if counterpart_balance > 0.0 else 0.0,
                'credit': -counterpart_balance if counterpart_balance < 0.0 else 0.0,
                'partner_id': self.partner_id.id,
                'account_id': self.destination_account_id.id,
                # 'analytic_account_id': self.analytic_account_id.id if self.analytic_account_id else False
            },
        ]
        if not self.currency_id.is_zero(write_off_amount_currency):
            # Write-off line.
            line_vals_list.append({
                'name': write_off_line_vals.get('name') or default_line_name,
                'amount_currency': write_off_amount_currency,
                'currency_id': currency_id,
                'debit': write_off_balance if write_off_balance > 0.0 else 0.0,
                'credit': -write_off_balance if write_off_balance < 0.0 else 0.0,
                'partner_id': self.partner_id.id,
                'account_id': write_off_line_vals.get('account_id'),
            })
        return line_vals_list

    def action_draft(self):
        self.chief_approve = False
        self.is_submit = False
        self.move_id.button_draft()

    def open_reject_wizard(self):
        self.ensure_one()
        return {
            'name': _('Petty Cash Payment Register'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment.reject.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('archer_petty_cash.view_payment_reject_wizard').id,
            'target': 'new',
            'context': {
                'default_payment_id': self.id,
                'default_reject_level': self.state,
            },
        }


class PaymentRejectWizard(models.TransientModel):
    _name = 'account.payment.reject.wizard'

    payment_id = fields.Many2one(comodel_name='account.payment')
    reason = fields.Text(string='Reject Reason')
    reject_level = fields.Selection(selection=[('chief', 'Chief'), ('validate', 'Validate')])

    def action_reject(self):
        if self.reject_level == 'chief':
            self.payment_id.write({'state': 'cancel', 'chief_approve': 'reject'})
        if self.reject_level == 'validate':
            self.payment_id.write({'state': 'cancel', 'validate_approve': 'reject'})
        self.payment_id.message_post(body=self.reason, subject="Reject Reason")
