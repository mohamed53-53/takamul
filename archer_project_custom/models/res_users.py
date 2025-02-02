from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    project_ids = fields.Many2many(comodel_name='project.project')
    project_owner = fields.Boolean(string="Project Owner")

