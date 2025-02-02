from odoo import models, api, fields


class ProjectForecasted(models.AbstractModel):
    _name = 'report.archer_employee_request.salary_identification_report'
    _description = "Salary Identification"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['salary.identification'].browse(data['request_id'])

        return {
            'doc_ids': docids,
            'doc_model': 'project.project',
            'docs': docs,
            'data': data,
        }

