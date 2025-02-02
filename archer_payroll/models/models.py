import binascii
import tempfile

import xlrd

from odoo import models, fields, api, _
from collections import defaultdict
from markupsafe import Markup
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero, plaintext2html
import calendar


class Payslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_cancel(self):
        if not self.env.user._is_system() and self.filtered(lambda slip: slip.state == 'done'):
            raise UserError(_("Cannot cancel a payslip that is done."))
        self.write({'state': 'cancel'})
        if self.payslip_run_id:
            self.mapped('payslip_run_id').action_close()

    def _check_same_period_slip(self):
        payslips = self.search([('employee_id', '=', self.employee_id.id), ('month', '=', self.month),
                                ('year', '=', self.year), ('id', '!=', self.id)])
        if payslips:
            raise ValidationError(_('You can not create two payslips for the same employee in the same month.'))

    def create_payment(self):
        for rec in self:
            if rec.state != 'done':
                raise ValidationError(_("Can Create Payment For Done Slips Only!!!"))
            if not rec.employee_id.address_home_id:
                raise ValidationError(_("Employee must be linked with a partner"))
            if rec.employee_id.address_home_id and rec.state == 'done':
                vals = {
                    'partner_id': rec.employee_id.address_home_id.id,
                    'amount': rec.line_ids.filtered(lambda m: m.code == 'NET').total,
                    'payment_type': 'outbound',
                    'date': rec.date_to,
                    'ref': rec.name,
                }
                rec.payment_id = self.env['account.payment'].create(vals)

    def action_payslip_done(self):
        """
            Generate the accounting entries related to the selected payslips
            A move is created for each journal and for each month.
        """
        for rec in self:
            rec._action_create_account_move()
        res = super(Payslip, self).action_payslip_done()
        return res

    def _action_create_account_move(self):
        precision = self.env['decimal.precision'].precision_get('Payroll')

        # Add payslip without run
        payslips_to_post = self.filtered(lambda slip: not slip.payslip_run_id)

        # Adding pay slips from a batch and deleting pay slips with a batch that is not ready for validation.
        payslip_runs = (self - payslips_to_post).mapped('payslip_run_id')
        for run in payslip_runs:
            if run._are_payslips_ready():
                payslips_to_post |= run.slip_ids

        # A payslip need to have a done state and not an accounting move.
        payslips_to_post = payslips_to_post.filtered(lambda slip: slip.state == 'done' and not slip.move_id)

        # Check that a journal exists on all the structures
        if any(not payslip.struct_id for payslip in payslips_to_post):
            raise ValidationError(_('One of the contract for these payslips has no structure type.'))
        if any(not structure.journal_id for structure in payslips_to_post.mapped('struct_id')):
            raise ValidationError(_('One of the payroll structures has no account journal defined on it.'))

        # Map all payslips by structure journal and pay slips month.
        # {'journal_id': {'month': [slip_ids]}}
        slip_mapped_data = defaultdict(lambda: defaultdict(lambda: self.env['hr.payslip']))
        for slip in payslips_to_post:
            slip_mapped_data[slip.employee_id.id] = defaultdict(lambda: defaultdict(lambda: self.env['hr.payslip']))
            slip_mapped_data[slip.employee_id.id][slip.struct_id.journal_id.id][
                fields.Date().end_of(slip.date_to, 'month')] |= slip
        for slip in payslips_to_post:
            break
        for employee in slip_mapped_data:
            for journal_id in slip_mapped_data[employee]:  # For each journal_id.
                for slip_date in slip_mapped_data[employee][journal_id]:  # For each month.
                    line_ids = []
                    debit_sum = 0.0
                    credit_sum = 0.0
                    date = slip_date
                    move_dict = {
                        'narration': '',
                        'ref': date.strftime('%B %Y'),
                        'journal_id': journal_id,
                        'date': date,
                    }

                    for slip in slip_mapped_data[employee][journal_id][slip_date]:
                        move_dict['narration'] += plaintext2html(
                            slip.number or '' + ' - ' + slip.employee_id.name or '')
                        move_dict['narration'] += Markup('<br/>')
                        slip_lines = slip._prepare_slip_lines(date, line_ids)
                        line_ids.extend(slip_lines)

                    for line_id in line_ids:  # Get the debit and credit sum.
                        debit_sum += line_id['debit']
                        credit_sum += line_id['credit']

                    # The code below is called if there is an error in the balance between credit and debit sum.
                    if float_compare(credit_sum, debit_sum, precision_digits=precision) == -1:
                        slip._prepare_adjust_line(line_ids, 'credit', debit_sum, credit_sum, date)
                    elif float_compare(debit_sum, credit_sum, precision_digits=precision) == -1:
                        slip._prepare_adjust_line(line_ids, 'debit', debit_sum, credit_sum, date)

                    # Add accounting lines in the move
                    move_dict['line_ids'] = [(0, 0, line_vals) for line_vals in line_ids]
                    move = self._create_account_move(move_dict)
                    for slip in slip_mapped_data[employee][journal_id][slip_date]:
                        slip.write({'move_id': move.id, 'date': date})
        return True

    def _prepare_slip_lines(self, date, line_ids):
        self.ensure_one()
        precision = self.env['decimal.precision'].precision_get('Payroll')
        new_lines = []
        for line in self.line_ids.filtered(lambda line: line.category_id):
            amount = -line.total if self.credit_note else line.total
            if line.code == 'NET':  # Check if the line is the 'Net Salary'.
                for tmp_line in self.line_ids.filtered(lambda line: line.category_id):
                    if tmp_line.salary_rule_id.not_computed_in_net:  # Check if the rule must be computed in the 'Net Salary' or not.
                        if amount > 0:
                            amount -= abs(tmp_line.total)
                        elif amount < 0:
                            amount += abs(tmp_line.total)
            if float_is_zero(amount, precision_digits=precision):
                continue
            partner_id = self.employee_id.address_home_id.id if self.employee_id.address_home_id else False
            debit_account_id = line.salary_rule_id.account_debit.id
            credit_account_id = line.salary_rule_id.account_credit.id

            if debit_account_id:  # If the rule has a debit account.
                debit = amount if amount > 0.0 else 0.0
                credit = -amount if amount < 0.0 else 0.0

                debit_line = self._get_existing_lines(
                    line_ids + new_lines, line, debit_account_id, debit, credit, partner_id)

                if not debit_line:
                    debit_line = self._prepare_line_values(line, debit_account_id, date, debit, credit, partner_id)
                    debit_line['tax_ids'] = [(4, tax_id) for tax_id in line.salary_rule_id.account_debit.tax_ids.ids]
                    new_lines.append(debit_line)
                else:
                    debit_line['debit'] += debit
                    debit_line['credit'] += credit

            if credit_account_id:  # If the rule has a credit account.
                debit = -amount if amount < 0.0 else 0.0
                credit = amount if amount > 0.0 else 0.0
                credit_line = self._get_existing_lines(
                    line_ids + new_lines, line, credit_account_id, debit, credit, partner_id)

                if not credit_line:
                    credit_line = self._prepare_line_values(line, credit_account_id, date, debit, credit, partner_id)
                    credit_line['tax_ids'] = [(4, tax_id) for tax_id in line.salary_rule_id.account_credit.tax_ids.ids]
                    new_lines.append(credit_line)
                else:
                    credit_line['debit'] += debit
                    credit_line['credit'] += credit
        return new_lines

    def _prepare_line_values(self, line, account_id, date, debit, credit, partner_id):
        if debit > credit:
            return {
                'name': line.name,
                'partner_id': partner_id or line.partner_id.id,
                'account_id': account_id,
                'journal_id': line.slip_id.struct_id.journal_id.id,
                'date': date,
                'debit': debit,
                'credit': credit,
                'analytic_account_id': line.salary_rule_id.analytic_account_id.id or line.slip_id.contract_id.analytic_account_id.id,
            }
        else:
            return {
                'name': line.name,
                'partner_id': partner_id or line.partner_id.id,
                'account_id': account_id,
                'journal_id': line.slip_id.struct_id.journal_id.id,
                'date': date,
                'debit': debit,
                'credit': credit,
                'analytic_account_id': False,
            }

    def _get_existing_lines(self, line_ids, line, account_id, debit, credit, partner_id):
        existing_lines = (
            line_id for line_id in line_ids if
            line_id['name'] == line.name
            and line_id['account_id'] == account_id
            and line_id['partner_id'] == partner_id
            and line_id['analytic_account_id'] == (
                    line.salary_rule_id.analytic_account_id.id or line.slip_id.contract_id.analytic_account_id.id)
            and ((line_id['debit'] > 0 and credit <= 0) or (line_id['credit'] > 0 and debit <= 0)))
        return next(existing_lines, False)

    def _get_year_selection(self):
        """Return the list of values of current year."""
        years = []
        for seq in range(datetime.now().year - 1, datetime.now().year + 6):
            years.append((str(seq), str(seq)))
        return years

    month = fields.Selection([('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'),
                              ('6', 'June'), ('7', 'July'), ('8', 'August'), ('8', 'September'), ('10', 'October'),
                              ('11', 'November'), ('12', 'December')], string="Month", readonly=True,
                             states={'draft': [('readonly', False)]}, default=str(datetime.now().month))
    year = fields.Selection(_get_year_selection, readonly=True, states={'draft': [('readonly', False)]},
                            default=lambda self: str(datetime.now().year))
    date_from = fields.Date(string='From', required=True)
    payment_id = fields.Many2one(comodel_name="account.payment", string="Payment")
    date_to = fields.Date(string='To', required=True)

    @api.onchange('month', 'year')
    @api.depends('month', 'year')
    def _calculate_period(self):
        date_from = datetime.now().date().replace(month=int(self.month), year=(int(self.year)), day=1)
        date_to = date_from.replace(day=calendar.monthrange(date_from.year, date_from.month)[1])
        self.date_from = date_from
        self.date_to = date_to

    @api.model
    def create(self, vals):
        res = super(Payslip, self).create(vals)
        res._calculate_period()
        res._check_same_period_slip()
        return res

    def write(self, vals):
        for rec in self:
            if 'month' or 'year' in vals.keys():
                if 'month' in vals:
                    month = vals['month']
                else:
                    month = rec.month
                if 'year' in vals:
                    year = vals['year']
                else:
                    year = rec.year
                if int(year) and int(month):
                    date_from = datetime.now().date().replace(month=int(month), year=(int(year)), day=1)
                    date_to = date_from.replace(day=calendar.monthrange(date_from.year, date_from.month)[1])
                    vals['date_from'] = date_from
                    vals['date_to'] = date_to
        res = super(Payslip, self).write(vals)
        return res


