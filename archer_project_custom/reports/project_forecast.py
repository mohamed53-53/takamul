from odoo import models, api, fields


class ProjectForecasted(models.AbstractModel):
    _name = 'report.archer_project_custom.report_project_forcast'
    _description = "Project Forecasted"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['project.project'].browse(data['project_id'])
        current_salaries= self._get_current_salaries(docs)['current'],
        current_offers= self._get_offers(docs)['current'],
        current_provisions= self._get_provisions(docs)['current'],
        current_employee_expenses= self._get_employee_expenses(docs)['current'],
        current_logistics= self._get_logistics(docs)['current'],
        current_headhunts= self._get_headhunts(docs)['current'],
        return {
            'doc_ids': docids,
            'doc_model': 'project.project',
            'docs': docs,
            'data': data,
            'current_salaries':current_salaries,
            'current_offers':current_offers,
            'current_provisions':current_provisions,
            'current_employee_expenses':current_employee_expenses,
            'current_logistics':current_logistics,
            'current_headhunts':current_headhunts,
            'total': current_offers+current_provisions+current_employee_expenses+current_logistics+current_headhunts,
        }

    def _get_current_salaries(self, project):
        current_offers = 0.0

        return {
            'current': current_offers
        }
    def _get_offers(self, project):
        current_total = 0.0
        current_offers = self.env['archer.recruitment.application'].search([('project_id', '=', project.id), ('state', 'in', ['approve', 'done'])])
        if current_offers:
            current_total = sum(current_offers.mapped('salary_total'))

        return {
            'current': current_total
        }

    def _get_provisions(self, project):
        current_total = 0.0
        for employee in self.env['hr.employee'].search([('project_id', '=', project.id)]):
            employee_provision = self.env['monthly.eos.line'].search(
                [('employee_id', '=', employee.id), ('type', '=', 'monthly_eos'), ('date', '<=', fields.Date.today())])
            for eos in employee_provision:
                current_total += eos.amount
        return {
            'current': current_total
        }
    def _get_employee_expenses(self, project):
        current_total = 0.0
        employee_expenses = self.env['account.expense.revision'].search(
                [('project_id', '=', project.id), ('create_date', '<=', fields.Date.today())])
        if employee_expenses:
            current_total = sum(employee_expenses.mapped('amount'))

        return {
            'current': current_total
        }
    def _get_logistics(self, project):
        current_total = 0.0
        logistics = self.env['archer.logistic.request'].search([('project_id', '=', project.id)])
        if logistics:
            current_total = sum(logistics.mapped('amount'))
        return {
            'current': current_total
        }
    def _get_headhunts(self, project):
        current_total = 0.0
        headhunts = self.env['archer.headhunt.request'].search([('project_id', '=', project.id)])
        if headhunts:
            current_total = sum(headhunts.mapped('amount'))
        return {
            'current': current_total
        }
