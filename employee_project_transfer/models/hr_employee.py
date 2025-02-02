# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    project_id = fields.Many2one('project.project', string='Current Project')
    project_transfer_ids = fields.One2many('employee.project.transfer', 'employee_id', string='Project Transfers')

    def open_transfer_project(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'employee.project.transfer',
            'name': 'Project Transfer',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }


class HrContract(models.Model):
    _inherit = 'hr.contract'

    transfer_ids = fields.One2many(comodel_name="employee.project.transfer", inverse_name="contract_id",
                                   string="Transfers")