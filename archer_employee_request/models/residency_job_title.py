# -*- coding: utf-8 -*-
from odoo.addons.archer_employee_request.models.fmc_helper import handle_approve_fcm_msg
from odoo.addons.archer_api_custom.controllers.utils.utils import get_next_approve
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from lxml import etree
import json
import simplejson


class ResidencyJobTitle(models.Model):
    _name = "residency.job.title"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']
    _rec_name = 'sequence'
    _description = 'Residency Job Title'

    sequence = fields.Char('Sequence', copy=False, readonly=True, default=lambda x: _('New'))
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True,
                                  domain="[('residency_issuance_id', '!=', False)]")
    project_id = fields.Many2one("project.project", related="employee_id.project_id", string="Project")
    residency_number = fields.Char(string="Residency Number", related="employee_id.residency_number")
    serial_number = fields.Char(string="Serial Number", related="employee_id.serial_number")
    employee_position_id = fields.Many2one("hr.job", string="Position", related="employee_id.job_id")
    old_job_title = fields.Char(string="Old Job Title", related="employee_id.job_title")
    new_job_title = fields.Char(string="New Job Title", required=True)
    change_reason = fields.Text(string="Change Reason", required=True)
    supportive_document_1 = fields.Binary(string="Supportive Document 1", attachment=True)
    supportive_document_2 = fields.Binary(string="Supportive Document 2", attachment=True)
    amount = fields.Float("Expense")
    state = fields.Selection([])
    expiration_date = fields.Date("Expiration Date")
    can_cancel = fields.Boolean(string='Can Cancel', default=False, compute='_compute_can_cancel_approve')
    can_approve = fields.Boolean(string='Can Approve', default=False, compute='_compute_can_cancel_approve')
    expense_revision_id = fields.Many2one(comodel_name='account.expense.revision', string='Expense Revision',
                                          readonly=True)
    active = fields.Boolean(string='Active', default=True)
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

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ResidencyJobTitle, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
                                                             submenu=False)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in res['fields']:
                for node in doc.xpath("//field[@name='%s']" % field):
                    modifiers = simplejson.loads(node.get("modifiers"))
                    modifiers_condition = ['state', '!=', 'draft']
                    if field == 'amount':
                        modifiers_condition = ['state', 'in',
                                               ['expense_approve', 'in_progress', 'approved', 'rejected']]
                    elif field == 'expiration_date':
                        modifiers_condition = ['state', 'in', ['approved', 'rejected']]
                    if 'readonly' not in modifiers:
                        modifiers['readonly'] = [modifiers_condition]
                    else:
                        if type(modifiers['readonly']) != bool:
                            modifiers['readonly'].insert(0, '|')
                            modifiers['readonly'] += [modifiers_condition]
                    node.set('modifiers', simplejson.dumps(modifiers))
                    res['arch'] = etree.tostring(doc)
        return res

    @api.model
    def create(self, vals):
        if (not vals.get('sequence') or vals['name'] == _('New')):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('residency.job.title') or '/'
        return super().create(vals)

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
            elif rec.state == 'po_approve':
                rec.write({'state': get_next_approve(rec)})
            elif rec.state == 'hr_approve':
                if rec.amount == 0:
                    raise ValidationError(_('Expense Amount must be greater then zero'))
                else:
                    return super(ResidencyJobTitle, self).action_approve()
            elif rec.state == 'expense_approve':
                expense_revision = self.crete_expense_revision(obj=self)
                expense_revision.message_post_with_view('mail.message_origin_link',
                                                        values={'self': expense_revision, 'origin': rec},
                                                        subtype_id=self.env.ref('mail.mt_note').id
                                                        )
                rec.write({
                    'expense_revision_id': expense_revision.id,
                })
                return super(ResidencyJobTitle, self).action_approve()
            elif rec.state == 'in_progress':
                if not rec.expiration_date:
                    raise ValidationError(_('Please Enter Expiration date before approve !'))
                else:
                    rec.employee_id.sudo().write({
                        'residency_job_title_date': rec.expiration_date,
                    })
                    return super(ResidencyJobTitle, self).action_approve()
            else:
                return super(ResidencyJobTitle, self).action_approve()

    def crete_expense_revision(self, obj):
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
                }
                return self.env['account.expense.revision'].create(vals)
            else:
                raise ValidationError(_('Please Check Service Account'))

    def write(self, vals):
        res = super(ResidencyJobTitle, self).write(vals)
        if self.state in ['approved','rejected']:
            handle_approve_fcm_msg(self)
        return res