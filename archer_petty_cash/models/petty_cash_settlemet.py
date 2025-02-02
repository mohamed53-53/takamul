import datetime

from odoo import models, fields, api, _
import simplejson
from lxml import etree

from odoo.exceptions import ValidationError


class PettyCashSettlement(models.Model):
    _name = 'archer.petty.cash.settlement'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']
    _order = 'id'
    _rec_name = 'sequence'

    sequence = fields.Char(string='Name', default='/')
    request_id = fields.Many2one(comodel_name='archer.petty.cash.request', string='Source Request')
    project_id = fields.Many2one(comodel_name='project.project', related='request_id.project_id', string='Source Request')
    responsible_id = fields.Many2one(comodel_name='res.partner', related='request_id.responsible_id')
    base_amount = fields.Float(related='request_id.paid_amount')
    consumed_amount = fields.Float(string='Consumed Amount', compute='_compute_remaining_consumed_amount')
    remaining_amount = fields.Float(string='Remaining Amount', compute='_compute_remaining_consumed_amount')
    base_remaining_amount = fields.Float(string='Base Remaining Amount', compute='_compute_remaining_consumed_amount')
    payment_journal_id = fields.Many2one(comodel_name='account.journal', related='request_id.payment_journal_id')
    state = fields.Selection([])
    settlement_line_ids = fields.One2many(comodel_name='archer.petty.cash.settlement.line', inverse_name='settlement_id', string='Lines')
    can_approve_draft = fields.Boolean(compute='_compute_can_approve_draft')
    currency_id = fields.Many2one(comodel_name='res.currency', related='request_id.currency_id')
    entry_id = fields.Many2one(comodel_name='account.move', string='Entry')
    sttel_month = fields.Selection(selection=[
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ], string='Month')
    sttel_year = fields.Selection([(str(y), str(y)) for y in range((datetime.datetime.now().year - 1), (datetime.datetime.now().year + 2) )], 'Year')

    def _compute_can_approve_draft(self):
        for rec in self:
            rec.can_approve_draft = False if rec.request_id.settlement_ids.filtered(
                lambda s: s.state != 'approved' and s.id != rec.id) else True

    @api.depends('settlement_line_ids')
    @api.onchange('settlement_line_ids')
    def _compute_remaining_consumed_amount(self):
        for rec in self:
            rec.base_remaining_amount = rec.base_amount - sum(
                rec.request_id.settlement_ids.filtered(lambda s: s.state == 'approved').mapped('consumed_amount'))
            rec.consumed_amount = sum(rec.settlement_line_ids.mapped('amount'))
            rec.remaining_amount = rec.base_remaining_amount - rec.consumed_amount

    @api.model
    def create(self, vals_list):
        vals_list['sequence'] = self.env['ir.sequence'].next_by_code('archer_petty_cash.petty_cash_settlement_seq') or '/'
        return super(PettyCashSettlement, self).create(vals_list)

    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    def action_reject(self, reason=None):
        self.write({'state': 'rejected'})
        if reason:
            self.message_post(body=reason, subject="Reject Reason")

    def action_approve(self):
        for rec in self:
            if rec.state == 'draft':
                if rec.settlement_line_ids:
                    rec.write({'state': 'hr_admin_approve'})
                else:
                    raise ValidationError(_('Please set lines first'))
            elif rec.state == 'fin_approve':
                if rec.settlement_line_ids.filtered(lambda s: not s.group_id):
                    raise ValidationError(_('Please set group for all lines'))
                else:
                    line_vals = [(0, 0, {
                        'name': '[%s] %s Petty Cash '%(rec.sequence,rec.responsible_id.name),
                        'account_id': rec.payment_journal_id.default_account_id.id,
                        'currency_id': rec.currency_id.id,
                        'debit': 0.0,
                        'credit': abs(rec.consumed_amount),
                    })]
                    for line in rec.settlement_line_ids:
                        line_vals.append((0, 0, {
                            'name': '[%s] %s' % (line.ref, line.line_description),
                            'account_id': line.group_id.account_id.id,
                            'currency_id': line.currency_id.id,
                            'debit': abs(line.amount),
                            'credit': 0.0,
                            'partner_id': line.partner_id.id,
                            'analytic_account_id': rec.project_id.analytic_account_id.id,
                        }))

                    vals = {
                        'move_type': 'entry',
                        'date': datetime.datetime.now().date(),
                        'ref': rec.sequence,
                        'model_name': rec._name,
                        'origin_id': rec.id,
                        'project_id': rec.project_id.id,
                        'journal_id': rec.payment_journal_id.id,
                        'line_ids': line_vals,
                    }
                    move = self.env['account.move'].create(vals)
                    rec.entry_id = move.id
                    super().action_approve()
            else:
                super().action_approve()


class PettyCashSettlementLine(models.Model):
    _name = 'archer.petty.cash.settlement.line'

    settlement_id = fields.Many2one(comodel_name='archer.petty.cash.settlement', string='Settlement')
    line_date = fields.Date(string='Date', required=True)
    line_description = fields.Char(string='Description', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
    amount = fields.Float(string='Amount', required=True)
    ref = fields.Char(string='Reference')
    attach = fields.Binary(string='Attachment', required=True)
    group_id = fields.Many2one(comodel_name='archer.petty.cash.group', string='Group')
    settle_state = fields.Selection(related='settlement_id.state')
    state = fields.Selection(selection=[('draft', 'Draft'), ('approve', 'Approve'), ('reject', 'Reject')])
    currency_id = fields.Many2one(comodel_name='res.currency', related='settlement_id.currency_id')

class PettyCashGroup(models.Model):
    _name = 'archer.petty.cash.group'

    name = fields.Char(string='Name')
    account_id = fields.Many2one(comodel_name='account.account', doamin=[('user_type_id.internal_group','=','expense')])