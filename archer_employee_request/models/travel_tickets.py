from odoo.addons.archer_employee_request.models.fmc_helper import handle_approve_fcm_msg
from odoo.addons.archer_api_custom.controllers.utils.utils import get_next_approve
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from lxml import etree
import json
import simplejson


class TravelTickets(models.Model):
    _name = "travel.tickets"
    _inherit = ["mail.thread", "mail.activity.mixin", "approval.record"]
    _rec_name = "sequence"
    _description = 'Travel Tickets'

    sequence = fields.Char(string="Sequence", copy=False, readonly=True, default=lambda x: _("New"))
    employee_id = fields.Many2one("hr.employee", required=True)
    project_id = fields.Many2one(comodel_name="project.project", related="employee_id.project_id")
    purpose = fields.Selection(
        selection=[("business_trip", _("Business Trip")), ("personal_vacation", _("Personal Vacation")), ],
        string="Purpose", required=True)
    travel_type = fields.Selection(selection=[("one_way", _("One Way")), ("round_trip", _("Round Trip"))],
                                   string="Type", required=True)
    origin = fields.Char(string="Origin", required=True)
    destination = fields.Char(string="Destination", required=True)
    date_from = fields.Date(string="Date (From)", required=True)
    date_to = fields.Date(string="Date (To)", required=True)
    travel_class = fields.Selection(selection=[("guest", _("Guest")), ("business", _("Business"))], string="Class",
                                    required=True)
    other_travelers = fields.Boolean(string="Other Travelers")
    other_travelers_ids = fields.One2many(comodel_name='other.travelers', inverse_name="travel_ticket_id",
                                          string="Other Travelers")
    amount = fields.Float(string="Expense Amount", required=True)
    rejection_reason = fields.Text("Rejection Reason", copy=False)
    state = fields.Selection([])
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

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(TravelTickets, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
                                                         submenu=False)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in res['fields']:
                for node in doc.xpath("//field[@name='%s']" % field):
                    modifiers = json.loads(node.get("modifiers"))
                    if 'readonly' not in modifiers:
                        modifiers['readonly'] = [['state', '!=', 'draft']]
                    else:
                        if type(modifiers['readonly']) != bool:
                            modifiers['readonly'].insert(0, '|')
                            modifiers['readonly'] += [['state', '!=', 'draft']]
                    node.set('modifiers', json.dumps(modifiers))
                    res['arch'] = etree.tostring(doc)
        return res

    @api.model
    def create(self, vals):
        if not vals.get("sequence") or vals["name"] == _("New"):
            vals["sequence"] = self.env["ir.sequence"].next_by_code("travel.tickets") or "/"
        return super().create(vals)

    @api.constrains('date_from', 'date_to')
    def _check_date(self):
        if self.date_from and self.date_from <= fields.Date.today():
            raise UserError(_('Date From Must be Greater Than Today.'))
        if self.date_to and self.date_to <= self.date_from:
            raise UserError(_('Date To Must be Greater Than Date From.'))

    @api.constrains('amount')
    def _check_expense_amount(self):
        if self.amount <= 0.0:
            raise UserError(_('Expense Amount must be greater then Zero.'))

    @api.model
    def _before_approval_states(self):
        return [("draft", _("Draft"))]

    def action_reject(self, reason=None):
        self.write({'state': 'rejected'})
        if reason:
            self.message_post(body=reason, subject=_("Reject Reason"))

    def action_approve(self):
        for rec in self:
            if rec.state == 'draft':
                self.write({"state": "submit"})
            elif rec.state == 'po_approve':
                rec.write({'state': get_next_approve(rec)})
            else:
                return super(TravelTickets, self).action_approve()

    def write(self, vals):
        res = super(TravelTickets, self).write(vals)
        if self.state in ['approved','rejected']:
            handle_approve_fcm_msg(self)
        return res

class OtherTravelers(models.Model):
    _name = "other.travelers"

    traveler_name = fields.Char(string="Traveler Name", required=True)
    relation = fields.Selection([("spouse", _("Spouse")), ("children", _("Children")), ("infant", _("Infant"))],
                                string="Relation", required=True)
    travel_ticket_id = fields.Many2one("travel.tickets")
