from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    for_petty_cash = fields.Boolean(string='Used For Petty Cash')
    petty_cash_responsible_id = fields.Many2one(comodel_name='res.partner')
