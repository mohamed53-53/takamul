# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api
import datetime
from datetime import date


class BankStatementReport(models.AbstractModel):
    _name = 'report.custom_reports.final_settlement'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, penality):
        sheet = workbook.add_worksheet('Final Settlement Report ')
        cell_format = workbook.add_format()
        cell_format.set_font_size(12)
        cell_format.set_bold()
        # cell_format.set_text_wrap()
        cell_format.set_align('center')
        cell_format.set_align('vcenter')

        body_format = workbook.add_format()
        body_format.set_font_size(20)
        body_format.set_bold()
        body_format.set_align('center')
        body_format.set_align('vcenter')


        sheet.merge_range("F2:M2", 'FINAL SETTLEMENT FORM', body_format)

        row = 4
        col = 0
        # for rr in data['second_row']:
        #     sheet.write(row, col, rr, cell_format)
        #     col += 1
        # row = 2
        # col = 0
        sheet.write(row, col, 'SN', body_format)
        sheet.write(row, col+1, 'هوية المستفيد/ المرجع', body_format)
        sheet.write(row, col+2, 'المستفيد / اسم الموظف', body_format)
        sheet.write(row, col+3, 'رقم الحساب', body_format)
        sheet.write(row, col+4, 'رمز البنك', body_format)
        sheet.write(row, col+5, 'إجمالي المبلغ', body_format)

        row = 3
        col = 0
        # for emp_row in data['all_emps']:
        #     sheet.write(row, col, emp_row['seq'], cell_format)
        #     sheet.write(row, col + 1, emp_row['emp_id'], cell_format)
        #     sheet.write(row, col + 2, emp_row['emp_name'], cell_format)
        #     sheet.write(row, col + 3, emp_row['account_num'], cell_format)
        #     sheet.write(row, col + 4, emp_row['bank_symbol'], cell_format)
        #     sheet.write(row, col + 5, emp_row['total'], cell_format)
        #     sheet.write(row, col + 6, emp_row['basic'], cell_format)
        #     row += 1
