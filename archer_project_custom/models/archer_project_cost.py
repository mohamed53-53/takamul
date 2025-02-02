from datetime import datetime, timedelta

from odoo import models, fields, _
import calendar

from odoo.exceptions import UserError


def get_dates_month(year, month):
    first_date = datetime(year, month, 1)
    if month == 12:
        last_date = datetime(year, month, 31)
    else:
        last_date = datetime(year, month + 1, 1) + timedelta(days=-1)

    month_dates = {'first': first_date.strftime("%Y-%m-%d"), 'last': last_date.strftime("%Y-%m-%d")}
    return month_dates


class ProjectCost(models.Model):
    _name = 'archer.project.cost'

    name = fields.Char(string='Name', compute='compute_name')
    project_id = fields.Many2one(comodel_name='project.project', string='Project', required=True)
    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', related='project_id.analytic_account_id')
    request_month = fields.Selection(selection=[
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
    ], string='Month', required=True)
    request_year = fields.Selection(
        [(str(y), str(y)) for y in range((datetime.now().year - 1), (datetime.now().year + 2))], string='Year',
        required=True)
    month_cost = fields.Float(string='Month Cost', compute='compute_month_cost')
    line_ids = fields.One2many(comodel_name='archer.project.cost.line', inverse_name='cost_id', string='Lines')

    def compute_month_cost(self):
        for rec in self:
            rec.month_cost = sum(rec.line_ids.mapped('service_month_cost'))

    def compute_name(self):
        for rec in self:
            rec.name = '%s-%s' % (rec.request_month, rec.request_year)

    def get_cost_lines(self):
        self.ensure_one()
        tree_view_id = self.env.ref('archer_project_custom.view_archer_project_cost_line_tree').id
        return {
            'name': _('Lines'),
            'view_mode': 'tree,graph,pivot',
            'res_model': 'archer.project.cost.line',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('project_id', '=', self.project_id.id), ('cost_id', '=', self.id)],
            'context': {
                'create': False,
                'edit': False,
                'duplicate': False,
                'delete': False
            },
        }

    def generate_cost_report(self):
        month_date = get_dates_month(int(self.request_year), int(self.request_month))

        return {
            'name': _('Lines'),
            'view_mode': 'tree,graph,pivot',
            'res_model': 'account.analytic.line',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('date', '<=', datetime.strptime(month_date['last'], '%Y-%m-%d')),
                       ('date', '>=', datetime.strptime(month_date['first'], '%Y-%m-%d')),('account_id', '=', self.analytic_account_id.id), ('general_account_id', 'in', self.project_id.service_ids.property_account_expense_id.ids)],
            'context': {
                'group_by':['date:month','general_account_id'],
                'create': False,
                'edit': False,
                'duplicate': False,
                'delete': False
            },
        }
    def generate_coc_report(self):
        month_date = get_dates_month(int(self.request_year), int(self.request_month))
        payslip_batch_obj = self.env['hr.payslip.run']
        payslip_batch = payslip_batch_obj.search([
            ('date_start', '>=', datetime.strptime(month_date['first'], '%Y-%m-%d')),
            ('date_end', '<=', datetime.strptime(month_date['last'], '%Y-%m-%d')),
            ('state', '=', 'close'),
        ])
        if not self.project_id.analytic_account_id:
            raise UserError("Project: %s \nHas No Analytic Account!" % self.project_id.name)
        exist_coc = self.env['archer.account.coc'].search([
            ('project_id', '=', self.project_id.id),
            ('date', '>=', datetime.strptime(month_date['first'], '%Y-%m-%d')),
            ('date', '<=', datetime.strptime(month_date['last'], '%Y-%m-%d')),
            # ('state', '=', 'approved'),
        ])
        # month = self.get_selection_label('request_month', self.request_month)
        # if exist_coc:
        #     raise UserError(_('Project: %s already has COC for month: %s') % (self.project_id.name, month))
        # else:
        coc_obj = self.project_id.create_coc(datetime.strptime(month_date['first'], '%Y-%m-%d'), datetime.strptime(month_date['last'], '%Y-%m-%d'), self.request_month, self.request_year)
        return {
                'name': _('COC'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'res_model': 'archer.account.coc.line',
                'target': 'current',
                'domain': [('coc_id', '=', coc_obj)]

            }

    def get_selection_label(self, field_name, field_value):
        return _(dict(self.fields_get(allfields=[field_name])[field_name]['selection'])[field_value])

class ProjectCostLines(models.Model):
    _name = 'archer.project.cost.line'
    service_name = fields.Char(string='Service')
    cost_id = fields.Many2one(comodel_name='archer.project.cost', string='Cost', required=True)
    project_id = fields.Many2one(comodel_name='project.project', string='Project', required=True)
    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', string='Analytic Account', required=True)
    service_id = fields.Many2one(comodel_name='product.template', )
    account_id = fields.Many2one(comodel_name='account.account', )
    service_month_cost = fields.Float(string=' Service Month Cost', compute='compute_service_month_cost')
    headhunt_id = fields.Many2one(comodel_name='archer.headhunt.request', string='Headhunting')
    logistic_id = fields.Many2one(comodel_name='archer.logistic.request', string='Logistic')
    line_type = fields.Selection(selection=[('product', 'Product'), ('logistic', 'logistic'), ('headhunt', 'Headhunt')], string='Line Type')

    def compute_service_month_cost(self):
        for rec in self:
            month_date = get_dates_month(int(rec.cost_id.request_year), int(rec.cost_id.request_month))
            move_items = self.env['account.analytic.line'].search(
                [('general_account_id', '=', rec.service_id.property_account_expense_id.id),
                 ('account_id', '=', rec.analytic_account_id.id), ('move_id.move_id.state', '=', 'posted'),
                 ('date', '<=', datetime.strptime(month_date['last'], '%Y-%m-%d')),
                 ('date', '>=', datetime.strptime(month_date['first'], '%Y-%m-%d'))])
            if rec.line_type == 'product':
                rec.service_month_cost = sum(move_items.mapped('amount'))
            elif rec.line_type == 'logistic':
                logistics = self.env['archer.logistic.request'].search(
                    [('project_id', '=', rec.project_id.id), ('request_month', '=', rec.cost_id.request_month),
                     ('request_year', '=', rec.cost_id.request_year), ('state', '=', 'approved')])
                rec.service_month_cost = -1 * sum(logistics.mapped('amount'))
            elif rec.line_type == 'headhunt':
                headhunts = self.env['archer.headhunt.request'].search(
                    [('project_id', '=', rec.project_id.id), ('request_month', '=', rec.cost_id.request_month),
                     ('request_year', '=', rec.cost_id.request_year), ('state', '=', 'approved')])
                rec.service_month_cost = -1 * sum(headhunts.mapped('amount'))
            else:
                rec.service_month_cost = 0.0
