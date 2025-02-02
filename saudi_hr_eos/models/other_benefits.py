from odoo import models, fields, api, _


class EOSOtherBenefits(models.Model):
    _name = 'eos.other.benefits'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    account_id = fields.Many2one("account.account", string="Accounts", required=True)


class EmployeeOtherBenefits(models.Model):
    _name = 'employee.eos.other.benefits'
    _rec_name = 'benefit_id'

    benefit_id = fields.Many2one(comodel_name="eos.other.benefits", string="Name", required=True)
    account_id = fields.Many2one("account.account", string="Accounts", related="benefit_id.account_id")
    amount = fields.Float(string="Amount",  required=True)
    description = fields.Char(string="Description", required=False)
    eos_id = fields.Many2one(comodel_name="hr.employee.eos", string="EOS", required=False)
    employee_id = fields.Many2one('hr.employee', "Employee", related="eos_id.employee_id")

