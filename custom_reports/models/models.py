import re
from odoo import models, fields, api
import re


class MOCDetailedReport(models.TransientModel):
    _name = 'moc.detailed.report'

    date = fields.Date(string="Date", required=True, )

    def get_lang(self, data):
        if data.get('form', False) and data['form'].get('lang_id', False):
            # print 'iam in get lang', data['form'].get('lang_id')
            if data['form'].get('lang_id') in ['ar_SA', 'ar_SY']:
                return data['form'].get('lang_id'), 'rtl'
            else:
                return data['form'].get('lang_id'), 'ltr'
        else:
            return self.env.user.lang, 'ltr'

    def arabic_num(self, string, lang):
        if 'ar' not in lang:
            return string
        final_string = str(string)
        string = str(string)
        span_list = []
        span_list_2 = []
        test_2 = re.findall('color:.*?;', string)
        i = 0
        for span_2 in test_2:
            i += 1
            string = string.replace(span_2, str(i) * len(span_2))
            span_list_2.append(str(i) * len(span_2))
        test = re.findall('<.*?>', string)
        for span in test:
            string_span = re.search(span, string)
            span_list.append(string_span.span())
        lst = [
            ('1', '١'),
            ('2', '٢'),
            ('3', '٣'),
            ('4', '٤'),
            ('5', '٥'),
            ('6', '٦'),
            ('7', '٧'),
            ('8', '٨'),
            ('9', '٩'),
            ('0', '٠'),
            ('-', '-'),
            ('/', '/'),
            (' ', ' '),
            ('False', ''),
            ('January', 'يناير'),
            ('February', 'فبراير'),
            ('March', 'مارس'),
            ('April', 'أبريل'),
            ('May', 'مايو'),
            ('June', 'يونيو'),
            ('July', 'يوليو'),
            ('August', 'أغسطس'),
            ('September', 'سبتمبر'),
            ('October', 'أكتوبر'),
            ('November', 'نوفمبر'),
            ('December', 'ديسمبر'),
        ]
        for l in lst:
            final_string = final_string.replace(l[0], l[1])
        for ss in range(len(span_list)):
            final_string = final_string[:span_list[ss][0]] + test[ss] + final_string[span_list[ss][1]:]
        for cc in range(len(test_2)):
            final_string = re.sub(span_list_2[cc], test_2[cc], final_string)
        return final_string

    def extract_num(self, text):
        res = [int(i) for i in text.split() if i.isdigit()]
        return res

    def print_xlsx_report(self):
        data = {'model': 'moc.detailed.report', 'form': self.read()[0]}
        header = ['No', 'Employee Company ID',
                  'Name',
                  'Identification',
                  'Parent Department',
                  'Department',
                  'Project',
                  'Project Department(AR)',
                  'Project Department(EN)',
                  'Initial date',
                  'Work Days',
                  'GOSI Company Amount',
                  'Days Adjustment',
                  'Exact GOSI Months',
                  'Basic',
                  'Housing Allowance Other',
                  'Transportaion Allowance Other',
                  'Cost of Living Other',
                  'Cost of Living allowance',
                  'Phone Allowance Other',
                  'Other Allowance other',
                  'Gross',
                  '1st Payslips',
                  '1st Month last day',
                  'Current Month Days',
                  'Previous Days',
                  'Basic (Net)',
                  'Housing Allowance Other (Net)',
                  'Transport Allowance Other (Net)',
                  'Phone Allowance Other (Net)',
                  'Cost of Living Other Allowance (Net)',
                  'Other Allowance Other (Net)',
                  'Total Earning',
                  'Employee GOSI',
                  'Other Deductions',
                  'Net',
                  'Company GOSI Other',
                  'Total Cost',
                  'Bank',
                  'Account']
        all_payslips = self.env['hr.payslip'].search([('date_from', '<=', self.date), ('date_to', '>=', self.date), ])
        all_emps = []
        seq = 0
        for payslip in all_payslips:
            seq += 1
            initial_date = \
                self.env['hr.contract.history'].search([('employee_id', '=', payslip.employee_id.id)]).contract_ids[
                    0].date_start
            other_allowance_other = 0
            other_deductions = 0
            bank = ''
            if payslip.employee_id.international_bank:
                bank = payslip.employee_id.bank_name if payslip.employee_id.bank_name else ""
            else:
                bank = payslip.employee_id.bank_id.bank_name if payslip.employee_id.bank_id else ""

            for rec in payslip.line_ids.filtered(lambda x: x.category_id.name in ['Allowance']):
                if rec.code in ['HOUALLOW', 'TRAALLOW']:
                    pass
                else:
                    other_allowance_other += rec.total
            for rec in payslip.line_ids.filtered(lambda x: x.category_id.name in ['Deduction']):
                if rec.code in ['GE']:
                    pass
                else:
                    other_deductions += rec.total
            all_emps.append({
                'seq': seq,
                'emp_company_id': payslip.employee_id.id if payslip.employee_id.id else " ",
                'emp_name': payslip.employee_id.name,
                'emp_id': payslip.employee_id.identification_id if payslip.employee_id.identification_id else " ",
                'emp_parent_department': payslip.employee_id.department_id.name if payslip.employee_id.department_id else " ",
                'emp_department': payslip.employee_id.department_id.name if payslip.employee_id.department_id else " ",
                'project': payslip.employee_id.project_id.name if payslip.employee_id.project_id else " ",
                'emp_project_dep_ar': " ",
                'emp_project_dep_en': " ",
                'emp_initial_date': initial_date.strftime('%Y/%m/%d'),
                'emp_work_days': payslip.worked_days_line_ids[0].number_of_days if payslip.worked_days_line_ids and
                                                                                   payslip.worked_days_line_ids[
                                                                                       0] else " ",
                'gosi_company_name': payslip.employee_id.company_id.name if payslip.employee_id.company_id else " ",
                'gosi_company_months': '1',
                'days_adjustment': 30 - payslip.worked_days_line_ids[0].number_of_days if payslip.worked_days_line_ids
                                                                                          and
                                                                                          payslip.worked_days_line_ids[
                                                                                              0].number_of_days else "",
                'exact_gosi_adjustment': '1',
                'basic': payslip.line_ids.filtered(lambda x: x.code == 'NET').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'NET') else " ",
                'housing_allowance_other': payslip.line_ids.filtered(
                    lambda x: x.code == 'HOUALLOW').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'HOUALLOW') else " ",
                'transportation_allowance_other': payslip.line_ids.filtered(
                    lambda x: x.code == 'TRAALLOW').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'TRAALLOW') else " ",
                'cost_of_living': ' ',
                'cost_of_living_allowance': ' ',
                'phone_allowance_other': " ",
                'other_allowance_other': other_allowance_other,
                'gross': payslip.line_ids.filtered(
                    lambda x: x.code == 'NET').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'NET') else 0 + payslip.line_ids.filtered(
                    lambda x: x.code == 'HOUALLOW').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'HOUALLOW') else 0 + other_allowance_other,
                'first_payslips': '0',
                'first_month_last_day': '0',
                'current_months_days': payslip.worked_days_line_ids[
                    0].number_of_days if payslip.worked_days_line_ids and
                                         payslip.worked_days_line_ids[0].number_of_days else "",
                'previous_days': '0',
                'basic_net': payslip.line_ids.filtered(lambda x: x.code == 'NET').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'NET') else " ",
                'housing_allowance_other_net': payslip.line_ids.filtered(
                    lambda x: x.code == 'HOUALLOW').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'HOUALLOW') else " ",
                'transportation_allowance_other_net': payslip.line_ids.filtered(
                    lambda x: x.code == 'TRAALLOW').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'TRAALLOW') else " ",
                'phone_allowance_other_net': " ",
                'cost_of_living_allowance_net': ' ',
                'other_allowance_other_net': other_allowance_other,
                'total_earning': payslip.line_ids.filtered(
                    lambda x: x.code == 'GROSS').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'GROSS') else " ",
                'employee_gosi': payslip.line_ids.filtered(
                    lambda x: x.code == 'GE').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'GE') else " ",
                'other_deductions': other_deductions,
                'basic_net_3': payslip.line_ids.filtered(lambda x: x.code == 'NET').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'NET') else " ",
                'company_gosi': payslip.line_ids.filtered(
                    lambda x: x.code == 'GC').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'GC') else " ",
                'total_cost': payslip.line_ids.filtered(lambda x: x.code == 'NET').total + payslip.line_ids.filtered(
                    lambda x: x.code == 'GC').total,
                'bank_name': bank,
                'iban': payslip.employee_id.iban_no if payslip.employee_id.iban_no else ""

            })
        data['all_emps'] = all_emps
        data['header'] = header
        data['period'] = '' + str(self.date.month) + '/' + str(self.date.year)
        data['date'] = self.arabic_num(self.date.strftime('%Y/%m/%d'), 'ar')
        return self.env.ref('custom_reports.moc_detailed_report_xlsx').report_action(self, data=data)


