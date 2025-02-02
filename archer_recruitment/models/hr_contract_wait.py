import datetime

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrContract(models.Model):
    _inherit = 'hr.contract'

    empl_type = fields.Selection(selection=[('full', 'Full Time'), ('part', 'Part Time')], string='Employee Type')


class HrContractWait(models.Model):
    _name = 'hr.contract.wait'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    offer_id = fields.Many2one(comodel_name='archer.recruitment.application', string='Offer')
    application_id = fields.Many2one(comodel_name='hr.applicant', string='Application', required=True)
    project_id = fields.Many2one("project.project", related='application_id.project_id')
    job_id = fields.Many2one(comodel_name='hr.job', string='Offer Job', related='application_id.job_id')
    currency_id = fields.Many2one(comodel_name='res.currency', related='application_id.currency_id')
    country_id = fields.Many2one(comodel_name='res.country', string='Nationality', related='application_id.country_id')
    birthday = fields.Date(string='Date Of Birth', related='application_id.birthday')
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], related='application_id.gender')
    civil_id = fields.Char(string='Civil ID', related='application_id.civil_id')
    grade_id = fields.Many2one('hr.grade', string="Grade", related='application_id.grade_id')
    sponsor_name = fields.Char(string='Sponsor Name', related='application_id.sponsor_name')
    resid_number = fields.Char(string="Residency Number", related='application_id.resid_number')
    resid_expiration_date = fields.Date("Residency Expiration Date", related='application_id.resid_expiration_date')
    salary_total = fields.Monetary(string='Salary Total', currency_field='currency_id',
                                   related='application_id.salary_total')
    certificate = fields.Selection([('graduate', 'Graduate'),
                                    ('bachelor', 'Bachelor'),
                                    ('master', 'Master'),
                                    ('doctor', 'Doctor'),
                                    ('other', 'Other'),
                                    ], 'Certificate Level', related='application_id.certificate')
    study_field = fields.Char("Field of Study", related='application_id.study_field')
    gosi_number = fields.Char('Social Insurance Number', related='application_id.gosi_number')
    rule_ids = fields.One2many(comodel_name='arch.hr.contract.allowance', string='Allowance',
                               related='application_id.rule_ids')
    structure_type_id = fields.Many2one('hr.payroll.structure.type', string="Salary Structure Type",
                                        related='application_id.structure_type_id')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')], default='new')
    date_start = fields.Date(string='Start Date', related='offer_id.date_start' ,store=True)
    date_end = fields.Date(string='End Date', related='offer_id.date_end')
    contract_id = fields.Many2one(comodel_name='hr.contract', string='Contract')
    active = fields.Boolean(string='Active')
    empl_type = fields.Selection(selection=[('full', 'Full Time'), ('part', 'Part Time')],
                                 related='application_id.empl_type', string='Employee Type')
    work_starting_id= fields.Many2one(comodel_name='archer.work.starting', string='Work Starting')
    work_start_state = fields.Selection(related='work_starting_id.state')
    def create_employee_contract(self):
        for rec in self:
            trial_period_count = int(
                self.env['ir.config_parameter'].sudo().get_param('archer_employee_evaluation.first_evaluation_months'))
            basic_salary_rule = rec.rule_ids.filtered(lambda r: r.rule_id.code == 'BASIC')
            vals = {
                'name': '%s Contract' % rec.employee_id.name,
                'employee_id': rec.employee_id.id,
                'project_id': rec.project_id.id,
                'date_start': rec.date_start,
                'date_end': rec.date_end,
                'structure_type_id': rec.structure_type_id.id,
                'resource_calendar_id': rec.employee_id.resource_calendar_id.id,
                'job_id': rec.job_id.id,
                'wage': basic_salary_rule.value if basic_salary_rule else 0.0,
                'trial_date_end': rec.date_start or fields.Date.today() + datetime.timedelta(days=trial_period_count),
                'empl_type': rec.empl_type

            }
            contract = self.env['hr.contract'].create(vals)
            rec.rule_ids.write({'contract_id': contract.id})
            rec.write({'state': 'done'})

    def create_work_starting(self):
        return {
            'name': _('Work Starting'),
            'view_mode': 'form',
            'view_id': self.env.ref('archer_recruitment.view_archer_work_starting_form').id,

            'res_model': 'archer.work.starting',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {
                'default_pending_contract_id': self.id,
                'default_employee_id': self.employee_id.id,
            }
        }
class WorkStarting(models.Model):
    _name = 'archer.work.starting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    pending_contract_id = fields.Many2one(comodel_name='hr.contract.wait', string='Pending Contract')
    contract_id = fields.Many2one(comodel_name='hr.contract', string='Contract')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    start_date = fields.Date(string='Start Date', required=True)
    duration = fields.Integer(string='New Duration/Months', required=True)
    end_date = fields.Date(string='End Date', required=True)
    state = fields.Selection(selection=[('draft', _('Draft')), ('confirm', _('Confirm'))], default='draft')


    @api.depends('start_date','duration')
    @api.onchange('start_date','duration')
    def _compute_duration(self):
        for rec in self:
            rec.end_date = rec.start_date + relativedelta(months=rec.duration)-relativedelta(days=1)

    @api.constrains('uration')
    def _constraint_duration(self):
        for rec in self:
            if rec.duration <= 0:
                raise ValidationError(_('Duration Must be greater then zero'))
    @api.onchange('start_date')
    def onchange_start_date(self):
        for rec in self:
            if rec.start_date:
                if rec.start_date < fields.Date.today():
                    raise ValidationError(_('Start Date Must be Greater then today'))

    @api.model
    def create(self, vals_list):
        res = super(WorkStarting,self).create(vals_list)
        res.pending_contract_id.work_starting_id = res.id
        return  res

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            rec.pending_contract_id.date_start = rec.start_date
            rec.pending_contract_id.date_end = rec.end_date

