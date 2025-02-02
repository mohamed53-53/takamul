'''
Created on Dec 27, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields

class AnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    
    def _owner_id_domain(self):
        return [('user_id.groups_id', '=', self.env.ref('oi_certification_of_completion.group_business_owner').id)]

    owner_ids = fields.Many2many('hr.employee', relation='analytic_account_owner_rel', string='Business Owner', domain = _owner_id_domain)