# -*- coding: utf-8 -*-
from odoo.addons.archer_employee_request.models.fmc_helper import handle_approve_fcm_msg
from odoo.addons.archer_api_custom.controllers.utils.utils import get_next_approve
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from lxml import etree
import json
import simplejson


class BusinessTrip(models.Model):
    _name = "business.trip"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']
    _rec_name = 'sequence'
    _description = 'Business Trip'

    sequence = fields.Char('Sequence', copy=False, readonly=True, default=lambda x: _('New'))
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    project_id = fields.Many2one("project.project", related="employee_id.project_id", string="Project")
    destination_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Destination Country",
        domain=[('name', '!=', 'Israel')],
        required=True,
    )
    destination_city_id = fields.Many2one(comodel_name="res.country.state", string="Destination City")
    date_from = fields.Date("Date From", required=True)
    date_to = fields.Date("Date To", required=True)
    number_of_days = fields.Integer(string="Number of Days", compute="_compute_number_of_days")
    purpose = fields.Selection(
        string="Purpose",
        selection=[("work_stay", "Work Stay"), ("training_or_education", "Training/Education"), ("other", "Other")],
        required=True,
    )
    occasion_or_purpose = fields.Text(string="Occasion/Purpose")
    method_of_payment = fields.Selection(
        selection=[("direct_deposit", "Direct Deposit"), ("cash", "Cash")],
        string="Method of Payment",
        required=True,
    )
    travel_tickets = fields.Boolean(string="Travel Tickets", required=True)
    rejection_reason = fields.Text("Rejection Reason")
    supportive_document = fields.Binary(string="Supportive Document", attachment=True)
    state = fields.Selection([])
    can_cancel = fields.Boolean(string='Can Cancel', default=False, compute='_compute_can_cancel_approve')
    can_approve = fields.Boolean(string='Can Approve', default=False, compute='_compute_can_cancel_approve')
    active = fields.Boolean(string='Active', default=True)
    amount = fields.Float(string='Amount')
    expense_revision_id = fields.Many2one(comodel_name='account.expense.revision', string='Expense Revision',
                                          readonly=True)
    account_move_id = fields.Many2one(comodel_name='account.move', string='Related Entry')

    def _compute_can_cancel_approve(self):
        for rec in self:
            rec.can_cancel = True if rec.state in ['submit'] and rec.env.uid == rec.create_uid.id else False
            state = rec.env['approval.config'].sudo().search([('model', '=', rec._name), ('state', '=', rec.state)],
                                                             limit=1)
            if state:
                if rec.env.uid in state.group_ids.users.ids:
                    rec.can_approve = True
                else:
                    rec.can_approve = False
            else:
                rec.can_approve = False

    @api.onchange('date_to')
    def onchange_date_to(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                if rec.date_from > rec.date_to:
                    raise ValidationError(_('To date must be grater then from date'))

    @api.model
    def create(self, vals):
        if (not vals.get('sequence') or vals['name'] == _('New')):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('business.trip') or '/'
        return super().create(vals)

    @api.depends('date_from', 'date_to')
    def _compute_number_of_days(self):
        for business in self:
            days = 0
            if business.date_to and business.date_from:
                no_days = business.date_to - business.date_from
                days = no_days.days
            business.number_of_days = days

    @api.model
    def _before_approval_states(self):
        return [("draft", "Draft")]

    def action_reject(self, reason=None):
        for rec in self:
            rec.write({'state': 'rejected'})
            if reason:
                rec.message_post(body=reason, subject="Reject Reason")

    def action_approve(self):
        for rec in self:
            if rec.state == 'draft':
                rec.write({'state': 'submit'})
            elif rec.state == 'submit':
                rec.write({'state': get_next_approve(rec)})
            elif rec.state == 'hr_approve':
                rec.expense_revision_id = rec.create_expense_revision(rec).id
                return super().action_approve()

            else:
                return super().action_approve()

    def write(self, vals):
        res = super(BusinessTrip, self).write(vals)
        if self.state not in ['draft', 'submit', 'po_approve'] and self.amount <= 0:
            raise ValidationError(_('Amount must be greater then zero'))

        if self.state in ['approved', 'rejected']:
            handle_approve_fcm_msg(self)
        return res

    def create_expense_revision(self, obj):
        account_expense_id = self.env['account.expense.service'].search([('model_id.model', '=', obj._name)],
                                                                        limit=1).product_id.property_account_expense_id
        accrued_expense_account_id = self.env['ir.config_parameter'].sudo().get_param(
            'archer_project_custom.accrued_expense_account_id')
        accrued_expense_journal_id = self.env['ir.config_parameter'].sudo().get_param(
            'archer_project_custom.accrued_expense_journal_id')
        if not accrued_expense_account_id:
            raise ValidationError(_('Please Check Accrued Expense Account'))
        if not accrued_expense_journal_id:
            raise ValidationError(_('Please Check Accrued Expense Journal'))
        else:
            if account_expense_id:
                vals = {
                    'origin_model': obj._name,
                    'origin_id': obj.id,
                    'reference': obj.sequence if obj.sequence else False,
                    'project_id': obj.project_id.id,
                    'accrued_expense_journal_id': int(accrued_expense_journal_id),
                    'expense_account_id': account_expense_id.id,
                    'accrued_expense_account_id': int(accrued_expense_account_id),
                    'amount': obj.amount,
                    'state': 'draft',
                    'partner_id': obj.employee_id.user_partner_id.id
                }
                return self.env['account.expense.revision'].create(vals)
            else:
                raise ValidationError(_('Please Check Service Account'))
