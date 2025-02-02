# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SalaryTax(models.Model):
    _inherit = 'hr.salary.rule'

    taxable = fields.Boolean(string="Under Tax", )
    currency_id = fields.Many2one('res.currency', string='Currency', help="The optional other currency if it is a multi-currency entry.")



