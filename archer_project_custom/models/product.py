from odoo import models, fields, _
from odoo.exceptions import ValidationError, UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    provide_service = fields.Boolean(string="Provided Service")

    is_used_in_project_service = fields.Boolean()

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        for product in self:
            if not product.provide_service and product.is_used_in_project_service:
                raise UserError(_('This product used in project services, you can not remove the provide service'))
            if product.detailed_type != 'service' and product.is_used_in_project_service:
                raise UserError(
                    _('This product used in project services, you can not change the type of product'))
        return res
