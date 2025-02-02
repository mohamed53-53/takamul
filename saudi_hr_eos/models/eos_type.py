from odoo import api, fields, models


class EOSTypeLine(models.Model):
    _name = 'eos.type.line'

    eos_type_id = fields.Many2one(comodel_name="eos.type")
    service_from = fields.Integer(string="From", )
    service_to = fields.Integer(string="To", )
    rate = fields.Float()
    month_rate = fields.Float()


class EOSType(models.Model):
    _name = 'eos.type'

    name = fields.Char(string="Reason")
    eos_line_ids = fields.One2many(comodel_name="eos.type.line", inverse_name="eos_type_id",
                                   string="Slices", required=False, )
