from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import calendar
from datetime import date


class HrAllowance(models.Model):
    _inherit = 'arch.hr.contract.allowance'

    history_contract_id = fields.Many2one(comodel_name='hr.contract', string='Contract')
    promotion_id = fields.Many2one(comodel_name='arch.hr.contract.allowance.promotion', string='Promotion')
    date = fields.Date(string="Date Applied", required=True, default=fields.Date.today())
    date_history = fields.Date(string="Date Applied", required=True, default=fields.Date.today())


class Allowances(models.Model):
    _name = 'arch.hr.contract.allowance.promotion'

    company_id = fields.Many2one(comodel_name='res.company', readonly=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name='res.currency', related='company_id.currency_id')
    contract_id = fields.Many2one(comodel_name='hr.contract', string='Contract')
    structure_type_id = fields.Many2one(comodel_name='hr.payroll.structure.type', related='contract_id.structure_type_id')
    default_struct_id = fields.Many2one(comodel_name='hr.payroll.structure', related='structure_type_id.default_struct_id')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', related='contract_id.employee_id')
    rule_id = fields.Many2one(comodel_name='hr.salary.rule', required=True,
                              domain="[('struct_id','=',default_struct_id),('is_dynamic','=',True)]")
    rule_code = fields.Char(related='rule_id.code')
    value_type = fields.Selection(selection=[('amount', 'Amount'), ('percent', 'Percent')], required=True, default='amount')
    old_value = fields.Float(string='Value')
    total_value = fields.Float(string='Value')
    promo_id = fields.Many2one(comodel_name="employee.promotion", string="", required=False)
    new_value = fields.Float(string='New Value', required=True, default=0.0)
    new_total_value = fields.Float(string='New Total Value', compute="compute_new_total_value")

    # @api.depends('value_type', 'contract_id', 'old_value')
    # @api.onchange('value_type', 'contract_id', 'old_value')
    # def compute_total_value(self):
    #     for rec in self:
    #         if rec.value_type == 'amount':
    #             rec.total_value = rec.old_value
    #         elif rec.value_type == 'percent':
    #             if rec.contract_id and rec.contract_id.basic_sal:
    #                 rec.total_value = rec.old_value * rec.contract_id.basic_sal / 100
    #             elif not rec.contract_id and rec.filtered(lambda m: m.rule_id.code == 'BASIC' and not m.contract_id and m.date == rec.date):
    #                 rec.total_value = rec.old_value * rec.filtered(lambda m: m.rule_id.code == 'BASIC' and not m.contract_id and m.date == rec.date).total_value / 100
    #             else:
    #                 rec.total_value = rec.old_value * rec.contract_id.wage / 100
    #         else:
    #             rec.total_value = 0

    # @api.depends('value_type')
    @api.onchange('value_type')
    def validate_basic_value_type(self):
        for rec in self:
            if rec.rule_id.code == 'BASIC' and rec.value_type != 'amount':
                raise ValidationError(_('Basic salary must be amount'))


    @api.depends('rule_id')
    @api.onchange('rule_id')
    def onchange_base_rule_id(self):
        if self.contract_id:
            exsist_items = self.contract_id.rule_ids.rule_id
            if exsist_items:
                domain = {
                    'domain': {'rule_id': [('id', 'not in', exsist_items.ids), ('struct_id', '=', self.default_struct_id.id),
                                           ('is_dynamic', '=', True)]}}
                return domain

    # @api.depends('value_type', 'value')
    # @api.onchange('value_type', 'value')
    # def compute_total_value(self):
    #     for rec in self:
    #         if rec.value_type == 'amount':
    #             rec.total_value = rec.value
    #         elif rec.value_type == 'percent':
    #             if self.filtered(lambda m: m.rule_id.code == 'BASIC'):
    #                 rec.total_value = rec.value * self.filtered(lambda m: m.rule_id.code == 'BASIC').total_value / 100
    #             else:
    #                 rec.total_value = rec.value * rec.promo_id.employee_id.contract_id.wage / 100
    #         else:
    #             rec.total_value = 0

    @api.depends('value_type', 'new_value')
    @api.onchange('value_type', 'new_value')
    def compute_new_total_value(self):
        for rec in self:
            if rec.value_type == 'amount':
                rec.new_total_value = rec.new_value
            elif rec.value_type == 'percent':
                if self.filtered(lambda m: m.rule_id.code == 'BASIC'):
                    rec.new_total_value = rec.new_value * self.filtered(lambda m: m.rule_id.code == 'BASIC').new_total_value / 100
                else:
                    rec.new_total_value = 0
            else:
                rec.total_value = 0


