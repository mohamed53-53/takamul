from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    from_request = fields.Boolean(string='From Request', default=False)
    residency_type = fields.Many2one(comodel_name='residency.residency', string='Residency Type')
    residency_job_title_date = fields.Date(string="Residency Job Title Date")
    residency_issuance_id = fields.Many2one(comodel_name='residency.issuance', string='Residency Issuance')
