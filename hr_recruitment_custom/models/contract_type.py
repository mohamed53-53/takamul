from odoo import api, fields, models


class ContractType(models.Model):
    _name = 'contract.type'
    _rec_name = 'name'

    name = fields.Char()
