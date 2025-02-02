from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    arabic_name = fields.Char(string='Arabic Name')
    gender = fields.Selection([
        ('male', _('Male')),
        ('female', _('Female')),
    ], groups="hr.group_hr_user", tracking=True)
    religion = fields.Selection([
        ('muslim', _('Muslim')),
        ('not_muslim', _("Not Muslim"))], "Religion")
    national_address = fields.Char(string='National Address')
    national_address_attach = fields.Binary(string='National Address Attach')
    relative_ids = fields.One2many(comodel_name='hr.employee.relative', string='Relative', inverse_name='employee_id')
    graduate_date = fields.Date(string='Graduation Date')
    experience_ids = fields.One2many(comodel_name='hr.employee.experience', string='Experience', inverse_name='employee_id')
    certificate_ids = fields.One2many(comodel_name='hr.employee.certificate', string='Certificate', inverse_name='employee_id')
    sponsor_name = fields.Char(string='Name')
    sponsor_phone = fields.Char(string='Phone')
    sponsor_address = fields.Text(string='Address')
    bank_country_id = fields.Many2one(comodel_name='res.country', string='Country')
    international_bank = fields.Boolean("International Bank")
    branch_name_code = fields.Char("Branch Name/Code")
    bank_name = fields.Char(string='Bank Name')
    iban_no = fields.Char(string='IBAN Number')
    beneficiary_name = fields.Char(string='Beneficiary Name')
    swift_code = fields.Char(string='Swift Code')
    is_locked = fields.Boolean("Is Locked")
    bank_id = fields.Many2one("bank.bank", string="Bank Name")
    certificate_attach = fields.Binary(string='Certificate Attach')
    flight_ticket = fields.Float(string='Flight Ticket')
    empl_type = fields.Selection(selection=[('full', _('Full Time')), ('part', _('Part Time'))], default='full',required=True, string='Employee Type')
    empl_no = fields.Char(string='Employee Number')
    @api.depends('relative_ids')
    @api.onchange('relative_ids')
    def check_exist_product_in_line(self):
        for employee in self:
            exist_product_list = []
            for line in employee.relative_ids:
                if line.relation and line.gender:
                    if line.relation == 'spouse' and line.gender == 'male':
                        if (line.relation, line.gender) in exist_product_list:
                            raise ValidationError(_('This relation can\'t repeated'))
                        exist_product_list.append((line.relation, line.gender))

    @api.depends('relative_ids')
    @api.onchange('relative_ids')
    def onchange_relative_ids_birthdate(self):
        for employee in self:
            for line in employee.relative_ids:
                if line.relation == 'spouse':
                    age = relativedelta(datetime.today(), line.birthdate).years
                    if age < 18:
                        line.birthdate = False
                        raise ValidationError(_('select correct spouse date of birth  '))

    @api.depends('iban_no')
    @api.onchange('iban_no')
    def onchange_iban_no(self):
        if not self.international_bank:
            if self.iban_no and not self.iban_no[:2] == 'SA':
                raise ValidationError(_('IBAN must start with SA'))
        if self.international_bank:
            if not len(self.iban_no) >= 34:
                raise ValidationError(_('International IBAN must be 34 characters or more'))

    @api.depends('job_id')
    def _compute_job_title(self):
        for employee in self:
            employee.job_title = employee.job_id.name

    @api.model
    def create(self, vals_list):
        vals_list['empl_no'] = self.env['ir.sequence'].next_by_code('archer_base_hr.create_employee_seq') or '/'
        res = super(HrEmployee, self).create(vals_list)
        return res

    def unlink(self):
        current_sequence = self.env['ir.sequence'].search([('code','=','archer_base_hr.create_employee_seq')])
        current_sequence.number_next_actual -= 1
        return super(HrEmployee, self).unlink()
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', ('name', operator, name), ('identification_id', operator, name), ('empl_no', operator, name),]
        return self._search(domain + args,  limit=limit)

    def create_user_employee(self):
        for rec in self:
            new_partner_id = self.env['res.partner'].create({
                'is_company': False,
                'type': 'private',
                'name': rec.partner_name,
                'email': rec.email_from,
                'phone': rec.partner_phone,
                'mobile': rec.partner_mobile
            })
            address_id = new_partner_id.address_get(['contact'])['contact']
            user_id = self.env['res.users'].create(
                {
                    'name': new_partner_id.name,
                    'login': new_partner_id.email,
                    'partner_id': new_partner_id.id,
                    'project_id': rec.project_id.id,
                    'login_status': 'mob_first',
                    'web_login': True,
                    'user_type': 'external_employee',
                    'employee_id': rec.id,
                    'groups_id': [(6, 0, self.env.ref('base.group_portal').ids)],

                })
            rec.write({'user_id': user_id.id})

    def disable_employee_user(self):
        for rec in self:
            rec.user_id.write({'active':False})
class HrEmployeeRelative(models.Model):
    _name = 'hr.employee.relative'
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    name = fields.Char(string='Name', required=True)
    id_number = fields.Char(string='ID Number')
    birthdate = fields.Date(string='Date Of Birth')
    relation = fields.Selection(selection=[('spouse', _('Spouse')), ('child', _('Child')), ('father', _('Father')), ('mother', _('Mother'))],
                                string='Relation', required=True)
    gender = fields.Selection([
        ('male', _('Male')),
        ('female', _('Female'))
    ], tracking=True, required=True)
    phone = fields.Char("Phone")
    attach = fields.Binary(string='Attach')


class HrEmployeeExperience(models.Model):
    _name = 'hr.employee.experience'

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    job_name = fields.Char(string='Job Name', required=True)
    employer_name = fields.Char(string='Employer', required=True)
    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
    service_certificate = fields.Binary(string='Certificate File', attachment=True)

    @api.depends('date_from', 'date_to')
    def onchange_dates(self):
        for rec in self:
            if rec.date_from or self.date_from > self.date_to or self.date_to > datetime.today():
                raise ValidationError(_('Please set correct period'))


class HrEmployeeCertificate(models.Model):
    _name = 'hr.employee.certificate'

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    certificate_name = fields.Char(string='Certificate Name', required=True)
    certificate_date = fields.Date(string='Certificate Date')
    certificate_issuer = fields.Date(string='Certificate Issuer')
    certificate_attach = fields.Binary(string='Certificate File', attachment=True)
