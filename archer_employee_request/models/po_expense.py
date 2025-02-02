# -*- coding: utf-8 -*-

import simplejson
import json
from lxml import etree

from odoo.addons.archer_employee_request.models.fmc_helper import handle_approve_fcm_msg
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class PoExpense(models.Model):
    _name = "po.expense"
    _inherit = ["mail.thread", "mail.activity.mixin", "approval.record"]
    _rec_name = "sequence"


    sequence = fields.Char(
        "Sequence", copy=False, readonly=True, default=lambda x: _("New")
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee", string="Employee", required=True
    )
    project_id = fields.Many2one(
        comodel_name="project.project", related="employee_id.project_id"
    )
    desc = fields.Text(string="Description", required=True)
    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account", string="Analytic Account",
        related="project_id.analytic_account_id",
    )
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product",
    )
    product_id_domain = fields.Char(
        compute="_compute_product_id_domain",
        readonly=True,
        store=False,
    )
    account_id = fields.Many2one(comodel_name="account.account", string="Account")
    amount = fields.Float(string="Total")
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Approver Name",
        related="project_id.owner_id",
    )
    approve_date = fields.Date(string="Approval Date")
    rejection_reason = fields.Text("Rejection Reason", copy=False)
    expense_revision_id = fields.Many2one(comodel_name='account.expense.revision', string='Expense Revision', readonly=True)
    state = fields.Selection([])
    can_cancel = fields.Boolean(string='Can Cancel', default=False, compute='_compute_can_cancel_approve')
    can_approve = fields.Boolean(string='Can Approve', default=False, compute='_compute_can_cancel_approve')
    active = fields.Boolean(string='Active', default=True)
    expense_revision_id = fields.Many2one(comodel_name='account.expense.revision', string='Expense Revision', readonly=True)

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


    @api.constrains('amount')
    def _check_amount(self):
        if self.amount <= 0.0:
            raise UserError(_('Total Must be greater than Zero !'))


    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(PoExpense, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
                                                                submenu=False)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in res['fields']:
                for node in doc.xpath("//field[@name='%s']" % field):
                    modifiers = simplejson.loads(node.get("modifiers"))
                    modifiers_condition = ['state', '!=', 'draft']
                    if field == 'approve_date':
                        modifiers_condition = ['state', 'in',
                                               ['in_progress', 'approved', 'rejected']]
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
        if not vals.get("sequence") or vals["name"] == _("New"):
            vals["sequence"] = (
                    self.env["ir.sequence"].next_by_code("po.expense") or "/"
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
            elif rec.state == 'po_approve':
                expense_revision = self.create_expense_revision(obj=self)
                expense_revision.message_post_with_view('mail.message_origin_link',
                                                        values={'self': expense_revision, 'origin': rec},
                                                        subtype_id=self.env.ref('mail.mt_note').id
                                                        )
                rec.write({'expense_revision_id': expense_revision.id})
                return super(PoExpense, self).action_approve()
            else:
                return super(PoExpense, self).action_approve()

    def create_expense_revision(self, obj):
        account_expense_id = obj.product_id.property_account_expense_id
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
                }
                return self.env['account.expense.revision'].create(vals)
            else:
                raise ValidationError(_('Please Check Service Account'))

    def write(self, vals):
        res = super(PoExpense, self).write(vals)
        if self.state in ['approved','rejected']:
            handle_approve_fcm_msg(self)
        return res