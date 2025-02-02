# -*- coding: utf-8 -*-
import base64

import simplejson
from lxml import etree

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SalaryIdentification(models.Model):
    _name = "salary.identification"
    _inherit = ["mail.thread", "mail.activity.mixin"]
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
    identity_name = fields.Char(string="Identity Name")
    unknown = fields.Boolean(string="To whom it may concern", default=False)
    whom_name = fields.Char(string="Whom Name")
    e_stamp = fields.Binary(string="Electronic Stamp", attachment=True)
    qr_code = fields.Char(string="QR Identification Code")
    state = fields.Selection([('draft','Draft'),('done','Done')])
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


    @api.constrains('identity_name', 'unknown')
    def _check_identity(self):
        if all([not self.identity_name, not self.unknown]) :
            raise UserError(_('You must enter Identity name or mark unknown !'))

    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(SalaryIdentification, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
    #                                                             submenu=False)
    #     if view_type == 'form':
    #         doc = etree.XML(res['arch'])
    #         for field in res['fields']:
    #             for node in doc.xpath("//field[@name='%s']" % field):
    #                 modifiers = simplejson.loads(node.get("modifiers"))
    #                 modifiers_condition = ['state', '!=', 'draft']
    #                 if 'readonly' not in modifiers:
    #                     modifiers['readonly'] = [modifiers_condition]
    #                 else:
    #                     if type(modifiers['readonly']) != bool:
    #                         modifiers['readonly'].insert(0, '|')
    #                         modifiers['readonly'] += [modifiers_condition]
    #                 node.set('modifiers', simplejson.dumps(modifiers))
    #                 res['arch'] = etree.tostring(doc)
    #     return res

    @api.model
    def create(self, vals):
        if not vals.get("sequence") or vals["name"] == _("New"):
            vals["sequence"] = (
                    self.env["ir.sequence"].next_by_code("salary.ident") or "/"
            )
        return super(SalaryIdentification,self).create(vals)

    def action_draft_approve(self):
        for rec in self:
            rec.state = 'done'
            data = {
                'request_id': self.id
            }
            pdf_report = self.env.ref('archer_employee_request.action_report_salary_identification')._render_qweb_pdf(self.id,data=data)[0]
            self.e_stamp = base64.b64encode(pdf_report).decode()


