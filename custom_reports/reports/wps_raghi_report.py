# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api
import datetime
from datetime import date


class BankStatementReport(models.AbstractModel):
    _name = 'report.custom_reports.wps_raghi'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, penality):
        sheet = workbook.add_worksheet('Bank Rajhi WPS ')
        cell_format = workbook.add_format()
        cell_format.set_font_size(12)
        cell_format.set_font_color('white')
        cell_format.set_bg_color('#1e1d7f')
        cell_format.set_align('center')
        cell_format.set_align('vcenter')
        cell_format.set_underline()

        pure_format = workbook.add_format()
        pure_format.set_font_size(12)
        pure_format.set_align('center')
        pure_format.set_align('vcenter')

        row = 0
        col = 0
        sheet.set_column('A:Z', 30)
        sheet.set_column('C:C', 50)
        sheet.write(row, col, 'Bank Name', cell_format)
        sheet.write(row, col + 1, 'Account Number(34N)', cell_format)
        sheet.write(row, col + 2, 'Employee Name', cell_format)
        sheet.write(row, col + 3, 'Employee Number', cell_format)
        sheet.write(row, col + 4, 'National ID Number (15N)', cell_format)
        sheet.write(row, col + 5, 'Salary (15N)', cell_format)
        sheet.write(row, col + 6, 'Basic Salary', cell_format)
        sheet.write(row, col + 7, 'Housing Allowance', cell_format)
        sheet.write(row, col + 8, 'Other Earnings', cell_format)
        sheet.write(row, col + 9, 'Deductions', cell_format)
        sheet.write(row, col + 10, 'Branch Code', cell_format)
        sheet.write(row, col + 11, 'Branch Name', cell_format)
        sheet.write(row, col + 12, 'Employee Remarks', cell_format)
        sheet.write(row, col + 13, 'Employee Department', cell_format)
        row = 1
        col = 0
        sheet.write(row, col, '', cell_format)
        sheet.write(row, col + 1, '', cell_format)
        sheet.write(row, col + 2, 'إسم الموظف', cell_format)
        sheet.write(row, col + 3, 'الرقم الوظيفي', cell_format)
        sheet.write(row, col + 4, 'رقم الهوية', cell_format)
        sheet.write(row, col + 5, 'الراتب', cell_format)
        sheet.write(row, col + 6, 'الراتب الأساسي', cell_format)
        sheet.write(row, col + 7, 'بدل السكن', cell_format)
        sheet.write(row, col + 8, 'بدل أخرى', cell_format)
        sheet.write(row, col + 9, 'الخصومات', cell_format)
        sheet.write(row, col + 10, 'رمز الفرع', cell_format)
        sheet.write(row, col + 11, 'اسم الفرع', cell_format)
        sheet.write(row, col + 12, 'ملاحظات الموظف', cell_format)
        sheet.write(row, col + 13, 'قسم الموظف', cell_format)

        row = 2
        col = 0
        for emp_row in data['all_emps']:
            sheet.write(row, col,  emp_row['bank_name'], pure_format)
            sheet.write(row, col + 1,  emp_row['iban'], pure_format)
            sheet.write(row, col + 2, emp_row['emp_name'], pure_format)
            sheet.write(row, col + 3, '', pure_format)
            sheet.write(row, col + 4, emp_row['emp_id'], pure_format)
            sheet.write(row, col + 5, emp_row['net'], pure_format)
            sheet.write(row, col + 6, emp_row['basic'], pure_format)
            sheet.write(row, col + 7, emp_row['home_allowance'], pure_format)
            sheet.write(row, col + 8, emp_row['another_earnings'], pure_format)
            sheet.write(row, col + 9, emp_row['deductions'], pure_format)
            sheet.write(row, col + 10, ' ', pure_format)
            sheet.write(row, col + 11, ' ', pure_format)
            sheet.write(row, col + 12, ' ', pure_format)
            sheet.write(row, col + 13, emp_row['emp_department'], pure_format)
            row += 1
