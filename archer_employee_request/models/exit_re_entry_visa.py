# -*- coding: utf-8 -*-
import simplejson
from lxml import etree

from odoo.addons.archer_employee_request.models.fmc_helper import handle_approve_fcm_msg
from odoo.addons.archer_api_custom.controllers.utils.utils import get_next_approve

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class ReEntryVisa(models.Model):
    _name = "re.entry.visa"
    _inherit = ["mail.thread", "mail.activity.mixin", "approval.record"]
    _rec_name = "sequence"
    _description = 'Exit & Entry Visa'
    sequence = fields.Char(string="Sequence", copy=False, readonly=True, default=lambda x: _("New"))
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=True)
    project_id = fields.Many2one(comodel_name="project.project", related="employee_id.project_id")
    purpose = fields.Selection(selection=[
        ("business_trip", "Business Trip"),
        ("personal_vacation", "Personal Vacation"), ], string="Purpose", required=True)
    personal_vacation = fields.Boolean("1st Personal Vacation")
    expense_on_project = fields.Boolean("Expense on Project")

    visa_type = fields.Selection(selection=[("single", "Single"), ("multiple", "Multiple")], string="Visa Type", required=True)
    date_from = fields.Date(string="Date (From)", required=True)
    date_to = fields.Date(string="Date (To)", required=True)
    visa_document = fields.Binary(string="Visa Document", required=True)
    amount = fields.Float("Expense Amount")
    rejection_reason = fields.Text("Rejection Reason", copy=False)
    state = fields.Selection([])
    expense_revision_id = fields.Many2one(comodel_name='account.expense.revision', string='Expense Revision', readonly=True)
    can_cancel = fields.Boolean(string='Can Cancel', default=False, compute='_compute_can_cancel_approve')
    can_approve = fields.Boolean(string='Can Approve', default=False, compute='_compute_can_cancel_approve')
    active = fields.Boolean(string='Active', default=True)
    related_deduction_id = fields.Many2one(comodel_name='employee.deduction', string='Related Deduction')

    def _compute_can_cancel_approve(self):
        for rec in self:
            rec.can_cancel = True if rec.state in ['submit'] and rec.env.uid == rec.create_uid.id else False
            state = rec.env['approval.config'].sudo().search([('model', '=', rec._name), ('state', '=', rec.state)],limit=1)
            if state:
                if rec.env.uid in state.group_ids.users.ids:
                    rec.can_approve = True
                else:
                    rec.can_approve = False
            else:
                rec.can_approve = False


    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ReEntryVisa, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
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

    @api.onchange('purpose', 'personal_vacation')
    def _onchange_purpose(self):
        if self.purpose == 'business_trip' or (self.purpose == 'personal_vacation' and self.personal_vacation):
            self.expense_on_project = True

    @api.constrains('date_from', 'date_to')
    def _check_date(self):
        if self.date_from and self.date_from <= fields.Date.today():
            raise UserError(_('Date From Must be greater Than Today.'))
        if self.date_to and self.date_to <= self.date_from:
            raise UserError(_('Date To Must be greater Than Date From.'))

    @api.model
    def create(self, vals):
        if not vals.get("sequence") or vals["name"] == _("New"):
            vals["sequence"] = (
                    self.env["ir.sequence"].next_by_code("re.entry.visa") or "/"
            )
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
            elif rec.state == 'hr_approve':
                if rec.expense_on_project and rec.amount <= 0:
                    raise ValidationError(_('Expense Amount must be greater then zero'))
                else:
                    if rec.expense_on_project == False:
                        deduction_type = self.env['other.deduction.type'].sudo().search([('code', '=', 'VR')], limit=1)
                        vals = {
                            'employee_id': rec.employee_id.id,
                            'type': 'utilities',
                            'other_type_id': deduction_type.id,
                            'amount_type': 'amount',
                            'amount': rec.amount,
                            'date': fields.Date.today(),
                            'state': 'draft',
                        }
                        deduction = self.env['employee.deduction'].create(vals)
                        rec.write({'related_deduction_id': deduction.id})
                    return super(ReEntryVisa, self).action_approve()
            elif rec.state == 'expense_approve':
                expense_revision = self.crete_expense_revision(obj=self)
                expense_revision.message_post_with_view('mail.message_origin_link',
                                                        values={'self': expense_revision, 'origin': rec},
                                                        subtype_id=self.env.ref('mail.mt_note').id
                                                        )
                rec.write({'expense_revision_id': expense_revision.id})
                return super(ReEntryVisa, self).action_approve()
            else:
                return super(ReEntryVisa, self).action_approve()

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
        res = super(ReEntryVisa, self).write(vals)
        if self.state not in ['draft','submit'] and self.amount<=0:
            raise ValidationError(_('Amount must be greater then zero'))

        if self.state in ['approved','rejected']:
            handle_approve_fcm_msg(self)
        return res