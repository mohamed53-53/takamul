from odoo import models, fields, _, api
from odoo.exceptions import UserError, ValidationError
from lxml import etree
import json
import simplejson


class ProjectRequest(models.Model):
    _name = "project.request"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record', ]

    name = fields.Char("Name", index=True, required=True, tracking=True, translate=True)
    partner_id = fields.Many2one('res.partner', string='Customer', auto_join=True, tracking=True,
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    user_id = fields.Many2one('res.users', string='Project Manager', default=lambda self: self.env.user, tracking=True)
    date_start = fields.Date(string='Start Date')
    date = fields.Date(string='Expiration Date', index=True, tracking=True)
    company_id = fields.Many2one(comodel_name='res.company', string='Company', required=True, default=lambda self: self.env.company)
    owner_id = fields.Many2one(comodel_name='res.partner', string="Project Owner", required=True, domain="[('parent_id','=',partner_id)]")
    coc_template_id = fields.Many2one(comodel_name="coc.template", string="COC Template", required=True)
    business_domain = fields.Many2one(comodel_name="account.analytic.group")
    coc_template_item_ids = fields.One2many(comodel_name="project.coc.template.items", inverse_name="project_request_id", )
    salary_constraint_ids = fields.One2many(comodel_name="salary.constraint", inverse_name="project_request_id")
    petty_cash_allowed = fields.Boolean("Petty Cash Allowed")
    petty_cash_responsible_id = fields.Many2one('res.partner', "Petty Cash Responsible")
    contract_value = fields.Float("Contract Value")
    vat_included = fields.Boolean("VAT Included?")
    actual_value = fields.Float("Value (Without Taxes)", compute="_compute_actual_value", store=True)
    markup = fields.Float("Markup (%)")
    budget = fields.Float("Budget", compute="_compute_budget", store=True)
    top_cost_limit = fields.Float("Top Cost-Limit (%)")
    bottom_cost_limit = fields.Float("Bottom Cost-Limit (%)")
    service_ids = fields.Many2many(comodel_name='product.template', string="Services")
    state = fields.Selection([], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account")
    constraint_ids = fields.One2many(comodel_name='project.expense.constraint.list', inverse_name='project_request_id',
                                     string="Constraints")
    rejection_reason = fields.Text("Rejection Reason", copy=False)
    project_id = fields.Many2one(comodel_name='project.project', string='Related Project')
    structure_type_id = fields.Many2one(comodel_name='hr.payroll.structure.type', string="Salary Structure Type", )
    structure_id = fields.Many2one(comodel_name='hr.payroll.structure', string="Salary Structure ",
                                   related='structure_type_id.default_struct_id')
    salary_rule_ids = fields.Many2many(comodel_name='hr.salary.rule', string='Salary Rules')
    max_loan_percentage = fields.Float(string="Max Loan Percentage",  required=True)
    max_loan_installments = fields.Integer(string="Max Loan Installments",  required=True)
    categ_id = fields.Many2one(comodel_name='project.project.category', string='Project Category')

    @api.depends('petty_cash_responsible_id')
    @api.onchange('petty_cash_responsible_id')
    def onchange_petty_cash_responsible_id(self):
        for rec in self:
            if rec.petty_cash_responsible_id:
                if rec.petty_cash_responsible_id.project_ids:
                    raise ValidationError(_('This Partner already In project'))
    @api.depends('coc_template_item_ids', 'coc_template_id')
    @api.onchange('coc_template_item_ids', 'coc_template_id')
    def onchange_coc_template_item_ids(self):
        for rec in self:
            rec.service_ids = False
            product_ids = self.env['product.template'].search(
                [('property_account_expense_id', 'in', rec.coc_template_item_ids.coc_template_item_id.account_id.ids)])
            if product_ids:
                domain = {'domain': {'service_ids': [('id', '=', product_ids.ids)]}}
            else:
                domain = {'domain': {'service_ids': [('id', '=', [])]}}
            return domain

    @api.depends('markup')
    @api.onchange('markup')
    def onchange_markup(self):
        for rec in self:
            rec.coc_template_item_ids.write({'margin': rec.markup})

    @api.constrains('salary_constraint_ids')
    def _check_exist_grade_in_line(self):
        for request in self:
            exist_grade_list = []
            for line in request.salary_constraint_ids:
                if line.grade_id.id in exist_grade_list:
                    raise ValidationError(_('Grade should be unique one per Salary Constraint.'))
                exist_grade_list.append(line.grade_id.id)

    @api.onchange('coc_template_id')
    def _onchange_coc_template_id(self):
        self.coc_template_item_ids = False
        self.service_ids = False

        self.coc_template_item_ids = [(0, 0, {
            'project_request_id': self.id,
            'coc_template_item_id': x.id,
            'margin': 0.0
        }) for x in self.coc_template_id.coc_template_item_ids]

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProjectRequest, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
                                                          submenu=False)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in res['fields']:
                field_list = ['name', 'partner_id', 'user_id', 'owner_id', 'date_start', 'date', 'company_id',
                              'coc_template_id', 'contract_value', 'business_domain',
                              'vat_included', 'markup', 'budget', 'actual_value', 'top_cost_limit', 'bottom_cost_limit',
                              'petty_cash_allowed', 'petty_cash_responsible_id', 'service_ids', 'coc_template_item_ids',
                              'salary_constraint_ids', 'analytic_account_id', 'constraint_ids']
                if field in field_list:
                    for node in doc.xpath("//field[@name='%s']" % field):
                        modifiers = simplejson.loads(node.get("modifiers"))
                        if 'readonly' not in modifiers:
                            modifiers['readonly'] = [['state', 'not in', ['to_edit', 'draft']]]
                        else:
                            if type(modifiers['readonly']) != bool:
                                modifiers['readonly'].insert(0, '|')
                                modifiers['readonly'] += [
                                    ['state', 'not in', ['draft', 'to_edit']]]
                        node.set('modifiers', simplejson.dumps(modifiers))
                        res['arch'] = etree.tostring(doc)
        return res

    @api.depends('constraint_ids')
    @api.onchange('constraint_ids')
    def check_exist_product_in_line(self):
        for request in self:
            exist_product_list = []
            for line in request.constraint_ids:
                if line.product_id and line.grade_id and line.period:
                    if (line.product_id.id, line.grade_id.id, line.period) in exist_product_list:
                        raise ValidationError(_('Service/Grade/Period must be unique'))
                    exist_product_list.append((line.product_id.id, line.grade_id.id, line.period))

    @api.constrains('contract_value')
    def _check_contract_value(self):
        if self.contract_value == 0.0:
            raise UserError(_('Contract Value should not be zero.'))

    @api.constrains('top_cost_limit', 'bottom_cost_limit')
    def _check_limit_value(self):
        if self.top_cost_limit <= 0.0:
            raise UserError(_('Please Set Top Cost Limit >= 0.0'))
        if self.bottom_cost_limit >= 0.0:
            raise UserError(_('Please Set Bottom Cost Limit <= 0.0'))

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

    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    @api.model
    def _after_approval_states(self):
        return [('active', 'Active'), ('rejected', 'Rejected')]

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

    def create_user(self):
        user_id = self.env['res.users'].sudo().create(
            {
                'name': self.owner_id.name,
                'login': self.owner_id.email,
                'partner_id': self.owner_id.id,
                'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],

            })
        return user_id


    def create_project(self):
        project = self.env['project.project'].create(
            {
                'project_request_id': self.id,
                'name': self.name,
                'categ_id': self.categ_id.id,
                'partner_id': self.partner_id.id,
                'date_start': self.date_start,
                'date': self.date,
                'user_id': self.user_id.id,
                'owner_id': self.owner_id.id,
                'coc_template_id': self.coc_template_id.id,
                'petty_cash_allowed': self.petty_cash_allowed,
                'petty_cash_responsible_id': self.petty_cash_responsible_id.id if self.petty_cash_responsible_id else False,
                'contract_value': self.contract_value,
                'vat_included': self.vat_included,
                'actual_value': self.actual_value,
                'markup': self.markup,
                'budget': self.budget,
                'top_cost_limit': self.top_cost_limit,
                'bottom_cost_limit': self.bottom_cost_limit,
                'analytic_account_id': self.analytic_account_id.id,
                'state': self.state,
                'service_ids': [(6,0,self.service_ids.ids)],
                'constraint_ids': self.constraint_ids.ids,
                'salary_constraint_ids': self.salary_constraint_ids.ids,
                'coc_template_item_ids': [(6, 0, self.coc_template_item_ids.ids)],
                'project_state': 'active',
                'structure_type_id': self.structure_type_id.id,
                'structure_id': self.structure_id.id,
                'max_loan_percentage': self.max_loan_percentage,
                'max_loan_installments': self.max_loan_installments,
                'salary_rule_ids': [(6, 0, self.salary_rule_ids.ids)],

            })
        return project

    def action_approve(self):
        if self.state == 'to_active':
            self.write({'state': 'active'})
            self.message_post(attachment_ids=[], body="Project '%s' Created, Please Check." % (self.name),
                              content_subtype='html',
                              message_type='notification', partner_ids=[self.user_id.partner_id.id],
                              email_from=self.env.user.partner_id.email,
                              author_id=self.env.user.partner_id and self.env.user.partner_id.id)
            self.owner_id.project_owner = True
            if self.petty_cash_allowed:
                self.owner_id.petty_cash_responsible = True
            project_id = self.create_project()
            self.constraint_ids.write({'project_id': project_id.id})
            self.coc_template_item_ids.write({'project_id': project_id.id})
            self.salary_constraint_ids.write({'project_id': project_id.id})
            self.owner_id.write({'project_ids':[(6,0,project_id.ids)]})


            # self.structure_type_id.write({'project_id': [(6,0,project_id.ids)]})
            # self.structure_id.write({'project_id': [(6,0,project_id.ids)]})
            # self.salary_rule_ids.write({'project_id': [(6,0,project_id.ids)]})
            if self.business_domain:
                analytic_account = project_id.create_analytic_account(self.name, self.partner_id.id, self.business_domain.id)
            else:
                analytic_account = project_id.create_analytic_account(self.name, self.partner_id.id)

            self.owner_id.write({'project_ids': [(4, project_id.id)]})
            self.project_id = project_id.id
            self.project_id.analytic_account_id = analytic_account.id
            self.project_id.generate_cost()
            self.analytic_account_id = analytic_account.id
            if self.state == 'active' and self.owner_id:
                users = self.env['res.users'].search([('login', '=', self.owner_id.email)])
                if users:
                    if not users.partner_id.project_owner:
                        users.partner_id.project_owner = True
                else:
                    self.create_user()
        elif self.state == 'to_edit':
            self.write({'state': 'to_approve'})
        elif self.state == 'draft':
            self.write({'state': 'to_approve'})
        else:
            return super(ProjectRequest, self).action_approve()

    def _on_approve(self):
        result = super(ProjectRequest, self)._on_approve()
        self.write({'state': 'to_edit'})
        self.message_post(attachment_ids=[], body="Project Request '%s' In 'To Edit' State Please Check." % (self.name),
                          content_subtype='html',
                          message_type='notification', partner_ids=[self.user_id.partner_id.id],
                          email_from=self.env.user.partner_id.email,
                          author_id=self.env.user.partner_id and self.env.user.partner_id.id)
        return result

    @api.model
    def create(self, vals_list):
        self.env['res.partner'].browse(vals_list['owner_id']).write({'project_owner': True})
        if 'petty_cash_responsible_id' in vals_list:
            self.env['res.partner'].browse(vals_list['petty_cash_responsible_id']).write({'petty_cash_responsible': True})
        res = super(ProjectRequest, self).create(vals_list)

        return res

    def write(self, vals):
        if 'petty_cash_responsible_id' in vals:
            self.env['res.partner'].browse(self.petty_cash_responsible_id.id).write({'petty_cash_responsible': False})
            self.env['res.partner'].browse(vals['petty_cash_responsible_id']).write({'petty_cash_responsible': True})
        return super(ProjectRequest, self).write(vals)

    def action_reject(self, reason=None):
        if self.state != 'to_edit':
            self.write({'state': 'to_edit'})
        else:
            self.write({'state': 'rejected'})
        if reason:
            self.message_post(body=reason, subject="Reject Reason")


class ProjectCocTemplateItems(models.Model):
    _name = 'project.coc.template.items'
    project_request_id = fields.Many2one("project.request")
    project_id = fields.Many2one("project.project")
    coc_template_id = fields.Many2one("coc.template", related='project_request_id.coc_template_id')
    coc_template_item_id = fields.Many2one("coc.template.items")
    account_id = fields.Many2many("account.account", string="Account", related='coc_template_item_id.account_id')
    margin = fields.Float("Margin(%)", related='project_id.markup', readonly=False)

    @api.depends('coc_template_item_id')
    @api.onchange('coc_template_item_id')
    def onchange_coc_template_item_id(self):
        exsist_items = self.project_request_id.coc_template_item_ids.coc_template_item_id
        if exsist_items:
            domain = {
                'domain': {'coc_template_item_id': [('coc_template_id', '=', self.coc_template_id.id), ('id', 'not in', exsist_items.ids)]}}
            return domain
