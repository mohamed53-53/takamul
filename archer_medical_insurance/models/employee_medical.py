from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    med_insurance_id = fields.One2many(comodel_name='archer.medical.employee', inverse_name='employee_id')
    med_insurance_count = fields.Integer(compute='count_employee_medical')

    def count_employee_medical(self):
        for rec in self:
            rec.med_insurance_count = len(rec.med_insurance_id)

    def get_employee_medical(self):
        return {
            'name': _('Medical Insurance'),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'archer.medical.employee',
            'target': 'current',
            'domain': [('id', 'in', self.med_insurance_id.ids)],
            'context': {
                'default_employee_id': self.id,
                'delete': False,
                'group_by':'ins_for'
            },
        }


class EmployeeMedical(models.Model):
    _name = 'archer.medical.employee'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']

    name = fields.Char(string='Name', default="/")
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    provider_id = fields.Many2one(comodel_name='res.partner', string='Provider', domain=[('is_med_ins_comp', '=', True)])
    ins_for = fields.Selection(selection=[
        ('employee', 'Employee'),
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('spouse', 'Spouse'),
        ('child', 'Child'),
    ], required=True)
    family_id = fields.Many2one(comodel_name='hr.employee.relative', domain="[('employee_id','=',employee_id),('relation','=',ins_for)]")
    license_no = fields.Char(string='License Number')
    med_group_id = fields.Many2one(comodel_name='archer.medical.group', string='Medical Group', domain="[('provider_id','=',provider_id)]")
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    status = fields.Selection(selection=[], string='Status')

    @api.model
    def create(self, vals_list):
        vals_list['name'] = self.env['ir.sequence'].next_by_code('archer_medical_insurance.medical_insurance_seq') or _('/')
        return super(EmployeeMedical, self).create(vals_list)
    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    def action_reject(self, reason=None):
        self.write({'state': 'rejected'})
        if reason:
            self.message_post(body=reason, subject="Reject Reason")

    # def action_approve(self):
    #     for rec in self:
