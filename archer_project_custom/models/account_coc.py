from odoo import api, fields, models
from datetime import datetime


_COC_STATE = [
    ("draft", "Draft"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("canceled", "Cancelled"),
]


_MONTH_SELECTION = [
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]


class AccountCOC(models.Model):
    _name = "archer.account.coc"
    _rec_name = 'name'
    _description = 'COC'

    def _get_year_selection(self):
        years = []
        for seq in range(datetime.now().year - 6, datetime.now().year + 6):
            years.append((str(seq), str(seq)))
        return years

    name = fields.Char(string='Name', required=True, translate=True)
    date = fields.Date(string="Date", default=fields.Date.today)
    project_id = fields.Many2one(comodel_name='project.project')
    partner_id = fields.Many2one(comodel_name='res.partner')
    year = fields.Selection(selection=_get_year_selection, default=lambda self: str(datetime.now().year))
    month = fields.Selection(selection=_MONTH_SELECTION, required=True, string='COC for Month')
    user_id = fields.Many2one(comodel_name='res.users', string='Responsible', required=False, default=lambda self: self.env.user)
    line_ids = fields.One2many(comodel_name='archer.account.coc.line', inverse_name='coc_id')
    amount_total = fields.Float(compute='_compute_amount_total')
    state = fields.Selection(string="State", selection=_COC_STATE, default='draft')

    def _compute_amount_total(self):
        for rec in self:
            rec.amount_total = sum(rec.line_ids.mapped('amount_total'))
