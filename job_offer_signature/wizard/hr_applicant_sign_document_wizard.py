# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrApplicantSignDocumentWizard(models.TransientModel):
    _name = 'hr.applicant.sign.document.wizard'
    _description = 'Sign document in Application'

    def _group_hr_contract_domain(self):
        group = self.env.ref('hr_contract.group_hr_contract_manager', raise_if_not_found=False)
        return [('groups_id', 'in', group.ids)] if group else []

    applicant_id = fields.Many2one('hr.applicant', string='Contract',
        default=lambda self: self.env.context.get('active_id'))
    user_id = fields.Many2one('res.users', string='Applicant', compute='_compute_partner')
    responsible_id = fields.Many2one('res.users', string='Responsible', required=True,
                                     domain=_group_hr_contract_domain)
    applicant_role_id = fields.Many2one("sign.item.role", string="Employee Role", required=True)

    sign_template_id = fields.Many2one('sign.template', string="Document to Sign", required=True,
                                       help="Document that the applicant will have to sign.")

    subject = fields.Char(string="Subject", required=True, default='Job Offer Signature Request')
    message = fields.Html("Message")
    follower_ids = fields.Many2many('res.partner', string="Copy to")

    @api.onchange('sign_template_id')
    def _onchange_sign_template_id(self):
        return {'domain': {'applicant_role_id': [('id', 'in', self.sign_template_id.mapped('sign_item_ids.responsible_id').ids)]}}

    @api.depends('applicant_id')
    def _compute_partner(self):
        for applicant in self:
            applicant.user_id = applicant.applicant_id.user_id.id

    def validate_signature(self):
        if not self.user_id and not self.user_id.partner_id:
            raise ValidationError(_('Applicant must be linked to a user and a partner.'))

        sign_request = self.env['sign.request']
        if not self.check_access_rights('create', raise_exception=False):
            sign_request = sign_request.sudo()

        second_role = set(self.sign_template_id.mapped('sign_item_ids.responsible_id').ids)
        second_role.remove(self.applicant_role_id.id)

        res = sign_request.initialize_new(
            self.sign_template_id.id,
            [
                {'role': self.applicant_role_id.id,
                 'partner_id': self.user_id.partner_id.id},
                {'role': second_role.pop(),
                 'partner_id': self.responsible_id.partner_id.id}
            ],
            self.follower_ids.ids.append(self.responsible_id.partner_id.id),
            'Job Offer Signature Request - ' + self.applicant_id.name,
            self.subject,
            self.message
        )

        sign_request = self.env['sign.request'].browse(res['id'])
        if not self.check_access_rights('write', raise_exception=False):
            sign_request = sign_request.sudo()

        sign_request.toggle_favorited()
        sign_request.action_sent()
        sign_request.write({'state': 'sent'})
        sign_request.request_item_ids.write({'state': 'sent'})

        self.applicant_id.sign_request_ids += sign_request

        # self.contract_id.message_post(body=_('%s requested a new signature on document: %s.<br/>%s and %s are the signatories.') %
        #     (self.env.user.display_name, self.sign_template_id.name, self.employee_id.display_name, self.responsible_id.display_name))

        if self.env.user.id == self.responsible_id.id:
            return sign_request.go_to_document()