class BankStatementXLSX(models.TransientModel):
    _name = 'bank.statement.report'

    date = fields.Date(string="Date", required=True, )

    def get_lang(self, data):
        if data.get('form', False) and data['form'].get('lang_id', False):
            # print 'iam in get lang', data['form'].get('lang_id')
            if data['form'].get('lang_id') in ['ar_SA', 'ar_SY']:
                return data['form'].get('lang_id'), 'rtl'
            else:
                return data['form'].get('lang_id'), 'ltr'
        else:
            return self.env.user.lang, 'ltr'

    def arabic_num(self, string, lang):
        if 'ar' not in lang:
            return string
        final_string = str(string)
        string = str(string)
        span_list = []
        span_list_2 = []
        test_2 = re.findall('color:.*?;', string)
        i = 0
        for span_2 in test_2:
            i += 1
            string = string.replace(span_2, str(i) * len(span_2))
            span_list_2.append(str(i) * len(span_2))
        test = re.findall('<.*?>', string)
        for span in test:
            string_span = re.search(span, string)
            span_list.append(string_span.span())
        lst = [
            ('1', '١'),
            ('2', '٢'),
            ('3', '٣'),
            ('4', '٤'),
            ('5', '٥'),
            ('6', '٦'),
            ('7', '٧'),
            ('8', '٨'),
            ('9', '٩'),
            ('0', '٠'),
            ('-', '-'),
            ('/', '/'),
            (' ', ' '),
            ('False', ''),
            ('January', 'يناير'),
            ('February', 'فبراير'),
            ('March', 'مارس'),
            ('April', 'أبريل'),
            ('May', 'مايو'),
            ('June', 'يونيو'),
            ('July', 'يوليو'),
            ('August', 'أغسطس'),
            ('September', 'سبتمبر'),
            ('October', 'أكتوبر'),
            ('November', 'نوفمبر'),
            ('December', 'ديسمبر'),
        ]
        for l in lst:
            final_string = final_string.replace(l[0], l[1])
        for ss in range(len(span_list)):
            final_string = final_string[:span_list[ss][0]] + test[ss] + final_string[span_list[ss][1]:]
        for cc in range(len(test_2)):
            final_string = re.sub(span_list_2[cc], test_2[cc], final_string)
        return final_string

    def extract_num(self, text):
        res = [int(i) for i in text.split() if i.isdigit()]
        return res

    def print_xlsx_report(self):
        data = {'model': 'bank.statement.report', 'form': self.read()[0]}
        header = ['Type', 'اسم العميل', 'رمز الإتفاقية', 'حساب التمويل', 'رقم الفرع', 'تاريخ الإستحقاق(DDMMYYYY)',
                  'رقم  المنشأه في مكتب العمل ',
                  'رقم المنشأه في الغرفة التجارية', 'رمز البنك', 'العملة', 'رقم الدفعة ', 'مرجع الملف', ]
        second_row = ['111', 'PAY00999', 'PAY00999', '3545454509940', '313', '' + str(self.date.month) + '/' + str(self.date.year), '15-33676',
                      '2051046217', 'RIBL', 'SAR', '1', '', ]

        all_payslips = self.env['hr.payslip'].search([('date_from', '<=', self.date), ('date_to', '>=', self.date), ])
        f_payslip = all_payslips.filtered(
            lambda s: s.employee_id.bank_id.bank_type == 'riyadh')

        all_emps = []
        seq = 0
        for payslip in f_payslip:
            seq += 1
            other_income = 0
            deductions = 0
            for rec in payslip.line_ids.filtered(lambda x: x.category_id.name in ['Allowance']):
                if rec.code in ['HOUALLOW', ]:
                    pass
                else:
                    other_income += rec.total
            for rec in payslip.line_ids.filtered(lambda x: x.category_id.name in ['Deduction']):
                deductions += rec.total

            all_emps.append({
                'seq': seq,
                'emp_id': payslip.employee_id.identification_id if payslip.employee_id.identification_id else " ",
                'emp_name': payslip.employee_id.name,
                'account_num': payslip.employee_id.iban_no if payslip.employee_id.iban_no else "",
                'bank_symbol': '',
                'total': payslip.line_ids.filtered(lambda x: x.code == 'NET').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'NET') else " ",
                'basic': payslip.line_ids.filtered(lambda x: x.code == 'BASIC').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'BASIC') else " ",
                'home_allowance': payslip.line_ids.filtered(
                    lambda x: x.code == 'HOUALLOW').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'HOUALLOW') else " ",
                'another_income': other_income,
                'deductions': deductions,
                'address':  payslip.employee_id.national_address if payslip.employee_id.national_address else "",
                'currency': '',
                'status': '',
                'payment_type': '',
                'payment_ref': '',
            })
        data['all_emps'] = all_emps
        data['header'] = header
        data['second_row'] = second_row
        data['period'] = '' + str(self.date.month) + '/' + str(self.date.year)
        data['date'] = self.date.strftime('%Y/%m/%d')
        return self.env.ref('custom_reports.bank_stmt_xlsx').report_action(self, data=data)


