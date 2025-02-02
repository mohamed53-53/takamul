from odoo import api, fields, models


class HRLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    create_entry = fields.Boolean()
    journal_id = fields.Many2one(comodel_name="account.journal")
    source_account_id = fields.Many2one(comodel_name="account.account")
    destination_account_id = fields.Many2one(comodel_name="account.account")
    check_leave = fields.Boolean(string="Check Leave")
    def get_days(self, employee_id):
        # need to use `dict` constructor to create a dict per id
        result = dict((id, dict(max_leaves=0, leaves_taken=0, remaining_leaves=0,time_off_days=0, virtual_remaining_leaves=0)) for id in self.ids)

        requests = self.env['hr.leave'].search([
            ('employee_id', '=', employee_id),
            ('state', 'in', ['confirm', 'validate1', 'validate']),
            ('holiday_status_id', 'in', self.ids)
        ])
        print('zzzzzzzzzzzzzzzzzzzzsa')
        print(requests)

        allocations = self.env['hr.leave.allocation'].search([
            ('employee_id', '=', employee_id),
            ('state', 'in', ['confirm', 'validate1', 'validate']),
            ('holiday_status_id', 'in', self.ids)
        ])

        for request in requests:
            status_dict = result[request.holiday_status_id.id]
            status_dict['virtual_remaining_leaves'] -= (request.number_of_hours_display
                                                    if request.leave_type_request_unit == 'hour'
                                                    else request.number_of_days)
            print("2222222222222")
            status_dict['time_off_days'] = self.env['hr.employee'].search([('id', '=', employee_id)]).time_off_days

            if request.state == 'validate':
                status_dict['leaves_taken'] += (request.number_of_hours_display
                                            if request.leave_type_request_unit == 'hour'
                                            else request.number_of_days)
                status_dict['remaining_leaves'] -= (request.number_of_hours_display
                                                if request.leave_type_request_unit == 'hour'
                                                else request.number_of_days)
            print(result, '<=====''>')

        for allocation in allocations.sudo():

            status_dict = result[allocation.holiday_status_id.id]
            # status_dict['virtual_remaining_leaves'] -= (request.number_of_hours_display
            #                                         if request.leave_type_request_unit == 'hour'
            #                                         else request.number_of_days)
            if allocation.state == 'validate':
                # note: add only validated allocation even for the virtual
                # count; otherwise pending then refused allocation allow
                # the employee to create more leaves than possible
                status_dict['virtual_remaining_leaves'] += (allocation.number_of_hours_display
                                                          if allocation.type_request_unit == 'hour'
                                                          else allocation.number_of_days)
                status_dict['max_leaves'] += (allocation.number_of_hours_display
                                            if allocation.type_request_unit == 'hour'
                                            else allocation.number_of_days)
                status_dict['remaining_leaves'] += (allocation.number_of_hours_display
                                                  if allocation.type_request_unit == 'hour'
                                                  else allocation.number_of_days)
                status_dict['time_off_days'] = self.env['hr.employee'].search([('id','=',employee_id)]).time_off_days

            print(result, '<=====''>')

        return result

class HRLeave(models.Model):
    _inherit = 'hr.leave'
    TimeOffAmount = fields.Float(string="Time Off Amount",compute="ComputeTimeOffAmount")
    def ComputeTimeOffAmount(self):
        for rec in self:
            rec.TimeOffAmount = rec.employee_id.contract_id.day_value * rec.number_of_days if rec.number_of_days >= 1 else 1
    def action_approve(self):
        res = super(HRLeave, self).action_approve()
        if self.holiday_status_id.create_entry:
            move = self.env['account.move'].sudo().create({'journal_id': self.holiday_status_id.journal_id.id,
                                                    'ref': self.employee_id.name
                                                    })
            self.env['account.move.line'].with_context(check_move_validity=False).sudo().create(
                {'account_id': self.holiday_status_id.source_account_id.id,
                 'debit': self.employee_id.contract_id.day_value * self.number_of_days if self.number_of_days >= 1 else 1,
                 'move_id': move.id,
                 'partner_id': self.employee_id.address_home_id.id
                 })
            self.env['account.move.line'].with_context(check_move_validity=False).sudo().create(
                {'account_id': self.holiday_status_id.destination_account_id.id,
                 'credit': self.employee_id.contract_id.day_value * self.number_of_days if self.number_of_days >= 1 else 1,
                 'move_id': move.id,
                 'partner_id': self.employee_id.address_home_id.id
                 })
            # for usr in self.env.ref('saudi_hr_eos.group_leave_accounting').users:
            #     activity = self.env['mail.activity'].sudo().create({
            #         'activity_type_id': self.env.ref("mail.mail_activity_data_todo").id,
            #         'user_id': usr.id,
            #         'res_id': move.id,
            #         'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'account.move')], limit=1).id,
            #     })

        return res
