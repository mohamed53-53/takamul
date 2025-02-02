# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProjectProject(models.Model):
    _inherit = "project.project"

    leave_type_ids = fields.Many2many(comodel_name="hr.leave.type", string="Allowed Leave Types")


class ProjectRequest(models.Model):
    _inherit = 'project.request'

    def default_get(self, fields_list):
        res = super(ProjectRequest, self).default_get(fields_list)
        leaves = self.env['hr.leave.type'].search([])
        benifits = self.env['employee.eos.other.benefits'].search([])
        res['leave_type_ids'] = [(6,0,leaves.ids)]
        return res


    leave_type_ids = fields.Many2many(comodel_name="hr.leave.type", string="Allowed Leave Types")

    def create_project(self):
        res = super().create_project()
        res.leave_type_ids = [(6, 0, self.leave_type_ids.ids)]
        return res