class FinalSettlementXLSX(models.TransientModel):
    _name = 'final.settlement.report'

    date = fields.Date(string="Date", required=False, )
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=False, )

    def get_lang(self, data):
        if data.get('form', False) and data['form'].get('lang_id', False):
            # print 'iam in get lang', data['form'].get('lang_id')
            if data['form'].get('lang_id') in ['ar_SA', 'ar_SY']:
                return data['form'].get('lang_id'), 'rtl'
            else:
                return data['form'].get('lang_id'), 'ltr'
        else:
            return self.env.user.lang, 'ltr'

    def arabic_num(self, string, lang):
        if 'ar' not in lang:
            return string
        final_string = str(string)
        string = str(string)
        span_list = []
        span_list_2 = []
        test_2 = re.findall('color:.*?;', string)
        i = 0
        for span_2 in test_2:
            i += 1
            string = string.replace(span_2, str(i) * len(span_2))
            span_list_2.append(str(i) * len(span_2))
        test = re.findall('<.*?>', string)
        for span in test:
            string_span = re.search(span, string)
            span_list.append(string_span.span())
        lst = [
            ('1', '١'),
            ('2', '٢'),
            ('3', '٣'),
            ('4', '٤'),
            ('5', '٥'),
            ('6', '٦'),
            ('7', '٧'),
            ('8', '٨'),
            ('9', '٩'),
            ('0', '٠'),
            ('-', '-'),
            ('/', '/'),
            (' ', ' '),
            ('False', ''),
            ('January', 'يناير'),
            ('February', 'فبراير'),
            ('March', 'مارس'),
            ('April', 'أبريل'),
            ('May', 'مايو'),
            ('June', 'يونيو'),
            ('July', 'يوليو'),
            ('August', 'أغسطس'),
            ('September', 'سبتمبر'),
            ('October', 'أكتوبر'),
            ('November', 'نوفمبر'),
            ('December', 'ديسمبر'),
        ]
        for l in lst:
            final_string = final_string.replace(l[0], l[1])
        for ss in range(len(span_list)):
            final_string = final_string[:span_list[ss][0]] + test[ss] + final_string[span_list[ss][1]:]
        for cc in range(len(test_2)):
            final_string = re.sub(span_list_2[cc], test_2[cc], final_string)
        return final_string

    def extract_num(self, text):
        res = [int(i) for i in text.split() if i.isdigit()]
        return res

    def print_xlsx_report(self):
        data = {'model': 'final.settlement.report', 'form': self.read()[0]}

        data['date'] = self.date.strftime('%Y/%m/%d')
        return self.env.ref('custom_reports.final_settlement_xlsx').report_action(self, data=data)


