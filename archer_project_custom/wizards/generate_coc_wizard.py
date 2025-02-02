from odoo import fields, models, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
import json
import io
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class GenerateCOCWizard(models.TransientModel):
    _name = 'generate.coc.wizard'

    def _get_year_selection(self):
        """Return the list of values of current year."""
        years = []
        for seq in range(datetime.now().year - 6, datetime.now().year + 6):
            years.append((str(seq), str(seq)))
        return years

    project_ids = fields.Many2many('project.project', default=lambda self: self.env.context.get('active_ids', []))
    year = fields.Selection(_get_year_selection, default=lambda self: str(datetime.now().year))
    month = fields.Selection([
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ], required=True, string='COC for Month')

    def action_confirm(self):
        project_obj = self.env['project.project']
        payslip_batch_obj = self.env['hr.payslip.run']
        if self.month == "12":
            month = 1
        else:
            month = int(self.month) + 1
        from_date = datetime.today().replace(month=int(self.month), day=1, hour=0, minute=0, second=0, microsecond=0)
        to_date = (datetime.today().replace(month=month, day=1, hour=23, minute=59, second=59,
                                            microsecond=999999) - timedelta(days=1)).replace(
            year=datetime.today().date().year)

        if from_date > datetime.today():
            raise UserError(_('Please set valid Month!'))
        projects = project_obj.browse(self.env.context.get('active_ids'))
        payslip_batch = payslip_batch_obj.search([
            ('date_start', '>=', from_date),
            ('date_end', '<=', to_date),
            ('state', '=', 'close'),
        ])
        # if not payslip_batch:
        #     raise UserError(_('No Payroll for this month yet!'))

        coc_ids = []
        if not projects:
            projects = self.project_ids
        for project in projects:
            if not project.analytic_account_id:
                raise UserError("Project: %s \nHas No Analytic Account!" % project.name)
            exist_coc = self.env['archer.account.coc'].search([
                ('project_id', '=', project.id),
                ('date', '>=', from_date),
                ('date', '<=', to_date),
                # ('state', '=', 'approved'),
            ])
            print(exist_coc)
            month = self.get_selection_label('month', self.month)
            # if exist_coc:
            #     raise UserError(_('Project: %s already has COC for month: %s') % (project.name, month))
            # else:
            #     coc_ids.append(project.create_coc(from_date, to_date, self.month, self.year))
        if coc_ids and len(coc_ids) == 1:
            data = {
                'ids': coc_ids,
                'model': self._name,
                'month': self.month,
                'year': self.year,
                'coc': coc_ids,
                'project': self.project_ids.id,
            }
            return {
                'name': _('COC'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'res_model': 'archer.account.coc.line',
                'target': 'current',
                'domain': [('coc_id', 'in', coc_ids)]

            }
            # return {
            #     'type': 'ir.actions.report',
            #     'data': {'model': 'generate.coc.wizard',
            #              'options': json.dumps(data, default=date_utils.json_default),
            #              'output_format': 'xlsx',
            #              'report_name': 'COC Template 1.2',
            #              },
            #     'report_type': 'stock_xlsx'
            # }

        else:
            return project_obj.action_view_coc(self.env['archer.account.coc'].browse(coc_ids))

    def get_xlsx_report(self, data, response):
        project_obj = self.env['project.project']
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        coc = self.env['archer.account.coc'].sudo().browse(data['coc'])
        lines = coc.line_ids
        commercial_number = 'سجل تجاري 1010702982'
        address = 'العنوان: الرياض - حي الشهداء - واحة غرناظة'
        codes = 'صندوق بريد: 7343 | رمز بريدي: 13241 | المملكة العربية السعودية'
        mobile = 'تليفون: 0112762998 | بريد الكتروني: hr@rwafid.sa'
        tax_number = 'الرقم الضريبي: 302004650300003'
        sheet = workbook.add_worksheet('COC Template 1.2')
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True, 'border': 1})
        format11 = workbook.add_format({'font_size': 12, 'align': 'right', 'reading_order': 2, 'bold': True})
        format21 = workbook.add_format({'font_size': 12, 'font_color': 'white', 'bg_color': 'black', 'align': 'center', 'bold': True, 'border': 1})
        font_size_10 = workbook.add_format({'font_size': 10, 'align': 'center', 'border': 1, 'border_color': "gray"})
        justify = workbook.add_format({'font_size': 12})
        justify.set_align('justify')
        sheet.merge_range(1, 5, 2, 13, 'COC Template 1.2', format0)
        sheet.merge_range(3, 17, 3, 21, commercial_number, format11)
        sheet.merge_range(4, 17, 4, 21, address, format11)
        sheet.merge_range(5, 17, 5, 21, codes, format11)
        sheet.merge_range(6, 17, 6, 21, mobile, format11)
        sheet.merge_range(7, 17, 7, 21, tax_number, format11)

        prod_row = 10
        prod_col = 21

        sheet.merge_range(prod_row, 21, prod_row, 20, 'الرقم', format21)
        sheet.merge_range(prod_row, 19, prod_row, 16, 'الوصف', format21)
        sheet.merge_range(prod_row, 15, prod_row, 12, 'Description', format21)
        sheet.merge_range(prod_row, 11, prod_row, 10, 'القيمة الفعلية', format21)
        sheet.merge_range(prod_row, 9, prod_row, 8, 'قيمة الربح', format21)
        sheet.merge_range(prod_row, 7, prod_row, 6, 'الاجمالي', format21)
        sheet.merge_range(prod_row, 5, prod_row, 4, 'قيمة الضريبة', format21)
        sheet.merge_range(prod_row, 3, prod_row, 2, 'المجموع', format21)
        prod_row = prod_row + 1

        for line in lines:
            sheet.merge_range(prod_row, prod_col, prod_row, prod_col - 1, line.sequence, font_size_10)
            sheet.merge_range(prod_row, prod_col - 2, prod_row, prod_col - 5, line.item_arabic_name, font_size_10)
            sheet.merge_range(prod_row, prod_col - 6, prod_row, prod_col - 9, line.item_name, font_size_10)
            sheet.merge_range(prod_row, prod_col - 10, prod_row, prod_col - 11, line.real_amount, font_size_10)
            sheet.merge_range(prod_row, prod_col - 12, prod_row, prod_col - 13, line.profit_amount, font_size_10)
            sheet.merge_range(prod_row, prod_col - 14, prod_row, prod_col - 15, line.untaxed_total, font_size_10)
            sheet.merge_range(prod_row, prod_col - 16, prod_row, prod_col - 17, line.amount_tax, font_size_10)
            sheet.merge_range(prod_row, prod_col - 18, prod_row, prod_col - 19, line.amount_total, font_size_10)

            prod_row = prod_row + 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return project_obj.action_view_coc(coc)

    def get_selection_label(self, field_name, field_value):
        return _(dict(self.fields_get(allfields=[field_name])[field_name]['selection'])[field_value])