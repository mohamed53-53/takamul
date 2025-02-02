from odoo import models, fields, _
from odoo.exceptions import ValidationError, UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    project_ids = fields.Many2many('project.project', string="Projects", readonly=True, store=True)
    project_owner = fields.Boolean(string="Project Owner", readonly=True, store=True)
    petty_cash_responsible = fields.Boolean("Petty Cash Responsible", readonly=True, store=True)
