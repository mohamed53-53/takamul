from odoo import models, fields


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    expense_type = fields.Selection(
        [
            ("board_of_directors", "Bord of Directors"),
            ("business_trip", "Business Trip"),
            ("personal_vacation", "Personal Vacation"),
            ("travel_tickets", "Travel Tickets"),
            ("secondments", "Secondments"),
            ("direct_payment", "Direct Payment"),
            ("others", "Others"),
        ],
        string="Expense Type"
    )
    project_id = fields.Many2one("project.project")
    approver_name = fields.Char(string="Approver Name")
    approval_date = fields.Date(string="Approval Date")
