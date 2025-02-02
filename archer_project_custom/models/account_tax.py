from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import datetime
import re


class AccountTaxInherit(models.Model):
    _inherit = 'account.tax'

    for_coc = fields.Boolean()
