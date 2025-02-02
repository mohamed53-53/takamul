# -*- coding: utf-8 -*-

import base64
import io
import logging
import mimetypes
import re
import werkzeug

from PyPDF2 import PdfFileReader

from odoo import http, _
from odoo.http import request
_logger = logging.getLogger()


class SignReject(http.Controller):

    @http.route(['/offer/reject/<int:sign_request_id>'], type='json', auth='public',website=True)
    def check_encrypted(self, sign_request_id):
        request_obj = http.request.env['sign.request'].sudo().search([('id', '=', sign_request_id)],
                                                                           limit=1)
        if request_obj:
            application = request_obj.template_id.sudo().applicant_id
            if application:
                request_obj.template_id.applicant_id.sudo().rejected = True
                mail = http.request.env['mail.mail'].sudo().create({
                    'subject': 'Rejected Job Offer',
                    'body_html': '<strong>Dear </strong> ' + str(application.responsible_id.name) +
                                 '<br></br>Concerning Job Application : {} Was Rejected From Applicant .<br></br>'.format(
                                     application.name),
                    'email_to': application.responsible_id.login,
                })
                mail.send()
        return True

    @http.route(['/offer/reject/thank_you/'], type='http', auth="public", website=True)
    def offer_reject_thank_you(self, **kw):
        message = 'We will contact with you soon, Thank you.'
        return request.render("job_offer_signature.sign_rejected_template",
                              {'message': message})