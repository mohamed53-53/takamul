# -*- coding: utf-8 -*-
from odoo.addons.archer_employee_request.models.fmc_helper import handle_approve_fcm_msg
from odoo.addons.archer_api_custom.controllers.utils.utils import get_next_approve
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from lxml import etree
import json
import simplejson

class ExpenseRequest(models.Model):
    _name = "expense.request"
    _inherit = ["mail.thread", "mail.activity.mixin", "approval.record"]
    _rec_name = 'description'
    _description = 'Expense Request'

    sequence = fields.Char(
        "Sequence", copy=False, readonly=True, default=lambda x: _("New")
    )
    employee_id = fields.Many2one("hr.employee", required=True)
    project_id = fields.Many2one("project.project", related="employee_id.project_id")
    expense_type_id = fields.Many2one(comodel_name='expense.request.type',
        string="Expense Type",
        required=True,
    )
    product_id = fields.Many2one(comodel_name='product.template', related='expense_type_id.product_id')
    description = fields.Text("Expense Description", required=True)
    date_from = fields.Date("Date (From)", default=fields.Date.today())
    date_to = fields.Date("Date (To)",default=fields.Date.today())
    amount = fields.Float("Expense Amount", required=True)
    supportive_doc = fields.Binary("Supportive Document")
    rejection_reason = fields.Text("Rejection Reason", copy=False)
    state = fields.Selection([])
    approver_id = fields.Many2one("res.users", string="Approver Name", copy=False)
    expense_approval_date = fields.Date("Expense Approval Date", copy=False)
    can_cancel = fields.Boolean(string='Can Cancel', default=False, compute='_compute_can_cancel_approve')
    can_approve = fields.Boolean(string='Can Approve', default=False, compute='_compute_can_cancel_approve')
    active = fields.Boolean(string='Active', default=True)
    expense_revision_id = fields.Many2one(comodel_name='account.expense.revision', string='Expense Revision', readonly=True)
    account_move_id = fields.Many2one(comodel_name='account.move', string='Journal Entry')
    request_by = fields.Selection(selection=[('hr','HR'),('employee','Employee')], default='employee')
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
        res = super(ExpenseRequest, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
                                                         submenu=False)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in res['fields']:
                for node in doc.xpath("//field[@name='%s']" % field):
                    modifiers = json.loads(node.get("modifiers"))
                    if 'readonly' not in modifiers:
                        modifiers['readonly'] = [['state', '!=', 'draft']]
                    else:
                        if type(modifiers['readonly']) != bool:
                            modifiers['readonly'].insert(0, '|')
                            modifiers['readonly'] += [['state', '!=', 'draft']]
                    node.set('modifiers', json.dumps(modifiers))
                    res['arch'] = etree.tostring(doc)
        return res

    @api.model
    def create(self, vals):
        if not vals.get("sequence") or vals["name"] == _("New"):
            vals["sequence"] = (
                    self.env["ir.sequence"].next_by_code("expense.claim") or "/"
            )
        return super(ExpenseRequest,self).create(vals)

    @api.constrains("date_from", "date_to")
    def _check_date(self):
        if self.date_from and self.date_to:
            if self.date_from and self.date_from < fields.Date.today():
                raise UserError(_("Date From Must be Greater Than/Equal Today."))
            if self.date_to and self.date_to < self.date_from:
                raise UserError(_("Date To Must be Greater Than/Equal Date From."))


    @api.depends("date_from", "date_to")
    @api.onchange("date_from", "date_to")
    def _onchange_dates(self):
        if self.date_from and self.date_from < fields.Date.today():
            raise UserError(_("Date From Must be Greater Than/Equal Today."))
        if self.date_to and self.date_to < self.date_from:
            raise UserError(_("Date To Must be Greater Than/Equal Date From."))

    @api.constrains("amount")
    def _check_expense_amount(self):
        if self.amount < 0.0:
            raise UserError(_("Expense Amount must be positive."))

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
                if rec.request_by == 'hr':
                    rec.write({'state': 'po_approve'})
                else:
                    rec.write({'state': 'submit'})
            elif rec.state == 'po_approve':
                rec.write({'state': get_next_approve(rec)})
            elif rec.state == 'expense_approve':
                expense_revision = self.crete_expense_revision(obj=self)
                expense_revision.message_post_with_view('mail.message_origin_link',
                                                        values={'self': expense_revision, 'origin': rec},
                                                        subtype_id=self.env.ref('mail.mt_note').id
                                                        )
                rec.write({
                    'expense_revision_id': expense_revision.id,
                    'expense_approval_date': fields.Date.today(),
                })
                return super(ExpenseRequest, self).action_approve()
            else:
                return super(ExpenseRequest, self).action_approve()

    def crete_expense_revision(self, obj):
        accrued_expense_account_id = self.env['ir.config_parameter'].sudo().get_param('archer_project_custom.accrued_expense_account_id')
        accrued_expense_journal_id = self.env['ir.config_parameter'].sudo().get_param('archer_project_custom.accrued_expense_journal_id')
        if not accrued_expense_account_id:
            raise ValidationError(_('Please Check Accrued Expense Account'))
        if not accrued_expense_journal_id:
            raise ValidationError(_('Please Check Accrued Expense Journal'))
        else:
            if obj.expense_type_id.product_id.property_account_expense_id:
                vals = {
                    'origin_model': obj._name,
                    'origin_id': obj.id,
                    'reference': obj.sequence if obj.sequence else False,
                    'project_id': obj.project_id.id,
                    'accrued_expense_journal_id': int(accrued_expense_journal_id),
                    'expense_account_id': obj.expense_type_id.product_id.property_account_expense_id.id,
                    'accrued_expense_account_id': int(accrued_expense_account_id),
                    'amount': obj.amount,
                    'state': 'draft',
                    'partner_id':obj.employee_id.user_partner_id.id
                }
                return self.env['account.expense.revision'].create(vals)
            else:
                raise ValidationError(_('Please Check Expense Type Account'))

    def write(self, vals):
        res = super(ExpenseRequest, self).write(vals)
        if self.state in ['approved','rejected']:
            handle_approve_fcm_msg(self)
        return res
class ExpensesRequestType(models.Model):
    _name = 'expense.request.type'

    name = fields.Char(string='Name', required=True)
    product_id = fields.Many2one(comodel_name='product.template', domain=[('detailed_type','=','service'),('provide_service','=',True)], required=True)