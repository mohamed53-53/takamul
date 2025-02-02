import datetime

from odoo import models, fields, _, api


class HrContract(models.Model):
    _inherit = 'hr.contract'
    evaluation_ids = fields.One2many(comodel_name='hr.probation.period.evaluation', inverse_name='contract_id', string='Evaluations')
    eval_state = fields.Selection(selection=[('new', 'New'), ('extend', 'Extended'), ('approve', 'Approve'), ('reject', 'Reject')],
                                  default='new', string='Trial Period State')

    def open_evalation_wizard(self):

        return {
            'name': _('Set Employee Evaluation'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.probation.period.eval.employee.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('archer_employee_evaluation.view_hr_probation_period_empl_evaluation_wizard').id,
            'target': 'new',
            'context': {
                'default_employee_id': self.employee_id.id,
                'default_eval_state': self.eval_state
            },
        }

    def send_eval_email_po(self):
        for rec in self.env['hr.contract'].search([('state', '=', 'open')]):
            if datetime.datetime.now().date() == rec.trial_date_end and rec.state == 'draft':
                eval = self.env['hr.probation.period.evaluation'].create({
                    'employee_id': rec.employee_id.id,
                    'eval_state': False,
                    'first_evaluate_date': False,
                    'extend_date': False,
                    'extend_period': 0,
                    'contract_id': rec.employee_id.contract_id.id
                })
                self.env.ref('archer_employee_evaluation.mail_template_employee_eval').with_context(**{
                    'email_from': rec.create_uid.email_formatted or self.env.user.email_formatted,
                    'email_to': rec.employee_id.project_id.owner_id.email,
                    'subject': rec.employee_id.project_id.name + ' Evaluation',
                    'project_owner': rec.employee_id.project_id.owner_id.name,
                    'employee_name': rec.employee_id.name,
                    'project_name': rec.employee_id.project_id.name,
                    'eval_state': rec.employee_id.contract_id.eval_state,
                }).send_mail(eval.id,force_send=True)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    evaluation_ids = fields.One2many(comodel_name='hr.probation.period.evaluation', inverse_name='employee_id', string='Evaluations')
    eval_state = fields.Selection(selection=[('new', 'New'), ('extend', 'Extended'), ('approve', 'Approve'), ('reject', 'Reject')],
                                  default='new', string='Trial Period State')

    def open_evalation_wizard(self):
        return {
            'name': _('Set Employee Evaluation'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.probation.period.eval.employee.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('archer_employee_evaluation.view_hr_probation_period_empl_evaluation_wizard').id,
            'target': 'new',
            'context': {
                'default_employee_id': self.id
            },
        }


class ProbationPeriodEvaluation(models.Model):
    _name = 'hr.probation.period.evaluation'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    eval_state = fields.Selection(selection=[('new', 'New'), ('extend', 'Extended'), ('approve', 'Approve'), ('reject', 'Reject')], string='Trial Period State')
    first_evaluate_date = fields.Date(string='First Evaluate Date')
    second_evaluate_date = fields.Date(string='Second Evaluate Date')
    approve_date = fields.Date(string='Approve Date')
    reject_date = fields.Date(string='Reject Date')
    extend_date = fields.Date(string='Extend')
    state = fields.Selection([])
    extend_period = fields.Integer(string='Period/Month')
    contract_id = fields.Many2one(comodel_name='hr.contract', string='Contract')
    eval_action_state = fields.Selection(selection=[('extend', 'Extended'), ('approve', 'Approve'), ('reject', 'Reject')])

    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    def action_reject(self, reason=None):
        self.write({'state': 'rejected'})
        if reason:
            self.message_post(body=reason, subject="Reject Reason")

    def action_approve(self):
        for rec in self:
            if rec.state == 'approve':
                if rec.eval_action_state == 'extend':
                    rec.employee_id.write({'eval_state': 'extend'})
                    rec.employee_id.contract_id.write(
                        {'trial_date_end': rec.employee_id.contract_id.trial_date_end + datetime.timedelta(days=rec.extend_period)})
                if rec.eval_action_state == 'approve':
                    rec.employee_id.write({'eval_state': 'approve'})
                if rec.eval_action_state == 'reject':
                    rec.employee_id.write({'eval_state': 'reject'})
                return super(ProbationPeriodEvaluation, self).action_approve()
            else:

                return super(ProbationPeriodEvaluation, self).action_approve()
