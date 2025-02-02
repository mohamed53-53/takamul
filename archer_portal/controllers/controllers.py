import base64
import json
from datetime import datetime

from odoo import http, _
from odoo.http import request


class PortalWebsite(http.Controller):

    def prepare_attachment(self, attach):
        encoded = None
        filename = None
        if attach:
            attachment = attach
            attachment = attachment.read()
            encoded = base64.b64encode(attachment)
        return encoded

    def prepare_json_base64(self, base64):
        try:
            attach = base64.strip(base64.split(',')[0])[1:]
            Attachments = request.env['ir.attachment']
            attachment = Attachments.sudo().create({
                'name': base64,
                'type': 'binary',
                'datas': attach,
            })

            return attachment.datas
        except:
            return False

    @http.route('/job/offer', type='http', auth='public', website=True, sitemap=False)
    def offer_app_employee_response(self, **kw):
        if 'offer' in kw:
            offer = request.env['archer.recruitment.application'].sudo().search([('application_token', '=', kw['offer'])])
            if offer and 'state' not in kw:
                return http.request.render('archer_portal.job_offer', {'offer': offer})
            if offer and 'state' in kw:
                if kw['state'] == 'accept':
                    offer.sudo().action_applicant_approve()
                if kw['state'] == 'reject':
                    offer.sudo().action_applicant_reject()
                return http.request.render('archer_portal.job_offer_thank_page')
            else:
                return request.not_found()
        else:
            return request.not_found()

    @http.route('/job/app', type='http', methods=['GET'], auth='public', website=True, sitemap=False, csrf=False)
    def job_app_profile_employee_entry(self, **kw):
        if 'app' in kw:
            appl = request.env['hr.applicant'].sudo().search([('application_token', '=', kw['app'])])
            countries = request.env['res.country'].sudo().search([])
            banks = request.env['bank.bank'].sudo().search([])
            family_relations = request.env['hr.employee.relative'].sudo().search([('application_id', '=', appl.id)])
            experiences = request.env['hr.employee.experience'].sudo().search([('application_id', '=', appl.id)])
            if appl:
                return http.request.render('archer_portal.employee_appl_new',
                                           {'appl': appl, 'countries': countries, 'country_code': appl.country_id.code,
                                            'banks': banks,
                                            'family_relations': family_relations, 'experiences': experiences})
            else:
                return request.not_found()
        else:
            return request.not_found()

    @http.route('/job/apptest', type='http', methods=['GET'], auth='public', website=True, sitemap=False, csrf=False)
    def app_profile_employee_entry(self, **kw):
        if 'app' in kw:

            appl = request.env['hr.applicant'].sudo().search([('application_token', '=', kw['app'])])
            countries = request.env['res.country'].sudo().search([])
            banks = request.env['bank.bank'].sudo().search([])
            family_relations = request.env['hr.employee.relative'].sudo().search([('application_id', '=', appl.id)])
            experiences = request.env['hr.employee.experience'].sudo().search([('application_id', '=', appl.id)])
            if appl:
                return http.request.render('archer_portal.employee_appl_new',
                                           {'appl': appl, 'countries': countries, 'country_code': appl.country_id.code,
                                            'banks': banks,
                                            'family_relations': family_relations, 'experiences': experiences})
            else:
                return request.not_found()
        else:
            return request.not_found()

    @http.route('/job/app/submit', type='json', auth='public', csrf=False)
    def app_profile_employee_submit(self, **kw):
        jsondb = json.loads(request.jsonrequest['db'])
        personal_tbl = jsondb[0]['rows'][0]
        father_tbl = jsondb[1]['rows'][0] if jsondb[1]['rows'] else False
        mother_tbl = jsondb[2]['rows'][0] if jsondb[2]['rows'] else False
        spouse_tbl = jsondb[3]['rows'][0] if jsondb[3]['rows'] else False
        children_tbl = jsondb[4]['rows'] if jsondb[4]['rows'] else False
        experience_tbl = jsondb[5]['rows'] if jsondb[5]['rows'] else False
        attach_tbl = jsondb[6]['rows'] if jsondb[6]['rows'] else False

        appl = request.env['hr.applicant'].sudo().search([('application_token', '=', request.jsonrequest['application_token'])])
        appl.relative_ids.sudo().unlink()
        appl.experience_ids.sudo().unlink()

        person_val = {
            'partner_name': personal_tbl['name_en'] if 'name_en' in personal_tbl else False,
            'name_ar': personal_tbl['name_ar'] if 'name_ar' in personal_tbl else False,
            'partner_phone': personal_tbl['phone'] if 'phone' in personal_tbl else False,
            'partner_mobile': personal_tbl['partner_mobile'] if 'partner_mobile' in personal_tbl else False,
            'birthday': datetime.strptime(personal_tbl['birthday'], '%Y-%m-%d').date() if 'birthday' in personal_tbl else False,
            'civil_id': personal_tbl['civil_id'] if 'civil_id' in personal_tbl else False,
            'passport': personal_tbl['passport'] if 'passport' in personal_tbl else False,
            'marital': personal_tbl['marital'] if 'marital' in personal_tbl else False,
            'gender': personal_tbl['gender'] if 'gender' in personal_tbl else False,
            'religion': personal_tbl['religion'] if 'religion' in personal_tbl else False,
            'national_address': personal_tbl['national_address'] if 'national_address' in personal_tbl else False,
            'graduate_date': datetime.strptime(personal_tbl['graduate_date'],
                                               '%Y-%m-%d').date() if 'graduate_date' in personal_tbl else False,
            'sponsor_name': personal_tbl['sponsor_name'] if 'sponsor_name' in personal_tbl else False,
            'sponsor_phone': personal_tbl['sponsor_phone'] if 'sponsor_name' in personal_tbl else False,
            'sponsor_address': personal_tbl['sponsor_address'] if 'sponsor_name' in personal_tbl else False,
            'bank_country_id': personal_tbl['bank_country_id'] if 'bank_country_id' in personal_tbl else False,
            'international_bank': personal_tbl['international_bank'] if 'international_bank' in personal_tbl else False,
            'branch_name_code': personal_tbl['branch_name_code'] if 'branch_name_code' in personal_tbl else False,
            'bank_name': personal_tbl['bank_name'] if 'bank_name' in personal_tbl else False,
            'iban_no': personal_tbl['iban_no'] if 'iban_no' in personal_tbl else False,
            'bank_id': personal_tbl['bank_id'] if 'bank_id' in personal_tbl else False,
            'resid_number': personal_tbl['residency_number'] if 'residency_number' in personal_tbl else False,
            'serial_number': personal_tbl['serial_number'] if 'serial_number' in personal_tbl else False,
            'resid_job_title': personal_tbl['resid_job_title'] if 'resid_job_title' in personal_tbl else False,
            'place_of_issuance': personal_tbl['place_of_issuance'] if 'place_of_issuance' in personal_tbl else False,
            'resid_issuance_date': datetime.strptime(personal_tbl['resid_issuance_date'],
                                                     '%Y-%m-%d').date() if 'resid_issuance_date' in personal_tbl and not personal_tbl[
                                                                                                                             'resid_issuance_date'] == '' else False,
            'resid_expiration_date': datetime.strptime(personal_tbl['expiration_date'],
                                                       '%Y-%m-%d').date() if 'expiration_date' in personal_tbl and not personal_tbl[
                                                                                                                           'expiration_date'] == '' else False,
            'resid_expiration_date_in_hijri': personal_tbl['expiration_date_in_hijri'] if 'expiration_date_in_hijri' in personal_tbl else False,
            'arrival_date': datetime.strptime(personal_tbl['arrival_date'], '%Y-%m-%d').date() if 'arrival_date' in personal_tbl and not
            personal_tbl['arrival_date'] == '' else False,
            'place_of_birth': personal_tbl['place_of_birth'] if 'place_of_birth' in personal_tbl else False,
            'country_of_birth': int(personal_tbl['country_of_birth']) if 'country_of_birth' in personal_tbl else False,
            'certificate': personal_tbl['certificate'] if 'certificate' in personal_tbl else False,
            'study_field': personal_tbl['study_field'] if 'study_field' in personal_tbl else False,
            'study_school': personal_tbl['study_school'] if 'study_school' in personal_tbl else False,
            'gosi_number': personal_tbl['gosi_number'] if 'gosi_number' in personal_tbl and personal_tbl['gosi_number'] else False,
            'gosi_start_date': datetime.strptime(personal_tbl['gosi_start_date'],
                                                 '%Y-%m-%d').date() if 'gosi_start_date' in personal_tbl and personal_tbl[
                'gosi_start_date'] and not personal_tbl['gosi_start_date'] == '' else False,
        }
        appl.sudo().write(person_val)
        family_vals = []
        experience_vals = []
        attach_vals = []
        if father_tbl:
            if not father_tbl['father_name'] == '':
                family_vals.append({
                    'application_id': appl.id,
                    'name': father_tbl['father_name'] if 'father_name' in father_tbl else False,
                    'id_number': father_tbl['father_id_number'] if 'father_id_number' in father_tbl else False,
                    'birthdate': datetime.strptime(father_tbl['father_birthdate'],
                                                   '%Y-%m-%d').date() if 'father_birthdate' in father_tbl and not father_tbl[
                                                                                                                      'father_birthdate'] == '' else False,
                    'relation': 'father',
                    'gender': 'male',
                    'phone': father_tbl['father_phone'] if 'father_phone' in father_tbl else False,
                    'attach': self.prepare_json_base64(
                        father_tbl['father_family_attach']) if 'father_family_attach' in father_tbl else False
                })
        if mother_tbl:
            if not mother_tbl['mother_name'] == '':
                family_vals.append({
                    'application_id': appl.id,
                    'name': mother_tbl['mother_name'] if 'mother_name' in mother_tbl else False,
                    'id_number': mother_tbl['mother_id_number'] if 'mother_id_number' in mother_tbl else False,
                    'birthdate': datetime.strptime(mother_tbl['mother_birthdate'],
                                                   '%Y-%m-%d').date() if 'mother_birthdate' in mother_tbl and not mother_tbl[
                                                                                                                      'mother_birthdate'] == '' else False,
                    'relation': 'mother',
                    'gender': 'female' if personal_tbl['gender'] == 'male' else 'male',
                    'phone': mother_tbl['mother_phone'] if 'mother_phone' in mother_tbl else False,
                    'attach': self.prepare_json_base64(
                        mother_tbl['mother_family_attach']) if 'mother_family_attach' in mother_tbl else False
                })
        if spouse_tbl:
            if not spouse_tbl['spouse_name'] == '':
                family_vals.append({
                    'application_id': appl.id,
                    'name': spouse_tbl['spouse_name'] if 'spouse_name' in spouse_tbl else False,
                    'id_number': spouse_tbl['spouse_id_number'] if 'spouse_id_number' in spouse_tbl else False,
                    'birthdate': datetime.strptime(spouse_tbl['spouse_birthdate'],
                                                   '%Y-%m-%d').date() if 'spouse_birthdate' in spouse_tbl and not spouse_tbl[
                                                                                                                      'spouse_birthdate'] == '' else False,
                    'relation': 'spouse',
                    'gender': 'female',
                    'phone': spouse_tbl['spouse_phone'] if 'spouse_phone' in spouse_tbl else False,
                    'attach': self.prepare_json_base64(
                        spouse_tbl['spouse_family_attach']) if 'spouse_family_attach' in spouse_tbl else False
                })
        if children_tbl:
            for child in children_tbl:
                if 'child_name' in child:
                    child_val = {
                        'application_id': appl.id,
                        'name': child['child_name'] if 'child_name' in child else False,
                        'id_number': child['child_id_number'] if 'child_id_number' in child else False,
                        'birthdate': datetime.strptime(child['child_birthdate'],
                                                       '%Y-%m-%d').date() if 'child_birthdate' in child else False,
                        'relation': 'child',
                        'gender': child['child_gender'] if 'child_gender' in child else False,
                        'phone': child['child_phone'] if 'child_phone' in child else False,
                        'attach': self.prepare_json_base64(child['child_family_attach']) if 'child_family_attach' in child else False
                    }
                    family_vals.append(child_val)
        if family_vals:
            family = request.env['hr.employee.relative'].sudo().create(family_vals)
        if experience_tbl:
            for experience in experience_tbl:
                if not experience['job_name'] == '':
                    experience_val = {
                        'application_id': appl.id,
                        'job_name': experience['job_name'] if 'job_name' in experience else False,
                        'employer_name': experience['employer_name'] if 'employer_name' in experience else False,
                        'date_from': datetime.strptime(experience['date_from'],
                                                       '%Y-%m-%d').date() if 'date_from' in experience else False,
                        'date_to': datetime.strptime(experience['date_to'],
                                                     '%Y-%m-%d').date() if 'date_to' in experience else False,
                        'service_certificate': experience['service_certificate'] if 'service_certificate' in experience else False
                    }
                    experience_vals.append(experience_val)
        if experience_vals:
            experience = request.env['hr.employee.experience'].sudo().create(experience_vals)

        if attach_tbl:
            for att in attach_tbl:
                atta = request.env['hr.employee.document'].sudo().browse(att['dbid'])
                atta.write({'attach': self.prepare_json_base64(att['attach']) if 'attach' in att else False})

        appl.sudo().write({'data_state': 'revision'})
        return {'app_id': appl.id}
