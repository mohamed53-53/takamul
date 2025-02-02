from odoo import api, fields, models
from dateutil import relativedelta


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    airline_tickets = fields.Float()
    monthly_eos_category = fields.Many2one(comodel_name='employee.monthly.category',string='Provision Category')

class MonthlyEosLine(models.Model):
    _name = 'monthly.eos.line'

    monthly_eos_id = fields.Many2one(comodel_name="employee.monthly.eos")
    employee_id = fields.Many2one(comodel_name="hr.employee")
    join_date = fields.Date(related="employee_id.join_date")
    type = fields.Selection(related="monthly_eos_id.type")
    date = fields.Date(related="monthly_eos_id.date")
    amount = fields.Float()

class MonthlyEosCategory(models.Model):
    _name = 'employee.monthly.category'
    name = fields.Char('Probation Category')
    monthly_eos_type = fields.Selection(selection=[('monthly_eos', 'Monthly EOS'),
                                       ('airline_tickets', 'Airline Tickets'),
                                       ('time_off', 'TimeOff'),
                                       ], required=False,default='monthly_eos',readonly=True)


    monthly_eos_journal_id = fields.Many2one(comodel_name="account.journal")
    monthly_eos_source_account_id = fields.Many2one(comodel_name="account.account")
    monthly_eos_destination_account_id = fields.Many2one(comodel_name="account.account")
    eos_type = fields.Many2one(comodel_name="eos.type")
    airline_tickets_type = fields.Selection(selection=[('monthly_eos', 'Monthly EOS'),
                                       ('airline_tickets', 'Airline Tickets'),
                                       ('time_off', 'TimeOff'),
                                       ], required=False,default='airline_tickets',readonly=True)


    airline_tickets_journal_id = fields.Many2one(comodel_name="account.journal")
    airline_tickets_source_account_id = fields.Many2one(comodel_name="account.account")
    airline_tickets_destination_account_id = fields.Many2one(comodel_name="account.account")

    time_off_type = fields.Selection(selection=[('monthly_eos', 'Monthly EOS'),
                                       ('airline_tickets', 'Airline Tickets'),
                                       ('time_off', 'TimeOff'),
                                       ], required=False,default='time_off',readonly=True)


    # time_off_journal_id = fields.Many2one(comodel_name="account.journal")
    # time_off_source_account_id = fields.Many2one(comodel_name="account.account")
    # time_off_destination_account_id = fields.Many2one(comodel_name="account.account")




class MonthlyEos(models.Model):
    _name = 'employee.monthly.eos'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char()
    date = fields.Date(required=False)
    employee_ids = fields.Many2many(comodel_name="hr.employee")
    #('airline_tickets', 'Airline Tickets'),
    type = fields.Selection(selection=[('monthly_eos', 'Monthly EOS'),
                                       ('time_off', 'TimeOff'),
                                       ], required=False, )
    eos_type_id = fields.Many2one(comodel_name="eos.type")
    journal_id = fields.Many2one(comodel_name="account.journal")
    source_account_id = fields.Many2one(comodel_name="account.account")
    destination_account_id = fields.Many2one(comodel_name="account.account")
    monthly_eos_line_ids = fields.One2many(comodel_name="monthly.eos.line", inverse_name="monthly_eos_id", )
    state = fields.Selection(selection=[('draft', 'Draft'), ('posted', 'Posted'),],default='draft')
    move_id = fields.Many2one(comodel_name="account.move", string="Entry Move",)



    def calculate_amount(self):
        if self.type == 'monthly_eos':
            self.calculate_monthly_eos()
        elif self.type == 'airline_tickets':
            self.get_employee_airline_tickets()
        elif self.type == 'time_off':
            self.get_employee_timeoff_amount()

    def get_employee_airline_tickets(self):
        self.monthly_eos_line_ids.unlink()
        for emp in self.employee_ids:
            self.env['monthly.eos.line'].create({'employee_id': emp.id,
                                                 'amount': emp.flight_ticket / 12,
                                                 'monthly_eos_id': self.id})

    def get_employee_timeoff_amount(self):
        self.monthly_eos_line_ids.unlink()
        for emp in self.employee_ids:
            self.env['monthly.eos.line'].create({'employee_id': emp.id,
                                                 'amount': emp.monthly_balance_value,
                                                 'monthly_eos_id': self.id})

    def calculate_monthly_eos(self):
        self.monthly_eos_line_ids.unlink()
        for emp in self.employee_ids:
            diff = relativedelta.relativedelta(self.date, emp.join_date)
            duration_days = diff.days
            duration_months = diff.months
            duration_years = diff.years
            # work_years = round(duration_years + duration_months / 12 + (duration_days / 30) / 12, 2)
            work_months = round(duration_years * 12 + duration_months + (duration_days / 30), 2)
            eos_rate = self.env['eos.type.line'].search([('service_from', '<=', work_months),
                                                         # ('service_to', '>=', work_months),
                                                         ('eos_type_id', '=', self.eos_type_id.id)
                                                         ], order="service_to")

            wage = 0
            for line in emp.contract_id.rule_ids.filtered(lambda r: r.rule_id.is_social_rule):
                wage += line.total_value
            if not wage:
                wage = emp.contract_id.wage
            total_eos = 0
            remain_month = work_months
            for eos_rate_line in eos_rate:
                if eos_rate_line.service_to <= remain_month:
                    total_eos += ((wage * eos_rate_line.rate / 100 * eos_rate_line.month_rate) * eos_rate_line.service_to / 12)
                    remain_month -= eos_rate_line.service_to
                else:
                    total_eos += ((wage * eos_rate_line.rate / 100 * eos_rate_line.month_rate) * remain_month / 12)
            self.env['monthly.eos.line'].create({'employee_id': emp.id,
                                                 'amount': total_eos / work_months if work_months else 0,
                                                 'monthly_eos_id': self.id})

    def create_monthly_eos_move(self):
        if self.type != 'time_off':
            move = self.env['account.move'].create({'journal_id': self.journal_id.id,
                                                    'date': self.date,
                                                    'ref': self.name
                                                    })
            total_amount = 0
            for line in self.monthly_eos_line_ids:
                self.env['account.move.line'].with_context(check_move_validity=False).create(
                    {'account_id': self.source_account_id.id,
                     'debit': line.amount,
                     'move_id': move.id,
                     'partner_id': line.employee_id.address_home_id.id
                     })
                total_amount += line.amount
            self.env['account.move.line'].with_context(check_move_validity=False).create(
                {'account_id': self.destination_account_id.id,
                 'credit': total_amount,
                 'move_id': move.id,
                 'partner_id': line.employee_id.address_home_id.id
                 })
            self.move_id = move.id
        self.state = 'posted'

    def action_open_move(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Entry Move',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', '=', self.move_id.id)],
        }


