from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    accrued_expense_account_id = fields.Many2one(comodel_name='account.account', string='Accrued Expense Account')
    accrued_expense_journal_id = fields.Many2one(comodel_name='account.journal', string='Accrued Expense Journal')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['accrued_expense_account_id'] = int(self.env['ir.config_parameter'].sudo().get_param('archer_project_custom.accrued_expense_account_id'))
        res['accrued_expense_journal_id'] = int(self.env['ir.config_parameter'].sudo().get_param('archer_project_custom.accrued_expense_journal_id'))
        return res
    #
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param("archer_project_custom.accrued_expense_account_id", self.accrued_expense_account_id.id or False)
        self.env['ir.config_parameter'].set_param("archer_project_custom.accrued_expense_journal_id", self.accrued_expense_journal_id.id or False)
