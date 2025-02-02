from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class employee_contract_renewal(models.Model):
    _name = 'employee.contract.renewal'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']

    _rec_name = 'employee_id'

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=True)
    project_id = fields.Many2one(comodel_name="project.project", string="Project", related='employee_id.project_id')
    no_of_month = fields.Integer(string="Months", required=True)
    contract_id = fields.Many2one('hr.contract', related='employee_id.contract_id')
    date_start = fields.Date('Start Date', related='contract_id.date_start')
    date_end = fields.Date('End Date', related='contract_id.date_end')
    new_date_end = fields.Date('New End Date', compute="compute_new_date_end")
    state = fields.Selection(string="State", selection=[], default='draft')

    @api.depends('date_end', 'no_of_month')
    def compute_new_date_end(self):
        for rec in self:
            if rec.date_end:
                rec.new_date_end = rec.date_end + relativedelta(months=rec.no_of_month)
            else:
                rec.new_date_end = False

    def action_approve(self):
        for rec in self:
            if rec.state == 'confirm':
                if rec.contract_id and not rec.contract_id.date_end:
                    raise ValidationError("You Cannot Renew An Open Contract!!")
                rec.contract_id.date_end = rec.new_date_end
            super(employee_contract_renewal, self).action_approve()
    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]
    def action_reject(self, reason=None):
        self.write({'state': 'rejected'})
        if reason:
            self.message_post(body=reason, subject="Reject Reason")
