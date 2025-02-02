from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Document(models.Model):
    _name = "document.document"
    _rec_name = "document"

    document = fields.Char(string='Document', required=True)
    residency_id = fields.Many2one("residency.residency")

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if self.env.context.get('domain_residency_id', False):
            args = args or []
            args += [['id', 'in', self.residency_id.browse(self.env.context.get('domain_residency_id', False)).document_ids.ids]]
        return super(Document, self).name_search(name=name, args=args, operator=operator, limit=limit)
