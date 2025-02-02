# -*- coding: utf-8 -*-

import datetime

from odoo.addons.archer_employee_request.models.fmc_helper import handle_approve_fcm_msg
from odoo.addons.archer_api_custom.controllers.utils.utils import get_next_approve
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from lxml import etree
import json
import simplejson


class ResidencyIssuance(models.Model):
    _name = "residency.issuance"
    _description = 'Residency Issuance'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']
    _rec_name = 'sequence'

    sequence = fields.Char('Sequence', copy=False, readonly=True, default=lambda x: _('New'))
    request_type = fields.Selection([
        ('residency_issuance', 'Residency Issuance'),
        ('residency_renewal', "Residency Renewal")], "Request Type")

    employee_id = fields.Many2one(comodel_name='hr.employee', domain=[('country_code', '!=', 'SA')])
    employee_position = fields.Many2one('hr.job', related="employee_id.job_id")
    project_id = fields.Many2one("project.project", related="employee_id.project_id")
    residency_id = fields.Many2one("residency.residency", string="Residency Type", )
    residency_type = fields.Selection(related="residency_id.residency_type")
    document_ids = fields.One2many("residency.issuance.document", string="Documents", inverse_name='request_id')
    sponsor_name = fields.Char("Sponsor Name")
    sponsor_phone = fields.Char("Sponsor Phone")
    sponsor_address = fields.Text("Sponsor Address")

    name = fields.Char("Name (As in Passport)")
    arabic_name = fields.Char("Arabic Name")
    relation = fields.Selection([('father', 'Father'), ('mother', 'Mother'), ('spouse', 'Spouse'), ('child', "Child")], string="Relation")
    nationality = fields.Many2one('res.country', 'Nationality')
    religion = fields.Selection([
        ('muslim', 'Muslim'),
        ('not_muslim', "Not Muslim")], "Religion")
    date_of_birth = fields.Date("Date of Birth")
    job_title = fields.Char("Residency Job Title")
    company_id = fields.Many2one('res.company', string='Company', readonly=True, related='project_id.company_id')
    currency_id = fields.Many2one(comodel_name='res.currency', related='company_id.currency_id')
    number = fields.Char("Residency Number")
    serial_number = fields.Char("Residency Serial Number")
    re_job_title = fields.Char("Residency Job Title")
    place_of_issuance = fields.Char("Place of Issuance")
    issuance_date = fields.Date("Issuance Date")
    expiration_date = fields.Date("Expiration Date")
    expiration_date_in_hijri = fields.Char("Expiration Date in Hijri", readonly=True )
    arrival_date = fields.Date("Arrival Date")
    state = fields.Selection([])
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], required=True)
    employee_renewal_id = fields.Many2one('hr.employee', string="Employee",
                                          domain="[('issuance_date', '<=', context_today().strftime('%Y-%m-%d'))]")
    renewal_project_id = fields.Many2one("project.project", related="employee_renewal_id.project_id")
    employee_renewal_residency_number = fields.Char("Residency Number", related="employee_renewal_id.residency_number")
    renewal_expiration_date = fields.Date("Residency Expiration Date", related="employee_renewal_id.expiration_date")
    amount = fields.Monetary(string="Fees Amount", currency_field='currency_id')
    renewal_reason = fields.Text("Renewal Reason")
    expense_revision_id = fields.Many2one(comodel_name='account.expense.revision', string='Expense Revision', readonly=True)
    account_move_id = fields.Many2one(comodel_name='account.move', string='Journal Entry')
    pending_fees_paid = fields.Boolean(string="Pending Fees Paid")
    can_cancel = fields.Boolean(string='Can Cancel', default=False, compute='_compute_can_cancel_approve')
    can_approve = fields.Boolean(string='Can Approve', default=False, compute='_compute_can_cancel_approve')
    active = fields.Boolean(string='Active', default=True)


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

    @api.depends('expiration_date')
    @api.onchange('expiration_date')
    def onchange_expiration_date(self):
        for rec in self:
            if rec.expiration_date < rec.issuance_date:
                raise ValidationError(_('Expiration Date must be greater then Issuance Date'))

    @api.depends('employee_id')
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        for rec in self:
            if rec.residency_type == 'employee' or not rec.residency_type:
                rec.nationality = rec.employee_id.country_id.id
                rec.gender = rec.employee_id.gender
                rec.religion = rec.employee_id.religion
                rec.date_of_birth = rec.employee_id.birthday

    @api.depends('date_of_birth')
    @api.onchange('date_of_birth')
    def onchange_birthdate(self):
        for resd in self:
            if resd.date_of_birth:
                if resd.date_of_birth > datetime.datetime.now().date():
                    raise ValidationError(_('Date of Birth must be equal or greater then today'))

    @api.depends('residency_id')
    @api.onchange('residency_id')
    def onchange_residency_type(self):
        for rec in self:
            rec.document_ids = False
            rec.document_ids = [(0, 0, {
                'document_name': x.id,
            }) for x in rec.residency_id.document_ids]

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ResidencyIssuance, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
                                                             submenu=False)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in res['fields']:
                field_list = ['employee_id', 'employee_position', 'project_id', 'residency_id', 'sponsor_name', 'sponsor_phone',
                              'sponsor_address',
                              'name', 'arabic_name', 'residency_type', 'expense',
                              'relation', 'nationality', 'religion', 'date_of_birth', 'job_title',
                              ]
                if field in field_list:
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

    @api.model
    def create(self, vals):
        request_type = vals.get('request_type', False)
        if  request_type and request_type == 'residency_issuance':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('residency.issuance') or '/'
        elif request_type and request_type == 'residency_renewal':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('residency.renewal') or '/'
        res = super().create(vals)
        res.document_ids.write({'request_id': res.id})
        return res

    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        if self.date_of_birth and self.date_of_birth >= fields.Date.today():
            raise UserError(_('Date of Birth Must be greater Than Today.'))

    def action_reject(self, reason=None):
        for rec in self:
            if rec.state == 'pending_fees':
                rec.pending_fees_paid = False
            else:
                rec.write({'state': 'rejected'})
                if reason:
                    rec.message_post(body=reason, subject="Reject Reason")

    def action_approve(self):
        for rec in self:
            if rec.state == 'draft':
                rec.write({'state': 'po_approve'})
            elif rec.state == 'po_approve':
                rec.write({'state': get_next_approve(rec)})
            elif rec.state == 'hr_approve':
                if rec.document_ids.filtered(lambda d: not d.received):
                    raise ValidationError(_('You must receive all documents'))
                elif rec.amount == 0:
                    raise ValidationError(_('Expense Amount must be greater then zero'))
                else:
                    if rec.request_type == 'residency_renewal':
                        return super(ResidencyIssuance, self).action_approve()
                    else:
                        rec.write({'state': 'expense_approve'})
            elif rec.state == 'pending_fees':
                rec.pending_fees_paid = True
                return super(ResidencyIssuance, self).action_approve()
            elif rec.state == 'expense_approve':
                expense_revision = self.crete_expense_revision(obj=self)
                expense_revision.message_post_with_view('mail.message_origin_link',
                                                        values={'self': expense_revision, 'origin': rec},
                                                        subtype_id=self.env.ref('mail.mt_note').id
                                                        )
                rec.write({'expense_revision_id': expense_revision.id})
                return super(ResidencyIssuance, self).action_approve()
            elif rec.state == 'in_progress':
                rec.employee_id.write({
                    'residency_number': rec.number,
                    'serial_number': rec.serial_number,
                    'resid_job_title': rec.re_job_title,
                    'place_of_issuance': rec.place_of_issuance,
                    'issuance_date': rec.issuance_date,
                    'expiration_date': rec.expiration_date,
                    'expiration_date_in_hijri': rec.expiration_date_in_hijri,
                    'residency_issuance_id' : rec.id
                })
                rec.employee_id.message_post(body='Residency Updated by Request #%s' % rec.sequence, subject="Residency Updated")
                return super(ResidencyIssuance, self).action_approve()
            else:
                return super(ResidencyIssuance, self).action_approve()

    def crete_expense_revision(self, obj):
        account_expense_id = self.env['account.expense.service'].search([('model_id.model', '=', obj._name)],
                                                                        limit=1).product_id.property_account_expense_id
        accrued_expense_account_id = self.env['ir.config_parameter'].sudo().get_param('archer_project_custom.accrued_expense_account_id')
        accrued_expense_journal_id = self.env['ir.config_parameter'].sudo().get_param('archer_project_custom.accrued_expense_journal_id')
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
                    'partner_id':obj.employee_id.user_partner_id.id
                }
                return self.env['account.expense.revision'].create(vals)
            else:
                raise ValidationError(_('Please Check Service Account'))

    def write(self, vals):
        res = super(ResidencyIssuance, self).write(vals)
        if self.state in ['approved','rejected']:
            handle_approve_fcm_msg(self)
        return res
class ResidencyIssuanceDocument(models.Model):
    _name = 'residency.issuance.document'
    _rec_name = 'document_name'

    request_id = fields.Many2one(comodel_name='residency.issuance')
    document_name = fields.Many2one(comodel_name='residency.residency.document', store=True)
    received = fields.Boolean(string='Received', default=False)