class Promotion(models.Model):
    _name = 'employee.promotion'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=False)
    job_id = fields.Many2one(comodel_name="hr.job", string="Job Position", required=False, )
    rule_ids = fields.One2many(comodel_name='arch.hr.contract.allowance.promotion', inverse_name='promo_id',
                               string='Allowance')
    date = fields.Date(string="Date Applied", required=True, default=fields.Date.today())
    state = fields.Selection([], default='draft')

    @api.onchange('employee_id')
    # @api.depends('employee_id')
    def onchange_employee(self):
        for rec in self:
            rec.department_id = False
            rec.job_id = False
            if rec.employee_id and rec.employee_id.contract_id:
                rec.department_id = rec.employee_id.contract_id.department_id.id if rec.employee_id.contract_id.department_id else False
                rec.job_id = rec.employee_id.contract_id.job_id.id if rec.employee_id.contract_id.job_id else False
                line_vals = []
                if not rec.rule_ids:
                    for line in rec.employee_id.contract_id.rule_ids:
                        line_vals.append([0, 0, {
                            'rule_id': line.rule_id.id,
                            'value_type': line.value_type,
                            'old_value': line.value,
                            'new_value': line.value,
                        }])
                    rec.rule_ids = line_vals

    @api.model
    def create(self, vals):
        res = super(Promotion, self).create(vals)
        for rule in res.employee_id.contract_id.rule_ids:
            res.rule_ids.filtered(lambda m: m.rule_id.code == rule.rule_id.code).value_type = rule.value_type
            res.rule_ids.filtered(lambda m: m.rule_id.code == rule.rule_id.code).old_value = rule.value
            res.rule_ids.filtered(lambda m: m.rule_id.code == rule.rule_id.code).total_value = rule.total_value
        return res

    def write(self, vals):
        res = super(Promotion, self).write(vals)
        for rule in self.employee_id.contract_id.rule_ids:
            if not self.rule_ids.filtered(lambda m: m.rule_id.code == rule.rule_id.code).value_type:
                self.rule_ids.filtered(lambda m: m.rule_id.code == rule.rule_id.code).value_type = rule.value_type
            if not self.rule_ids.filtered(lambda m: m.rule_id.code == rule.rule_id.code).old_value:
                self.rule_ids.filtered(lambda m: m.rule_id.code == rule.rule_id.code).old_value = rule.value
            if not self.rule_ids.filtered(lambda m: m.rule_id.code == rule.rule_id.code).total_value:
                self.rule_ids.filtered(lambda m: m.rule_id.code == rule.rule_id.code).total_value = rule.total_value
        return res

    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]
    def action_reject(self, reason=None):
        self.write({'state': 'rejected'})
        if reason:
            self.message_post(body=reason, subject="Reject Reason")

    def action_approve(self):
        for rec in self:
            if rec.state == 'confirm':
                line_vals = []
                for line in rec.employee_id.contract_id.rule_ids:
                    line.history_contract_id = line.contract_id.id
                    line.contract_id = False
                    line.date_history = rec.date
                for rule in rec.rule_ids:
                    if rule.rule_id.code == 'BASIC':
                        rec.employee_id.contract_id.basic_sal = rule.total_value
                    line_vals.append([0, 0, {
                        'rule_id': rule.rule_id.id,
                        'value_type': rule.value_type,
                        'promotion_id': rule.id,
                        'value': rule.new_value,
                        'date': rec.date,
                    }])
                if line_vals:
                    rec.employee_id.contract_id.rule_ids = line_vals
                    rec.employee_id.contract_id.department_id = rec.department_id.id
                    rec.employee_id.contract_id.job_id = rec.job_id.id
                self.env['gosi.promotion'].create({
                    'project_id': rec.employee_id.project_id.id,
                    'employee_id': rec.employee_id.id,
                    'company_id': rec.employee_id.company_id.id,
                    # 'number': rec.employee_id.gosi_number,
                    'start_date': rec.date,
                    'state': 'draft',
                })
            super(Promotion, self).action_approve()


