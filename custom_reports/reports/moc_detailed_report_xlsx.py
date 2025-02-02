# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api
import datetime
from datetime import date


class MOCDETAILEDXLSX(models.AbstractModel):
    _name = 'report.custom_reports.moc_detailed_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, penality):
        sheet = workbook.add_worksheet('  MOC Detailed Report ' + '')
        cell_format = workbook.add_format()
        cell_format.set_font_size(12)
        cell_format.set_bold()
        # cell_format.set_text_wrap()
        cell_format.set_align('left')
        cell_format.set_align('vcenter')

        body_format = workbook.add_format()
        body_format.set_font_size(12)
        body_format.set_align('left')
        body_format.set_align('vcenter')

        left_format = workbook.add_format({'align': 'left', 'font_size': '12px', 'bold': True, })
        left_format.set_border(2)

        border_format = workbook.add_format({'align': 'center', 'font_size': '12px', 'bold': True, })
        border_format.set_border(2)

        normal_format = workbook.add_format({'align': 'center', 'font_size': '12px', })
        normal_format.set_bottom(0)
        normal_format.set_top(0)
        normal_format.set_left(2)
        normal_format.set_right(2)

        sheet.set_column('A:C', 20)
        row = 0
        col = 0
        # sheet.write(row, col, 'Pay Period', cell_format)

        sheet.merge_range('A1:B1', 'Pay Period    ' + data['period'], left_format)
        sheet.merge_range('A2:K2', ' ', left_format)
        sheet.merge_range('L2:N2', 'Period', left_format)
        sheet.merge_range('O2:V2', 'Salary information', left_format)
        sheet.merge_range('W2:AG2', 'Earning', left_format)
        sheet.merge_range('AH2:AI2', 'Deduction', left_format)
        sheet.write('AJ2', 'Net', left_format)
        sheet.merge_range('AK2:AL2', 'Cost', left_format)

        row = 2
        col = 0
        for head in data['header']:
            sheet.write(row, col, head, border_format)
            col += 1

        row = 3
        col = 0
        for emp_row in data['all_emps']:
            sheet.write(row, col, emp_row['seq'], normal_format)
            sheet.write(row, col + 1, emp_row['emp_company_id'], normal_format)
            sheet.write(row, col + 2, emp_row['emp_name'], normal_format)
            sheet.write(row, col + 3, emp_row['emp_id'], normal_format)
            sheet.write(row, col + 4, emp_row['emp_parent_department'], normal_format)
            sheet.write(row, col + 5, emp_row['emp_department'], normal_format)
            sheet.write(row, col + 6 , emp_row['project'], normal_format)
            sheet.write(row, col + 7, emp_row['emp_project_dep_ar'], normal_format)
            sheet.write(row, col + 8, emp_row['emp_project_dep_en'], normal_format)
            sheet.write(row, col + 9, emp_row['emp_initial_date'], normal_format)
            sheet.write(row, col +10, emp_row['emp_work_days'], normal_format)
            sheet.write(row, col + 11, emp_row['gosi_company_name'], normal_format)
            sheet.write(row, col + 12, emp_row['days_adjustment'], normal_format)
            sheet.write(row, col + 13, emp_row['exact_gosi_adjustment'], normal_format)
            sheet.write(row, col + 14, emp_row['basic'], normal_format)
            sheet.write(row, col + 15, emp_row['housing_allowance_other'], normal_format)
            sheet.write(row, col + 16, emp_row['transportation_allowance_other'], normal_format)
            sheet.write(row, col + 17, emp_row['cost_of_living'], normal_format)
            sheet.write(row, col + 18, emp_row['cost_of_living_allowance'], normal_format)
            sheet.write(row, col + 19, emp_row['phone_allowance_other'], normal_format)
            sheet.write(row, col + 20, emp_row['other_allowance_other'], normal_format)
            sheet.write(row, col + 21, emp_row['gross'], normal_format)
            sheet.write(row, col + 22, emp_row['first_payslips'], normal_format)
            sheet.write(row, col + 23, emp_row['first_month_last_day'], normal_format)
            sheet.write(row, col + 24, emp_row['current_months_days'], normal_format)
            sheet.write(row, col + 25, emp_row['previous_days'], normal_format)
            sheet.write(row, col + 26, emp_row['basic_net'], normal_format)
            sheet.write(row, col + 27, emp_row['housing_allowance_other_net'], normal_format)
            sheet.write(row, col + 28, emp_row['transportation_allowance_other_net'], normal_format)
            sheet.write(row, col + 29, emp_row['phone_allowance_other_net'], normal_format)
            sheet.write(row, col + 30, emp_row['cost_of_living_allowance_net'], normal_format)
            sheet.write(row, col + 31, emp_row['other_allowance_other_net'], normal_format)
            sheet.write(row, col + 32, emp_row['total_earning'], normal_format)
            sheet.write(row, col + 33, emp_row['employee_gosi'], normal_format)
            sheet.write(row, col + 34, emp_row['other_deductions'], normal_format)
            sheet.write(row, col + 35, emp_row['basic_net_3'], normal_format)
            sheet.write(row, col + 36, emp_row['company_gosi'], normal_format)
            sheet.write(row, col + 37, emp_row['total_cost'], normal_format)
            sheet.write(row, col + 38, emp_row['bank_name'], normal_format)
            sheet.write(row, col + 39, emp_row['iban'], normal_format)

            row += 1
        for i in range(1, 250):
            sheet.write(row, col, '', normal_format)
            sheet.write(row, col + 1, '', normal_format)
            sheet.write(row, col + 2, '', normal_format)
            sheet.write(row, col + 3, '', normal_format)
            sheet.write(row, col + 4, '', normal_format)
            sheet.write(row, col + 5, '', normal_format)
            sheet.write(row, col + 6, '', normal_format)
            sheet.write(row, col + 7, '', normal_format)
            sheet.write(row, col + 8, '', normal_format)
            sheet.write(row, col + 9, '', normal_format)
            sheet.write(row, col + 10, '', normal_format)
            sheet.write(row, col + 11, '', normal_format)
            sheet.write(row, col + 12, '', normal_format)
            sheet.write(row, col + 13, '', normal_format)
            sheet.write(row, col + 14, '', normal_format)
            sheet.write(row, col + 15, '', normal_format)
            sheet.write(row, col + 16, '', normal_format)
            sheet.write(row, col + 17, '', normal_format)
            sheet.write(row, col + 18, '', normal_format)
            sheet.write(row, col + 19, '', normal_format)
            sheet.write(row, col + 20, '', normal_format)
            sheet.write(row, col + 21, '', normal_format)
            sheet.write(row, col + 22, '', normal_format)
            sheet.write(row, col + 23, '', normal_format)
            sheet.write(row, col + 24, '', normal_format)
            sheet.write(row, col + 25, '', normal_format)
            sheet.write(row, col + 26, '', normal_format)
            sheet.write(row, col + 27, '', normal_format)
            sheet.write(row, col + 28, '', normal_format)
            sheet.write(row, col + 29, '', normal_format)
            sheet.write(row, col + 30, '', normal_format)
            sheet.write(row, col + 31, '', normal_format)
            sheet.write(row, col + 32, '', normal_format)
            sheet.write(row, col + 33, '', normal_format)
            sheet.write(row, col + 34, '', normal_format)
            sheet.write(row, col + 35, '', normal_format)
            sheet.write(row, col + 36, '', normal_format)
            sheet.write(row, col + 37, '', normal_format)
            sheet.write(row, col + 38, '', normal_format)
            sheet.write(row, col + 39, '', normal_format)
            row += 1
