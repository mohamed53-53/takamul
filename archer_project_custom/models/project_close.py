from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectTermination(models.Model):
    _name = "project.close"
    _rec_name = 'project_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', ]

    project_id = fields.Many2one("project.project")
    project_start_date = fields.Date(string='Project Start Date', related='project_id.date_start')
    project_end_date = fields.Date(string='Project End Date', related='project_id.date')
    state = fields.Selection([('draft', 'Draft'), ('submit', 'Submit')], default='draft', tracking=True)

    def action_submit(self):
        activity_mail_template = self.env.ref('archer_project_custom.mail_template_employee_project_close')

        self.write({'state':'submit'})
        for user in self.env['res.users'].search([('project_ids','in', self.project_id.ids)]):
            email_values = {
                'email_to': user.login,
                'subject': 'Project [%s] Termination'%self.project_id.name,
                'user_name' : user.partner_id.name,
                'project_name' : self.project_id.name,
                'close_date': self.project_end_date,
            }
            activity_mail_template.send_mail(self.id, force_send=True,raise_exception=True,
                                                                                       email_values=email_values)
        self.project_id.write({'project_state':'in_close'})

