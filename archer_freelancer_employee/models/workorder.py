import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FreelanceApplication(models.Model):
    _name = 'archer.freelance.workorder'
    _rec_name = 'sequence'
    _description = 'Freelancer Workorder'

    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']

    sequence = fields.Char(string='Sequence')
    project_id = fields.Many2one(comodel_name='project.project', string='Project', required=True)
    freelancer_id = fields.Many2one(comodel_name='res.partner', string='Freelancer', domain="[('project_id','=',project_id),('is_freelance','=',True)]", required=True)
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    description = fields.Text(string='Description', required=True)
    amount = fields.Float(string='Amount', required=True)
    expense_id =  fields.Many2one(comodel_name='account.expense.revision', string='Related Expense')
    state = fields
    account_move_id = fields.Many2one(comodel_name='account.move', string='Entry')

    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    def action_reject(self, reason=None):
        self.write({'state': 'rejected'})
        if reason:
            self.message_post(body=reason, subject="Reject Reason")

    def action_approve(self):
        for rec in self:
            accrued_expense_account_id = self.env['ir.config_parameter'].sudo().get_param('archer_project_custom.accrued_expense_account_id')
            accrued_expense_journal_id = self.env['ir.config_parameter'].sudo().get_param('archer_project_custom.accrued_expense_journal_id')
            if not accrued_expense_account_id:
                raise ValidationError(_('Please Check Accrued Expense Account'))
            if not accrued_expense_journal_id:
                raise ValidationError(_('Please Check Accrued Expense Journal'))
            else:
                if accrued_expense_account_id:
                    vals = {
                        'origin_model': rec._name,
                        'origin_id': rec.id,
                        'reference': rec.sequence if rec.sequence else False,
                        'project_id': rec.project_id.id,
                        'accrued_expense_journal_id': int(accrued_expense_journal_id),
                        'accrued_expense_account_id': int(accrued_expense_account_id),
                        'amount': rec.amount,
                        'state': 'draft',
                        'partner_id':rec.freelancer_idid
                    }
                    expense = self.env['account.expense.revision'].create(vals)
                    rec.expense_id = expense.id
            return  super().action_approve()
    @api.model
    def create(self, vals_list):
        vals_list['sequence'] = self.env['ir.sequence'].next_by_code('archer_freelancer_employee.archer_freelance_workorder_seq') or '/'
        return super(FreelanceApplication, self).create(vals_list)
