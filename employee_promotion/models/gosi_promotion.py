from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import re


class GosiHire(models.Model):
    _name = 'gosi.promotion'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record', ]

    project_id = fields.Many2one(comodel_name='project.project', string='Project')
    name = fields.Char("Employee Name", related="employee_id.name")
    employee_id = fields.Many2one(
        'hr.employee', string='Employee', required=True, readonly=True,
        states={'draft': [('readonly', False)], },
        domain="[('project_id','=', project_id),'|', ('company_id', '=', False), ('company_id', '=', company_id),  ('active', '=', True)]")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    number = fields.Char('Social Insurance Number', size=9)
    start_date = fields.Date(string="Start Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', "Done"),
        ('cancel', "Cancel"), ], readonly=True, index=True, copy=False, default='draft', tracking=True)
    attach = fields.Binary(string='Attach')

    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    @api.model
    def _after_approval_states(self):
        return [('done', 'Done'), ('cancel', 'Cancel')]

    def _on_approve(self):
        self.write({'state': 'done'})
        contract_ids = self.employee_id.contract_ids.filtered(lambda co: co.state and co.state == 'open')
        if contract_ids:
            values = {
                'is_insured': True,
                'social_insurance_number': self.number,
                'status': 'in',
                'insurance_start_date': self.start_date,
            }
            self.employee_id.update(values)
        else:
            raise ValidationError("Please check employee have active contract or not.")

    # @api.constrains('number')
    # def _check_number(self):
    #     for rec in self:
    #         if rec.number:
    #             if re.match("^[0-9]{9}$", rec.number):
    #                 return True
    #             raise ValidationError("Please enter valid 9 digit number")

    # def action_project_change_request(self):
    #     self.write({'state': 'done'})
    #
    def action_cancel(self):
        self.write({'state': 'cancel'})
