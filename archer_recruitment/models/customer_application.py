from odoo import models, fields, api


class CustomerApplication(models.Model):
    _name = 'archer.customer.application'
    _rec_name = 'sequence'
    sequence = fields.Char(string='Sequence', default="/")
    name = fields.Char(string='English Name')
    ar_name = fields.Char(string='Arabic Name')
    country_id = fields.Many2one(comodel_name='res.country', string='Nationality')
    cv_attach = fields.Binary(string='CV')
    project_id = fields.Many2one(comodel_name='project.project', string='Project', )
    apply_job = fields.Char(string='Job To apply')
    grade_id = fields.Many2one(comodel_name='hr.grade', )
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email')
    civil_id = fields.Char(string='ID')
    description = fields.Char(string='Description')
    state = fields.Selection(selection=[('draft', 'Draft'), ('done', 'Done')], default="draft")
    offer_id = fields.Many2one(comodel_name='archer.recruitment.application')

    @api.model
    def create(self, vals_list):
        vals_list['sequence'] = self.env['ir.sequence'].next_by_code(
            'archer_recruitment.new_customer_application_seq') or '/'
        return super(CustomerApplication, self).create(vals_list)

    def action_convert_to_offer(self):
        offer = self.env['archer.recruitment.application'].create({
            'project_id': self.project_id.id,
            'applicant_ar_name': self.ar_name,
            'applicant_en_name': self.name,
            'applicant_email': self.email,
            'applicant_mobile': self.mobile,
            'applicant_country_id': self.country_id.id,
            'notes': self.description,
            'civil_id': self.civil_id,
            'grade_id': self.grade_id.id,

        })
        self.write({'state': 'done','offer_id':offer.id})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'archer.recruitment.application',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': self.offer_id.id,
        }
