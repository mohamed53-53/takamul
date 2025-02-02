# -*- coding: utf-8 -*-

import simplejson
import json
from lxml import etree

from odoo.addons.archer_employee_request.models.fmc_helper import handle_approve_fcm_msg
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SalaryConfirmation(models.Model):
    _name = "salary.confirmation"
    _inherit = ["mail.thread", "mail.activity.mixin", "approval.record"]
    _rec_name = "sequence"
    _description = 'Salary Confirmation'

    sequence = fields.Char(
        "Sequence", copy=False, readonly=True, default=lambda x: _("New")
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee", string="Employee", required=True
    )
    project_id = fields.Many2one(
        comodel_name="project.project", related="employee_id.project_id"
    )
    rejection_reason = fields.Text("Rejection Reason", copy=False)
    expense_revision_id = fields.Many2one(comodel_name='account.expense.revision', string='Expense Revision',
                                          readonly=True)
    desc = fields.Text(string="Description")
    bank_id = fields.Many2one(comodel_name="bank.bank", string="Bank Name", required=True)
    state = fields.Selection([])
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

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(SalaryConfirmation, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
                                                              submenu=False)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in res['fields']:
                for node in doc.xpath("//field[@name='%s']" % field):
                    modifiers = simplejson.loads(node.get("modifiers"))
                    modifiers_condition = ['state', '!=', 'draft']
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
                    self.env["ir.sequence"].next_by_code("salary.conf") or "/"
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
                # todo create confirmation letter & attach it to current request
                return super(SalaryConfirmation, self).action_approve()
            else:
                return super(SalaryConfirmation, self).action_approve()

    def write(self, vals):
        res = super(SalaryConfirmation, self).write(vals)
        if self.state in ['approved','rejected']:
            handle_approve_fcm_msg(self)
        return res