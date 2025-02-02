from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HREmployee(models.Model):
    _inherit = "hr.employee"

    residency_number = fields.Char(string="Number", tracking=True)
    serial_number = fields.Char(string="Serial Number", tracking=True)
    resid_job_title = fields.Char(string="Job Title", tracking=True)
    place_of_issuance = fields.Char("Place of Issuance", tracking=True)
    issuance_date = fields.Date("Issuance Date", tracking=True)
    expiration_date = fields.Date("Expiration Date", tracking=True)
    expiration_date_in_hijri = fields.Char("Expiration Date in Hijri", tracking=True, readonly=True )
    arrival_date = fields.Date("Arrival Date", tracking=True)
    grade_id = fields.Many2one("hr.grade")
    country_code = fields.Char(related='country_id.code')
    employee_age = fields.Integer(string="Age", compute='_compute_age')
    residency_attach = fields.Binary('Residency Attach')
    employee_document = fields.One2many(comodel_name='hr.employee.document', inverse_name='employee_id', string='Document',
                                        domain=[('used_for', 'in', ['both', 'employee'])])
    done_documents_count = fields.Integer(string='Done Documents', compute='compute_document_state')
    all_documents_count = fields.Integer(string='All Documents', compute='compute_document_state')

    def action_open_plan_activity(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Boarding Plan Activity',
            'res_model': 'hr.boarding.plan.employee',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
        }

    def compute_document_state(self):
        for rec in self:
            rec.done_documents_count = rec.employee_document.filtered(lambda d: d.state == 'approve')
            rec.all_documents_count = len(rec.employee_document)

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
                rec.employee_age = False

    def get_hr_employee_document(self):

        return {
            'name': _('HR Document'),
            'res_model': 'hr.employee.document',
            'type': 'ir.actions.act_window',
            'view_mode': 'list',
            'views': [(self.env.ref('archer_hr_custom.view_hr_employee_document_tree').id, 'list')],
            'target': 'current',
            'context': {
                'default_employee_id': self.id,'default_used_for':'employee','default_state':'new',
            },
            'domain': [('id', 'in', self.employee_document.ids)]
        }


class HrContract(models.Model):
    _inherit = 'hr.contract'
    contract_document = fields.One2many(comodel_name='hr.employee.document', inverse_name='contract_id', string='Document',
                                        domain=[('used_for', 'in', ['both', 'contract'])])
    done_documents_count = fields.Integer(string='Done Documents', compute='compute_document_state')
    all_documents_count = fields.Integer(string='All Documents', compute='compute_document_state')
    def compute_document_state(self):
        for rec in self:
            rec.done_documents_count = rec.contract_document.filtered(lambda d: d.state == 'approve')
            rec.all_documents_count = len(rec.contract_document)

    def get_hr_contract_document(self):

        return {
            'name': _('HR Document'),
            'res_model': 'hr.employee.document',
            'type': 'ir.actions.act_window',
            'view_mode': 'list',
            'views': [(self.env.ref('archer_hr_custom.view_hr_contract_document_tree').id, 'list')],
            'target': 'current',
            'context': {
                'default_employee_id': self.employee_id.id,'default_contract_id': self.id,'default_used_for':'contract','default_state':'new',
            },
            'domain': [('id', 'in', self.contract_document.ids)]
        }