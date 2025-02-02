from datetime import timedelta, datetime
from pytz import timezone
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EmployeeProjectTransferBatch(models.Model):
    _name = 'employee.project.transfer.batch'
    _rec_name = 'project_id'

    date = fields.Date(string="Date", required=1, default=fields.Date.context_today)
    project_id = fields.Many2one('project.project', string='New Project', required=1)
    src_project_id = fields.Many2one('project.project', string='Source Project')
    state = fields.Selection(string="State", selection=[('draft', 'Draft'), ('confirmed', 'Confirmed')],
                             default='draft', required=1)
    transfer_ids = fields.One2many(comodel_name="employee.project.transfer", inverse_name='batch_id',
                                   string="Transfers")
    employee_ids = fields.Many2many(comodel_name="hr.employee", relation="employee_transfer_batch_rel",
                                    column1="batch_id", column2="employee_id", string="Employees")

    @api.onchange('src_project_id')
    def get_employee_domain(self):
        if self.src_project_id:
            return {'domain': {'employee_ids': [('project_id', '=', self.src_project_id.id)]}}
        else:
            return {'domain': {'employee_ids': []}}

    @api.onchange('employee_ids')
    def onchange_employee_ids(self):
        for record in self:
            employee_list = record.transfer_ids.mapped('employee_id').ids
            transfer_vals = []
            del_list = list(set(employee_list) - set(record.employee_ids.ids))
            record.write({'transfer_ids': [(2, c.id) for c in record.transfer_ids.filtered(lambda m: m.employee_id.id in del_list)]})
            for rec in record.employee_ids.ids:
                if rec not in employee_list:
                    transfer_vals.append([0, 0, {
                        'employee_id': rec,
                        'project_id': record.project_id.id,
                        'date': record.date,
                    }])
            record.transfer_ids = transfer_vals

    def confirm(self):
        for rec in self.transfer_ids:
            if rec.current_project_id.date > rec.date:
                raise ValidationError("%s Current Project will end in %s", (rec.employee_id.name, rec.date))
            rec.confirm()
        self.state = 'confirmed'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_('You can delete draft transfers only.'))
        return super(EmployeeProjectTransferBatch, self).unlink()


class EmployeeProjectTransfer(models.Model):
    _name = 'employee.project.transfer'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=1, domain=[('contract_id', '!=', False)])
    contract_id = fields.Many2one('hr.contract', related='employee_id.contract_id')
    current_project_id = fields.Many2one('project.project', string='Current Project')
    analytic_account_id = fields.Many2one(related="current_project_id.analytic_account_id")
    date = fields.Date(string="Date", required=1)
    project_id = fields.Many2one('project.project', string='New Project', required=1)
    state = fields.Selection(string="State", selection=[('draft', 'Draft'), ('confirmed', 'Confirmed')],
                             default='draft', required=1)
    batch_id = fields.Many2one(comodel_name="employee.project.transfer.batch", string="", required=False)
    last_date_in_project = fields.Date(string="Last Date", compute='get_next_transfer_date', store=1)

    @api.constrains('date', 'employee_id', 'state')
    def check_uniqe_transfer(self):
        for rec in self:
            if rec.employee_id and rec.date and self.env['employee.project.transfer'].search_count(
                    [('date', '=', rec.date), ('employee_id', '=', rec.employee_id.id), ('state', '!=', 'draft')]) > 1:
                raise ValidationError(_('Employee has another transfer in the same day.'))

    @api.depends('employee_id.project_transfer_ids', 'employee_id.project_transfer_ids.state', 'date')
    def get_next_transfer_date(self):
        for rec in self:
            if rec.id:
                next_transfers = self.env['employee.project.transfer'].search(
                    [('date', '>', rec.date), ('id', '!=', rec.id)], order='date asc')
                rec.last_date_in_project = (next_transfers[0].date - timedelta(days=1)) if len(
                    next_transfers) else False
            else:
                rec.last_date_in_project = False

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id:
            self.current_project_id = self.employee_id.project_id.id
        else:
            self.current_project_id = False

    def confirm(self):
        self.state = 'confirmed'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_('You can delete draft transfers only.'))
        return super(EmployeeProjectTransfer, self).unlink()

    def transfer_employees(self):
        transfers = self.search([('date', '=', datetime.now().astimezone(timezone(self.env.user.tz)).date())])
        for rec in transfers:
            rec.employee_id.project_id = rec.project_id.id
            rec.employee_id.analytic_account_id = rec.project_id.analytic_account_id.id
            if rec.employee_id.contract_id:
                rec.employee_id.contract_id.date_end = rec.project_id.date
                rec.employee_id.contract_id.analytic_account_id = rec.project_id.analytic_account_id.id
