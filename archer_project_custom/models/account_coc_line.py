from odoo import api, fields, models
from datetime import datetime


class AccountCOC(models.Model):
    _name = "archer.account.coc.line"

    coc_id = fields.Many2one('archer.account.coc')
    item_name = fields.Char("Item Name")
    item_arabic_name = fields.Char("Item Arabic Name")
    sequence = fields.Integer("Sequence")
    real_amount = fields.Float()
    margin_percentage = fields.Float()
    profit_amount = fields.Float()
    untaxed_total = fields.Float()
    amount_tax = fields.Float()
    tax_rate = fields.Float()
    amount_total = fields.Float()
    date = fields.Date(string="Date", related='coc_id.date', store=True)
    project_id = fields.Many2one('project.project', related='coc_id.project_id', store=True)
    year = fields.Selection(related='coc_id.year', store=True)
    month = fields.Selection(related='coc_id.month', store=True)
    state = fields.Selection(related='coc_id.state', store=True)
