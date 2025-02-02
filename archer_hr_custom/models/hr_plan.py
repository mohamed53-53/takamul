from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class HrBoardingPlanActivityType(models.Model):
    _name = "hr.boarding.plan.activity.type"

    name = fields.Char(string='Name', copy=False, required=True, tracking=True)


class HrBoardingPlan(models.Model):
    _name = "hr.boarding.plan"

    name = fields.Char(string='Name', copy=False, required=True, tracking=True)
    activity_ids = fields.One2many('hr.boarding.plan.activity', 'boarding_plan_id', string="Activities")
    project_id = fields.Many2one(comodel_name="project.project", string="Project", required=False)
    plan_type = fields.Selection(
        [('onboarding', _('Onboarding')), ('offboarding', _('Offboarding'))],
        string="Plan Type")

    @api.constrains('activity_ids')
    def validate_payment(self):
        if not self.project_id:
            plans = self.search([('project_id', '=', False), ('id', '!=', self.id)])
            if plans:
                raise UserError(_("You cannot have 2 plans without project."))
        else:
            plans = self.search([('project_id', '=', self.project_id.id), ('plan_type', '=', 'onboarding'),
                                 ('id', '!=', self.id)])
            if plans:
                raise UserError(_("You cannot have 2 onboarding plans for the same project."))
        for activity in self:
            if not activity.activity_ids:
                raise UserError(_("You must add at least one activity."))


class HrBoardingPlanActivity(models.Model):
    _name = "hr.boarding.plan.activity"

    boarding_plan_id = fields.Many2one('hr.boarding.plan')
    name = fields.Many2one('hr.boarding.plan.activity.type', "Activity", required=True, tracking=True)
    user_id = fields.Many2one('res.users', "Responsible", required=True, tracking=True)
    no_of_days = fields.Integer(string="Days To Complete", required=True, default=2)


class HrBoardingPlanEmployee(models.Model):
    _name = "hr.boarding.plan.employee"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    boarding_plan_id = fields.Many2one('hr.boarding.plan')
    name = fields.Many2one('hr.boarding.plan.activity', "Activity", required=True, tracking=True)
    user_id = fields.Many2one('res.users', "Responsible", required=True, tracking=True)
    employee_id = fields.Many2one('hr.employee', "Employee", required=True, tracking=True)
    state = fields.Selection(string="Status", selection=[('new', 'New'), ('done', 'Done'), ], required=False,
                             default='new')
    no_of_days = fields.Integer(string="Days To Complete", required=True, )
    assign_date = fields.Date(string='Assign Date')
    done_date = fields.Date(string='Done Date')
    description = fields.Char(string="Description", required=False)
    deadline_date = fields.Date(string='Deadline Date')

    def action_confirm(self):
        self.state = 'done'
        self.done_date = fields.Date.today()
