# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    less_than_five_years = fields.Integer(string="Less Than 5 Years", required=False, default=21)
    up_to_five_years = fields.Integer(string="Greater Than 5 Years", required=False, default=30)
    eos_expense_account_id = fields.Many2one(
        comodel_name='account.account',domain=lambda x:[('user_type_id','=',x.env.ref('account.data_account_type_expenses').id),('company_id','=',x.env.company.id)],
        string="EOS Expense Account", help="Set expense account for end of service journal entry",)

    eos_leaves_account_id = fields.Many2one(
        comodel_name='account.account',domain=lambda x:[('company_id','=',x.env.company.id)],
        string="EOS Leaves Account", help="Set leaves account for end of service journal entry",)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    less_than_five_years = fields.Integer(string="Less Than 5 Years", required=True, readonly=False,
                                          related='company_id.less_than_five_years', )
    up_to_five_years = fields.Integer(string="Greater Than 5 Years", required=True, readonly=False,
                                      related='company_id.up_to_five_years', )

    eos_expense_account_id = fields.Many2one(related="company_id.eos_expense_account_id", readonly=False)
    eos_leaves_account_id = fields.Many2one(related="company_id.eos_leaves_account_id", readonly=False)