class HrContract(models.Model):
    _inherit = 'hr.contract'

    history_rule_ids = fields.One2many(comodel_name='arch.hr.contract.allowance', inverse_name='history_contract_id',
                                       string='Allowance')
    previous_days_check = fields.Boolean()
    previous_days_int = fields.Float()

    def get_employee_rule_amount(self, employee, contract, rule, date_from, date_to):
        contract_rule = contract.rule_ids.filtered(lambda r: r.rule_id.code == rule and r.employee_id.id == employee.id)
        employee_eos = self.env['hr.employee.eos'].search([('employee_id', '=', self.employee_id.id),
                                                           ('state', '=', 'approved'), ('contract_id', '=', self.id),
                                                           ('date_of_leave', '>', date_from),
                                                           ('date_of_leave', '<', date_to)], limit=1)
        if employee_eos:
            date_to = employee_eos.date_of_leave
        if contract_rule:
            percent = 1
            if date_from and date_to:
                last_day_in_month = date_from.replace(
                    day=calendar.monthrange(date_from.year, date_from.month)[1])
                if date_from <= contract_rule.date <= date_to:
                    percent = ((date_to - contract_rule.date).days + 1) / int(last_day_in_month.day)
                elif date_to < last_day_in_month:
                    percent = ((date_to - date_from).days + 1) / int(last_day_in_month.day)
                if percent == 1:
                    total_value = contract_rule.total_value
                    if contract.date_start < date_from:
                        last_payslips = self.env['hr.payslip'].search([('employee_id', '=', employee.id),
                                                                       ('date_from', '!=', date_from),
                                                                       ('date_to', '!=', date_to),
                                                                       ('state', '!=', 'cancel')])
                        if not last_payslips:
                            last_day_in_month = contract.date_start.replace(
                                day=calendar.monthrange(contract.date_start.year, contract.date_start.month)[1])
                            last_month_percent = ((last_day_in_month - contract.date_start).days + 1) / int(
                                last_day_in_month.day)
                            contract.previous_days_check = True
                            contract.previous_days_int = last_month_percent * sum(rule.total_value for rule in contract.rule_ids)
                            total_value += contract_rule.total_value * last_month_percent
                        else:
                            contract.previous_days_check = False
                            contract.previous_days_int = 0
                    return total_value
                elif percent < 1:
                    total_value = contract_rule.total_value * percent
                    contract.previous_days_check = False
                    contract.previous_days_int = 0
                    if date_to < last_day_in_month:
                        return total_value
                    history_contract_rule = contract.history_rule_ids.filtered(
                        lambda r: r.rule_id.id in rule and r.date_history == contract_rule.date)
                    total_value += (history_contract_rule.total_value * (1 - percent))
                    return total_value
                else:
                    return 0.0
            else:
                if contract_rule.value_type == 'percent':
                    return (contract.wage * contract_rule.value) / 100
                elif contract_rule.value_type == 'amount':
                    return contract_rule.value
                else:
                    return 0.0
        return 0.0


class Payslip(models.Model):
    _inherit = 'hr.payslip'

    promo_note = fields.Many2one('employee.promotion', string="Promotion Note", compute="compute_promo_note")

    def compute_promo_note(self):
        for rec in self:
            rec.promo_note = False
            if rec.contract_id:
                for rule in rec.contract_id.rule_ids:
                    if rec.date_from <= rule.date <= rec.date_to and rule.promotion_id:
                        rec.promo_note = rule.promotion_id.promo_id.id
