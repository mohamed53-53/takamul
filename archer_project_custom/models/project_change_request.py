from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectChangeRequest(models.Model):
    _name = "project.change.request"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record', ]
    _rec_name = 'name'

    name = fields.Char("Name")
    project_id = fields.Many2one("project.project")
    new_user_id = fields.Many2one('res.users', "Project Manager")
    project_manager = fields.Many2one('res.users')
    new_owner_id = fields.Many2one('res.partner', "project Owner")
    project_owner_id = fields.Many2one('res.partner')
    date = fields.Date("End Date")
    new_end_date = fields.Date("End Date")
    contract_value = fields.Float("Contract Value")
    new_project_contract_value = fields.Float("Contract Value")
    vat_included = fields.Boolean("VAT Included?")
    new_vat_included = fields.Boolean("VAT Included?")
    markup = fields.Float("Markup (%)")
    new_markup = fields.Float("Markup (%)")
    request_type = fields.Selection(
        [('actors', 'Actors'), ('time_and_value', 'Time & Value')],
        string="Request", default='actors')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', "Done"),
        ('cancel', "Cancel"),], readonly=True, index=True, copy=False, default='draft', tracking=True)

    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    @api.model
    def _after_approval_states(self):
        return [('done', 'Done'), ('cancel', 'Cancel')]

    def create_user(self):
        user_id = self.env['res.users'].create(
            {
                'name': self.project_owner_id.name,
                'login': self.project_owner_id.email,
                'partner_id': self.project_owner_id.id,
                'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],

            })
        user_id.partner_id.project_owner = True
        return user_id

    def _on_approve(self):
        self.write({'state': 'done'})
        values = {}
        if self.request_type == 'actors':
            values = {
                'user_id': self.new_user_id.id,
                'owner_id': self.new_owner_id.id,
            }
        elif self.request_type == 'time_and_value':
            values = {
                'contract_value': self.new_project_contract_value,
                'vat_included': self.new_vat_included,
                'markup': self.new_markup,
                'date': self.new_end_date,
            }
        else:
            raise UserError(_('Please Select Request Type.'))
        self.project_id.update(values)
        self.project_id.project_request_id.update(values)

        if self.project_id.state == 'active' and self.project_owner_id:
            users = self.env['res.users'].search([('login', '=', self.project_owner_id.email)])
            partner = self.env['res.partner'].search([('project_ids', 'in', self.project_id.id)])
            if partner:
                partner.update({'project_ids': [(3, self.project_id.id)]})
            self.project_owner_id.write({'project_ids': [(4, self.project_id.id)]})
            if users:
                if not users.partner_id.project_owner:
                    users.partner_id.project_owner = True
            else:
                self.create_user()

    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.model
    def create(self, vals):
        request = super(ProjectChangeRequest, self).create(vals)
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('project.change.sequence') or _('New')
        if request.project_id:
            request.project_id.write({'project_change_request_ids': [(4, self.id)]})
        return request

