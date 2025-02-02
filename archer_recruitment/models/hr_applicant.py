import uuid
from datetime import datetime, timedelta
import re

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class GosiHire(models.Model):
    _inherit = 'gosi.hire'
    application_id = fields.Many2one('hr.applicant')


class HrEmployeeRelative(models.Model):
    _inherit = 'hr.employee.relative'
    application_id = fields.Many2one(comodel_name='hr.applicant')


class HrEmployeeExperience(models.Model):
    _inherit = 'hr.employee.experience'
    application_id = fields.Many2one(comodel_name='hr.applicant')


class HrEmployeeCertificate(models.Model):
    _inherit = 'hr.employee.certificate'
    application_id = fields.Many2one(comodel_name='hr.applicant')


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    @api.depends('project_id')
    def compute_plan_project(self):
        for rec in self:
            if rec.project_id:
                plan_id = self.env['hr.boarding.plan'].search(
                    [('project_id', '=', rec.project_id.id), ('plan_type', '=', 'onboarding')],
                    limit=1)
                if not plan_id:
                    plan_id = self.env['hr.boarding.plan'].search(
                        [('project_id', '=', False), ('plan_type', '=', 'onboarding')], limit=1)
            else:
                plan_id = self.env['hr.boarding.plan'].search(
                    [('project_id', '=', False), ('plan_type', '=', 'onboarding')], limit=1)
            if plan_id:
                rec.plan_id = plan_id.id
            else:
                rec.plan_id = False

    project_id = fields.Many2one("project.project", required=True)
    contract_start_date = fields.Date('Contract Start Date', default=fields.Date.today())
    contract_duration = fields.Integer(string='Contract Duration/Mooths')
    contract_end_date = fields.Date('Contract End Date', compute='_compute_contract_duration')
    name_ar = fields.Char(string='Arabic Name', required=True)
    project_owner_id = fields.Many2one(related="project_id.owner_id")
    currency_id = fields.Many2one(comodel_name='res.currency', related='company_id.currency_id')
    country_id = fields.Many2one(comodel_name='res.country', string='Nationality', required=True)
    country_code = fields.Char(related='country_id.code')
    birthday = fields.Date(string='Date Of Birth')
    basic_sal = fields.Float(string="", required=False)
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')])
    civil_id = fields.Char(string='Civil ID')
    passport = fields.Char(string='Passport')
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', )
    religion = fields.Selection([
        ('muslim', 'Muslim'),
        ('not_muslim', "Not Muslim")], "Religion")
    national_address = fields.Binary(string='National Address')
    relative_ids = fields.One2many(comodel_name='hr.employee.relative', string='Relative',
                                   inverse_name='application_id')
    experience_ids = fields.One2many(comodel_name='hr.employee.experience', string='Experience',
                                     inverse_name='application_id')
    certificate_ids = fields.One2many(comodel_name='hr.employee.certificate', string='Certificate',
                                      inverse_name='application_id')
    grade_id = fields.Many2one('hr.grade', string="Grade")
    sponsor_name = fields.Char(string='Name')
    sponsor_phone = fields.Char(string='Phone')
    sponsor_address = fields.Text(string='Address')
    bank_country_id = fields.Many2one(comodel_name='res.country', string='Country')
    international_bank = fields.Boolean("International Bank")
    work_email = fields.Char(string="Work Email", required=False, )
    branch_name_code = fields.Char("Branch Name/Code")
    bank_name = fields.Char(string='Bank Name')
    iban_no = fields.Char(string='IBAN Number')
    bank_id = fields.Many2one(comodel_name="bank.bank", string="Bank Name")
    resid_number = fields.Char(string="Number")
    serial_number = fields.Char(string="Serial Number")
    resid_job_title = fields.Char(string="Job Title")
    place_of_issuance = fields.Char("Place of Issuance")
    resid_issuance_date = fields.Date("Issuance Date")
    resid_expiration_date = fields.Date("Expiration Date")
    resid_expiration_date_in_hijri = fields.Char("Expiration Date in Hijri", readonly=True)
    arrival_date = fields.Date("Arrival Date")
    data_state = fields.Selection(
        selection=[('draft', 'Draft'), ('employee_entry', 'Employee Entry'), ('revision', 'Under Revision'),
                   ('approve', 'Approve'),
                   ('return', 'Returned To Employee'), ('done', 'Done')], default='draft', copy=False)
    application_token = fields.Char()
    from_app = fields.Boolean(default=False)
    app_state = fields.Selection(selection=[('direct_data', 'Direct with Data'), ('direct', 'Direct')], default=False)
    employee_age = fields.Integer(string="Age", compute='_compute_age')
    offer_id = fields.Many2one(comodel_name="archer.recruitment.application", string="Offer", readonly=True)
    return_reason = fields.Text()
    place_of_birth = fields.Char('Place of Birth', tracking=True)
    country_of_birth = fields.Many2one('res.country', string="Country of Birth")
    graduate_date = fields.Date(string='Graduation Date')
    plan_id = fields.Many2one(comodel_name="hr.boarding.plan", string="Plan", compute=compute_plan_project)
    certificate = fields.Selection([
        ('graduate', 'Graduate'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('doctor', 'Doctor'),
        ('other', 'Other'),
    ], 'Certificate Level', tracking=True)
    study_field = fields.Char("Field of Study", tracking=True)
    study_school = fields.Char("School", tracking=True)

    not_have_gosi = fields.Boolean(string='Not Have GOSI')
    gosi_number = fields.Char('Social Insurance Number', size=9)
    gosi_start_date = fields.Date(string="Start Date")
    gosi_id = fields.Many2one(comodel_name='gosi.hire', string='Related GOSI')
    rule_ids = fields.One2many(comodel_name='arch.hr.contract.allowance', inverse_name='application_id',
                               string='Allowance')
    salary_total = fields.Monetary(string='Salary Total', currency_field='currency_id',
                                   compute='salary_total_compute_rule')
    structure_type_id = fields.Many2one('hr.payroll.structure.type', string="Salary Structure Type",
                                        domain="[('project_ids','in', project_id)]")
    pending_contract_id = fields.Many2one(comodel_name='hr.contract.wait', string='Pending Contract')
    appl_documents_ids = fields.One2many(comodel_name='hr.employee.document', inverse_name='application_id',
                                         string='Document',
                                         domain=[('used_for', 'in', ['both', 'employee'])])
    empl_type = fields.Selection(selection=[('full', 'Full Time'), ('part', 'Part Time')], default='full',
                                 required=True,
                                 string='Employee Type')
    email_from = fields.Char(string="Email", help="Applicant email")

    @api.depends('contract_start_date','contract_duration')
    @api.onchange('contract_start_date','contract_duration')
    def _compute_contract_duration(self):
        for rec in self:
            rec.contract_end_date = rec.contract_start_date + relativedelta(months=rec.contract_duration)-relativedelta(days=1)

    @api.constrains('contract_duration')
    def _constraint_contract_duration(self):
        for rec in self:
            if rec.contract_duration <= 0:
                raise ValidationError(_('Contract Duration Must be greater then zero'))
    @api.depends('structure_type_id')
    @api.onchange('structure_type_id')
    def onchange_structure_type_id_rule(self):
        for rec in self:
            rec.rule_ids = False
            rec.rule_ids = [(0,0,{
                'company_id': rec.company_id.id,
                'currency_id':rec.company_id.currency_id.id,
                'structure_type_id': rec.structure_type_id.id,
                'default_struct_id':rec.structure_type_id.default_struct_id.id,
                'rule_id': x.id,
                'rule_code':x.code,
            }) for x in rec.structure_type_id.default_struct_id.rule_ids.filtered(lambda r:r.is_dynamic)]
    @api.constrains('civil_id')
    def _check_mobile_unique(self):
        counts = self.search_count(
            [('civil_id', '=', self.civil_id),('civil_id', '!=', False), ('id', '!=', self.id)])
        if counts > 0:
            raise ValidationError(_("ID already exists!"))

    @api.depends('email_from')
    @api.onchange('email_from')
    def email_from_validate(self):
        if self.email_from:
            if not re.fullmatch(regex, self.email_from):
                self.email_from = False
                raise ValidationError(_("Invalid Email"))

    @api.depends('work_email')
    @api.onchange('work_email')
    def work_email_validate(self):
        if self.work_email:
            if not re.fullmatch(regex, self.work_email):
                self.work_email = False
                raise ValidationError(_("Invalid Email"))

    @api.depends("birthday")
    def _compute_age(self):
        for rec in self:
            if rec.birthday:
                age = relativedelta(datetime.today(), rec.birthday).years
                if age < 18:
                    rec.birthday = False
                    rec.employee_age = False
                    raise ValidationError(_('Age Must be greater then 18 year\'s'))
                else:
                    rec.employee_age = age
            else:
                rec.employee_age = 0.0

    @api.depends('rule_ids')
    @api.onchange('rule_ids')
    def salary_total_compute_rule(self):
        for rec in self:
            basic_salary_rule = rec.rule_ids.filtered(lambda r: r.rule_id.code == 'BASIC')
            total = 0.0
            for x in rec.rule_ids:
                if x.value_type == 'amount':
                    total += x.value
                if x.value_type == 'percent':
                    vv = ((x.value * basic_salary_rule.value) / 100) or 0
                    x.total_value = vv
                    total +=vv
            rec.salary_total = total

    @api.model
    def create(self, vals_list):
        res = super(HrApplicant, self).create(vals_list)
        res.application_token = str(res.id) + uuid.uuid4().hex
        return res

    def action_send_employee_profile(self):
        for rec in self:
            try:
                mail_template = self.env.ref('archer_recruitment.mail_template_new_application')
                email_sent = mail_template.send_mail(rec.id, force_send=True)
                rec.write({'data_state': 'employee_entry'})
            except Exception as ex:
                raise EOFError(ex)

    def action_approve(self):
        for rec in self:
            try:
                mail_template = self.env.ref('archer_recruitment.mail_template_approve_application')
                email_sent = mail_template.send_mail(rec.id, force_send=True)
                rec.write({'data_state': 'approve', 'application_token': False})
            except Exception as ex:
                raise EOFError(ex)

    def action_return_employee(self):
        return {
            'name': _("Return Reason"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.applicant.return.employee.wizard',
            'target': 'new',
            'context': {'default_application_id': self.id},
        }

    def create_employee_from_applicant(self):
        for rec in self:

            employee = self.env['hr.employee'].create({
                'application_id': rec.id,
                'identification_id': rec.civil_id,
                'project_id': rec.project_id.id,
                'grade_id': rec.grade_id.id,
                'name': rec.partner_name,
                'arabic_name': rec.name_ar,
                'private_email': rec.email_from,
                'country_id': rec.country_id.id,
                'job_id': rec.job_id.id or False,
                'job_title': rec.job_id.name,
                'department_id': rec.department_id.id or False,
                'birthday': rec.birthday or False,
                'work_email': rec.work_email or False,
                'graduate_date': rec.graduate_date or False,
                'international_bank': rec.international_bank,
                'bank_country_id': rec.bank_country_id.id,
                'branch_name_code': rec.branch_name_code,
                'bank_name': rec.bank_name,
                'iban_no': rec.iban_no,
                'bank_id': rec.bank_id.id,
                'residency_number': rec.resid_number,
                'serial_number': rec.serial_number,
                'resid_job_title': rec.resid_job_title,
                'place_of_issuance': rec.place_of_issuance,
                'issuance_date': rec.resid_issuance_date,
                'expiration_date': rec.resid_expiration_date,
                'expiration_date_in_hijri': rec.resid_expiration_date_in_hijri,
                'arrival_date': rec.arrival_date,
                'sponsor_name': rec.sponsor_name,
                'sponsor_phone': rec.sponsor_phone,
                'sponsor_address': rec.sponsor_address,
                'country_of_birth': rec.country_of_birth.id,
                'place_of_birth': rec.place_of_birth,
                'empl_type': rec.empl_type,

            })
            rec.relative_ids.write({'employee_id': employee.id})
            rec.experience_ids.write({'employee_id': employee.id})
            gosi = self.env['gosi.hire'].create({
                'application_id': rec.id,
                'project_id': rec.project_id.id,
                'employee_id': employee.id,
                'company_id': rec.company_id.id,
                'number': rec.gosi_number,
                'start_date': rec.gosi_start_date,
                # 'empl_type': rec.empl_type,
                'state': 'draft',
            })
            pending_contract = self.env['hr.contract.wait'].create({
                'offer_id': rec.offer_id.id,
                'application_id': rec.id,
                'employee_id': employee.id,
                'structure_type_id': rec.structure_type_id.id,
                'state': 'new',
                'active': True
            })

            if rec.plan_id:
                activity_mail_template = self.env.ref('archer_recruitment.mail_template_new_activity')
                for activity in rec.plan_id.activity_ids:
                    employee_plan_lines = {
                        'boarding_plan_id': rec.plan_id.id,
                        'name': activity.id,
                        'no_of_days': activity.no_of_days,
                        'user_id': self.env.uid,
                        'employee_id': employee.id,
                        'assign_date': datetime.now().date(),
                        'done_date': False,
                        'deadline_date': datetime.now().date() + timedelta(days=activity.no_of_days),
                    }
                    self.env['hr.boarding.plan.employee'].create(employee_plan_lines)
                    email_values = {
                        'email_to': employee.work_email,
                        'subject': 'Onboarding Employee',
                    }
                    activity_mail_template.with_context(user_name=activity.user_id.name, activity_name=activity.name,
                                                        employee_name=employee.name).send_mail(rec.id, force_send=True,
                                                                                               raise_exception=True,
                                                                                               email_values=email_values)
            rec.write({'data_state': 'done', 'emp_id': employee.id, 'gosi_id': gosi.id,
                       'pending_contract_id': pending_contract.id})


class ReturnToEmployeeReason(models.Model):
    _name = 'hr.applicant.return.employee.wizard'

    application_id = fields.Many2one(comodel_name='hr.applicant')
    reason = fields.Text(string='Reason', required=True)

    def action_return(self):
        try:
            self.application_id.write({'data_state': 'return', 'return_reason': self.reason})
            self._cr.commit()
            self.application_id.message_post(body=self.reason, subject="Reject Reason")
            mail_template = self.env.ref('archer_recruitment.mail_template_return_application')
            email_sent = mail_template.with_context(is_reminder=True).send_mail(self.application_id.id, force_send=True)
        except Exception as ex:
            raise EOFError(ex)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    application_id = fields.Many2one(comodel_name="hr.applicant", )

    def action_create_user(self):
        for rec in self:
            new_partner_id = self.env['res.partner'].create({
                'is_company': False,
                'type': 'private',
                'name': rec.partner_name,
                'email': rec.email_from,
                'phone': rec.partner_phone,
                'mobile': rec.partner_mobile
            })
            user_id = self.env['res.users'].create(
                {
                    'name': rec.name,
                    'login': rec.work_email,
                    'partner_id': new_partner_id.id,
                    'project_ids': [(6, 0, rec.project_id.ids)],
                    'login_status': 'mob_first',
                    'web_login': True,
                    'user_type': 'external_employee',
                    'employee_id': rec.id,
                    'groups_id': [(6, 0, self.env.ref('base.group_portal').ids)],

                })
            rec.write({'user_id': user_id.id})
