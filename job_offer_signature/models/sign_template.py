from odoo import api, fields, models


class SignRequest(models.Model):
    _inherit = 'sign.request'

    def reject_template(self,request_id):
        request_obj = self.env['sign.request'].browse(request_id)
        if request_obj:
            application = request_obj.template_id.applicant_id
            if application:
                request_obj.template_id.applicant_id.rejected = True
                mail = self.env['mail.mail'].sudo().create({
                    'subject': 'Rejected Job Offer',
                    'body_html': '<strong>Dear </strong> ' + str(application.responsible_id.name) +
                                 '<br></br>Concerning Job Application : {} Was Rejected From Applicant .<br></br>'.format(
                                     application.name),
                    'email_to': application.responsible_id.login,
                })
                mail.send()
        return True

class SignTemplate(models.Model):
    _inherit = 'sign.template'

    applicant_id = fields.Many2one(comodel_name="hr.applicant")
