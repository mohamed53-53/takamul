""" Initialize Hr Payroll """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    penalty_amount = fields.Float(compute='_compute_penalty_amount',store=1)
    penalty_ids = fields.Many2many('employee.penalty')
    utility_deduction_amount = fields.Float(compute='_compute_utility_deduction_amount', store=1,
                                         string="Utility Deduction")
    utility_deduction_ids = fields.Many2many(comodel_name='employee.deduction',relation='utility_deduction_rel', string="Utility Deduction",
                                             compute="_compute_employee_utility",store=True)
    other_deduction_amount = fields.Float(compute='_compute_other_deduction_amount', store=1, string="Other Deduction")
    other_deduction_ids = fields.Many2many(comodel_name='employee.deduction', relation='other_deduction_rel', string="Other",
                                           compute="_compute_employee_other_deduction",store=True)

    @api.depends('penalty_ids')
    def _compute_penalty_amount(self):
        """ Compute penalty_amount value """
        for rec in self:
            total = 0
            for pen in rec.penalty_ids:
                total += pen.penalty_amount
            rec.penalty_amount = total

    @api.depends('utility_deduction_ids')
    def _compute_utility_deduction_amount(self):
        for rec in self:
            total = 0
            for bon in rec.utility_deduction_ids:
                total += bon.deduction_amount
            rec.utility_deduction_amount = total

    @api.depends('other_deduction_ids')
    def _compute_other_deduction_amount(self):
        for rec in self:
            total = 0
            for bon in rec.other_deduction_ids:
                total += bon.deduction_amount
            rec.other_deduction_amount = total

    @api.onchange('employee_id','date_from','date_to')
    def _onchange_employee(self):
        employee = self.employee_id
        date_from = self.date_from
        date_to = self.date_to
        if employee and date_from and date_to:
            penalties = employee.penalty_ids.filtered(
                lambda l: not l.deducted and date_from <= l.date <= date_to and l.state == 'approve')
            self.penalty_ids = penalties.ids
            utilities = employee.utility_deduction_ids.filtered(
                lambda l: not l.deducted and date_from <= l.date <= date_to and l.state == 'approve')
            self.utility_deduction_ids = utilities.ids
            other_deduction = employee.other_deduction_ids.filtered(
                lambda l: not l.deducted and date_from <= l.date <= date_to and l.state == 'approve')
            self.other_deduction_ids = other_deduction.ids

    @api.depends('employee_id','date_from','date_to')
    def _compute_employee_utility(self):
        for rec in self:
            employee = rec.employee_id
            date_from = rec.date_from
            date_to = rec.date_to
            if employee and date_from and date_to:
                utilities = employee.utility_deduction_ids.filtered(
                    lambda l: not l.deducted and date_from <= l.date <= date_to and l.state == 'approve')
                rec.utility_deduction_ids = utilities.ids

    @api.depends('employee_id','date_from','date_to')
    def _compute_employee_other_deduction(self):
        for rec in self:
            employee = rec.employee_id
            date_from = rec.date_from
            date_to = rec.date_to
            if employee and date_from and date_to:
                other_deduction = employee.other_deduction_ids.filtered(
                    lambda l: not l.deducted and date_from <= l.date <= date_to and l.state == 'approve')
                rec.other_deduction_ids = other_deduction.ids

    def action_payslip_done(self):
        for rec in self:
            for pen in rec.penalty_ids:
                pen.deducted = True
            for pen in rec.utility_deduction_ids:
                pen.deducted = True
            for pen in rec.other_deduction_ids:
                pen.deducted = True
            super(HrPayslip, rec).action_payslip_done()
