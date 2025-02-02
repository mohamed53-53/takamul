import re
import uuid

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrAllowance(models.Model):
    _inherit = 'arch.hr.contract.allowance'

    offer_id = fields.Many2one(comodel_name='archer.recruitment.application', string='offer')
    application_id = fields.Many2one(comodel_name='hr.applicant', string='Application')

    @api.depends('rule_id')
    @api.onchange('rule_id')
    def onchange_rule_id(self):
        if self.offer_id and not self.contract_id:
            exsist_items = self.offer_id.rule_ids.rule_id
            if exsist_items:
                domain = {
                    'domain': {
                        'rule_id': [('id', 'not in', exsist_items.ids), ('struct_id', '=', self.default_struct_id.id),
                                    ('is_dynamic', '=', True)]}}
                return domain

    @api.depends('value_type', 'contract_id', 'value')
    @api.onchange('value_type', 'contract_id', 'value')
    def compute_total_value(self):
        for rec in self:
            if rec.value_type == 'amount':
                rec.total_value = rec.value
            elif rec.value_type == 'percent':
                if rec.contract_id and rec.contract_id.basic_sal:
                    rec.total_value = rec.value * rec.contract_id.basic_sal / 100
                elif rec.offer_id and not rec.contract_id and rec.offer_id.basic_sal:
                    rec.total_value = rec.value * rec.offer_id.basic_sal / 100
                elif rec.application_id and not rec.contract_id and rec.application_id.basic_sal:
                    rec.total_value = rec.value * rec.application_id.basic_sal / 100
                elif not rec.contract_id and rec.filtered(
                        lambda m: m.rule_id.code == 'BASIC' and not m.contract_id and m.date == rec.date):
                    rec.total_value = rec.value * rec.filtered(lambda
                                                                   m: m.rule_id.code == 'BASIC' and not m.contract_id and m.date == rec.date).total_value / 100
                else:
                    rec.total_value = rec.value * rec.contract_id.wage / 100
            else:
                rec.total_value = 0


class HrEmployeeDocument(models.Model):
    _inherit = 'hr.employee.document'
    offer_id = fields.Many2one(comodel_name='archer.recruitment.application', string='Offer')
    application_id = fields.Many2one(comodel_name='hr.applicant', string='Application')


