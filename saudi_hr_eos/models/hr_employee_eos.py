# -*- coding: utf-8 -*-
# Part of odoo. See LICENSE file for full copyright and licensing details.

import time
from odoo import models, fields, api, _
from dateutil import relativedelta
from datetime import date, datetime, timedelta
import calendar
from odoo.exceptions import UserError
from odoo.tools.misc import format_date
import logging
from odoo.exceptions import UserError, ValidationError, Warning

_logger = logging.getLogger(__name__)


class HrEmployeeEos(models.Model):
    _name = 'hr.employee.eos'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']
    _description = "End of Service Indemnity (EOS)"

    def _get_currency(self):
        """
            return currency of current user
        """
        return self.env.company.currency_id.id

    def _calc_payable_eos(self):
        """
            Calculate the payable eos
        """
        for eos_amt in self:
            if eos_amt.is_adjust:
                eos_amt.payable_eos = (eos_amt.total_eos + eos_amt.others + eos_amt.total_remaining_leaves_adjust) or (eos_amt.total_eos + eos_amt.others + eos_amt.total_remaining_leaves_a) or 0.0
            else:
                eos_amt.payable_eos = (eos_amt.total_eos + eos_amt.others + eos_amt.total_remaining_leaves) or 0.0

    name = fields.Char('Description', size=128, required=True, readonly=True,
                       states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    eos_date = fields.Date('Date', index=True, required=True, readonly=True,
                           states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                           default=lambda self: datetime.today().date())
    employee_id = fields.Many2one('hr.employee', "Employee", required=True, readonly=True,
                                  states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    date_of_join = fields.Date(related='employee_id.join_date', type="date", string="Joining Date", store=True,
                               readonly=True)
    date_of_leave = fields.Date(string="Leaving Date", default=fields.Date.context_today)
    duration_days = fields.Integer('No of Days', readonly=True,
                                   states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    duration_months = fields.Integer('No of Months', readonly=True,
                                     states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    plan_id = fields.Many2one(comodel_name="hr.boarding.plan", string="Plan")
    duration_years = fields.Integer('No. of Years', readonly=True,
                                    states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    benefit_ids = fields.One2many(comodel_name="employee.eos.other.benefits", inverse_name="eos_id",
                                  string="Other Benefits", required=False)
    type = fields.Selection([
        ('resignation', 'الاستقالة'),
        ('contract_end', 'انتهاء عقد عمل'),
        ('training_end', 'انهاء خدمات خلال فترة التجربة '),
        ('rule_80', 'انهاء خدمات وفقا للمادة ثامنون '),
    ], 'Type', readonly=True, states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    calc_year = fields.Float('Total Years', readonly=False, )
    payslip_id = fields.Many2one('hr.payslip', 'Payslip', readonly=True)
    current_month_salary = fields.Float('Salary of Current month', readonly=True,
                                        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    others = fields.Float('Other Benefits', compute="onchange_benefits")
    user_id = fields.Many2one('res.users', 'User', required=True, default=lambda self: self.env.user.id)
    date_confirm = fields.Date('Confirmation Date', index=True,
                               help="Date of the confirmation of the sheet expense. It's filled when the button Confirm is pressed.")
    date_valid = fields.Date('Validation Date', index=True,
                             help="Date of the acceptation of the sheet eos. It's filled when the button Validate is pressed.",
                             readonly=True)
    date_approve = fields.Date('Approve Date', index=True,
                               help="Date of the Approval of the sheet eos. It's filled when the button Approve is pressed.",
                               readonly=True)
    user_valid = fields.Many2one('res.users', 'Validation by', readonly=True,
                                 states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, store=True)
    user_approve = fields.Many2one('res.users', 'Approval by', readonly=True,
                                   states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                                   store=True)
    note = fields.Text('Note')
    annual_leave_amount = fields.Float('Leave Balance', readonly=True,
                                       states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    department_id = fields.Many2one('hr.department', "Department", readonly=True)
    job_id = fields.Many2one('hr.job', 'Job', readonly=True)
    contract_id = fields.Many2one('hr.contract', 'Contract', readonly=True,
                                  states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True,
                                 states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                                 default=lambda self: self.env.company.id)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], 'Status',
                             readonly=False,
                             tracking=True,
                             default='draft',
                             help='When the eos request is created the status is \'Draft\'.\n It is confirmed by the user and request is sent to finance, the status is \'Waiting Confirmation\'.\
        \nIf the finance accepts it, the status is \'Accepted\'.')
    total_eos = fields.Float('Total Award')

    total_remaining_leaves = fields.Float('Remaining Leaves Award')
    total_remaining_leaves_adjust = fields.Float('Remaining Leaves Award', compute="onchange_adjustment")
    payable_eos = fields.Float(compute=_calc_payable_eos, string='Total Amount')
    eos_type_id = fields.Many2one(comodel_name="eos.type")
    taken_leave = fields.Float('Taken Leaves')
    remaining_leave = fields.Float('Remaining Leaves')
    is_adjust = fields.Boolean('Adjust Leaves')
    remaining_leave_adjust = fields.Float('Remaining Leaves Adjust')
    # account
    journal_id = fields.Many2one('account.journal', 'Force Journal', help="The journal used when the eos is done.")
    account_move_id = fields.Many2one('account.move', 'Ledger Posting')
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, readonly=True,
                                  states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                                  default=_get_currency)

    @api.onchange('benefit_ids', 'total_eos', 'total_remaining_leaves', 'total_remaining_leaves_adjust')
    @api.depends('benefit_ids')
    def onchange_benefits(self):
        for rec in self:
            rec.others = sum(benefit_id.amount for benefit_id in rec.benefit_ids)


    def _track_subtype(self, init_values):
        """
            Track Subtypes of EOS
        """
        self.ensure_one()
        if 'state' in init_values and self.state == 'draft':
            return self.env.ref('saudi_hr_eos.mt_employee_eos_new')
        elif 'state' in init_values and self.state == 'confirm':
            # return 'saudi_hr_eos.mt_employee_eos_confirm'
            return self.env.ref('saudi_hr_eos.mt_employee_eos_confirm')
        elif 'state' in init_values and self.state == 'accepted':
            return self.env.ref('saudi_hr_eos.mt_employee_eos_accept')
        elif 'state' in init_values and self.state == 'validate':
            return self.env.ref('saudi_hr_eos.mt_employee_eos_validate')
        elif 'state' in init_values and self.state == 'done':
            return self.env.ref('saudi_hr_eos.mt_employee_eos_done')
        elif 'state' in init_values and self.state == 'cancelled':
            return self.env.ref('saudi_hr_eos.mt_employee_eos_cancel')
        return super(HrEmployeeEos, self)._track_subtype(init_values)

    def copy(self, default=None):
        """
            Duplicate record
        """
        default = dict(default or {})
        default.update(
            account_move_id=False,
            date_confirm=False,
            date_valid=False,
            date_approve=False,
            user_valid=False)
        return super(HrEmployeeEos, self).copy(default=default)

    @api.model
    def create(self, values):
        """
            Create a new Record
        """
        if values.get('employee_id'):
            employee = self.env['hr.employee'].browse(values['employee_id'])
            values.update({'job_id': employee.job_id.id,
                           'department_id': employee.department_id.id})
        return super(HrEmployeeEos, self).create(values)

    def write(self, values):
        """
            update existing record
        """
        if values.get('employee_id'):
            employee = self.env['hr.employee'].browse(values['employee_id'])
            values.update({'job_id': employee.job_id.id,
                           'department_id': employee.department_id.id})
        return super(HrEmployeeEos, self).write(values)

    def unlink(self):
        """
            Remove record
        """
        for record in self:
            if record.state in ['confirm', 'validate', 'accepted', 'done', 'cancelled']:
                raise UserError(_('You cannot remove the record which is in %s state!') % record.state)
        return super(HrEmployeeEos, self).unlink()

    @api.onchange('currency_id', 'company_id')
    def onchange_currency_id(self):
        """
            find the journal using currency
        """
        journal_ids = self.env['account.journal'].search(
            [('type', '=', 'purchase'), ('currency_id', '=', self.currency_id.id),
             ('company_id', '=', self.company_id.id)], limit=1)
        if journal_ids:
            self.journal_id = journal_ids[0].id

    def calc_eos(self):
        """
            Calculate eos
        """
        payslip_obj = self.env['hr.payslip']
        for eos in self:
            if not eos.date_of_leave:
                raise UserError(_('Please define employee date of leaving!'))
            diff = relativedelta.relativedelta(eos.date_of_leave, eos.date_of_join)
            duration_days = diff.days
            duration_months = diff.months
            duration_years = diff.years
            work_years = round(duration_years + duration_months / 12 + (duration_days / 30) / 12, 2)
            work_months = round(duration_years * 12 + duration_months + (duration_days / 30), 2)
            eos.write({
                'duration_days': duration_days,
                'duration_months': duration_months,
                'duration_years': duration_years
            })
            selected_month = eos.date_of_leave.month
            selected_year = eos.date_of_leave.year
            date_from = date(selected_year, selected_month, 1)
            date_to = date_from + relativedelta.relativedelta(day=eos.date_of_leave.day)
            contract_ids = self.employee_id._get_contracts(date_from, date_to)
            if not contract_ids:
                raise UserError(_('Please define contract for selected Employee!'))
            if not eos.contract_id.structure_type_id.default_struct_id.journal_id:
                raise UserError(_('Please configure employee contract for journal.'))
            selected_month = eos.eos_date.month
            selected_year = eos.eos_date.year
            date_from = date(selected_year, selected_month, 1)
            date_to = date_from + relativedelta.relativedelta(day=eos.date_of_leave.day)
            dates = eos.eos_date
            # date_to = datetime(dates.year, dates.month, calendar.mdays[dates.month])
            values = {
                'employee_id': eos.employee_id.id or False,
                'date_from': date_from,
                'date_to': date_to,
                'contract_id': eos.contract_id.id,
                'struct_id': eos.contract_id.structure_type_id.default_struct_id.id or False,
                'journal_id': eos.contract_id.structure_type_id.default_struct_id.journal_id.id or False,
            }
            payslip_name = eos.contract_id.structure_type_id.default_struct_id.payslip_name or _('Salary Slip')
            name = '%s - %s - %s' % (
                payslip_name, self.employee_id.name or '', format_date(self.env, date_from, date_format="MMMM y"))
            values.update({
                'name': name
            })
            if not eos.payslip_id:
                payslip_id = payslip_obj.create(values)
                eos.write({'payslip_id': payslip_id.id})
            eos.payslip_id.compute_sheet()
            net = 0.00
            payslip_line_obj = self.env['hr.payslip.line']
            net_rule_id = payslip_line_obj.search([('slip_id', '=', eos.payslip_id.id),
                                                   ('code', 'ilike', 'NET')])
            if net_rule_id:
                net_rule_obj = net_rule_id[0]
                net = net_rule_obj.total
            eos.write({'current_month_salary': net})
            # print("=======================work_months",work_months)
            wage = 0
            for line in self.contract_id.rule_ids.filtered(lambda r: r.rule_id.is_social_rule):
                wage += line.total_value
            print(wage)
            eos_type = self.env['eos.type.line'].search([('eos_type_id', '=', self.eos_type_id.id)], order='service_to')
            total_eos = 0
            remaining_months = work_months
            for line in eos_type:
                if remaining_months >= line.service_to:
                    total_eos += wage * line.month_rate * (line.rate / 100) * int(line.service_to / 12)
                    remaining_months -= line.service_to
                elif line.service_from <= work_months <= line.service_to:
                    total_eos += (wage * (line.month_rate) * (line.rate / 100) * (remaining_months / 12))
            payable_eos = total_eos
            # TODO: Annual Leave Calc
            # TODO: if eos.employee_id.is_saudi:
            leaves_taken = 0
            time_off_days = 0
            remaining_leaves = 0
            holiday_status_ids = self.env['hr.leave.type'].search([('check_leave', '=', True)])
            # print(holiday_status_ids)
            if holiday_status_ids:

                for recs in holiday_status_ids:
                    leave_values = recs.get_days(eos.employee_id.id)
                    print('recs', leave_values)  # eos.year_id.id
                    leaves_taken = leaves_taken + leave_values[recs[0].id]['leaves_taken']
                    remaining_leaves = remaining_leaves + leave_values[recs[0].id]['remaining_leaves']
                    time_off_days = time_off_days + leave_values[recs[0].id]['time_off_days']
                print('remaining_leaves', remaining_leaves)

                # print('leaves_taken',leaves_taken)
            allocate_leave_days = 0
            # if eos.employee_id.is_saudi:
            diff_date = relativedelta.relativedelta(eos.date_of_leave, eos.date_of_join)
            _logger.info(("allocate_leave_month:{}".format(diff_date.years * 12 + diff_date.months)))
            if not eos.company_id.less_than_five_years:
                raise ValidationError(_("Please set number of days for employees spend less than 5 Years"))
            if diff_date.years < 5 or (diff_date.years == 5 and diff_date.months == 0 and diff_date == 0):
                allocate_leave_days = ((diff_date.years * 12 * 30) + (
                        diff_date.months * 30) + diff_date.days) * (
                                              eos.company_id.less_than_five_years / 360)
            else:
                if not eos.company_id.up_to_five_years:
                    raise ValidationError(_("Please set number of days for employees spend more than 5 Years"))
                years = diff_date.years - 5
                allocate_leave_days = ((5 * 12 * 30) * (eos.company_id.less_than_five_years / 360)) + \
                                      (((years * 12 * 30) + (diff_date.months * 30) + diff_date.days) *
                                       (eos.company_id.up_to_five_years / 360))

                # allocate_leave_month = (diff_date.years * 12 + diff_date.months) * eos.job_id.annual_leave_rate
            # else:
            #     work_back = self.env['hr.work.back'].search(
            #         [('employee_id', '=', eos.employee_id.id), ('company_id', '=', eos.company_id.id),
            #          ('state', '=', 'confirm')], order='date_work_back desc')
            #     if work_back:
            #         work_back = work_back[0]
            #         diff_hireto_date = relativedelta.relativedelta(eos.date_of_leave, eos.date_of_join)
            #         diff_hirefrom_date = relativedelta.relativedelta(work_back.date_work_back, eos.date_of_join)
            #         diff_date = relativedelta.relativedelta(eos.date_of_leave, work_back.date_work_back)
            #         if not eos.company_id.less_than_five_years:
            #             raise ValidationError(_("Please set number of days for employees spend less than 5 Years"))
            #         if diff_hireto_date.years < 5 or (
            #                 diff_hireto_date.years == 5 and diff_hireto_date.months == 0 and diff_hireto_date == 0):
            #             allocate_leave_days = ((diff_date.years * 12 * 30) + (
            #                     diff_date.months * 30) + diff_date.days) * (
            #                                           eos.company_id.less_than_five_years / 360)
            #         else:
            #             if not eos.company_id.up_to_five_years:
            #                 raise ValidationError(
            #                     _("Please set number of days for employees spend more than 5 Years"))
            #             hire_five = eos.date_of_join.year + 5
            #             hire_after_five = eos.date_of_join.replace(year=hire_five)
            #             if hire_after_five > work_back.date_work_back:
            #                 diff_hirefive_workback = relativedelta.relativedelta(hire_after_five,
            #                                                                      work_back.date_work_back)
            #                 diff_hirefive_workback_days = ((diff_hirefive_workback.years * 360) + (
            #                         diff_hirefive_workback.months * 30) + diff_hirefive_workback.days)
            #                 diff_hirefive_workback_amount = diff_hirefive_workback_days * (
            #                         eos.company_id.less_than_five_years / 360)
            #
            #                 diff_hirefive_leave = relativedelta.relativedelta(eos.date_of_leave, hire_after_five)
            #                 diff_hirefive_leave_days = ((diff_hirefive_leave.years * 360) + (
            #                         diff_hirefive_leave.months * 30) + diff_hirefive_leave.days)
            #                 diff_hirefive_leave_days_amount = diff_hirefive_leave_days * (
            #                         eos.company_id.up_to_five_years / 360)
            #
            #                 allocate_leave_days = diff_hirefive_workback_amount + diff_hirefive_leave_days_amount
            #             else:
            #                 allocate_leave_days = ((diff_date.years * 12 * 30) + (
            #                         diff_date.months * 30) + diff_date.days) * (
            #                                               eos.company_id.up_to_five_years / 360)
            #     else:
            #         raise ValidationError(_("No Work Back for employee"))
            total_eos_years = eos.duration_years * 12
            total_eos_month = eos.duration_months
            total_eos_days = eos.duration_days / 30
            employee_mounthly_balance = eos.employee_id.monthly_balance if eos.employee_id.monthly_balance else 0
            total_eos_sum = (total_eos_years + total_eos_month + total_eos_days) * employee_mounthly_balance

            print('total_eos_years', total_eos_years, 'total_eos_month', total_eos_month, 'total_eos_days',
                  total_eos_days)
            print('total_eos_sum', total_eos_sum)
            print('remaining_leaves', remaining_leaves,
                  'leaves_taken', leaves_taken,
                  'employee_mounthly_balance', employee_mounthly_balance)
            total_remaining_leaves = 0
            # remaining_leaves = allocate_leave_days - leaves_taken
            # print('alooc',allocate_leave_days)
            # print('leave',leave_values)
            if remaining_leaves > 0:
                total_remaining_leaves = remaining_leaves * eos.contract_id.day_value
            #
            remaining_leaves_days = total_eos_sum - leaves_taken
            if remaining_leaves_days > 0:
                total_remaining_leaves = remaining_leaves_days * eos.contract_id.day_value
            print('total_remaining_leaves', total_remaining_leaves)
            # else:
            #     total_remaining_leaves = remaining_leaves * eos.contract_id.day_value
            annual_leave_amount = eos.employee_id.contract_id.day_value * remaining_leaves_days
            eos.write({
                'total_eos': payable_eos,
                'annual_leave_amount': annual_leave_amount,
                'remaining_leave': remaining_leaves_days,
                'taken_leave': leaves_taken,
                'total_remaining_leaves': total_remaining_leaves
            })
            eos.onchange_adjustment()
            return True

    @api.onchange('is_adjust', 'remaining_leave_adjust', 'employee_id')
    @api.depends('is_adjust', 'remaining_leave_adjust', 'employee_id')
    def onchange_adjustment(self):
        for rec in self:
            if rec.is_adjust:
                rec.total_remaining_leaves_adjust = rec.remaining_leave_adjust * rec.contract_id.day_value
                rec.payable_eos = rec.total_eos + rec.total_remaining_leaves_adjust + rec.others
            else:
                rec.total_remaining_leaves_adjust = rec.remaining_leave * rec.contract_id.day_value
                rec.payable_eos = rec.total_eos + rec.total_remaining_leaves + rec.others

    @api.onchange('employee_id', 'eos_date')
    def onchange_employee_id(self):
        """
            Calculate total no of year, month, days, etc depends on employee
        """
        if self.employee_id:
            if not self.date_of_leave:
                raise UserError(_('Please define employee date of leaving!'))
            if not self.employee_id.join_date:
                raise UserError(_('Please define employee date of join!'))
            selected_date = self.date_of_leave
            date_from = date(selected_date.year, selected_date.month, 1)
            date_to = date_from + relativedelta.relativedelta(day=selected_date.day)
            contract_ids = self.employee_id._get_contracts(date_from=date_from, date_to=date_to)
            if not contract_ids:
                raise UserError(_('Please define contract for selected Employee!'))
            calc_years = round(((self.date_of_leave - self.employee_id.join_date).days / 365.0), 2)
            diff = relativedelta.relativedelta(self.date_of_leave, self.employee_id.join_date)

            self.contract_id = contract_ids[0]
            if self.employee_id.date_of_leave:
                self.date_of_leave = self.employee_id.date_of_leave
            self.date_of_join = self.employee_id.join_date
            self.calc_year = calc_years
            self.department_id = self.employee_id.department_id.id or False
            self.company_id = self.employee_id.company_id.id or False
            self.job_id = self.employee_id.sudo().job_id.id or False
            self.duration_years = diff.years or 0
            self.duration_months = diff.months or 0
            self.duration_days = diff.days or 0

    def eos_draft(self):
        """
            EOS set to draft state
        """
        self.ensure_one()
        self.state = 'draft'
        self.message_post(subtype_id=self.env.ref('mail.mt_comment').id, body=_('EOS Draft.'))

    def action_approve(self):
        for rec in self:
            if rec.state == 'draft':
                self.message_post(subtype_id=self.env.ref('mail.mt_comment').id, body=_('EOS Confirmed.'))
            if rec.state == 'confirm':
                self.message_post(subtype_id=self.env.ref('mail.mt_comment').id, body=_('EOS Validated.'))
            if rec.state == 'validate':
                self.message_post(subtype_id=self.env.ref('mail.mt_comment').id, body=_('EOS Approved.'))
            self.env['gosi.eos'].create({
                'project_id': rec.employee_id.project_id.id,
                'employee_id': rec.employee_id.id,
                'company_id': rec.employee_id.company_id.id,
                # 'number': rec.employee_id.gosi_number,
                'start_date': rec.eos_date,
                'state': 'draft',
            })
            if rec.plan_id:
                activity_mail_template = self.env.ref('archer_recruitment.mail_template_new_activity')
                for activity in rec.plan_id.activity_ids:
                    employee_plan_lines = {
                        'boarding_plan_id': rec.plan_id.id,
                        'name': activity.id,
                        'no_of_days': activity.no_of_days,
                        'user_id': activity.user_id.id,
                        'employee_id': rec.employee_id.id,
                        'assign_date': datetime.now().date(),
                        'done_date': False,
                        'deadline_date': datetime.now().date() + timedelta(days=activity.no_of_days),
                    }
                    self.env['hr.boarding.plan.employee'].create(employee_plan_lines)
                    email_values = {
                        'email_to': activity.user_id.email,
                        'subject': 'Offboarding Employee',
                    }
                    activity_mail_template.with_context(user_name=activity.user_id.name, activity_name=activity.name,
                                                        employee_name=rec.employee_id.name).send_mail(rec.id,
                                                                                                      force_send=True,
                                                                                                      raise_exception=True,
                                                                                                      email_values=email_values)

            super(HrEmployeeEos, self).action_approve()

    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    def action_reject(self, reason=None):
        self.write({'state': 'rejected'})
        if reason:
            self.message_post(body=reason, subject="Reject Reason")
        self.message_post(subtype_id=self.env.ref('mail.mt_comment').id, body=_('EOS Cancelled.'))

    def account_move_get(self):
        """
            This method prepare the creation of the account move related to the given expense.

            :param eos_id: Id of voucher for which we are creating account_move.
            :return: mapping between field name and value of account move to create
            :rtype: dict
        """
        self.ensure_one()
        journal_obj = self.env['account.journal']
        company_id = self.company_id.id
        date = self.date_confirm
        ref = self.name
        if self.journal_id:
            journal_id = self.journal_id.id
        else:
            journal_id = journal_obj.search([('type', '=', 'purchase'), ('company_id', '=', company_id)])
            if not journal_id:
                raise UserError(_("No EOS journal found. "
                                  "Please make sure you have a journal with type 'purchase' configured."))
            journal_id = journal_id[0].id
        return self.env['account.move'].account_move_prepare(journal_id, date=date, ref=ref, company_id=company_id)

    def line_get_convert(self, x, part, date):
        """
            line get convert
        """
        partner_id = self.env['res.partner']._find_accounting_partner(part).id
        return {
            'date_maturity': x.get('date_maturity', False),
            'partner_id': partner_id,
            'name': x['name'][:64],
            'date': date,
            'debit': x['price'] > 0 and x['price'],
            'credit': x['price'] < 0 and -x['price'],
            'account_id': x['account_id'],
            # 'analytic_lines': x.get('analytic_lines', False),
            'amount_currency': x['price'] > 0 and abs(x.get('amount_currency', False)) or -abs(
                x.get('amount_currency', False)),
            'currency_id': x.get('currency_id', False),
            # 'tax_code_id': x.get('tax_code_id', False),
            # 'tax_amount': x.get('tax_amount', False),
            'ref': x.get('ref', False),
            'quantity': x.get('quantity', 1.00),
            'product_id': x.get('product_id', False),
            'product_uom_id': x.get('uos_id', False),
            'analytic_account_id': x.get('account_analytic_id', False),
        }

    def action_receipt_create(self):
        """
            main function that is called when trying to create the accounting entries related to an expense
        """
        for eos in self:
            if not eos.employee_id.address_home_id:
                raise UserError(_('The employee must have a home address.'))
            if not eos.employee_id.address_home_id.property_account_payable_id.id:
                raise UserError(_('The employee must have a payable account set on his home address.'))
            company_currency = eos.company_id.currency_id.id
            diff_currency_p = eos.currency_id.id != company_currency
            eml = []
            if not eos.contract_id.structure_type_id.default_struct_id.journal_id:
                raise UserError(_('Please configure employee contract for journal.'))

            move_id = self.env['account.move'].create({
                'journal_id': eos.contract_id.structure_type_id.default_struct_id.journal_id.id,
                'company_id': eos.env.user.company_id.id
            })

            # create the move that will contain the accounting entries
            # ctx = self._context.copy()
            # ctx.update({'force_company': eos.company_id.id})
            # acc = self.env['ir.property'].with_context(ctx).get('property_account_expense_categ_id', 'product.category')
            # if not acc:
            #     raise UserError(_(
            #         'Please configure Default Expense account for Product purchase: `property_account_expense_categ`.'))
            if not self.env.company.eos_expense_account_id:
                raise UserError(_('Please set expense account for eos entry'))
            acc_expense = self.env.company.eos_expense_account_id
            print('account.acc_expense', acc_expense)
            # if not self.env.company.eos_leaves_account_id:
            #     raise UserError(_('Please set leaves account for eos entry'))
            # acc_leaves = self.env.company.eos_leaves_account_id

            acc1 = eos.employee_id.address_home_id.property_account_payable_id if eos.employee_id.address_home_id else False
            price = eos.total_eos + eos.annual_leave_amount
            eml.append({
                'type': 'src',
                'name': eos.name.split('\n')[0][:64],
                'price': price,
                'account_id': acc_expense.id,
                'partner_id': eos.employee_id.address_home_id.id if eos.employee_id.address_home_id else False,
                'date_maturity': eos.date_confirm
            })
            # eml.append({
            #     'type': 'src',
            #     'name': eos.name.split('\n')[0][:64],
            #     'price': eos.annual_leave_amount,
            #     'account_id': acc_leaves.id,
            #     'partner_id': eos.employee_id.address_home_id.id,
            #     'date_maturity': eos.date_confirm
            # })

            total = 0.0
            total -= price
            eml.append({
                'type': 'dest',
                'name': '/',
                'price': total,
                'account_id': acc1.id,
                'date_maturity': eos.date_confirm,
                'amount_currency': diff_currency_p and eos.currency_id.id or False,
                'currency_id': diff_currency_p and eos.currency_id.id or False,
                'partner_id': eos.employee_id.address_home_id.id if eos.employee_id.address_home_id else False,
                'ref': eos.name,
            })

            # convert eml into an osv-valid format
            # lines = map(lambda x:
            #             (0, 0, self.line_get_convert(x, eos.employee_id.address_home_id, eos.date_confirm)), eml)
            vals = []
            print(eml)
            for l in eml:
                vals.append((0, 0, self.line_get_convert(l, eos.employee_id.address_home_id, eos.date_confirm)))
            print('move_id', vals)
            # journal_id = move_obj.browse(cr, uid, move_id, context).journal_id

            # post the journal entry if 'Skip 'Draft' State for Manual Entries' is checked
            # if journal_id.entry_posted:
            #     move_obj.button_validate(cr, uid, [move_id], context)

            move_id.write({
                'line_ids': vals
            })
            print("zzzzzzzzzzzzzzzzzzzzzzzzzz")

            self.write({'account_move_id': move_id.id, 'state': 'done'})
            self.env['account.move.line'].with_context(check_move_validity=False).create(
                {'account_id': self.env.company.eos_leaves_account_id.id,
                 'credit': self.employee_id.monthly_balance_value,
                 'move_id': move_id.id,
                 'partner_id': self.employee_id.address_home_id.id if eos.employee_id.address_home_id else False
                 })
            print("-------------------------------")

            # for usr in self.env.ref('account.group_account_invoice').users:
            #     activity = self.env['mail.activity'].create({
            #         'activity_type_id': self.env.ref("mail.mail_activity_data_todo").id,
            #         'user_id': usr.id,
            #         'res_id': move_id.id,
            #         'res_model_id': self.env['ir.model'].search([('model', '=', 'account.move')], limit=1).id,
            #     })

        return True

    def action_view_receipt(self):
        """
            This function returns an action that display existing account.move of given expense ids.
        """
        assert len(self.ids) == 1, 'This option should only be used for a single id at a time'
        self.ensure_one()
        assert self.account_move_id
        result = {
            'name': _('EOS Account Move'),
            'view_mode': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': self.account_move_id.id,
        }
        return result


class HrJob(models.Model):
    _inherit = 'hr.job'
    _description = 'HR Job'

    annual_leave_rate = fields.Float('Annual Leave Rate', default=2)


class HrEmployeeTermination(models.Model):
    _name = 'hr.employee.termination'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']
    _description = "Termination Indemnity"

    def _get_currency(self):
        """
            return currency of current user
        """
        return self.env.company.currency_id.id

    def _calc_payable_termination(self):
        """
            Calculate the payable eos
        """
        for termination_amt in self:
            termination_amt.payable_eos = (
                                                  termination_amt.total_eos + termination_amt.others + termination_amt.total_remaining_leaves) or 0.0

    name = fields.Char('Description', size=128, required=True, readonly=True,
                       states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    termination_date = fields.Date('Date', index=True, required=True, readonly=True,
                                   states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                                   default=lambda self: datetime.today().date())
    employee_id = fields.Many2one('hr.employee', "Employee", required=True, readonly=True,
                                  states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    date_of_join = fields.Date(related='employee_id.join_date', type="date", string="Joining Date", store=True,
                               readonly=True)
    date_of_leave = fields.Date(string="Leaving Date", default=fields.Date.context_today)
    duration_days = fields.Integer('No of Days', readonly=True,
                                   states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    duration_months = fields.Integer('No of Months', readonly=True,
                                     states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    plan_id = fields.Many2one(comodel_name="hr.boarding.plan", string="Plan")
    duration_years = fields.Integer('No. of Years', readonly=True,
                                    states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    type = fields.Selection([
        ('resignation', 'الاستقالة'),
        ('contract_end', 'انتهاء عقد عمل'),
        ('training_end', 'انهاء خدمات خلال فترة التجربة '),
        ('rule_80', 'انهاء خدمات وفقا للمادة ثامنون '),
    ], 'Type', readonly=True, states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    calc_year = fields.Float('Total Years', readonly=False, )
    payslip_id = fields.Many2one('hr.payslip', 'Payslip', readonly=True)
    current_month_salary = fields.Float('Salary of Current month', readonly=True,
                                        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    others = fields.Float('Others', readonly=True,
                          states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    user_id = fields.Many2one('res.users', 'User', required=True, default=lambda self: self.env.user.id)
    date_confirm = fields.Date('Confirmation Date', index=True,
                               help="Date of the confirmation of the sheet expense. It's filled when the button Confirm is pressed.")
    date_valid = fields.Date('Validation Date', index=True,
                             help="Date of the acceptation of the sheet eos. It's filled when the button Validate is pressed.",
                             readonly=True)
    date_approve = fields.Date('Approve Date', index=True,
                               help="Date of the Approval of the sheet eos. It's filled when the button Approve is pressed.",
                               readonly=True)
    user_valid = fields.Many2one('res.users', 'Validation by', readonly=True,
                                 states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, store=True)
    user_approve = fields.Many2one('res.users', 'Approval by', readonly=True,
                                   states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                                   store=True)
    note = fields.Text('Note')
    annual_leave_amount = fields.Float('Leave Balance', readonly=True,
                                       states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    department_id = fields.Many2one('hr.department', "Department", readonly=True)
    job_id = fields.Many2one('hr.job', 'Job', readonly=True)
    contract_id = fields.Many2one('hr.contract', 'Contract', readonly=True,
                                  states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True,
                                 states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                                 default=lambda self: self.env.company.id)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], 'Status',
                             readonly=False,
                             tracking=True,
                             default='draft',
                             help='When the eos request is created the status is \'Draft\'.\n It is confirmed by the user and request is sent to finance, the status is \'Waiting Confirmation\'.\
        \nIf the finance accepts it, the status is \'Accepted\'.')
    total_eos = fields.Float('Total Award', readonly=True, states={'draft': [('readonly', False)]})

    total_remaining_leaves = fields.Float('Remaining Leaves Award', readonly=True,
                                          states={'draft': [('readonly', False)]})
    payable_eos = fields.Float(compute=_calc_payable_termination, string='Total Amount')
    termination_type_id = fields.Many2one(comodel_name="eos.type", )
    remaining_leave = fields.Float('Remaining Leave')
    # account
    journal_id = fields.Many2one('account.journal', 'Force Journal', help="The journal used when the eos is done.")
    account_move_id = fields.Many2one('account.move', 'Ledger Posting')
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, readonly=True,
                                  states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                                  default=_get_currency)

    def _track_subtype(self, init_values):
        """
            Track Subtypes of EOS
        """
        self.ensure_one()
        if 'state' in init_values and self.state == 'draft':
            return self.env.ref('saudi_hr_eos.mt_employee_termination_new')
        elif 'state' in init_values and self.state == 'confirm':
            # return 'saudi_hr_eos.mt_employee_termination_confirm'
            return self.env.ref('saudi_hr_eos.mt_employee_termination_confirm')
        elif 'state' in init_values and self.state == 'accepted':
            return self.env.ref('saudi_hr_eos.mt_employee_termination_accept')
        elif 'state' in init_values and self.state == 'validate':
            return self.env.ref('saudi_hr_eos.mt_employee_termination_validate')
        elif 'state' in init_values and self.state == 'done':
            return self.env.ref('saudi_hr_eos.mt_employee_termination_done')
        elif 'state' in init_values and self.state == 'cancelled':
            return self.env.ref('saudi_hr_eos.mt_employee_termination_cancel')
        return super(HrEmployeeTermination, self)._track_subtype(init_values)

    def copy(self, default=None):
        """
            Duplicate record
        """
        default = dict(default or {})
        default.update(
            account_move_id=False,
            date_confirm=False,
            date_valid=False,
            date_approve=False,
            user_valid=False)
        return super(HrEmployeeTermination, self).copy(default=default)

    @api.model
    def create(self, values):
        """
            Create a new Record
        """
        if values.get('employee_id'):
            employee = self.env['hr.employee'].browse(values['employee_id'])
            values.update({'job_id': employee.job_id.id,
                           'department_id': employee.department_id.id})
        return super(HrEmployeeTermination, self).create(values)

    def write(self, values):
        """
            update existing record
        """
        if values.get('employee_id'):
            employee = self.env['hr.employee'].browse(values['employee_id'])
            values.update({'job_id': employee.job_id.id,
                           'department_id': employee.department_id.id})
        return super(HrEmployeeTermination, self).write(values)

    def unlink(self):
        """
            Remove record
        """
        for record in self:
            if record.state in ['confirm', 'validate', 'accepted', 'done', 'cancelled']:
                raise UserError(_('You cannot remove the record which is in %s state!') % record.state)
        return super(HrEmployeeTermination, self).unlink()

    @api.onchange('currency_id', 'company_id')
    def onchange_currency_id(self):
        """
            find the journal using currency
        """
        journal_ids = self.env['account.journal'].search(
            [('type', '=', 'purchase'), ('currency_id', '=', self.currency_id.id),
             ('company_id', '=', self.company_id.id)], limit=1)
        if journal_ids:
            self.journal_id = journal_ids[0].id

    def calc_eos(self):
        """
            Calculate eos
        """
        payslip_obj = self.env['hr.payslip']
        for eos in self:
            if not eos.date_of_leave:
                raise UserError(_('Please define employee date of leaving!'))
            diff = relativedelta.relativedelta(eos.date_of_leave, eos.date_of_join)
            duration_days = diff.days
            duration_months = diff.months
            duration_years = diff.years
            work_years = round(duration_years + duration_months / 12 + (duration_days / 30) / 12, 2)
            work_months = round(duration_years * 12 + duration_months + (duration_days / 30), 2)
            eos.write({
                'duration_days': duration_days,
                'duration_months': duration_months,
                'duration_years': duration_years
            })
            selected_month = eos.date_of_leave.month
            selected_year = eos.date_of_leave.year
            date_from = date(selected_year, selected_month, 1)
            date_to = date_from + relativedelta.relativedelta(day=eos.date_of_leave.day)
            contract_ids = self.employee_id._get_contracts(date_from, date_to)
            if not contract_ids:
                raise UserError(_('Please define contract for selected Employee!'))
            if not eos.contract_id.structure_type_id.default_struct_id.journal_id:
                raise UserError(_('Please configure employee contract for journal.'))
            selected_month = eos.termination_date.month
            selected_year = eos.termination_date.year
            date_from = date(selected_year, selected_month, 1)
            # date_to = date_from + relativedelta.relativedelta(day=eos.termination_date.day)
            dates = eos.termination_date
            date_to = datetime(dates.year, dates.month, calendar.mdays[dates.month])
            values = {
                'employee_id': eos.employee_id.id or False,
                'date_from': date_from,
                'date_to': date_to,
                'contract_id': eos.contract_id.id,
                'struct_id': eos.contract_id.structure_type_id.default_struct_id.id or False,
                'journal_id': eos.contract_id.structure_type_id.default_struct_id.journal_id.id or False,
            }
            payslip_name = eos.contract_id.structure_type_id.default_struct_id.payslip_name or _('Salary Slip')
            name = '%s - %s - %s' % (
                payslip_name, self.employee_id.name or '', format_date(self.env, date_from, date_format="MMMM y"))
            values.update({
                'name': name
            })
            if not eos.payslip_id:
                payslip_id = payslip_obj.create(values)
                eos.write({'payslip_id': payslip_id.id})
            eos.payslip_id.compute_sheet()
            net = 0.00
            payslip_line_obj = self.env['hr.payslip.line']
            net_rule_id = payslip_line_obj.search([('slip_id', '=', eos.payslip_id.id),
                                                   ('code', 'ilike', 'NET')])
            if net_rule_id:
                net_rule_obj = net_rule_id[0]
                net = net_rule_obj.total
            eos.write({'current_month_salary': net})
            # print("=======================work_months",work_months)
            wage = 0
            for line in self.contract_id.rule_ids.filtered(lambda r: r.rule_id.is_social_rule):
                wage += line.total_value
            termination_type = self.env['eos.type.line'].search([('eos_type_id', '=', self.termination_type_id.id)],
                                                                order='service_to')
            total_eos = 0
            remaining_months = work_months
            for line in termination_type:
                if remaining_months >= line.service_to:
                    total_eos += wage * line.month_rate * (line.rate / 100) * int(line.service_to / 12)
                    remaining_months -= line.service_to
                elif line.service_from <= work_months <= line.service_to:
                    total_eos += wage * (line.month_rate) * (line.rate / 100) * (remaining_months / 12)
            payable_eos = total_eos
            # TODO: Annual Leave Calc
            # TODO: if eos.employee_id.is_saudi:
            leaves_taken = 0
            time_off_days = 0
            remaining_leaves = 0
            holiday_status_ids = self.env['hr.leave.type'].search([('check_leave', '=', True)])
            # print(holiday_status_ids)
            if holiday_status_ids:

                for recs in holiday_status_ids:
                    leave_values = recs.get_days(eos.employee_id.id)
                    print('recs', leave_values)  # eos.year_id.id
                    leaves_taken = leaves_taken + leave_values[recs[0].id]['leaves_taken']
                    remaining_leaves = remaining_leaves + leave_values[recs[0].id]['remaining_leaves']
                    time_off_days = time_off_days + leave_values[recs[0].id]['time_off_days']
                print('remaining_leaves', remaining_leaves)

                # print('leaves_taken',leaves_taken)
            allocate_leave_days = 0
            # if eos.employee_id.is_saudi:
            diff_date = relativedelta.relativedelta(eos.date_of_leave, eos.date_of_join)
            _logger.info(("allocate_leave_month:{}".format(diff_date.years * 12 + diff_date.months)))
            if not eos.company_id.less_than_five_years:
                raise ValidationError(_("Please set number of days for employees spend less than 5 Years"))
            if diff_date.years < 5 or (diff_date.years == 5 and diff_date.months == 0 and diff_date == 0):
                allocate_leave_days = ((diff_date.years * 12 * 30) + (
                        diff_date.months * 30) + diff_date.days) * (
                                              eos.company_id.less_than_five_years / 360)
            else:
                if not eos.company_id.up_to_five_years:
                    raise ValidationError(_("Please set number of days for employees spend more than 5 Years"))
                years = diff_date.years - 5
                allocate_leave_days = ((5 * 12 * 30) * (eos.company_id.less_than_five_years / 360)) + \
                                      (((years * 12 * 30) + (diff_date.months * 30) + diff_date.days) *
                                       (eos.company_id.up_to_five_years / 360))

                # allocate_leave_month = (diff_date.years * 12 + diff_date.months) * eos.job_id.annual_leave_rate
            # else:
            #     work_back = self.env['hr.work.back'].search(
            #         [('employee_id', '=', eos.employee_id.id), ('company_id', '=', eos.company_id.id),
            #          ('state', '=', 'confirm')], order='date_work_back desc')
            #     if work_back:
            #         work_back = work_back[0]
            #         diff_hireto_date = relativedelta.relativedelta(eos.date_of_leave, eos.date_of_join)
            #         diff_hirefrom_date = relativedelta.relativedelta(work_back.date_work_back, eos.date_of_join)
            #         diff_date = relativedelta.relativedelta(eos.date_of_leave, work_back.date_work_back)
            #         if not eos.company_id.less_than_five_years:
            #             raise ValidationError(_("Please set number of days for employees spend less than 5 Years"))
            #         if diff_hireto_date.years < 5 or (
            #                 diff_hireto_date.years == 5 and diff_hireto_date.months == 0 and diff_hireto_date == 0):
            #             allocate_leave_days = ((diff_date.years * 12 * 30) + (
            #                     diff_date.months * 30) + diff_date.days) * (
            #                                           eos.company_id.less_than_five_years / 360)
            #         else:
            #             if not eos.company_id.up_to_five_years:
            #                 raise ValidationError(
            #                     _("Please set number of days for employees spend more than 5 Years"))
            #             hire_five = eos.date_of_join.year + 5
            #             hire_after_five = eos.date_of_join.replace(year=hire_five)
            #             if hire_after_five > work_back.date_work_back:
            #                 diff_hirefive_workback = relativedelta.relativedelta(hire_after_five,
            #                                                                      work_back.date_work_back)
            #                 diff_hirefive_workback_days = ((diff_hirefive_workback.years * 360) + (
            #                         diff_hirefive_workback.months * 30) + diff_hirefive_workback.days)
            #                 diff_hirefive_workback_amount = diff_hirefive_workback_days * (
            #                         eos.company_id.less_than_five_years / 360)
            #
            #                 diff_hirefive_leave = relativedelta.relativedelta(eos.date_of_leave, hire_after_five)
            #                 diff_hirefive_leave_days = ((diff_hirefive_leave.years * 360) + (
            #                         diff_hirefive_leave.months * 30) + diff_hirefive_leave.days)
            #                 diff_hirefive_leave_days_amount = diff_hirefive_leave_days * (
            #                         eos.company_id.up_to_five_years / 360)
            #
            #                 allocate_leave_days = diff_hirefive_workback_amount + diff_hirefive_leave_days_amount
            #             else:
            #                 allocate_leave_days = ((diff_date.years * 12 * 30) + (
            #                         diff_date.months * 30) + diff_date.days) * (
            #                                               eos.company_id.up_to_five_years / 360)
            #     else:
            #         raise ValidationError(_("No Work Back for employee"))
            total_termination_years = eos.duration_years * 12
            total_termination_month = eos.duration_months
            total_termination_days = eos.duration_days / 30
            employee_mounthly_balance = eos.employee_id.monthly_balance if eos.employee_id.monthly_balance else 0
            total_termination_sum = (
                                                total_termination_years + total_termination_month + total_termination_days) * employee_mounthly_balance

            print('total_termination_years', total_termination_years, 'total_termination_month',
                  total_termination_month, 'total_termination_days', total_termination_days)
            print('total_termination_sum', total_termination_sum)
            print('remaining_leaves', remaining_leaves,
                  'leaves_taken', leaves_taken,
                  'employee_mounthly_balance', employee_mounthly_balance)
            total_remaining_leaves = 0
            # remaining_leaves = allocate_leave_days - leaves_taken
            # print('alooc',allocate_leave_days)
            # print('leave',leave_values)
            if remaining_leaves > 0:
                total_remaining_leaves = remaining_leaves * eos.contract_id.day_value
            #
            remaining_leaves_days = total_termination_sum - leaves_taken
            if remaining_leaves_days > 0:
                total_remaining_leaves = remaining_leaves_days * eos.contract_id.day_value
            print('total_remaining_leaves', total_remaining_leaves)
            # else:
            #     total_remaining_leaves = remaining_leaves * eos.contract_id.day_value
            annual_leave_amount = eos.employee_id.contract_id.day_value * remaining_leaves_days
            eos.write({
                'total_eos': payable_eos,
                'annual_leave_amount': annual_leave_amount,
                'remaining_leave': remaining_leaves_days,
                'total_remaining_leaves': total_remaining_leaves
            })
            return True

    @api.onchange('employee_id', 'termination_date')
    def onchange_employee_id(self):
        """
            Calculate total no of year, month, days, etc depends on employee
        """
        if self.employee_id:
            if not self.date_of_leave:
                raise UserError(_('Please define employee date of leaving!'))
            if not self.employee_id.join_date:
                raise UserError(_('Please define employee date of join!'))
            selected_date = self.date_of_leave
            date_from = date(selected_date.year, selected_date.month, 1)
            date_to = date_from + relativedelta.relativedelta(day=selected_date.day)
            contract_ids = self.employee_id._get_contracts(date_from=date_from, date_to=date_to)
            if not contract_ids:
                raise UserError(_('Please define contract for selected Employee!'))
            calc_years = round(((self.date_of_leave - self.employee_id.join_date).days / 365.0), 2)
            diff = relativedelta.relativedelta(self.date_of_leave, self.employee_id.join_date)

            self.contract_id = contract_ids[0]
            if self.employee_id.date_of_leave:
                self.date_of_leave = self.employee_id.date_of_leave
            self.date_of_join = self.employee_id.join_date
            self.calc_year = calc_years
            self.department_id = self.employee_id.department_id.id or False
            self.company_id = self.employee_id.company_id.id or False
            self.job_id = self.employee_id.sudo().job_id.id or False
            self.duration_years = diff.years or 0
            self.duration_months = diff.months or 0
            self.duration_days = diff.days or 0

    def termination_draft(self):
        """
            EOS set to draft state
        """
        self.ensure_one()
        self.state = 'draft'
        self.message_post(subtype_id=self.env.ref('mail.mt_comment').id, body=_('Termination Draft.'))

    def action_approve(self):
        for rec in self:
            if rec.state == 'draft':
                self.message_post(subtype_id=self.env.ref('mail.mt_comment').id, body=_('Termination Confirmed.'))
            if rec.state == 'confirm':
                self.message_post(subtype_id=self.env.ref('mail.mt_comment').id, body=_('Termination Validated.'))
            if rec.state == 'validate':
                self.message_post(subtype_id=self.env.ref('mail.mt_comment').id, body=_('Termination Approved.'))
            self.env['gosi.eos'].create({
                'project_id': rec.employee_id.project_id.id,
                'employee_id': rec.employee_id.id,
                'company_id': rec.employee_id.company_id.id,
                # 'number': rec.employee_id.gosi_number,
                'start_date': rec.termination_date,
                'state': 'draft',
            })
            if rec.plan_id:
                activity_mail_template = self.env.ref('archer_recruitment.mail_template_new_activity')
                for activity in rec.plan_id.activity_ids:
                    employee_plan_lines = {
                        'boarding_plan_id': rec.plan_id.id,
                        'name': activity.id,
                        'no_of_days': activity.no_of_days,
                        'user_id': activity.user_id.id,
                        'employee_id': rec.employee_id.id,
                        'assign_date': datetime.now().date(),
                        'done_date': False,
                        'deadline_date': datetime.now().date() + timedelta(days=activity.no_of_days),
                    }
                    self.env['hr.boarding.plan.employee'].create(employee_plan_lines)
                    email_values = {
                        'email_to': activity.user_id.email,
                        'subject': 'Offboarding Employee',
                    }
                    activity_mail_template.with_context(user_name=activity.user_id.name, activity_name=activity.name,
                                                        employee_name=rec.employee_id.name).send_mail(rec.id,
                                                                                                      force_send=True,
                                                                                                      raise_exception=True,
                                                                                                      email_values=email_values)
            super(HrEmployeeTermination, self).action_approve()

    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    def action_reject(self, reason=None):
        self.write({'state': 'rejected'})
        if reason:
            self.message_post(body=reason, subject="Reject Reason")
        self.message_post(subtype_id=self.env.ref('mail.mt_comment').id, body=_('EOS Cancelled.'))

    def account_move_get(self):
        """
            This method prepare the creation of the account move related to the given expense.

            :param termination_id: Id of voucher for which we are creating account_move.
            :return: mapping between field name and value of account move to create
            :rtype: dict
        """
        self.ensure_one()
        journal_obj = self.env['account.journal']
        company_id = self.company_id.id
        date = self.date_confirm
        ref = self.name
        if self.journal_id:
            journal_id = self.journal_id.id
        else:
            journal_id = journal_obj.search([('type', '=', 'purchase'), ('company_id', '=', company_id)])
            if not journal_id:
                raise UserError(_("No EOS journal found. "
                                  "Please make sure you have a journal with type 'purchase' configured."))
            journal_id = journal_id[0].id
        return self.env['account.move'].account_move_prepare(journal_id, date=date, ref=ref, company_id=company_id)

    def line_get_convert(self, x, part, date):
        """
            line get convert
        """
        partner_id = self.env['res.partner']._find_accounting_partner(part).id
        return {
            'date_maturity': x.get('date_maturity', False),
            'partner_id': partner_id,
            'name': x['name'][:64],
            'date': date,
            'debit': x['price'] > 0 and x['price'],
            'credit': x['price'] < 0 and -x['price'],
            'account_id': x['account_id'],
            # 'analytic_lines': x.get('analytic_lines', False),
            'amount_currency': x['price'] > 0 and abs(x.get('amount_currency', False)) or -abs(
                x.get('amount_currency', False)),
            'currency_id': x.get('currency_id', False),
            # 'tax_code_id': x.get('tax_code_id', False),
            # 'tax_amount': x.get('tax_amount', False),
            'ref': x.get('ref', False),
            'quantity': x.get('quantity', 1.00),
            'product_id': x.get('product_id', False),
            'product_uom_id': x.get('uos_id', False),
            'analytic_account_id': x.get('account_analytic_id', False),
        }

    def action_receipt_create(self):
        """
            main function that is called when trying to create the accounting entries related to an expense
        """
        for eos in self:
            if not eos.employee_id.address_home_id:
                raise UserError(_('The employee must have a home address.'))
            if not eos.employee_id.address_home_id.property_account_payable_id.id:
                raise UserError(_('The employee must have a payable account set on his home address.'))
            company_currency = eos.company_id.currency_id.id
            diff_currency_p = eos.currency_id.id != company_currency
            eml = []
            if not eos.contract_id.structure_type_id.default_struct_id.journal_id:
                raise UserError(_('Please configure employee contract for journal.'))

            move_id = self.env['account.move'].create({
                'journal_id': eos.contract_id.structure_type_id.default_struct_id.journal_id.id,
                'company_id': eos.env.user.company_id.id
            })

            # create the move that will contain the accounting entries
            # ctx = self._context.copy()
            # ctx.update({'force_company': eos.company_id.id})
            # acc = self.env['ir.property'].with_context(ctx).get('property_account_expense_categ_id', 'product.category')
            # if not acc:
            #     raise UserError(_(
            #         'Please configure Default Expense account for Product purchase: `property_account_expense_categ`.'))
            if not self.env.company.termination_expense_account_id:
                raise UserError(_('Please set expense account for eos entry'))
            acc_expense = self.env.company.termination_expense_account_id
            print('account.acc_expense', acc_expense)
            # if not self.env.company.termination_leaves_account_id:
            #     raise UserError(_('Please set leaves account for eos entry'))
            # acc_leaves = self.env.company.termination_leaves_account_id

            acc1 = eos.employee_id.address_home_id.property_account_payable_id if eos.employee_id.address_home_id else False
            price = eos.total_eos + eos.annual_leave_amount
            eml.append({
                'type': 'src',
                'name': eos.name.split('\n')[0][:64],
                'price': price,
                'account_id': acc_expense.id,
                'partner_id': eos.employee_id.address_home_id.id if eos.employee_id.address_home_id else False,
                'date_maturity': eos.date_confirm
            })
            # eml.append({
            #     'type': 'src',
            #     'name': eos.name.split('\n')[0][:64],
            #     'price': eos.annual_leave_amount,
            #     'account_id': acc_leaves.id,
            #     'partner_id': eos.employee_id.address_home_id.id,
            #     'date_maturity': eos.date_confirm
            # })

            total = 0.0
            total -= price
            eml.append({
                'type': 'dest',
                'name': '/',
                'price': total,
                'account_id': acc1.id,
                'date_maturity': eos.date_confirm,
                'amount_currency': diff_currency_p and eos.currency_id.id or False,
                'currency_id': diff_currency_p and eos.currency_id.id or False,
                'partner_id': eos.employee_id.address_home_id.id if eos.employee_id.address_home_id else False,
                'ref': eos.name,
            })

            # convert eml into an osv-valid format
            # lines = map(lambda x:
            #             (0, 0, self.line_get_convert(x, eos.employee_id.address_home_id, eos.date_confirm)), eml)
            vals = []
            print(eml)
            for l in eml:
                vals.append((0, 0, self.line_get_convert(l, eos.employee_id.address_home_id, eos.date_confirm)))
            print('move_id', vals)
            # journal_id = move_obj.browse(cr, uid, move_id, context).journal_id

            # post the journal entry if 'Skip 'Draft' State for Manual Entries' is checked
            # if journal_id.entry_posted:
            #     move_obj.button_validate(cr, uid, [move_id], context)

            move_id.write({
                'line_ids': vals
            })
            print("zzzzzzzzzzzzzzzzzzzzzzzzzz")

            self.write({'account_move_id': move_id.id, 'state': 'done'})
            self.env['account.move.line'].with_context(check_move_validity=False).create(
                {'account_id': self.env.company.termination_leaves_account_id.id,
                 'credit': self.employee_id.monthly_balance_value,
                 'move_id': move_id.id,
                 'partner_id': self.employee_id.address_home_id.id if eos.employee_id.address_home_id else False
                 })
            print("-------------------------------")

            # for usr in self.env.ref('account.group_account_invoice').users:
            #     activity = self.env['mail.activity'].create({
            #         'activity_type_id': self.env.ref("mail.mail_activity_data_todo").id,
            #         'user_id': usr.id,
            #         'res_id': move_id.id,
            #         'res_model_id': self.env['ir.model'].search([('model', '=', 'account.move')], limit=1).id,
            #     })

        return True

    def action_view_receipt(self):
        """
            This function returns an action that display existing account.move of given expense ids.
        """
        assert len(self.ids) == 1, 'This option should only be used for a single id at a time'
        self.ensure_one()
        assert self.account_move_id
        result = {
            'name': _('EOS Account Move'),
            'view_mode': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': self.account_move_id.id,
        }
        return result