class WPSRajhi(models.TransientModel):
    _name = 'wps.raghi.report'

    date = fields.Date(string="Date", required=False, )

    def get_lang(self, data):
        if data.get('form', False) and data['form'].get('lang_id', False):
            # print 'iam in get lang', data['form'].get('lang_id')
            if data['form'].get('lang_id') in ['ar_SA', 'ar_SY']:
                return data['form'].get('lang_id'), 'rtl'
            else:
                return data['form'].get('lang_id'), 'ltr'
        else:
            return self.env.user.lang, 'ltr'

    def arabic_num(self, string, lang):
        if 'ar' not in lang:
            return string
        final_string = str(string)
        string = str(string)
        span_list = []
        span_list_2 = []
        test_2 = re.findall('color:.*?;', string)
        i = 0
        for span_2 in test_2:
            i += 1
            string = string.replace(span_2, str(i) * len(span_2))
            span_list_2.append(str(i) * len(span_2))
        test = re.findall('<.*?>', string)
        for span in test:
            string_span = re.search(span, string)
            span_list.append(string_span.span())
        lst = [
            ('1', '١'),
            ('2', '٢'),
            ('3', '٣'),
            ('4', '٤'),
            ('5', '٥'),
            ('6', '٦'),
            ('7', '٧'),
            ('8', '٨'),
            ('9', '٩'),
            ('0', '٠'),
            ('-', '-'),
            ('/', '/'),
            (' ', ' '),
            ('False', ''),
            ('January', 'يناير'),
            ('February', 'فبراير'),
            ('March', 'مارس'),
            ('April', 'أبريل'),
            ('May', 'مايو'),
            ('June', 'يونيو'),
            ('July', 'يوليو'),
            ('August', 'أغسطس'),
            ('September', 'سبتمبر'),
            ('October', 'أكتوبر'),
            ('November', 'نوفمبر'),
            ('December', 'ديسمبر'),
        ]
        for l in lst:
            final_string = final_string.replace(l[0], l[1])
        for ss in range(len(span_list)):
            final_string = final_string[:span_list[ss][0]] + test[ss] + final_string[span_list[ss][1]:]
        for cc in range(len(test_2)):
            final_string = re.sub(span_list_2[cc], test_2[cc], final_string)
        return final_string

    def extract_num(self, text):
        res = [int(i) for i in text.split() if i.isdigit()]
        return res

    def print_xlsx_report(self):
        data = {'model': 'wps.raghi.report', 'form': self.read()[0]}

        all_payslips = self.env['hr.payslip'].search([('date_from', '<=', self.date), ('date_to', '>=', self.date), ])
        f_payslip = all_payslips.filtered(
            lambda s: s.employee_id.bank_id.bank_type == 'rajhi')
        all_emps = []
        for payslip in f_payslip:
            other_income = 0
            deductions = 0
            bank = ''
            if payslip.employee_id.international_bank:
                bank = payslip.employee_id.bank_name if payslip.employee_id.bank_name else ""
            else:
                bank = payslip.employee_id.bank_id.bank_name if payslip.employee_id.bank_id else ""

            for rec in payslip.line_ids.filtered(lambda x: x.category_id.name in ['Allowance']):
                if rec.code in ['HOUALLOW', ]:
                    pass
                else:
                    other_income += rec.total
            for rec in payslip.line_ids.filtered(lambda x: x.category_id.name in ['Deduction']):
                deductions += rec.total

            all_emps.append({
                'bank_name': bank,
                'iban': payslip.employee_id.iban_no if payslip.employee_id.iban_no else "",
                'emp_id': payslip.employee_id.identification_id if payslip.employee_id.identification_id else " ",
                'emp_name': payslip.employee_id.name,
                'account_num': payslip.employee_id.iban_no if payslip.employee_id.iban_no else "",
                'net': payslip.line_ids.filtered(lambda x: x.code == 'NET').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'NET') else " ",
                'basic': payslip.line_ids.filtered(lambda x: x.code == 'BASIC').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'BASIC') else " ",
                'home_allowance': payslip.line_ids.filtered(
                    lambda x: x.code == 'HOUALLOW').total if payslip.line_ids.filtered(
                    lambda x: x.code == 'HOUALLOW') else " ",
                'another_earnings': other_income,
                'deductions': deductions,
                'emp_department': payslip.employee_id.department_id.name if payslip.employee_id.department_id else " ",
            })
        data['all_emps'] = all_emps
        data['date'] = self.date.strftime('%Y/%m/%d')
        return self.env.ref('custom_reports.wps_raghi_report_xlsx').report_action(self, data=data)
