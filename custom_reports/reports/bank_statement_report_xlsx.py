# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api
import datetime
from datetime import date


class BankStatementReport(models.AbstractModel):
    _name = 'report.custom_reports.bank_statement_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, penality):
        sheet = workbook.add_worksheet('  Bank Statement Report ')
        cell_format = workbook.add_format()
        cell_format.set_font_size(12)
        cell_format.set_bold()
        # cell_format.set_text_wrap()
        cell_format.set_align('center')
        cell_format.set_align('vcenter')

        body_format = workbook.add_format()
        body_format.set_font_size(14)
        body_format.set_align('center')
        body_format.set_align('vcenter')
        # body_format.set_bold()
        body_format.set_bg_color('#187f1b')
        body_format.set_font_color('white')

        off_format = workbook.add_format()
        off_format.set_font_size(14)
        off_format.set_align('center')
        off_format.set_align('vcenter')
        # off_format.set_bold()
        off_format.set_bg_color('#d1e0a8')
        off_format.set_font_color('black')
        # body_format.set_text_wrap()
        sheet.set_column('A:Z', 20)

        row = 0
        col = 0

        for head in data['header']:
            sheet.write(row, col, head, body_format)
            col += 1

        row = 1
        col = 0
        for rr in data['second_row']:
            sheet.write(row, col, rr, cell_format)
            col += 1
        row = 2
        col = 0
        sheet.write(row, col, 'SN', body_format)
        sheet.write(row, col+1, 'هوية المستفيد/ المرجع', body_format)
        sheet.write(row, col+2, 'المستفيد / اسم الموظف', body_format)
        sheet.write(row, col+3, 'رقم الحساب', body_format)
        sheet.write(row, col+4, 'رمز البنك', body_format)
        sheet.write(row, col+5, 'إجمالي المبلغ', body_format)

        sheet.write(row, col+6, 'الراتب الأساسي', off_format)
        sheet.write(row, col+7, 'بدل السكن', off_format)
        sheet.write(row, col+8, 'دخل آخر', off_format)
        sheet.write(row, col+9, 'الخصومات', off_format)

        sheet.write(row, col+10, 'العنوان', body_format)
        sheet.write(row, col+11, 'العملة', body_format)
        sheet.write(row, col+12, 'الحالة', body_format)
        sheet.write(row, col+13, 'وصف الدفع', body_format)
        sheet.write(row, col+14, 'مرجع الدفع', body_format)

        row = 3
        col = 0
        for emp_row in data['all_emps']:
            sheet.write(row, col, emp_row['seq'], cell_format)
            sheet.write(row, col + 1, emp_row['emp_id'], cell_format)
            sheet.write(row, col + 2, emp_row['emp_name'], cell_format)
            sheet.write(row, col + 3, emp_row['account_num'], cell_format)
            sheet.write(row, col + 4, emp_row['bank_symbol'], cell_format)
            sheet.write(row, col + 5, emp_row['total'], cell_format)
            sheet.write(row, col + 6, emp_row['basic'], cell_format)
            sheet.write(row, col + 7, emp_row['home_allowance'], cell_format)
            sheet.write(row, col + 8, emp_row['another_income'], cell_format)
            sheet.write(row, col + 9, emp_row['deductions'], cell_format)
            sheet.write(row, col + 10, emp_row['address'], cell_format)
            sheet.write(row, col + 11, emp_row['currency'], cell_format)
            sheet.write(row, col + 12, emp_row['status'], cell_format)
            sheet.write(row, col + 13, emp_row['payment_type'], cell_format)
            sheet.write(row, col + 14, emp_row['payment_ref'], cell_format)
            row += 1
