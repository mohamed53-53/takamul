from odoo import api, fields, models,_


class BankBank(models.Model):
    _name = "bank.bank"
    _rec_name = 'bank_name'

    bank_name = fields.Char(string="Bank Name")
    bank_type = fields.Selection(selection=[('rajhi', _('AlRajhi Bank')), ('riyadh', _('AlRiyadh Bank')), ('other', _('Other'))],
                                 default='other')
