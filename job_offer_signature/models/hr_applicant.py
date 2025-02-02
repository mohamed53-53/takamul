# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError, ValidationError, Warning
import base64
import os

class RecruitmentStage(models.Model):
    _inherit = 'hr.recruitment.stage'

    is_cancel = fields.Boolean(string="Cancel Stage")


class Application(models.Model):
    _inherit = 'hr.applicant'

    responsible_id = fields.Many2one(comodel_name="res.users",default=lambda x: x.env.user)
    user_id = fields.Many2one(comodel_name="res.users",string="Related User")
    sign_request_ids = fields.Many2many('sign.request', string='Requested Signatures')
    sign_request_count = fields.Integer(compute='_compute_sign_request_count')
    rejected = fields.Boolean(string="")
    is_cancel = fields.Boolean(related='stage_id.is_cancel')

    @api.depends('sign_request_ids')
    def _compute_sign_request_count(self):
        for contract in self:
            contract.sign_request_count = len(contract.sign_request_ids)

    def applicant_portal_invitation(self):
        name = self.name
        login = self.email_from
        if self.user_id:
            raise ValidationError(_('Already Have User'))
        if not login:
            raise ValidationError(_('Please Define Email For this Applicant'))
        company_id = self.env.user.company_id.id
        portal_group = self.env.ref('base.group_portal')
        user = self.env['res.users'].with_context(create_user=True).sudo().create({'name': name,
                                                                             'login': login,
                                                                             'company_id': company_id,
                                                                             'groups_id': [(6, 0, [portal_group.id])],
                                                                             })
        user.partner_id.email = login
        # user.action_reset_password()
        self.user_id = user.id
        return user

    def get_sign_items(self):
        sign_items = []
        sign_items.append((0, 0, {'type_id': self.env.ref('sign.sign_item_type_initial').id,
                                  'required': True,
                                  'responsible_id': self.env.ref('sign.sign_item_role_company').id,
                                  'page': 5,
                                  'posX': 0.137,
                                  'posY': 0.653,
                                  'width': 0.488,
                                  'height': 0.030,
                                  }))
        sign_items.append((0, 0, {'type_id': self.env.ref('sign.sign_item_type_initial').id,
                                  'required': True,
                                  'responsible_id': self.env.ref('sign.sign_item_role_employee').id,
                                  'page': 5,
                                  'posX': 0.137,
                                  'posY': 0.653,
                                  'width': 0.085,
                                  'height': 0.030,
                                  }))
        return sign_items

    def validate_signature(self,user_id,sign_template_id):
        if not user_id:
            raise ValidationError(_('Applicant must be linked to a user and a partner.'))

        sign_request = self.env['sign.request']
        if not self.check_access_rights('create', raise_exception=False):
            sign_request = sign_request.sudo()
        second_role = set(sign_template_id.mapped('sign_item_ids.responsible_id').ids)
        applicant_role_id = self.env.ref('sign.sign_item_role_employee')
        second_role.remove(applicant_role_id.id)

        res = sign_request.initialize_new(
            sign_template_id.id,
            [
                {'role': applicant_role_id.id,
                 'partner_id': user_id.partner_id.id},
                {'role': second_role.pop(),
                 'partner_id': self.responsible_id.partner_id.id}
            ],
            False,
            'Job Offer Signature Request - ' + self.name,
            'Job Offer Signature Request',
            ''
        )

        sign_request = self.env['sign.request'].browse(res['id'])
        if not self.check_access_rights('write', raise_exception=False):
            sign_request = sign_request.sudo()

        sign_request.toggle_favorited()
        sign_request.action_sent()
        sign_request.write({'state': 'sent'})
        sign_request.request_item_ids.write({'state': 'sent'})
        self.sign_request_ids += sign_request
        if self.env.user.id == self.responsible_id.id:
            return sign_request.go_to_document()

    def create_job_offer_sign_requests(self):
        user = self.user_id
        if not self.user_id:
            user = self.applicant_portal_invitation()
        report = self.env.ref('job_offer_signature.email_template_job_offer', raise_if_not_found=False)

        data, data_format = report.with_context(snailmail_layout=True).render()
        # save the attachment
        att_id = self.env['ir.attachment'].create({
            'name': self.name,
            'type': 'binary',
            'datas': base64.encodestring(data),
            'res_model': 'hr.applicant',
            'res_id': self.id,
            'mimetype': 'application/pdf'
        })
        sign = self.env['sign.template'].create({'name': self.name,
                                                 'attachment_id': att_id.id,
                                                 'datas': att_id.datas,
                                                 'applicant_id': self.id
                                                 })
        sign.sign_item_ids = self.get_sign_items()
        self.validate_signature(user,sign)
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Signature Requests',
        #     'view_mode': 'form',
        #     'res_model': 'hr.applicant.sign.document.wizard',
        #     'target': 'new',
        #     'context':{'default_sign_template_id': sign.id,
        #                'default_responsible_id': self.responsible_id.id},
        # }

    def open_sign_requests(self):
        self.ensure_one()
        if len(self.sign_request_ids.ids) == 1:
            return self.sign_request_ids.go_to_document()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Signature Requests',
            'view_mode': 'kanban',
            'res_model': 'sign.request',
            'domain': [('id', 'in', self.sign_request_ids.ids)]
        }