class PayslipBatch(models.Model):
    _inherit = 'hr.payslip.run'

    def _get_year_selection(self):
        """Return the list of values of current year."""
        years = []
        for seq in range(datetime.now().year - 1, datetime.now().year + 6):
            years.append((str(seq), str(seq)))
        return years

    month = fields.Selection([('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'),
                              ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'),
                              ('11', 'November'), ('12', 'December')], string="Month", readonly=True,
                             states={'draft': [('readonly', False)]}, default=str(datetime.now().month))
    year = fields.Selection(_get_year_selection, readonly=True, states={'draft': [('readonly', False)]},
                            default=lambda self: str(datetime.now().year))
    date_start = fields.Date(string='Date From', required=True)
    date_end = fields.Date(string='Date To', required=True)
    total_cost = fields.Float(string="Total Cost", compute="compute_total_cost")
    total_net = fields.Float(string="Net", compute="compute_total_cost")

    def create_payment(self):
        for rec in self:
            for slip in rec.slip_ids:
                slip.create_payment()

    @api.depends("slip_ids")
    def compute_total_cost(self):
        for rec in self:
            total_cost = 0
            net = 0
            for slip in rec.slip_ids:
                total_cost += slip.line_ids.filtered(lambda m: m.name == 'Total Cost').total
                net += slip.line_ids.filtered(lambda m: m.code == 'NET').total
            rec.total_cost = total_cost
            rec.total_net = net

    @api.onchange('month', 'year')
    @api.depends('month', 'year')
    def _calculate_period(self):
        date_from = datetime.now().date().replace(month=int(self.month), year=(int(self.year)), day=1)
        date_to = date_from.replace(day=calendar.monthrange(date_from.year, date_from.month)[1])
        self.date_start = date_from
        self.date_end = date_to

    @api.model
    def create(self, vals):
        res = super(PayslipBatch, self).create(vals)
        res._calculate_period()
        return res

    def write(self, vals):
        if 'month' or 'year' in vals.keys():
            if 'month' in vals and vals['month']:
                month = vals['month']
            else:
                month = self.month
            if 'year' in vals and vals['year']:
                year = vals['year']
            else:
                year = self.year
            if year and month:
                date_from = datetime.now().date().replace(month=int(month), year=(int(year)), day=1)
                date_to = date_from.replace(day=calendar.monthrange(date_from.year, date_from.month)[1])
                vals['date_start'] = date_from
                vals['date_end'] = date_to
        res = super(PayslipBatch, self).write(vals)
        return res

    def recompute_slips(self):
        for rec in self:
            for slip_id in rec.slip_ids:
                slip_id.write({'month': rec.month, 'year': rec.year})
                slip_id.compute_sheet()
            rec.state = 'verify'


