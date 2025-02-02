from odoo import api, fields, models


class Loan(models.Model):
    _name = 'loan.type'
    _rec_name = 'name'

    name = fields.Char()
    # factor = fields.Float(default=1)