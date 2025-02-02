from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import calendar
from datetime import date


class HrContract(models.Model):
    _inherit = 'hr.contract'
    rule_ids = fields.One2many(comodel_name='arch.hr.contract.allowance', inverse_name='contract_id', string='Allowance')
    basic_sal = fields.Float(string="",  required=False)
    
    @api.onchange("rule_ids")
    def oncchange_rules(self):
        for rec in self:
            if rec.rule_ids.filtered(lambda m: m.rule_id.code == 'BASIC'):
                rec.basic_sal = rec.rule_ids.filtered(lambda m: m.rule_id.code == 'BASIC').total_value
                rec.rule_ids.compute_total_value()

    def get_employee_rule_amount(self, employee, contract, rule, date_from, date_to):

        contract_rule = contract.rule_ids.filtered(lambda r: r.rule_id.code == rule and r.employee_id.id == employee.id)
        if contract_rule:
            if contract_rule.value_type == 'percent':
                return (contract.wage * contract_rule.value) / 100
            elif contract_rule.value_type == 'amount':
                return contract_rule.value
            else:
                return 0.0
        return 0.0


class HrAllowance(models.Model):
    _name = 'arch.hr.contract.allowance'

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
    value = fields.Float(string='Value', required=True, default=0.0)
    total_value = fields.Float(string='Value', compute="compute_total_value", store=True)
    @api.depends('value_type', 'contract_id', 'value')
    @api.onchange('value_type', 'contract_id', 'value')
    def compute_total_value(self):
        for rec in self:
            if rec.value_type == 'amount':
                rec.total_value = rec.value
            elif rec.value_type == 'percent':
                if rec.contract_id and rec.contract_id.basic_sal:
                    rec.total_value = rec.value * rec.contract_id.basic_sal / 100
                elif not rec.contract_id and rec.filtered(lambda m: m.rule_id.code == 'BASIC' and not m.contract_id and m.date == rec.date):
                    rec.total_value = rec.value * rec.filtered(lambda m: m.rule_id.code == 'BASIC' and not m.contract_id and m.date == rec.date).total_value / 100
                else:
                    rec.total_value = rec.value * rec.contract_id.wage / 100
            else:
                rec.total_value = 0

    @api.depends('value_type')
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