class HrPayslipEmployee(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    def compute_sheet(self):
        res = super(HrPayslipEmployee, self).compute_sheet()
        payslip_run = self.env['hr.payslip.run'].browse(self.env.context.get('active_id'))
        payslip_run.recompute_slips()
        return res


class HrContractImport(models.TransientModel):
    _name = 'arch.import.hr.contract'

    file_name = fields.Binary(string='Attached File')

    def import_hr_contract(self):
        fx = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fx.write(binascii.a2b_base64(self.file_name))
        fx.seek(0)
        workbook = xlrd.open_workbook(fx.name)
        sheet = workbook.sheet_by_index(0)
        try:
            contract_date = []
            for row_no in range(sheet.nrows):
                if row_no <= 0:
                    field = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
                else:
                    field_data = list(map(lambda row: str(row.value), sheet.row(row_no)))
                    employee_name = field_data[3]
                    employee_wage = field_data[33]
                    baisc_salary = field_data[22]
                    home_alow = field_data[23]
                    trans_alow = field_data[24]
                    phone_alow = field_data[25]
                    other_alow = field_data[27]
                    employee_obj = self.env['hr.employee'].search([('name', '=', employee_name)], limit=1)
                    baisc_salary_obj = self.env['hr.salary.rule'].search(
                        [('code', '=', 'BASIC'), ('struct_id', '=', 5)], limit=1)
                    home_alow_obj = self.env['hr.salary.rule'].search(
                        [('code', '=', 'HOUALLOW'), ('struct_id', '=', 5)], limit=1)
                    trans_alow_obj = self.env['hr.salary.rule'].search(
                        [('code', '=', 'TRAALLOW'), ('struct_id', '=', 5)], limit=1)
                    phone_alow_obj = self.env['hr.salary.rule'].search([('code', '=', 'PHNALW'), ('struct_id', '=', 5)],
                                                                       limit=1)
                    other_alow_obj = self.env['hr.salary.rule'].search([('code', '=', 'OTHALW'), ('struct_id', '=', 5)],
                                                                       limit=1)
                    vals = [
                        (0, 0, {'rule_id': baisc_salary_obj.id, 'value_type': 'amount', 'value': baisc_salary}),
                        (0, 0, {'rule_id': home_alow_obj.id, 'value_type': 'amount', 'value': home_alow}),
                        (0, 0, {'rule_id': trans_alow_obj.id, 'value_type': 'amount', 'value': trans_alow}),
                        (0, 0, {'rule_id': phone_alow_obj.id, 'value_type': 'amount', 'value': phone_alow}),
                        (0, 0, {'rule_id': other_alow_obj.id, 'value_type': 'amount', 'value': other_alow}),
                    ]
                    contract_date.append({
                        'name': employee_obj.name + 'Contract',
                        'structure_type_id': 5,
                        'employee_id': employee_obj.id,
                        'wage': employee_wage,
                        'rule_ids': vals
                    })
            self.env['hr.contract'].create(contract_date)
        except IndexError:
            pass
