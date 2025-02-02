from odoo import api, fields, models

class CocTemplate(models.Model):
    _name = "coc.template"
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    coc_template_item_ids = fields.One2many("coc.template.items", "coc_template_id", string="COC Template Items" )


class CocTemplateItems(models.Model):
    _name = "coc.template.items"
    _rec_name = 'item_name'

    item_name = fields.Char("Item Name")
    item_arabic_name = fields.Char("Item Arabic Name")
    tab_number = fields.Integer("Sequence")
    account_id = fields.Many2many("account.account", string="Accounts")
    coc_template_id = fields.Many2one("coc.template")


