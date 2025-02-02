from odoo import api, fields, models,_
from datetime import datetime, time, timedelta
from collections import defaultdict
from odoo.tools.date_utils import get_timedelta
from dateutil.relativedelta import relativedelta


class HolidayAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    # def _process_accrual_plans(self):
    #     """
    #     This method is part of the cron's process.
    #     The goal of this method is to retroactively apply accrual plan levels and progress from nextcall to today
    #     """
    #     today = fields.Date.today()
    #     first_allocation = _("""This allocation have already ran once, any modification won't be effective to the days allocated to the employee. If you need to change the configuration of the allocation, cancel and create a new one.""")
    #     for allocation in self:
    #         level_ids = allocation.accrual_plan_id.level_ids.sorted('sequence')
    #         if not level_ids:
    #             continue
    #         if not allocation.nextcall:
    #             first_level = level_ids[0]
    #             first_level_start_date = allocation.date_from + get_timedelta(first_level.start_count, first_level.start_type)
    #             print("@@@@@@@@@@@@@@@@@@@@@@@@first_level_start_date",first_level_start_date)
    #             if today < first_level_start_date:
    #                 # Accrual plan is not configured properly or has not started
    #                 continue
    #             allocation.lastcall = max(allocation.lastcall, first_level_start_date)
    #             allocation.nextcall = first_level._get_next_date(allocation.lastcall)
    #             allocation._message_log(body=first_allocation)
    #         days_added_per_level = defaultdict(lambda: 0)
    #         while allocation.nextcall <= today:
    #             (current_level, current_level_idx) = allocation._get_current_accrual_plan_level_id(allocation.nextcall)
    #             nextcall = current_level._get_next_date(allocation.nextcall)
    #             # Since _get_previous_date returns the given date if it corresponds to a call date
    #             # this will always return lastcall except possibly on the first call
    #             # this is used to prorate the first number of days given to the employee
    #             period_start = current_level._get_previous_date(allocation.lastcall)
    #             print("---------------------period_start",period_start)
    #             period_end = current_level._get_next_date(allocation.lastcall)
    #             print("---------------------period_end",period_end)
    #             # Also prorate this accrual in the event that we are passing from one level to another
    #             if current_level_idx < (len(level_ids) - 1) and allocation.accrual_plan_id.transition_mode == 'immediately':
    #                 next_level = level_ids[current_level_idx + 1]
    #                 current_level_last_date = allocation.date_from + get_timedelta(next_level.start_count, next_level.start_type) - relativedelta(days=1)
    #                 if allocation.nextcall != current_level_last_date:
    #                     nextcall = min(nextcall, current_level_last_date)
    #             days_added_per_level[current_level] += allocation._process_accrual_plan_level(
    #                 current_level, period_start, allocation.lastcall, period_end, allocation.nextcall)
    #             allocation.lastcall = allocation.nextcall
    #             allocation.nextcall = nextcall
    #         if days_added_per_level:
    #             print("-----------------days_added_per_level",days_added_per_level)
    #             number_of_days_to_add = 0
    #             for value in days_added_per_level.values():
    #                 number_of_days_to_add += value
    #             # Let's assume the limit of the last level is the correct one
    #             allocation.write({'number_of_days': min(allocation.number_of_days + number_of_days_to_add, current_level.maximum_leave)})

    def _end_of_year_accrual(self):
        # to override in payroll
        first_day_this_year = fields.Date.today() + relativedelta(month=1, day=1)
        for allocation in self:
            current_level = allocation._get_current_accrual_plan_level_id(first_day_this_year)[0]
            if current_level and current_level.action_with_unused_accruals == 'lost':
                lastcall = current_level._get_previous_date(first_day_this_year)
                nextcall = current_level._get_next_date(first_day_this_year)
                if lastcall == first_day_this_year:
                    lastcall = current_level._get_previous_date(first_day_this_year - relativedelta(days=1))
                    nextcall = first_day_this_year
                # Allocations are lost but number_of_days should not be lower than leaves_taken
                allocation.write({'number_of_days': allocation.leaves_taken, 'lastcall': lastcall, 'nextcall': nextcall})
            elif current_level and current_level.action_with_unused_accruals == 'postponed_amount':
                lastcall = current_level._get_previous_date(first_day_this_year)
                nextcall = current_level._get_next_date(first_day_this_year)
                if lastcall == first_day_this_year:
                    lastcall = current_level._get_previous_date(first_day_this_year - relativedelta(days=1))
                    nextcall = first_day_this_year
                no_of_days = allocation.number_of_days
                if no_of_days > allocation.employee_id.project_id.no_of_allocation_days:
                    no_of_days = allocation.employee_id.project_id.no_of_allocation_days
                # Allocations are lost but number_of_days should not be lower than leaves_taken
                allocation.write({'number_of_days': no_of_days, 'lastcall': lastcall, 'nextcall': nextcall})

    # @api.model
    # def _update_accrual(self):
    #     """
    #         Method called by the cron task in order to increment the number_of_days when
    #         necessary.
    #     """
    #     # Get the current date to determine the start and end of the accrual period
    #     today = datetime.combine(fields.Date.today(), time(0, 0, 0))
    #     current_academic_year = self.env['academic.year'].search([('current','=',True)],limit=1)
    #     if today.day == current_academic_year.date_start.day and today.month == current_academic_year.date_start.month:
    #         end_of_year_allocations = self.search(
    #             [('allocation_type', '=', 'accrual'), ('state', '=', 'validate'), ('accrual_plan_id', '!=', False),
    #              ('employee_id', '!=', False),
    #              '|', ('date_to', '=', False), ('date_to', '>', fields.Datetime.now())])
    #         end_of_year_allocations._end_of_year_accrual()
    #         end_of_year_allocations.flush()
    #     allocations = self.search(
    #         [('allocation_type', '=', 'accrual'), ('state', '=', 'validate'), ('accrual_plan_id', '!=', False),
    #          ('employee_id', '!=', False),
    #          '|', ('date_to', '=', False), ('date_to', '>', fields.Datetime.now()),
    #          ])
    #     allocations._process_accrual_plans()
