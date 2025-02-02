# -*- coding: utf-8 -*-
from odoo.addons.archer_employee_request.models.fmc_helper import handle_approve_fcm_msg
from odoo.addons.archer_api_custom.controllers.utils.utils import get_next_approve
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from lxml import etree
import json
import simplejson


class LeaveRequest(models.Model):
    _name = "leave.request"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'approval.record']
    _rec_name = 'sequence'
    _description = 'Leave Request'
    sequence = fields.Char('Sequence', copy=False, readonly=True, default=lambda x: _('New'))
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    project_id = fields.Many2one(comodel_name="project.project", related="employee_id.project_id", string="Project")
    leave_type_id = fields.Many2one(comodel_name="hr.leave.type", string="Leave Type", required=True)
    leave_type_id_domain = fields.Char(
        compute="_compute_leave_type_id_domain",
        readonly=True,
        store=False,
    )
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    number_of_days = fields.Integer(string="Leave Days", compute="_compute_number_of_days")
    desc = fields.Text(string="Description")
    leave_current_balance = fields.Float(string="Leave Current Balance", required=True)
    balance_after_leave = fields.Float(string="Balance After Leave", compute="_get_balance_after_leave")
    allow_extend = fields.Boolean(string="Allow Extend ?", compute="_get_allow_extend")
    supportive_document = fields.Binary(string="Supportive Document", attachment=True)
    state = fields.Selection(selection=[])
    rejection_reason = fields.Text("Rejection Reason")
    can_cancel = fields.Boolean(string='Can Cancel', default=False, compute='_compute_can_cancel_approve')
    can_approve = fields.Boolean(string='Can Approve', default=False, compute='_compute_can_cancel_approve')
    active = fields.Boolean(string='Active', default=True)
    account_move_id = fields.Many2one(comodel_name='account.move', string='Related Entry')

    def _compute_can_cancel_approve(self):
        for rec in self:
            rec.can_cancel = True if rec.state in ['submit'] and rec.env.uid == rec.create_uid.id else False
            state = rec.env['approval.config'].sudo().search([('model', '=', rec._name), ('state', '=', rec.state)],
                                                             limit=1)
            if state:
                if rec.env.uid in state.group_ids.users.ids:
                    rec.can_approve = True
                else:
                    rec.can_approve = False
            else:
                rec.can_approve = False

    @api.depends('project_id')
    def _compute_leave_type_id_domain(self):
        for rec in self:
            domain = [('id', 'in',
                       rec.project_id.leave_type_ids.ids)] if rec.project_id and rec.project_id.leave_type_ids else []
            rec.leave_type_id_domain = json.dumps(domain)

    @api.depends('date_from', 'date_to')
    def _compute_number_of_days(self):
        for rec in self:
            days = 0
            if rec.date_from and rec.date_to:
                no_days = rec.date_to - rec.date_from
                days = no_days.days
            rec.number_of_days = days

    @api.depends('leave_current_balance', 'number_of_days')
    def _get_balance_after_leave(self):
        for rec in self:
            balance_after_leave = rec.leave_current_balance
            if rec.number_of_days:
                balance_after_leave -= rec.leave_current_balance
            rec.balance_after_leave = balance_after_leave

    @api.depends('leave_type_id')
    def _get_allow_extend(self):
        for rec in self:
            rec.allow_extend = True if rec.leave_type_id.employee_requests == 'yes' else False

    @api.onchange('employee_id')
    def get_leave_current_balance(self):
        for rec in self:
            rec.leave_current_balance = rec.employee_id.monthly_balance if rec.employee_id else 0.0


    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(LeaveRequest, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
                                                        submenu=False)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in res['fields']:
                for node in doc.xpath("//field[@name='%s']" % field):
                    modifiers = simplejson.loads(node.get("modifiers"))
                    if 'readonly' not in modifiers:
                        modifiers['readonly'] = [['state', '!=', 'draft']]
                    else:
                        if type(modifiers['readonly']) != bool:
                            modifiers['readonly'].insert(0, '|')
                            modifiers['readonly'] += [['state', '!=', 'draft']]
                    node.set('modifiers', simplejson.dumps(modifiers))
                    res['arch'] = etree.tostring(doc)
        return res

    @api.model
    def create(self, vals):
        if (not vals.get('sequence') or vals['name'] == _('New')):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('leave.request') or '/'
        return super().create(vals)

    @api.constrains('date_from', 'date_to')
    def _check_date(self):
        if self.date_from and self.date_from <= fields.Date.today():
            raise UserError(_('Date From Must be Greater Than Today.'))
        if self.date_to and self.date_to <= self.date_from:
            raise UserError(_('Date To Must be Greater Than Date From.'))

    def _before_approval_states(self):
        return [("draft", "Draft")]

    def action_reject(self, reason=None):
        for rec in self:
            rec.write({'state': 'rejected'})
            if reason:
                rec.message_post(body=reason, subject="Reject Reason")

    def action_approve(self):
        for rec in self:
            if rec.state == 'draft':
                rec.write({'state': 'submit'})
            elif rec.state == 'submit':
                if rec.balance_after_leave <= 0 and not rec.allow_extend:
                    raise UserError("Balance after Leave should be greater than 0 !")
                if rec.allow_extend or rec.balance_after_leave > 0:
                    if rec.create_new_leave():
                        return super(LeaveRequest, self).action_approve()
                    else:
                        raise UserError(_("Couldn't create leave for this employee !"))
            elif rec.state == 'po_approve':
                rec.write({'state': get_next_approve(rec)})
            else:
                return super(LeaveRequest, self).action_approve()

    def create_new_leave(self):
        vals = {
            'employee_id': self.employee_id.id,
            'employee_ids': [(6,0, [self.employee_id.id])],
            'holiday_status_id': self.leave_type_id.id,
            'holiday_type': 'employee',
            'request_date_from': self.date_from,
            'request_date_to': self.date_to,
        }
        leave_id = self.env['hr.leave'].sudo().create(vals)
        return bool(leave_id)

    def write(self, vals):
        res = super(LeaveRequest, self).write(vals)
        if self.state in ['approved','rejected']:
            handle_approve_fcm_msg(self)
        return res