from odoo import models, fields, api, _
from odoo.exceptions import UserError
from lxml import etree
import json
import simplejson
from datetime import datetime, timedelta
import datetime
import time
from dateutil.rrule import rrule, MONTHLY


class Project(models.Model):
    _inherit = "project.project"

    # region Compute Methods
    def _compute_is_project_manager(self):
        for rec in self:
            rec.is_project_manager = True if self.env.uid == rec.user_id.id else False

    @api.depends('project_change_request_ids')
    def _compute_project_change_request_ids(self):
        for request in self:
            request.project_change_request_count = len(request.project_change_request_ids)

    @api.depends('actual_value', 'markup')
    def _compute_budget(self):
        for project in self:
            if project.actual_value:
                project.budget = project.actual_value / (1 + (project.markup / 100))

    @api.depends('vat_included', 'contract_value')
    def _compute_actual_value(self):
        for project in self:
            if project.vat_included:
                project.actual_value = project.contract_value / 1.15
            else:
                project.actual_value = project.contract_value

    # endregion

    # region Fields
    owner_id = fields.Many2one('res.partner', "Project Owner", required=True)
    coc_template_id = fields.Many2one("coc.template")
    coc_template_item_ids = fields.One2many("project.coc.template.items", "project_id")
    salary_constraint_ids = fields.One2many("salary.constraint", "project_id")
    petty_cash_allowed = fields.Boolean("Petty Cash Allowed")
    petty_cash_responsible_id = fields.Many2one('res.partner', "Petty Cash Responsible")
    contract_value = fields.Float("Contract Value")
    vat_included = fields.Boolean("VAT Included?")
    actual_value = fields.Float("Value (Without Taxes)", compute="_compute_actual_value", store=True)
    markup = fields.Float("Margin")
    budget = fields.Float("Budget", compute="_compute_budget", store=True)
    top_cost_limit = fields.Float("Top Cost-Limit (%)")
    bottom_cost_limit = fields.Float("Bottom Cost-Limit (%)")
    constraint_ids = fields.One2many('project.expense.constraint.list', 'project_id', string="Constraints")
    service_ids = fields.Many2many('product.template', string="Services")
    project_request_id = fields.Many2one("project.request")
    project_change_request_ids = fields.One2many("project.change.request", "project_id", string='Projects',
                                                 copy=False, )
    project_change_request_count = fields.Integer(string='Number of Projects',
                                                  compute='_compute_project_change_request_ids', copy=False)
    project_state = fields.Selection([
        ('active', 'Active'),
        ('in_close', 'In Close'),
        ('close', "Close"), ], string="Project Status")
    structure_type_id = fields.Many2one(comodel_name='hr.payroll.structure.type', string="Salary Structure Type", )
    structure_id = fields.Many2one(comodel_name='hr.payroll.structure', string="Salary Structure ",
                                   related='structure_type_id.default_struct_id')
    salary_rule_ids = fields.Many2many(comodel_name='hr.salary.rule', string='Salary Rules')
    max_loan_percentage = fields.Float(string="Max Loan Percentage", required=True)
    max_loan_installments = fields.Integer(string="Max Loan Installments", required=True)
    is_project_manager = fields.Boolean(compute='_compute_is_project_manager')
    headhunt_count = fields.Integer(compute='compute_headhunts_logistic')
    logistic_count = fields.Integer(compute='compute_headhunts_logistic')
    cost_total = fields.Integer(compute='compute_total_cost')
    cost_count = fields.Integer(compute='compute_cost_count')
    close_id = fields.Many2one(comodel_name='project.close', string='Close  Date Confirmation')
    close_date = fields.Date(string='Close Date')
    close_uid = fields.Many2one(comodel_name='res.users', string='Close by')
    apply_salary_rule = fields.Boolean(string='Apply Salary Rule')
    apply_grade = fields.Boolean(string='Apply Grade Constrain')
    categ_id = fields.Many2one(comodel_name='project.project.category', string='Project Category')
    def compute_cost_count(self):
        for rec in self:
            rec.cost_count = self.env['archer.project.cost'].search_count([('project_id', '=', rec.id)])

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(Project, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
                                                   submenu=False)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in res['fields']:
                if not self.env.user.has_group('project.group_project_manager'):
                    for node in doc.xpath("//field[@name='%s']" % field):
                        node.set("readonly", "0")
                        modifiers = json.loads(node.get("modifiers"))
                        modifiers['readonly'] = True
                        node.set("modifiers", json.dumps(modifiers))
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    # endregion

    # region Action Methods
    def action_view_project_request_ids(self):
        view_id = self.env.ref('archer_project_custom.project_req_form_view').id
        context = self._context.copy()
        return {
            'name': 'Project Request',
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(view_id, 'form')],
            'res_model': 'project.request',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.project_request_id.id,
            'context': context}

    def action_view_project_change_request_ids(self):
        tree_view_id = self.env.ref('archer_project_custom.project_change_request_tree').id
        result = {
            "type": "ir.actions.act_window",
            "res_model": "project.change.request",
            "domain": [['id', 'in', self.project_change_request_ids.ids]],
            "views": [[tree_view_id, "tree"], [False, "form"]],
            "context": {"create": False},
            "name": "Project Change Request",
        }
        if len(self.project_change_request_ids) == 1:
            result['views'] = [(False, "form")]
            result['res_id'] = self.project_change_request_ids.id
        return result

    def open_project_change_request(self):
        name = self.env['ir.sequence'].next_by_code('project.change.sequence')
        view_id = self.env.ref('archer_project_custom.project_change_request_form_view').id
        return {
            'name': _('Project Change Request'),
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'project.change.request',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {
                'default_project_id': self.id,
                'default_project_manager': self.user_id.id,
                'default_project_owner_id': self.owner_id.id,
                'default_contract_value': self.contract_value,
                'default_vat_included': self.vat_included,
                'default_markup': self.markup,
                'default_name': name,
                'default_date': self.date,
            },
        }

    def create_analytic_account(self, name, partner, group=False):
        analytic_account = self.env['account.analytic.account'].create({
            'name': name,
            'partner_id': partner,
            'group_id': group,
        })
        return analytic_account

    def action_generate_coc(self):
        action = self.env.ref('archer_project_custom.action_generate_coc_wizard').read()[0]
        action['context'] = {
            'default_project_ids': self.ids,
        }
        action['views'] = [(self.env.ref('archer_project_custom.generate_coc_wizard_form_view').id, 'form')]
        action['target'] = 'new'
        return action

    def create_coc(self, date_from, date_to, month, year):
        coc_vals = self.prepare_coc_vals(date_from, date_to, month, year)
        coc = self.env['archer.account.coc'].with_context().create(coc_vals)
        return coc.id

    def _get_coc_tax(self):
        return self.env['account.tax'].search([('for_coc', '=', True)], limit=1)

    def prepare_coc_vals(self, date_from, date_to, month, year):
        coc_vals = {
            'name': 'COC for project ' + self.name + ' - ' + month + '/' + year,
            'project_id': self.id,
            'month': month,
            'partner_id': self.partner_id.id,
            'date': fields.Date.today(),
            'line_ids': self.prepare_coc_lines(date_from, date_to)
        }
        return coc_vals

    def prepare_coc_lines(self, date_from, date_to):
        journal_item_obj = self.env['account.move.line'].sudo()
        tax_rate = self._get_coc_tax().amount if self._get_coc_tax() else 0.0
        line_vals = []
        for item in self.coc_template_item_ids:
            journal_item_ids = journal_item_obj.search([
                ('analytic_account_id', '=', self.analytic_account_id.id),
                ('account_id', 'in', item.account_id.ids),
                ('date', '>=', date_from),
                ('date', '<=', date_to),
                ('parent_state', '=', 'posted'),
            ])
            real_amount = abs(sum(journal_item_ids.mapped('debit')) - sum(journal_item_ids.mapped('credit')))
            profit_amount = real_amount * (item.margin / 100)
            untaxed_total = real_amount + profit_amount
            amount_tax = (tax_rate / 100) * untaxed_total
            amount_total = (untaxed_total + amount_tax) if untaxed_total > 0.0 else 0.0
            line_vals.append((0, 0, {
                'item_name': item.coc_template_item_id.item_name,
                'item_arabic_name': item.coc_template_item_id.item_arabic_name,
                'sequence': item.coc_template_item_id.tab_number,
                'real_amount': real_amount,
                'profit_amount': profit_amount,
                'untaxed_total': untaxed_total,
                'amount_tax': amount_tax,
                'amount_total': amount_total,
            }))
        return line_vals

    def action_view_coc(self, coc=False):
        if not coc:
            self.sudo()._read(['coc_ids'])
            coc = self.coc_ids

        result = self.env['ir.actions.act_window']._for_xml_id('archer_project_custom.action_account_coc')
        if len(coc) > 1:
            result['domain'] = [('id', 'in', coc.ids)]
        elif len(coc) == 1:
            res = self.env.ref('archer_project_custom.account_coc_form_view', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state, view) for state, view in result['views'] if view != 'form']
            else:
                result['views'] = form_view
            result['res_id'] = coc.id
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result

    def get_selection_label(self, field_name, field_value):
        return _(dict(self.fields_get(allfields=[field_name])[field_name]['selection'])[field_value])

    # endregion

    def compute_headhunts_logistic(self):
        for rec in self:
            rec.headhunt_count = self.env['archer.headhunt.request'].search_count([('project_id', '=', rec.id)])
            rec.logistic_count = self.env['archer.logistic.request'].search_count([('project_id', '=', rec.id)])

    def get_headhunting_request(self):
        self.ensure_one()
        tree_view_id = self.env.ref('archer_project_custom.view_archer_headhunt_request_tree').id
        form_view_id = self.env.ref('archer_project_custom.view_archer_headhunt_request_form').id
        return {
            'name': _('Headhunting'),
            'view_mode': 'tree,form',
            'views': [(tree_view_id, 'list'), (form_view_id, 'form')],
            'res_model': 'archer.headhunt.request',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('project_id', '=', self.id)],
            'context': {
                'default_project_id': self.id,
                'create': True,
                'edit': True
            },
        }

    def get_logistic_request(self):
        self.ensure_one()
        tree_view_id = self.env.ref('archer_project_custom.view_archer_logistic_request_tree').id
        form_view_id = self.env.ref('archer_project_custom.view_archer_logistic_request_form').id
        return {
            'name': _('Logistics'),
            'view_mode': 'tree,form',
            'views': [(tree_view_id, 'list'), (form_view_id, 'form')],
            'res_model': 'archer.logistic.request',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('project_id', '=', self.id)],
            'context': {
                'default_project_id': self.id,
                'create': True,
                'edit': True
            },
        }

    def compute_total_cost(self):
        for rec in self:
            rec.cost_total = sum(
                self.env['archer.project.cost'].search([('project_id', '=', rec.id)]).mapped('month_cost')) or 0.0

    def get_project_cost(self):
        self.ensure_one()
        tree_view_id = self.env.ref('archer_project_custom.view_archer_project_cost_tree').id
        return {
            'name': _('Cost'),
            'view_mode': 'tree',
            'views': [(tree_view_id, 'list')],
            'res_model': 'archer.project.cost',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('project_id', '=', self.id)],
            'context': {
                'create': False,
                'edit': False,
                'duplicate': False,
                'delete': False
            },
        }

    def generate_cost(self):
        for rec in self:
            if rec.service_ids:
                date_list = [{'month': dt.strftime("%m"), 'year': dt.strftime("%Y")} for dt in
                             rrule(MONTHLY, dtstart=rec.date_start, until=rec.date)]
                for mydate in date_list:
                    cost_vals = {
                        'project_id': rec.id,
                        'request_month': mydate['month'],
                        'request_year': mydate['year'],
                    }
                    cost = self.env['archer.project.cost'].create(cost_vals)
                    line_list = []
                    for srv in rec.service_ids:
                        line_list.append({
                            'cost_id': cost.id,
                            'project_id': rec.id,
                            'analytic_account_id': rec.analytic_account_id.id,
                            'service_id': srv.id,
                            'account_id': srv.property_account_expense_id.id,
                            'service_name': srv.name,
                            'line_type': 'product'

                        })
                    line_list.append({
                        'cost_id': cost.id,
                        'project_id': rec.id,
                        'analytic_account_id': rec.analytic_account_id.id,
                        'service_name': 'Headhunting',
                        'line_type': 'headhunt'

                    })
                    line_list.append({
                        'cost_id': cost.id,
                        'project_id': rec.id,
                        'analytic_account_id': rec.analytic_account_id.id,
                        'service_name': 'Logistics',
                        'line_type': 'logistic'

                    })
                    cost_line = self.env['archer.project.cost.line'].create(line_list)

    def check_project_to_close(self):
        for rec in self:
            if rec.date == fields.Date.today():
                rec.activity_schedule(
                    activity_type_id='mail.mail_activity_data_todo',
                    summary='Project Termination',
                    note='Please Start Project close Process',
                    user_id=rec.user_id.id,
                    date_deadline=fields.Date.today() + timedelta(days=14)
                )
                mail_template = self.env.ref('archer_project_custom.mail_template_project_close')
                email_sent = mail_template.send_mail(rec.id, force_send=True)

    def action_confirm_close_date(self):
        return {
            'name': _('Close Project'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.close',
            'view_mode': 'tree',
            'views': [[self.env.ref('archer_project_custom.view_project_close_form').id, 'form']],
            'target': 'current',
            'context': {
                'default_project_id': self.id
            }
        }

    def action_close_project(self):
        for rec in self:
            project_users = self.env['res.users'].search(
                [('project_ids', 'in', rec.id), ('user_type', '!=', 'project_owner'), ('id', '!=', self.env.uid)])
            project_users.write({'active': False})
            rec.analytic_account_id.write({'active': False})
            rec.write({'close_date': fields.Date.today(), 'close_uid': self.env.uid, 'active': False,
                       'project_state': 'close'})

    def get_project_forecast_report(self):
        data = {
            'project_id': self.id
        }
        return self.env.ref('archer_project_custom.project_forecast_report_action').report_action(None, data=data)

class ProjectCategory(models.Model):
    _name = 'project.project.category'
    _rec_name = 'en_name'

    ar_name = fields.Char(string='Arabic Name')
    en_name = fields.Char(string='English Name')
    description = fields.Text(string='Description')
    project_ids = fields.One2many(comodel_name='project.project', string='Projects', inverse_name='categ_id')