# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

from odoo.exceptions import UserError


class Employee(models.AbstractModel):
    _inherit = 'hr.employee.base'

    application_id = fields.Many2one(comodel_name="hr.applicant", )


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    application_id = fields.Many2one(comodel_name="hr.applicant", )


class HRApplicant(models.Model):
    _inherit = 'hr.applicant'

    def _get_salary_breakdown(self):
        rules = self.env['salary.breakdown'].search([])
        lines = []
        for rule in rules:
            lines.append((0, 0, {'applicant_id': self.id,
                                 'salary_breakdown_id': rule.id,
                                 'salary_breakdown_rate': rule.rate,
                                 'is_experience_rule': rule.is_experience_rule,
                                 }))
        return lines

    def _default_stage_id(self):
        if self._context.get('default_job_id'):
            return self.env['hr.recruitment.stage'].search([
                '|',
                ('job_ids', '=', False),
                ('job_ids', '=', self._context['default_job_id']),
                ('fold', '=', False)
            ], order='sequence asc', limit=1).id
        return self.env['hr.recruitment.stage'].search([('sequence', '=', 1)], limit=1).id

    first_name = fields.Char(string="", required=False, )
    middle_name = fields.Char(string="", required=False, )
    last_name = fields.Char(string="", required=False, )
    offer_by = fields.Char()
    offer_type = fields.Selection(selection=[('full_time', 'Full Time'),
                                             ('part_time', 'Part Time'), ], default='full_time')
    deadline_date = fields.Date(string="Deadline", )
    contract_type_id = fields.Many2one(comodel_name="contract.type", )
    campus_id = fields.Many2one(comodel_name="hr.employee.campus", string="Default School", required=False, )
    country_id = fields.Many2one(comodel_name="res.country", string='Nationality1')
    academic_year_id = fields.Many2one(comodel_name="academic.year")
    annual_basic_salary = fields.Float()
    subtotal_salary = fields.Float(compute="compute_subtotal_salary")
    total_annual_salary = fields.Float(compute="compute_total_annual_salary")
    salary_breakdown_ids = fields.One2many(comodel_name="salary.breakdown.line", inverse_name="applicant_id",
                                           default=_get_salary_breakdown)
    stage_id = fields.Many2one('hr.recruitment.stage', 'Stage', ondelete='restrict', tracking=True,
                               domain="['|', ('job_ids', '=', False), ('job_ids', '=', job_id)]",
                               copy=False, index=True,
                               group_expand='_read_group_stage_ids',
                               default=_default_stage_id)

    @api.depends('salary_breakdown_ids.subtotal')
    def compute_subtotal_salary(self):
        for rec in self:
            rec.subtotal_salary = sum(rec.salary_breakdown_ids.mapped('subtotal'))

    @api.depends('annual_basic_salary', 'salary_breakdown_ids', 'salary_breakdown_ids.have_rule',
                 'salary_breakdown_ids.salary_breakdown_rate')
    def compute_total_annual_salary(self):
        for rec in self:
            total = 0
            for line in rec.salary_breakdown_ids:
                if line.have_rule:
                    if line.is_experience_rule:
                        total += (line.salary_breakdown_rate * line.num_experience_years)
                    else:
                        total += line.salary_breakdown_rate
            rec.total_annual_salary = rec.annual_basic_salary + total

    @api.onchange('first_name', 'middle_name', 'last_name')
    @api.constrains('first_name', 'middle_name', 'last_name')
    def compute_full_name(self):
        for rec in self:
            full_name = ""
            if rec.first_name:
                full_name += "{} ".format(rec.first_name)
            if rec.middle_name:
                full_name += "{} ".format(rec.middle_name)
            if rec.last_name:
                full_name += "{}".format(rec.last_name)
            rec.partner_name = full_name

    def create_employee_from_applicant(self):
        """ Create an hr.employee from the hr.applicants """
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])['contact']
                contact_name = applicant.partner_id.display_name
            else:
                if not applicant.partner_name:
                    raise UserError(_('You must define a Contact Name for this applicant.'))
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'type': 'private',
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile
                })
                address_id = new_partner_id.address_get(['contact'])['contact']
            if applicant.partner_name or contact_name:
                employee = self.env['hr.employee'].create({
                    'application_id': applicant.id,
                    'name': applicant.partner_name or contact_name,
                    'first_name': applicant.first_name,
                    'middle_name': applicant.middle_name,
                    'last_name': applicant.last_name,
                    'private_email': applicant.email_from,
                    'campus_id': applicant.campus_id.id,
                    'country_id': applicant.country_id.id,
                    'emp_state': 'new_hire',
                    'user_id': applicant.user_id.id,
                    'job_id': applicant.job_id.id or False,
                    'job_title': applicant.job_id.name,
                    'address_home_id': address_id,
                    'department_id': applicant.department_id.id or False,
                    'address_id': applicant.company_id and applicant.company_id.partner_id
                                  and applicant.company_id.partner_id.id or False,
                    'work_email': applicant.department_id and applicant.department_id.company_id
                                  and applicant.department_id.company_id.email or False,
                    'work_phone': applicant.department_id and applicant.department_id.company_id
                                  and applicant.department_id.company_id.phone or False})
                applicant.write({'emp_id': employee.id})
                if applicant.job_id:
                    applicant.job_id.write({'no_of_hired_employee': applicant.job_id.no_of_hired_employee + 1})
                    applicant.job_id.message_post(
                        body=_(
                            'New Employee %s Hired') % applicant.partner_name if applicant.partner_name else applicant.name,
                        subtype="hr_recruitment.mt_job_applicant_hired")
                applicant.message_post_with_view(
                    'hr_recruitment.applicant_hired_template',
                    values={'applicant': applicant},
                    subtype_id=self.env.ref("hr_recruitment.mt_applicant_hired").id)

        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        dict_act_window['context'] = {'form_view_initial_mode': 'edit'}
        dict_act_window['res_id'] = employee.id
        return dict_act_window

    def send_survey_link(self):
        self.ensure_one()
        token = self.env.context.get('survey_token')
        trail = "?answer_token=%s" % token if token else ""
        url = self.survey_id.public_url + trail
        mail = self.env['mail.mail'].sudo().create({
            'subject': 'Job Offer Survey',
            'body_html': '<strong>Dear </strong> ' + str(self.partner_name) +
                         '<br></br>Concerning Job Application : {} Please Fill This is Survey .<br></br>'.format(
                             self.name) +
                         '<br></br><a href=' + url + '>%s</a>' % (url),
            'email_to': self.email_from,
        })
        mail.send()
