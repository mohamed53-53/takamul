from odoo import models, fields


class MedInsCompany(models.Model):
    _inherit = 'res.partner'

    is_med_ins_comp = fields.Boolean(string='Is Medical Insurance Company')
    med_group_ids = fields.One2many(comodel_name='archer.medical.group', inverse_name='provider_id', string='Medical Groups')


class InsuranceGroup(models.Model):
    _name = 'archer.medical.group'
    provider_id = fields.Many2one(comodel_name='res.partner', string='Provider', domain=[('company_type','=','company'),('is_med_ins_comp','=',True)])
    name = fields.Char(string='Name')

