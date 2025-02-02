# -*- coding: utf-8 -*-

import json

import simplejson
from lxml import etree

from odoo.addons.archer_employee_request.models.fmc_helper import handle_approve_fcm_msg
from odoo import api, fields, models, _


class BenefitRequest(models.Model):
    _name = "benefit.request"
    _description = 'Benefit Request'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']
    _rec_name = 'sequence'

    BENEFIT_TYPES = [
        ('per', 'Periodical'),
        ('non_per', 'Non-Periodical'),
        ('other', 'Other Benefit based on project')
    ]
    sequence = fields.Char(string='Sequence', copy=False, readonly=True, default=lambda x: _('New'))
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=True)
    project_id = fields.Many2one(comodel_name="project.project", string="Project", related="employee_id.project_id")
    benefit_id = fields.Many2one(comodel_name="employee.monthly.eos", string="Benefit Name")
    benefit_id_domain = fields.Char(
        compute="_compute_benefit_id_domain",
        readonly=True,
        store=False,
    )
    other = fields.Boolean(string="Other Benefit", default=False)
    benefit_name = fields.Char(string="Benefit Name")
    benefit_type = fields.Selection(selection=BENEFIT_TYPES, string="Benefit Type")
    desc = fields.Text(string="Benefit Description")
    purpose = fields.Text(string="Purpose/Justification", required=True)
    rejection_reason = fields.Text(string="Rejection Reason", copy=False)
    state = fields.Selection([])
    can_cancel = fields.Boolean(string='Can Cancel', default=False, compute='_compute_can_cancel_approve')
    can_approve = fields.Boolean(string='Can Approve', default=False, compute='_compute_can_cancel_approve')
    active = fields.Boolean(string='Active', default=True)
    account_move_id = fields.Many2one(comodel_name='account.move', string='Related Entry')

    @api.depends('project_id')
    def _compute_benefit_id_domain(self):
        for rec in self:
            domain = [('id', 'in',
                       rec.project_id.benefit_ids.ids)] if rec.project_id and rec.project_id.benefit_ids else []
            rec.benefit_id_domain = json.dumps(domain)

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
        res = super(BenefitRequest, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
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

    @api.model
    def create(self, vals):
        if not vals.get("sequence") or vals["name"] == _("New"):
            vals["sequence"] = (
                    self.env["ir.sequence"].next_by_code("benefit.request") or "/"
            )
        return super().create(vals)

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
            elif rec.state == 'in_progress':
                # todo
                # add validation to make sure that the benefit creates before validation
                return super(BenefitRequest, self).action_approve()
            else:
                return super(BenefitRequest, self).action_approve()

    def write(self, vals):
        res = super(BenefitRequest, self).write(vals)
        if self.state in ['approved','rejected']:
            handle_approve_fcm_msg(self)
        return res
