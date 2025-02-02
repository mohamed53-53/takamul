from odoo import models, fields, api


TYPES = [
    ('employee', 'Employee'),
    ('family_member', "Family Member"),
    ('newborn_out', "Newborn (Born Outside KSA)"),
    ('newborn_in', 'Newborn (Born Inside KSA)'),
]
class ResidencyResidency(models.Model):
    _name = "residency.residency"

    name = fields.Char(compute='get_str_name')
    residency_type = fields.Selection(selection=TYPES, string='Type', index=True, copy=False, tracking=True)
    document_ids = fields.One2many(comodel_name="residency.residency.document", inverse_name="residency_id", string='Document Name')

    def get_str_name(self):
        for rec in self:
            rec.name = dict(TYPES)[rec.residency_type]

class ResidencyResidencyDocuments(models.Model):
    _name = 'residency.residency.document'
    _rec_name = 'document_name'

    residency_id = fields.Many2one(comodel_name='residency.residency', string='Residency')
    document_name = fields.Char(string='Document Name', required=True)