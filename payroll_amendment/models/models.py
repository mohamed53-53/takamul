from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class HrStructureRule(models.Model):
    _inherit = 'hr.salary.rule'

    is_amendment = fields.Boolean(string='Amendment Rule')

    @api.depends('is_amendment')
    @api.onchange('is_amendment')
    def onchange_is_amendment(self):
        if self.is_dynamic:
            raise ValidationError("You Can Not Apply Amendment on A Dynamic Rule!!")
        if self.is_amendment and self.code:
            self.amount_select = 'code'
            self.condition_select = 'python'
            self.condition_python = 'result = employee.get_amendment_rule_amount(employee, contract,{rule}, payslip.date_from, payslip.date_to)'.format(
                rule=self.ids)
            self.amount_python_compute = 'result = employee.get_amendment_rule_amount(employee, contract,{rule}, payslip.date_from, payslip.date_to)'.format(
                rule=self.ids)
        elif self.is_amendment and not self.code:
            self.is_amendment = False
            return {'warning': {'message': _('Please Set Code First')}}
        else:
            self.amount_select = 'fix'
            self.amount_python_compute = False


class PayrollAmendment(models.Model):
    _name = 'payroll.amendment'
    _inherit = ['mail.thread']

    def _get_year_selection(self):
        """Return the list of values of current year."""
        years = []
        for seq in range(datetime.now().year - 1, datetime.now().year + 6):
            years.append((str(seq), str(seq)))
        return years

    state = fields.Selection(string="State", selection=[('draft', 'Draft'), ('confirm', 'Confirmed')], required=True,
                             default='draft')
    month = fields.Selection([('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'),
                              ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'),
                              ('11', 'November'), ('12', 'December')], string="Month", readonly=True,
                             states={'draft': [('readonly', False)]}, default=str(datetime.now().month))
    year = fields.Selection(_get_year_selection, readonly=True, states={'draft': [('readonly', False)]},
                            default=lambda self: str(datetime.now().year))
    name = fields.Char(readonly=True, states={'draft': [('readonly', False)]})
    rule_id = fields.Many2one(comodel_name="hr.salary.rule", string="Salary Rule", required=False, readonly=True,
                              states={'draft': [('readonly', False)]})
    amount = fields.Float('Amount', readonly=True, states={'draft': [('readonly', False)]})
    type = fields.Selection(string="Type", selection=[('allow', 'Allowance'), ('ded', 'Deduction')], default="allow",
                            required=True, readonly=True, states={'draft': [('readonly', False)]})
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today, readonly=True,
                       states={'draft': [('readonly', False)]})
    employee_ids = fields.Many2many(comodel_name="hr.employee", relation="payroll_amendment_employee_rel",
                                    column1="amendment_id", column2="employee_id", string="Employees", readonly=True,
                                    states={'draft': [('readonly', False)]})

    @api.onchange('month', 'year')
    @api.depends('month', 'year')
    def _calculate_period(self):
        date = datetime.now().date().replace(month=int(self.month), year=(int(self.year)), day=1)
        self.date = date

    def action_confirm(self):
        for rec in self.employee_ids:
            payslips = self.env['hr.payslip'].search([('state', '=', 'draft'), ('employee_id', '=', rec.id),
                                                      ('month', '=', self.month), ('year', '=', self.year)])
            if not payslips:
                raise ValidationError("Employee %s has no payslip for this month!" % rec.name)
            rec.amendment_ids = [
                [0, 0, {'name': self.name, 'rule_id': self.rule_id.id, 'date': self.date,
                        'amount': self.amount if self.type == 'allow' else -self.amount}]]
        self.state = 'confirm'


class HrEmployeeAmendment(models.Model):
    _name = 'hr.employee.amendment'

    name = fields.Char(string="Name", required=False)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=True)
    rule_id = fields.Many2one(comodel_name="hr.salary.rule", string="Salary Rule", required=False)
    amount = fields.Float('Amount')
    date = fields.Date(string="Date", required=True)


class Employee(models.Model):
    _inherit = 'hr.employee'

    amendment_ids = fields.One2many(comodel_name="hr.employee.amendment", inverse_name="employee_id")

    def get_amendment_rule_amount(self, employee, contract, rule, date_from, date_to):
        employee_rules = employee.amendment_ids.filtered(
            lambda r: r.rule_id.id in rule and r.employee_id.id == employee.id)
        amount = 0
        for employee_rule in employee_rules:
            if employee_rule.amount and date_from <= employee_rule.date <= date_to:
                amount += employee_rule.amount
        return amount


class Contract(models.Model):
    _inherit = 'hr.contract'

    amendment_ids = fields.One2many(comodel_name="hr.employee.amendment", related='employee_id.amendment_ids')
