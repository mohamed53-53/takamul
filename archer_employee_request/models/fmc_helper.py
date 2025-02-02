def handle_approve_fcm_msg(obj):
        fcms = obj.create_uid.mapped('fmc_key')
        model_string = obj.env['ir.model'].sudo().search([('model', '=', obj._name)]).name
        obj_state = ''
        if obj.state == 'approved':
            obj_state = 'Approved'
        if obj.state == 'rejected':
            obj_state = 'Rejected'
        msg = obj.env['archer.fcm.notify'].sudo().send_fcm_notify(client_key=fcms,
                                                                  msg_header='%s' % model_string,
                                                                  msg_body='%s\nYour %s: %s \n%s' % (
                                                                      model_string,
                                                                      model_string, obj.sequence,
                                                                      obj_state))