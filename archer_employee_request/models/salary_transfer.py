# -*- coding: utf-8 -*-

import simplejson
from lxml import etree

from odoo.addons.archer_employee_request.models.fmc_helper import handle_approve_fcm_msg
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class SalaryTransfer(models.Model):
    _name = "salary.transfer"
    _inherit = ["mail.thread", "mail.activity.mixin", "approval.record"]
    _rec_name = "sequence"
    _description = 'Salary Transfer'
    sequence = fields.Char(
        "Sequence", copy=False, readonly=True, default=lambda x: _("New")
    )
    employee_id = fields.Many2one(comodel_name="hr.employee", required=True)
    project_id = fields.Many2one(
        "project.project", related="employee_id.project_id"
    )
    is_locked = fields.Boolean(related="employee_id.is_locked")
    bank_clearance_letter = fields.Binary(string="Bank Clearance Letter")
    international_bank = fields.Boolean(string="International Bank", related="employee_id.international_bank")
    bank_name = fields.Char(string="Bank Name")
    bank_id = fields.Many2one(comodel_name="bank.bank", string="Bank Name")
    branch_name = fields.Char(string="Branch Name")
    iban_number = fields.Char(string="IBAN Number", required=True)
    bank_country_id = fields.Many2one(comodel_name='res.country', string='Country')
    re_enter_iban_number = fields.Char(string="Re-Enter IBAN Number")
    terms_and_conditions = fields.Boolean(string="Terms & Conditions", default=False)
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
        res = super(SalaryTransfer, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
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

    @api.constrains('iban_number', 're_enter_iban_number')
    def _check_re_enter_iban_number(self):
        if (self.iban_number and self.re_enter_iban_number) and self.iban_number != self.re_enter_iban_number:
            raise UserError(_('Re-enter IBAN Number Must Be Same As IBAN Number.'))
    @api.model
    def create(self, vals):
        if not vals.get("sequence") or vals["name"] == _("New"):
            vals["sequence"] = (
                self.env["ir.sequence"].next_by_code("salary.transfer") or "/"
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
                if rec.is_locked and not rec.bank_clearance_letter:
                    raise ValidationError(_('Clearance Letter is Required'))
                else:
                    rec.write({'state': 'submit'})
            elif rec.state == 'in_progress':
                values = {
                    "bank_id": rec.bank_id,
                    "bank_name": rec.bank_name,
                    "iban_no": rec.iban_number,
                    "international_bank": rec.international_bank,
                    "is_locked": rec.is_locked,
                    "branch_name_code": rec.branch_name
                }
                rec.employee_id.update(values)
                return super(SalaryTransfer, self).action_approve()
            else:
                return super(SalaryTransfer, self).action_approve()


    def write(self, vals):
        res = super(SalaryTransfer, self).write(vals)
        if self.state in ['approved','rejected']:
            handle_approve_fcm_msg(self)
        return res