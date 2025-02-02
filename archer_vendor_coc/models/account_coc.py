# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from odoo.tools import groupby
from . import account_coc


class AccountMove(models.Model):
    _inherit = 'account.payment'
    vendor_coc_id = fields.Many2one(comodel_name='account.coc', string='Vendor CoC')


class AccountCoC(models.Model):
    _inherit = 'account.coc'
    coc_payment_type_id = fields.Many2one(comodel_name='account.coc.payment.type', string='Payment Type', required=True)
    po_related = fields.Boolean(string='PO Related', related='coc_payment_type_id.po_related')

    project_id = fields.Many2one(comodel_name='project.project', required=True)
    invoice_number = fields.Char(string='Invoice Number', required=True)

    @api.depends('project_id')
    @api.onchange('project_id')
    def onchange_project_id(self):
        for rec in self:
            rec.account_analytic_id = rec.project_id.analytic_account_id

    @api.constrains('invoice_number')
    def _check_mobile_unique(self):
        invoice_counts = self.search_count(
            [('invoice_number', '=', self.invoice_number), ('partner_id', '=', self.partner_id.id), ('id', '!=', self.id)])
        if invoice_counts > 0:
            raise ValidationError("Invoice number already exists!")

    contract = fields.Char(string='Contract')
    contract_from_date = fields.Date(string='Contract From Date')
    contract_to_date = fields.Date(string='Contract To Date')
    advance_payment = fields.Boolean(string='Advance Payment')
    expected_sla_approve = fields.Datetime(string='Expected SLA')
    waiting_time = fields.Char(string='Waiting Time')
    history_ids = fields.One2many(comodel_name='account.coc.history', string='History', inverse_name='coc_id')
    def action_register_payment(self):
        ''' Open the account.payment.register wizard to pay the selected journal entries.
        :return: An action opening the account.payment.register wizard.
        '''
        return {
            'name': _('Register Payment'),
            'res_model': 'account.coc.payment.register',
            'view_mode': 'form',
            'context': {
                'default_coc_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_amount': self.amount_total
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    def action_approve(self):
        history = self.env['account.coc.history'].create({
            'coc_id': self.id,
            'action_state': self.state,
            'action_date': fields.Date.today(),
            'action_uid': self.env.uid,
        })
        return super().action_approve()


class AccountCoCPaymentType(models.Model):
    _name = 'account.coc.payment.type'
    po_related = fields.Boolean(string='PO Related')
    name = fields.Char(string='Name')


class AccountCoCHistory(models.Model):
    _name = 'account.coc.history'

    def get_coc_states(self):
        states = self.env['approval.config'].sudo().search([('model','=','account.coc')], order='sequence')
        states_lis = states.mapped(lambda s:(s.state, s.name))
        return states_lis+[('draft','Draft'),('rejected','Rejected'),('approved','Approved')]

    coc_id = fields.Many2one(comodel_name='account.coc', string='Account COC')
    action_state = fields.Selection(get_coc_states, string='Action State')
    action_date = fields.Datetime(string='Action Date')
    action_uid = fields.Many2one(comodel_name='res.users', string='Action User')


class AccountSLA(models.Model):
    _name = 'account.coc.sla'

    def get_coc_states(self):
        states = self.env['approval.config'].sudo().search([('model','=','account.coc')], order='sequence')
        states_lis = states.mapped(lambda s:(s.state, s.name))
        return states_lis+[('draft','Draft'),('rejected','Rejected'),('approved','Approved')]

    action_state = fields.Selection(get_coc_states, string='Action State')
    timing = fields.Integer(string='waiting time in state/hours')
