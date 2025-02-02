# -*- coding: utf-8 -*-
# Part of odoo. See LICENSE file for full copyright and licensing details.

import time
from odoo import models, fields, api, _
from dateutil import relativedelta
from datetime import date, datetime, timedelta
import calendar
from odoo.exceptions import UserError
from odoo.tools.misc import format_date
import logging
from odoo.exceptions import UserError, ValidationError, Warning

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    join_date = fields.Date(related='contract_id.date_start')
    date_of_leave = fields.Date()

    def action_open_eos_lines(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Entry Move',
            'res_model': 'monthly.eos.line',
            'view_mode': 'tree',
            'domain': [('employee_id', '=', self.id)],
        }