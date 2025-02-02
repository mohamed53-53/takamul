import datetime

import simplejson
from lxml import etree

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PettyCashRequest(models.Model):
    _name = 'archer.petty.cash.request'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']
    _rec_name = 'sequence'

    project_id = fields.Many2one(comodel_name='project.project', string='Project', required=True,
                                 domain=lambda p: [('petty_cash_responsible_id', '=', p.env.user.partner_id.id)])
    responsible_id = fields.Many2one(comodel_name='res.partner', string="Petty Cash Responsible",
                                     related='project_id.petty_cash_responsible_id')
    amount = fields.Float(string='Amount', required=True)
    paid_amount = fields.Float(string='Paid Amount', required=True)
    state = fields.Selection([])
    payment_state = fields.Selection(selection=[('not_paid', 'Not Paid'), ('paid', 'Paid')], string='Payment Status', required=True,
                                     default='not_paid')
    sequence = fields.Char(string='Sequence', default="/")
    payment_id = fields.Many2one(comodel_name='account.payment', string='Payment')
    payment_entry_id = fields.Many2one(comodel_name='account.move', string='Payment Entry', related='payment_id.move_id')
    payment_journal_id = fields.Many2one(comodel_name='account.journal', string='Payment Journal', related='payment_id.journal_id')
    consumed_amount = fields.Float(string='Consumed Amount', compute='_compute_remaining_consumed_amount')
    remaining_amount = fields.Float(string='Remaining Amount', compute='_compute_remaining_consumed_amount')
    in_settlement_amount = fields.Float(string='In Settlement Amount', compute='_compute_remaining_consumed_amount')
    settlement_ids = fields.One2many(comodel_name='archer.petty.cash.settlement', inverse_name='request_id', string='Settlement')
    settlement_count = fields.Integer(compute='_compute_count_settlement')
    can_create_settlement = fields.Boolean(compute='_compute_create_settlement_state')
    company_id = fields.Many2one(comodel_name='res.company', readonly=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name='res.currency', related='company_id.currency_id')
    entries_count = fields.Integer(compute='compute_settlements_count')
    cluser_state = fields.Selection(selection=[('open', 'Open'), ('close', 'Close')], default='open')
    request_month = fields.Selection(selection=[
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
    ], string='Month', required=1)
    request_year = fields.Selection(
        [(str(y), str(y)) for y in range((datetime.datetime.now().year - 1), (datetime.datetime.now().year + 2))], string='Year',
        required=True)

    def action_close_request(self):
        for rec in self:
            if rec.remaining_amount != 0.0:
                raise ValidationError(_('Remaining Amount must be zero'))
            else:
                rec.cluser_state = 'close'

    @api.depends('request_month', 'request_year')
    @api.onchange('request_month', 'request_year')
    def validate_month_year(self):
        for rec in self:
            if rec.request_year:
                if int(rec.request_year) != datetime.datetime.now().year:
                    rec.request_year = False
                    raise ValidationError('Must select current Year')
            if rec.request_month:
                if int(rec.request_month) != datetime.datetime.now().month:
                    rec.request_month = False
                    raise ValidationError('Must select current Month')

    @api.depends('settlement_ids')
    @api.onchange('settlement_ids')
    def _compute_create_settlement_state(self):
        for rec in self:
            rec.can_create_settlement = False if rec.settlement_ids.filtered(lambda s: s.state == 'draft') else True

    @api.depends('settlement_ids')
    @api.onchange('settlement_ids')
    def _compute_remaining_consumed_amount(self):
        for rec in self:
            rec.consumed_amount = sum(
                rec.settlement_ids.filtered(lambda s: s.state == 'approved').mapped('consumed_amount')) if rec.settlement_ids else 0.0
            rec.remaining_amount = rec.paid_amount - rec.consumed_amount
            rec.in_settlement_amount = sum(
                rec.settlement_ids.filtered(lambda s: s.state != 'approved').mapped('consumed_amount')) if rec.settlement_ids else 0.0

    def compute_settlements_count(self):
        for rec in self:
            rec.entries_count = len(self.settlement_ids.entry_id)

    def open_sttelments_entries(self):
        self.ensure_one()
        return {
            'name': _('Entries'),
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False, 'duplicate': False},
            'domain': [('id', 'in', self.settlement_ids.entry_id.ids)],
            'target': 'current',
        }

    def _compute_count_settlement(self):
        for rec in self:
            rec.settlement_count = len(rec.settlement_ids)

    def get_request_settlements(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Settlement(s)'),
            'view_mode': 'tree,form',
            'res_model': 'archer.petty.cash.settlement',
            'domain': [('request_id', '=', self.id)],
            'context': {
                'create': False,
                'delete': False,
                'duplicate': False,
            }
        }

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(PettyCashRequest, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
                                                            submenu=False)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in res['fields']:
                for node in doc.xpath("//field[@name='%s']" % field):
                    modifiers = simplejson.loads(node.get("modifiers"))
                    if 'readonly' not in modifiers:
                        modifiers['readonly'] = [['state', '!=', 'draft']]
                    else:
                        if type(modifiers['readonly']) != bool:
                            modifiers['readonly'].insert(0, '|')
                            modifiers['readonly'] += [['state', '!=', 'draft']]
                    node.set('modifiers', simplejson.dumps(modifiers))
                    res['arch'] = etree.tostring(doc)
        return res

    def create_new_settlement(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Settlement'),
            'view_mode': 'form',
            'res_model': 'archer.petty.cash.settlement',
            'context': {
                'default_request_id': self.id,
                'default_sttel_month': self.request_month,
                'default_sttel_year': self.request_year
            }
        }

    @api.model
    def create(self, vals_list):
        if self.env['archer.petty.cash.request'].searc(
                [('request_month', '=', vals_list['request_month']), ('request_year', '=', vals_list['request_year']),
                 ('cluser_state', '=', 'open')]):
            raise ValidationError('You can\'t create new request for same month with open old request')
        else:
            vals_list['sequence'] = self.env['ir.sequence'].next_by_code('archer_petty_cash.petty_cash_request_seq') or '/'
            return super(PettyCashRequest, self).create(vals_list)

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
                if self.env['archer.petty.cash.request'].searc(
                        [('request_month', '=', rec.request_month), ('request_year', '=', rec.request_year),
                         ('cluser_state', '=', 'open')]):
                    raise ValidationError('You can\'t create new request for same month with open old request')
                else:
                    rec.write({'state': 'submit'})
            elif rec.state == 'fin_approve' and not rec.payment_id:
                raise ValidationError(_('Please Regist Payment First'))
            else:
                super().action_approve()

    def register_payment(self):
        self.ensure_one()
        return {
            'name': _('Petty Cash Payment Register'),
            'type': 'ir.actions.act_window',
            'res_model': 'archer.petty.cash.payment.register',
            'view_mode': 'form',
            'view_id': self.env.ref('archer_petty_cash.view_archer_petty_cash_payment_register_wizard').id,
            'target': 'new',
            'context': {
                'default_request_id': self.id,
                'default_partner_id': self.responsible_id.id,
                'default_amount': self.amount
            },
        }

    # def write(self, vals):
    #     if self.state == 'approved':
    #         raise ValidationError('You can\'t change status of Approved Request')
    #     elif self.payment_id and self.state in ['fin_approve','in_payment'] and vals['state'] in ['submit','hr_admin_approve','hr_mngr_approve','ceo_approve']:
    #         raise  ValidationError('You can\'t change status')
    #     else:
    #         return super(PettyCashRequest, self).write(vals)
