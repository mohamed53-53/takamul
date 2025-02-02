import datetime

from odoo import models, fields, api

class AccountPayment(models.Model):
    _inherit = 'account.payment'
    revision_id = fields.Many2one(comodel_name='account.expense.revision', string="Expense")
    for_revision = fields.Boolean(string='For Expense')
    def action_post(self):
        if self.for_revision:
            self.revision_id.write({'payment_status': 'paid'})
        return super(AccountPayment, self).action_post()

class AccountMove(models.Model):
    _inherit = 'account.move'
    model_name = fields.Char(compute='_compute_model_name')
    origin_id = fields.Integer(string='Origin ID', readonly=True)
    project_id = fields.Many2one(comodel_name='project.project')


class ServiceAccount(models.Model):
    _name = 'account.expense.service'
    _description = 'Request Service'
    _rec_name = 'product_id'
    product_id = fields.Many2one(comodel_name='product.template', string='Product', domain=[('provide_service', '=', True)], required=True)
    model_id = fields.Many2one(comodel_name='ir.model', string='Service', required=True, ondelete='cascade')


class AccountExpense(models.Model):
    _name = 'account.expense.revision'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Expense'
    _rec_name = 'sequence'

    origin_model = fields.Char(string='Source', readonly=True)
    model_name = fields.Char(compute='_compute_model_name')
    origin_id = fields.Integer(string='Origin ID', readonly=True)
    reference = fields.Char(string='Source Reference', readonly=True)
    sequence = fields.Char(string="Sequence", readonly=True)
    project_id = fields.Many2one(comodel_name='project.project', string='Project', readonly=True)
    customer_id = fields.Many2one(comodel_name='res.partner', related='project_id.partner_id')
    expense_account_id = fields.Many2one(comodel_name='account.account', string='Expense Account')
    accrued_expense_account_id = fields.Many2one(comodel_name='account.account', string='Accrued Expense Account')
    accrued_expense_journal_id = fields.Many2one(comodel_name='account.journal', string='Accrued Expense Journal')
    company_id = fields.Many2one(comodel_name='res.company', related='project_id.company_id')
    currency_id = fields.Many2one(comodel_name='res.currency', related='company_id.currency_id')
    amount = fields.Monetary(string='Amount', currency_field='currency_id', readonly=True)
    state = fields.Selection(selection=[('draft', 'Draft'), ('confirm', 'Confirm'), ('post', 'Post'), ])
    account_move_id = fields.Many2one(comodel_name='account.move', string='Journal Entry')
    payment_id = fields.Many2one(comodel_name='account.payment', string='Payment')
    payment_state = fields.Selection(related='payment_id.state')
    payment_status = fields.Selection(selection=[('not_paid','Not Paid'), ('in_payment','In Payment'), ('paid', 'Paid')], default='not_paid')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', related='project_id.analytic_account_id', string='Analytic Account')
    def _compute_model_name(self):
        for rec in self:
            rec.model_name = self.env['ir.model'].search([('model', '=', rec.origin_model)]).name

    @api.model
    def create(self, vals_list):
        vals_list['sequence'] = self.env['ir.sequence'].next_by_code('archer_project_custom.account_expense_revision_seq') or '/'
        return super(AccountExpense, self).create(vals_list)

    def action_confirm(self):
        for rec in self:
            if rec.state == 'draft':
                move = self.create_expense_journal_entry(obj=rec)

                move.message_post_with_view('mail.message_origin_link',
                                            values={'self': move, 'origin': rec},
                                            subtype_id=self.env.ref('mail.mt_note').id)
                self.env[rec.origin_model].search([('id', '=', rec.origin_id)]).write({'account_move_id': move.id})
                rec.write({
                    'account_move_id': move.id,
                    'state': 'confirm'
                })

    def create_expense_journal_entry(self, obj):
        vals = {
            'move_type': 'entry',
            'date': datetime.datetime.now().date(),
            'ref': obj.sequence,
            'model_name': obj._name,
            'origin_id': obj.id,
            'project_id': obj.project_id.id,
            'journal_id': obj.accrued_expense_journal_id.id,
            'line_ids': [
                (0, 0, {
                    'name': obj.model_name + ' ' + obj.sequence,
                    'account_id': obj.expense_account_id.id,
                    'currency_id': obj.currency_id.id,
                    'debit': obj.amount,
                    'credit': 0.0,
                    'partner_id': obj.project_id.partner_id.id,
                    'analytic_account_id': obj.project_id.analytic_account_id.id
                }),
                (0, 0, {
                    'name': obj.model_name + ' ' + obj.sequence,
                    'account_id': obj.accrued_expense_account_id.id,
                    'currency_id': obj.currency_id.id,
                    'debit': 0.0,
                    'credit': obj.amount,
                }),
            ],
        }
        return self.env['account.move'].create(vals)

    def action_entry_post(self):
        for rec in self:
            if rec.state == 'confirm':
                rec.account_move_id.action_post()
                rec.write({'state': 'post'})

    def action_confirm_entry_post(self):
        for rec in self:
            if rec.state == 'draft':
                rec.action_confirm()
                rec.action_entry_post()

    def action_confirm_payment(self):
        self.ensure_one()
        payment = self.env['account.payment'].create({
            'payment_type': 'outbound',
            'partner_type': 'customer',
            'amount': self.amount,
            'date': fields.Date.today(),
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'ref': 'Expense of %s - %s'%(self.model_name,self.reference),
            'analytic_account_id':self.project_id.analytic_account_id.id,
            'revision_id':self.id,
            'for_revision':True,
        })
        self.write({'payment_id':payment.id,'payment_status':'in_payment'})
