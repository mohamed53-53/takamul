from odoo import models, fields, api, _


class Company(models.Model):
    _inherit = 'res.company'

    max_pool_allocation = fields.Integer(string="Max. Pool Allocation")


class AccrualConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    max_pool_allocation = fields.Integer(string="Max. Pool Allocation",related="company_id.max_pool_allocation",readonly=False)
