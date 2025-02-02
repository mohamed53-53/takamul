import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    is_freelance = fields.Boolean(string='Is Freelancer', readonly=True, store=True)
    bank_name = fields.Char(string='Bank Name')
    iban = fields.Char(string='IBAN')
    project_id = fields.Many2one(comodel_name='project.project', string='Project')

class FreelanceApplication(models.Model):
    _name = 'archer.freelance.application'
    _rec_name = 'sequence'
    _description = 'Freelancer Application'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']

    sequence = fields.Char(string='Sequence')
    name = fields.Char(string='Name', required=True)
    ar_name = fields.Char(string='Arabic Name', required=True)
    project_id = fields.Many2one(comodel_name='project.project', string='Project', required=True)
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email', required=True)
    country_id = fields.Many2one(comodel_name='res.country', string='Country', required=True)
    bank_name = fields.Char(string='Bank Name', required=True)
    iban = fields.Char(string='IBAN', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Related Partner')
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([])

    @api.depends('email')
    @api.onchange('email')
    def onchange_email_validation(self):
        for rec in self:
            if rec.email:
                if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), rec.email):
                    raise ValidationError(_('Please enter valid email'))

    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    def action_reject(self, reason=None):
        self.write({'state': 'rejected'})
        if reason:
            self.message_post(body=reason, subject="Reject Reason")

    @api.model
    def create(self, vals_list):
        vals_list['sequence'] = self.env['ir.sequence'].next_by_code('archer_freelancer_employee.archer_freelance_application_seq') or '/'
        return super(FreelanceApplication, self).create(vals_list)

    def action_approve(self):
        for rec in self:
            if rec.state == 'hr_dir_approve':
               vals ={
                   'name':rec.name,
                   'project_id':rec.project_id.id,
                   'email':rec.email,
                   'mobile': rec.mobile,
                   'country_id':rec.country_id.id,
                   'is_freelance': True,
                   'bank_name': rec.bank_name,
                   'iban': rec.iban,

               }
               partner = self.env['res.partner'].create(vals)
               rec.partner_id = partner.id
            return super().action_approve()