class RecruitmentApplication(models.Model):
    _name = 'archer.recruitment.application'
    _rec_name = 'sequence'

    company_id = fields.Many2one(comodel_name='res.company', readonly=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name='res.currency', related='company_id.currency_id')
    project_id = fields.Many2one(comodel_name='project.project', string='Project',
                                 domain=[('project_state', '=', 'active')], required=1)
    apply_grade = fields.Boolean(string='Apply Grade Constrain', related='project_id.apply_grade')

    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer", related='project_id.partner_id')
    owner_id = fields.Many2one(comodel_name='res.partner', string="Project Owner", related='project_id.owner_id')
    user_id = fields.Many2one(comodel_name='res.users', string="Project Manager", related='project_id.user_id')

    applicant_ar_name = fields.Char(string='Applicant Arabic Name')
    applicant_en_name = fields.Char(string='Applicant English Name', required=True)
    applicant_email = fields.Char(string='Applicant Email', required=True)
    applicant_mobile = fields.Char(string='Applicant Mobile', required=True)
    applicant_country_id = fields.Many2one(comodel_name='res.country', string='Applicant Country', required=True)
    job_id = fields.Many2one(comodel_name='hr.job', string='Applicant Job')
    date_start = fields.Date(string='Start Date', default=fields.Date.today())
    date_end = fields.Date(string='End Date')
    contract_duration = fields.Integer(string='Contract Duration/Months')
    date_expiry = fields.Date(string='Expiration Date')
    notes = fields.Html(string='Notes')
    civil_id = fields.Char(string="Civil iD")
    grade_id = fields.Many2one('hr.grade', string="Grade")
    salary_constraint_ids = fields.Many2many(comodel_name="salary.constraint", readonly=True, store=True)
    structure_type_id = fields.Many2one('hr.payroll.structure.type', string="Salary Structure Type",
                                        domain="[('project_ids','in', project_id)]")
    basic_salary_min = fields.Float(string="Basic Salary Min", store=True)
    basic_salary_max = fields.Float(string="Basic Salary Max", store=True)
    salary_total = fields.Monetary(string='Salary Total', currency_field='currency_id',
                                   compute='salary_total_compute_rule')
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('sent', 'Sent To Applicant'), ('approve', 'Applicant Approve'),
                   ('reject', 'Applicant Reject'),
                   ('done', 'Done')], default='draft')
    application_token = fields.Char()
    sequence = fields.Char(string='Sequence')
    rule_ids = fields.One2many(comodel_name='arch.hr.contract.allowance', inverse_name='offer_id', string='Allowance')
    offer_documents_ids = fields.One2many(comodel_name='hr.employee.document', inverse_name='offer_id',
                                          string='Document',
                                          domain=[('used_for', 'in', ['both', 'employee'])])
    department_id = fields.Many2one(comodel_name='hr.department', string='Applicant Department')
    application_id = fields.Many2one(comodel_name='hr.applicant', string='Related Application')
    empl_type = fields.Selection(selection=[('full', 'Full Time'), ('part', 'Part Time')], default='full',
                                 required=True, string='Employee Type')
    basic_sal = fields.Float(string="", required=False)


    @api.depends('date_start','contract_duration')
    @api.onchange('date_start','contract_duration')
    def _compute_contract_duration(self):
        for rec in self:
            rec.date_end = rec.date_start + relativedelta(months=rec.contract_duration)-relativedelta(days=1)

    @api.constrains('contract_duration')
    def _constraint_contract_duration(self):
        for rec in self:
            if rec.contract_duration <= 0:
                raise ValidationError(_('Contract Duration Must be greater then zero'))
    @api.onchange("rule_ids")
    def onchange_rules(self):
        for rec in self:
            if rec.rule_ids.filtered(lambda m: m.rule_id.code == 'BASIC'):
                rec.basic_sal = rec.rule_ids.filtered(lambda m: m.rule_id.code == 'BASIC').total_value
                rec.rule_ids.compute_total_value()

    @api.constrains('rule_ids.value', 'grade_id')
    def constrain_basic_salary(self):
        for rec in self:
            if rec.grade_id and rec.apply_grade:
                for rule in rec.rule_ids:
                    if rule.rule_id.code == 'BASIC' and rule.value < rec.basic_salary_min or rule.value > rec.basic_salary_max:
                        raise ValidationError(_('Basic salary must be within project payroll policy'))

    @api.depends('structure_type_id')
    @api.onchange('structure_type_id')
    def onchange_structure_type_id(self):
        for rec in self:
            rec.rule_ids = [(0, 0, {
                'company_id': rec.company_id.id,
                'currency_id': rec.currency_id,
                'contract_id': False,
                'structure_type_id': rec.structure_type_id.id,
                'default_struct_id': rec.structure_type_id.default_struct_id.id,
                'employee_id': False,
                'rule_id': x.id,
                'value_type': 'amount'
            }) for x in rec.structure_type_id.default_struct_id.rule_ids.filtered(
                lambda r: r.is_dynamic and rec.project_id.id in r.project_ids.ids)]

    @api.depends('structure_type_id', 'rule_ids', 'rule_ids.value_type', 'rule_ids.value')
    @api.onchange('structure_type_id', 'rule_ids', 'rule_ids.value_type', 'rule_ids.value')
    def salary_total_compute_rule(self):
        for rec in self:
            basic_salary_rule = rec.rule_ids.filtered(lambda r: r.rule_id.code == 'BASIC')
            total = 0.0
            for x in rec.rule_ids:
                if x.value_type == 'amount':
                    total += x.value
                if x.value_type == 'percent':
                    total += ((x.value * basic_salary_rule.value) / 100) or 1
            rec.salary_total = total

    @api.depends('project_id')
    @api.onchange('project_id')
    def get_project_salary_constrain(self):
        for rec in self:
            rec.salary_constraint_ids = [(6, 0, rec.project_id.salary_constraint_ids.ids)]

    @api.depends('grade_id', 'project_id')
    @api.onchange('grade_id', 'project_id')
    def _compute_max_min_salary(self):
        for rec in self:
            rec.basic_salary_max = rec.salary_constraint_ids.filtered(
                lambda s: s.grade_id.id == rec.grade_id.id).basic_salary_max
            rec.basic_salary_min = rec.salary_constraint_ids.filtered(
                lambda s: s.grade_id.id == rec.grade_id.id).basic_salary_min

    @api.depends('applicant_email')
    @api.onchange('applicant_email')
    def onchange_applicant_email(self):
        if self.applicant_email:
            emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", self.applicant_email)
            if not emails:
                raise ValidationError(_('Please Enter Valid Email'))

    @api.model
    def default_get(self, fields_list):
        res = super(RecruitmentApplication, self).default_get(fields_list)
        documents = self.env['hr.document.document'].search(
            [('used_for', '!=', 'contract'), ('job_id', '=', False), ('country_id', '=', False)])
        res['offer_documents_ids'] = [(0, 0, {
            'document_id': x.id,
            'application_id': False,
            'employee_id': False,
            'contract_id': False,
            'attach': False,
            'state': 'new',
            'used_for': 'employee'
        }) for x in documents]
        return res

    @api.model
    def create(self, vals_list):
        vals_list['sequence'] = self.env['ir.sequence'].next_by_code('archer_recruitment.new_application_seq')
        res = super(RecruitmentApplication, self).create(vals_list)
        res.application_token = str(res.id) + uuid.uuid4().hex
        res.offer_documents_ids.write({'offer_id': res.id})
        return res

    def action_send_applicant_invitation(self):
        for rec in self:
            try:
                if rec.rule_ids:
                    basic_salary_rule = rec.rule_ids.filtered(lambda r: r.rule_id.code == 'BASIC')
                    if basic_salary_rule:
                        if rec.salary_total <= 0:
                            raise ValidationError(_('You Can\'t sent offer with zero salary'))
                        else:
                            mail_template = self.env.ref('archer_recruitment.mail_template_new_offer')
                            email_sent = mail_template.send_mail(rec.id, force_send=True)
                            rec.write({'state': 'sent'})
                    else:
                        raise ValidationError(_('Please Set Salary Rule Applied For Applicant'))
                else:
                    raise ValidationError(_('Please Set Salary Rule Applied For Applicant'))
            except Exception as ex:
                raise ValidationError(ex)

    def action_applicant_approve(self):
        self.application_token = False
        self.write({'state': 'approve'})

    def action_applicant_reject(self):
        self.application_token = False
        self.write({'state': 'reject'})

    def action_create_applicant_app(self):
        for rec in self:
            app = self.env['hr.applicant'].create({
                'project_id': rec.project_id.id,
                'name': rec.applicant_en_name + ' Application',
                'partner_name': rec.applicant_en_name,
                'name_ar': rec.applicant_ar_name,
                'job_id': rec.job_id.id,
                'company_id': rec.company_id.id,
                'partner_mobile': rec.applicant_mobile,
                'contract_start_date': rec.date_start,
                'contract_duration': rec.contract_duration,
                'contract_end_date': rec.date_end,
                'email_from': rec.applicant_email,
                'country_id': rec.applicant_country_id.id,
                'offer_id': rec.id,
                'grade_id': rec.grade_id.id,
                'structure_type_id': rec.structure_type_id.id,
                'salary_total': rec.salary_total,
                'department_id': rec.department_id.id,
                'from_app': True,
                'empl_type': rec.empl_type,
                'civil_id': rec.civil_id
            })
            rec.rule_ids.write({'application_id': app.id})
            rec.offer_documents_ids.write({'application_id': app.id})
            rec.write({'state': 'done', 'application_id': app.id})