class HrPaySlipRun(models.Model):
    _name = "hr.payslip.run"
    _inherit = ["hr.payslip.run","mail.thread", "mail.activity.mixin","approval.record"]

    state = fields.Selection([], string='Status', index=True, readonly=True, copy=False, default='draft')
    is_created_employee_benefits = fields.Boolean(copy=False)
    def get_monthly_category(self):
        for rec in self:
            monthly_eos = rec.env['employee.monthly.category'].search([('monthly_eos_type','=','monthly_eos')])
            employee = rec.env['hr.payslip'].search([('payslip_run_id','=',self.id)]).employee_id.ids

            for m_eos in monthly_eos:
                monthly_eos_type = rec.env['hr.employee'].search(
                    [('id','in',employee)])
                if monthly_eos_type:
                    monthly_vals = {
                        'name': m_eos.name +' / '+ 'Monthly EOS',
                        'type': 'monthly_eos',
                        'date': rec.date_start,
                        'eos_type_id': m_eos.eos_type.id,
                        'journal_id': m_eos.monthly_eos_journal_id.id,
                        'source_account_id': m_eos.monthly_eos_source_account_id.id,
                        'destination_account_id': m_eos.monthly_eos_destination_account_id.id,
                        'employee_ids': [(6, 0, monthly_eos_type.ids)]
                    }
                    monthly_create = rec.env['employee.monthly.eos'].create(monthly_vals)
                    monthly_create.calculate_amount()

    def get_airline_tickets_category(self):
        for rec in self:
            airline_tickets = rec.env['employee.monthly.category'].search([('airline_tickets_type','=','airline_tickets')])
            employee = rec.env['hr.payslip'].search([('payslip_run_id','=',self.id)]).employee_id.ids

            for m_eos in airline_tickets:
                monthly_eos_emp = rec.env['hr.employee'].search(
                    [('id','in',employee)])
                if monthly_eos_emp :
                    monthly_vals = {
                        'name':m_eos.name +' / '+ 'Airline Tickets',
                        'type':'airline_tickets',
                        'date':rec.date_start,
                        'eos_type_id':m_eos.eos_type.id,
                        'journal_id':m_eos.airline_tickets_journal_id.id,
                        'source_account_id':m_eos.airline_tickets_source_account_id.id,
                        'destination_account_id':m_eos.airline_tickets_destination_account_id.id,
                        'employee_ids':[(6,0, monthly_eos_emp.ids)]
                    }
                    monthly_create = rec.env['employee.monthly.eos'].create(monthly_vals)
                    monthly_create.calculate_amount()

    def get_time_off_category(self):
        for rec in self:
            time_off = rec.env['employee.monthly.category'].search([('time_off_type','=','time_off')])
            employee = rec.env['hr.payslip'].search([('payslip_run_id','=',self.id)]).employee_id.ids
            print(employee)
            for m_eos in time_off:
                monthly_eos_emp = rec.env['hr.employee'].search(
                    [('id','in',employee)])
                if monthly_eos_emp:
                    monthly_vals = {
                        'name':m_eos.name +' / '+ 'TimeOff',
                        'type':'time_off',
                        'date':rec.date_start,
                        'eos_type_id':m_eos.eos_type.id,
                        # 'journal_id':m_eos.time_off_journal_id.id,
                        # 'source_account_id':m_eos.time_off_source_account_id.id,
                        # 'destination_account_id':m_eos.time_off_destination_account_id.id,
                        'employee_ids':[(6,0, monthly_eos_emp.ids)]
                    }
                    monthly_create = rec.env['employee.monthly.eos'].create(monthly_vals)
                    monthly_create.calculate_amount()

    def action_create_employee_benefits(self):
        self.get_monthly_category()
        # self.get_airline_tickets_category()
        self.get_time_off_category()
        self.write({'is_created_employee_benefits':True})
    @api.model
    def _before_approval_states(self):
        return [("draft", "Draft")]


class HrPayslipEmployee(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    def compute_sheet(self):
        res = super(HrPayslipEmployee, self).compute_sheet()
        payslip_run = self.env['hr.payslip.run'].browse(self.env.context.get('active_id'))
        payslip_run.action_create_employee_benefits()
        return res
