from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self._context.get('analytic_account', False):
            project_request = self.env['project.request'].search([])
            analytic_account = project_request.mapped('analytic_account_id')
            args = [('id', 'not in', analytic_account.ids)]
        return super(AccountAnalyticAccount, self)._search(args, offset=offset, limit=limit, order=order, count=count,
                                                           access_rights_uid=access_rights_uid)


    @api.model
    def create(self, vals_list):
        vals_list['code'] = self.env['ir.sequence'].next_by_code('archer_project_custom.analytic_account_ref_sequence')
        res = super(AccountAnalyticAccount, self).create(vals_list)

        return  res
class AccountAccount(models.Model):
    _inherit = "account.account"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self._context.get('account_account', False):
            coc_template_items = self.env['coc.template.items'].search([])
            account_account = coc_template_items.mapped('account_id')
            args = [('id', 'not in', account_account.ids)]
        return super(AccountAccount, self)._search(args, offset=offset, limit=limit, order=order,
                                                   count=count, access_rights_uid=access_rights_uid)
