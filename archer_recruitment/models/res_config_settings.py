from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    first_evaluation_months = fields.Integer(string='First Probation Period')


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['first_evaluation_months'] = int(self.env['ir.config_parameter'].sudo().get_param('archer_employee_evaluation.first_evaluation_months'))
        return res
    #
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param("archer_employee_evaluation.first_evaluation_months", self.first_evaluation_months or False)
