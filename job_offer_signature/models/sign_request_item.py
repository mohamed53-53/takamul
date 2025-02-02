from odoo import api, fields, models,_
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, formataddr, config, get_lang
from werkzeug.urls import url_join
from odoo.exceptions import UserError, ValidationError


class SignRequestItem(models.Model):
    _inherit = 'sign.request.item'

    def send_signature_accesses(self, subject=None, message=None):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if self.sign_request_id.template_id.applicant_id:
            tpl = self.env.ref('job_offer_signature.job_offer_sign_mail_request')
        elif self.sign_request_id.template_id.contract_id:
            tpl = self.env.ref('contract_signature.contract_sign_mail_request')
        else:
            tpl = self.env.ref('sign.sign_template_mail_request')
        for signer in self:
            if not signer.partner_id or not signer.partner_id.email:
                continue
            if not signer.create_uid.email:
                continue
            signer_lang = get_lang(self.env, lang_code=signer.partner_id.lang).code
            tpl = tpl.with_context(lang=signer_lang)
            body = tpl.render({
                'record': signer,
                'link': url_join(base_url, "sign/document/mail/%(request_id)s/%(access_token)s" % {'request_id': signer.sign_request_id.id, 'access_token': signer.access_token}),
                'subject': subject,
                'body': message if message != '<p><br></p>' else False,
            }, engine='ir.qweb', minimal_qcontext=True)

            if not signer.signer_email:
                raise UserError(_("Please configure the signer's email address"))
            self.env['sign.request']._message_send_mail(
                body, 'mail.mail_notification_light',
                {'record_name': signer.sign_request_id.reference},
                {'model_description': 'signature', 'company': signer.create_uid.company_id},
                {'email_from': formataddr((signer.create_uid.name, signer.create_uid.email)),
                 'author_id': signer.create_uid.partner_id.id,
                 'email_to': formataddr((signer.partner_id.name, signer.partner_id.email)),
                 'subject': subject},
                force_send=True,
                lang=signer_lang,
            )
