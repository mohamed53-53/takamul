from odoo import api, fields, models


class Project(models.Model):
    _name = "project.project"
    _inherit = ['approval.record', 'project.project']

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to approve', 'To Approve'),
        ('to finance', 'To Finance'),
        ('active', 'Active'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    @api.model
    def _before_approval_states(self):
        return [('draft', 'Draft')]

    @api.model
    def _after_approval_states(self):
        return [('active', 'Active'), ('done', 'Done'), ('rejected', 'Rejected'), ('cancel', 'Cancelled')]

    def button_confirm(self):
        for project in self:
            if project.state not in ['draft']:
                continue
            project.action_approve()

            # if order.partner_id not in order.message_partner_ids:
            #     order.message_subscribe([order.partner_id.id])
        return True

    def button_cancel(self):
        self._remove_approval_activity()
        return super(Project, self).button_cancel()

    # def _on_approve(self):
    #     self.button_approve()

    @api.onchange('state')
    def _on_change_state(self):
        if self.state == 'active' and self.owner_id:
            users = self.env['res.users'].search([('login', '=', self.owner_id.email)])
            if users:
                if not users.partner_id.project_owner:
                    users.write({'project_owner': True,
                                 'project_ids': [(4, self.id, False)], })
            else:
                user_id = self.env['res.users'].sudo.create(
                    {'name': self.owner_id, 'login': self.owner_id.email, 'project_owner': True,
                     'project_ids': [(4, self.id, False)]})
