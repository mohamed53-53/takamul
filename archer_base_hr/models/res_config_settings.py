from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fcm_server_key = fields.Text(string='FCM Server Key')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['fcm_server_key'] = self.env['ir.config_parameter'].sudo().get_param('archer_base_hr.fcm_server_key')
        return res
    #
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param("archer_base_hr.fcm_server_key", self.fcm_server_key or False)
