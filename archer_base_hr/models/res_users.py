import random
import secrets

import pytz
from docutils.parsers import null

from odoo import models, fields, _
from odoo.exceptions import ValidationError, UserError


class ResUsers(models.Model):
    _inherit = 'res.users'

    fmc_key = fields.Text(string='User Firebase Client')
    login_status = fields.Selection(selection=[('mob_first',_('First Mobile Login')), ('not_allow', _('Not Allowed')), ], default=False)
    web_login = fields.Boolean(string='Web Login', help='False: as default, True: if user login from web for first time', default=False)
    user_type = fields.Selection(
        selection=[('external_employee', _('External Employee')), ('project_owner', _('Project Owner'))], default=False)

    # OTP fields
    otp_code = fields.Integer(string='OTP')
    otp_datetime = fields.Datetime(string='Create Date Time')
    otp_timout = fields.Integer(compute='_compute_otp_timeout')
    otp_attempt = fields.Integer(compute='_compute_otp_timeout')
    otp_atms = fields.Integer()
    tmp_passwd = fields.Char()

    def _compute_otp_timeout(self):
        for rec in self:
            rec.otp_timout = 2
            rec.otp_attempt = 3

    def generate_otp(self):
        try:
            self.sudo().write({
                'otp_code': 1234,#random.randint(0000, 9999),
                'otp_datetime': fields.Datetime.now(),
                'otp_atms':0
            })
            self._cr.commit()
            return True
        except Exception as ex:
            raise ValueError(_('Failed Generate OTP'))

    def verify_otp(self, otp):
        self = self.sudo()
        try:
            nowt = fields.Datetime.now()
            oldt = self.sudo().otp_datetime
            if oldt:
                if ( nowt- oldt).seconds / 60 <= self.sudo().otp_timout:
                    if self.sudo().otp_atms <= self.sudo().otp_attempt:
                        if otp == self.otp_code:
                            self.sudo().write({
                                'otp_code': 1234,#random.randint(0000, 9999),
                                'otp_atms':0
                            })
                            self.sudo().generate_temp_passwd()
                            return True
                        else:
                            self.sudo().write({'otp_atms' : self.otp_atms + 1})
                            self._cr.commit()
                            raise ValidationError(_('Invalid OTP : Wrong OTP'))

                    else:
                        raise AssertionError(_('Invalid OTP: Max Trying'))
                else:
                    raise TimeoutError(_('Invalid OTP : Timeout Expired'))
            else:
                raise TimeoutError(_('Invalid OTP : Timeout'))
        except Exception as ex:
            raise ValueError(_('Invalid OTP '))

    def generate_temp_passwd(self):
        try:

            tmp_passwod = 'Mm$123456789'#secrets.token_urlsafe(8)
            return self.sudo().write({'tmp_passwd': tmp_passwod})
        except ValidationError as ve:
            raise ValidationError(ve)
            # template = self.env.ref('auth_signup.reset_password_email')
            # assert template._name == 'mail.template'
            #
            # email_values = {
            #     'email_cc': False,
            #     'auto_delete': True,
            #     'recipient_ids': [],
            #     'partner_ids': [],
            #     'scheduled_date': False,
            # }
            #
            # email_values['email_to'] = self.login
            #
            # template.send_mail(self.id,raise_exception=True, email_values=email_values)
