import datetime

from odoo import models, fields,_
from odoo.exceptions import ValidationError


class ProbationPeriodEvaluationWizard(models.Model):
    _name = 'hr.probation.period.evaluation.wizard'

    employee_ids = fields.Many2many(comodel_name='hr.employee', string='Employees')
    extend_period = fields.Integer(string='Period/Days')
    is_extend = fields.Boolean(string='Are You need Extend Probation Period?')

    def action_approve(self):

        for employee in self.employee_ids:
            employee.evaluation_ids = [(0, 0, {
                'employee_id': employee.id,
                'eval_state': 'approve',
                'first_evaluate_date': datetime.datetime.now().date(),
                'approve_date': datetime.datetime.now().date(),
                'contract_id': employee.contract_id.id
            })]
            employee.write({'eval_state':'approve'})

    def action_reject(self):
        for employee in self.employee_ids:
            employee.evaluation_ids = [(0, 0, {
                'employee_id': employee.id,
                'eval_state': 'reject',
                'first_evaluate_date': datetime.datetime.now().date(),
                'reject_date': datetime.datetime.now().date(),
                'contract_id': employee.contract_id.id
            })]
            employee.write({'eval_state':'reject'})

    def action_extend(self):
        for employee in self.employee_ids:
            if employee.contract_id.trial_date_end:
                employee.evaluation_ids = [(0, 0, {
                    'employee_id': employee.id,
                    'eval_state': 'extend',
                    'first_evaluate_date': datetime.datetime.now().date(),
                    'extend_date': datetime.datetime.now().date(),
                    'extend_period': self.extend_period,
                    'contract_id': employee.contract_id.id
                })]
                employee.write({'eval_state':'extend'})
                employee.contract_id.write(
                    {'trial_date_end': employee.contract_id.trial_date_end + datetime.timedelta(days=self.extend_period)})
            else:
                raise  ValidationError(_('Please set Trial Period End Date`'))

class ProbationPeriodEmployeeEvalWizard(models.Model):
    _name = 'hr.probation.period.eval.employee.wizard'

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    extend_period = fields.Integer(string='Period/Days')
    is_extend = fields.Boolean(string='Are You need Extend Probation Period?')
    eval_state = fields.Selection(selection=[('new', 'New'), ('extend', 'Extended'), ('approve', 'Approve'), ('reject', 'Reject')], default='new', string='Trial Period State')

    def action_empl_approve(self):
        self.employee_id.evaluation_ids = [(0, 0, {
            'employee_id': self.employee_id.id,
            'eval_state': 'approve',
            'first_evaluate_date': datetime.datetime.now().date(),
            'approve_date': datetime.datetime.now().date(),
            'contract_id': self.employee_id.contract_id.id
        })]
        self.employee_id.contract_id.write({'eval_state':'approve'})
        self.employee_id.write({'eval_state':'approve'})


    def action_empl_reject(self):
        self.employee_id.evaluation_ids = [(0, 0, {
            'employee_id': self.employee_id.id,
            'eval_state': 'reject',
            'first_evaluate_date': datetime.datetime.now().date(),
            'reject_date': datetime.datetime.now().date(),
            'contract_id': self.employee_id.contract_id.id
        })]
        self.employee_id.contract_id.write({'eval_state':'reject'})
        self.employee_id.write({'eval_state':'reject'})
        mail_template = self.env.ref('archer_employee_evaluation.mail_template_end_employee_eval')
        email_sent = mail_template.send_mail(self.id, force_send=True)

    def action_empl_extend(self):
        self.employee_id.evaluation_ids = [(0, 0, {
            'employee_id': self.employee_id.id,
            'eval_state': 'extend',
            'first_evaluate_date': datetime.datetime.now().date(),
            'extend_date': datetime.datetime.now().date(),
            'extend_period': self.extend_period,
            'contract_id': self.employee_id.contract_id.id
        })]
        self.employee_id.write({'eval_state':'extend'})
        self.employee_id.contract_id.write(
            {'eval_state':'extend','trial_date_end': self.employee_id.contract_id.trial_date_end + datetime.timedelta(days=self.extend_period)})
