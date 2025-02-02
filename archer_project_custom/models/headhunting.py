from odoo import models, fields, api
import datetime

class HeadHuntingRequest(models.Model):
    _name = 'archer.headhunt.request'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']
    _rec_name = 'sequence'

    sequence = fields.Char(string='Sequence', default='/')
    project_id = fields.Many2one(comodel_name='project.project', string='Project', required=True)
    request_month = fields.Selection(selection=[
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
    ], string='Month', required=True)
    request_year = fields.Selection(
        [(str(y), str(y)) for y in range((datetime.datetime.now().year - 1), (datetime.datetime.now().year + 2))], string='Year',
        required=True)
    description = fields.Text(string='Description', required=True)
    amount = fields.Float(string='Amount', required=True)
    @api.model
    def create(self, vals_list):
        vals_list['sequence'] = self.env['ir.sequence'].next_by_code('archer_project_custom.headhunting_seq') or '/'
        res = super(HeadHuntingRequest, self).create(vals_list)
        return res

