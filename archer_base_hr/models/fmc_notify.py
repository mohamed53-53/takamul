from odoo import models, fields

from pyfcm import FCMNotification


class ArcherFCMNotification(models.Model):
    _name = 'archer.fcm.notify'

    server_ky = fields.Char(string='FCM Server Key')
    fcm_ky = fields.Char(string='FCM Client Key')
    user_id = fields.Many2one(comodel_name='res.users', string='User')
    msg_header = fields.Char(string='Message Header')
    msg_body = fields.Text(string='Message Body')

    def send_fcm_notify(self, client_key, msg_header, msg_body):
        try:
            push_service = FCMNotification(
                api_key=self.env['ir.config_parameter'].sudo().get_param('archer_base_hr.fcm_server_key'))
            result = push_service.notify_multiple_devices(registration_ids=client_key, message_title=msg_header,
                                                          message_body=msg_body)
            self.create({
                'server_ky': self.env['ir.config_parameter'].sudo().get_param('archer_base_hr.fcm_server_key'),
                'fcm_ky': client_key,
                'user_id': self.env.uid,
                'msg_header': msg_header,
                'msg_body': msg_body

            })
        except:
            pass
