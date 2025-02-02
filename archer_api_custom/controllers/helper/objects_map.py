from odoo import _


def get_mob_state(obj):
    if not obj.state in ['draft', 'approved', 'rejected']:
        return 'pending'
    elif obj.state == 'rejected':
        return 'rejected'
    elif obj.state == 'approved':
        return 'approve'
    else:
        return 'pending'


def get_request_states(obj):
    states = obj.env['approval.config'].sudo().search([('model', '=', obj._name)], order='sequence')
    states_lis = states.mapped(lambda s: (s.state, s.name))
    return states_lis + [('draft', _('Draft')), ('rejected', _('Rejected')), ('approved', _('Approved'))]


def handle_create_fcm_msg(obj):
    state = obj.env['approval.config'].sudo().search(
        [('model', '=', obj._name), ('state', '=', 'submit')],
        limit=1)
    users_fcm = state.group_ids.users.filtered(lambda s: obj.project_id.id in s.project_ids.ids)
    if users_fcm:
        fcms = users_fcm.mapped('fmc_key')
        model_string = obj.env['ir.model'].sudo().search([('model', '=', obj._name)]).name
        msg = obj.env['archer.fcm.notify'].sudo().send_fcm_notify(client_key=fcms,
                                                                  msg_header='%s' % model_string,
                                                                  msg_body=_('[%s]%s\nEmployee: %s \nCreate %s Request') % (
                                                                      obj.create_uid.employee_id.project_id.name,
                                                                      obj.sequence, obj.create_uid.employee_id.name,
                                                                      model_string))


def get_po_can_approve(obj):
    state = obj.env['approval.config'].sudo().search([('model', '=', obj._name), ('state', '=', obj.state)], limit=1)
    if state:
        if obj.env.uid in state.group_ids.users.ids:
            return True
        else:
            return False
    else:
        return False


def map_generic_object(obj, desc):
    return {
        'id': obj.id,
        'mode_name': obj._name,
        'type': obj.env['ir.model'].sudo().search([('model', '=', obj._name)]).name,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'create_date': obj.create_date,
        'sequence': obj.sequence,
        'desc': desc or None,
        'mob_state': get_mob_state(obj) or None or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
    }


def map_business_trip(obj):
    return {
        'id': obj.id,
        'model_name': obj._name,
        'type': _('Business Trip'),
        'sequence': obj.sequence or None,
        'employee_id': obj.employee_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'project_id': obj.project_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'destination_country_id': obj.destination_country_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'destination_city_id': obj.destination_city_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'date_from': obj.date_from or None,
        'date_to': obj.date_to or None,
        'number_of_days': obj.number_of_days or None,
        'purpose': dict(obj._fields['purpose'].selection)[obj.purpose] or None,
        'occasion_or_purpose': obj.occasion_or_purpose or None,
        'supportive_document': obj.supportive_document or None,
        'state': dict(get_request_states(obj))[obj.state] or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'create_date': obj.create_date,
        'mob_state': get_mob_state(obj) or None,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': obj.occasion_or_purpose or None,
    }


def map_re_entry_visa(obj):
    return {
        'id': obj.id,
        'model_name': obj._name,
        'type': _('Exit & Re-Entry Visa'),
        'sequence': obj.sequence or None,
        'employee_id': obj.employee_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'project_id': obj.project_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'purpose': dict(obj._fields['purpose'].selection)[obj.purpose] or None,
        'visa_type': dict(obj._fields['visa_type'].selection)[obj.visa_type] or None,
        'date_from': obj.date_from or None,
        'date_to': obj.date_to or None,
        'visa_document': obj.visa_document or None,
        'amount': obj.amount or None,
        'state': dict(get_request_states(obj))[obj.state] or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'create_date': obj.create_date,
        'mob_state': get_mob_state(obj) or None,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': _('This Request us Related to a Exit & Re-Entry Visa'),

    }


def map_expense_request(obj):
    return {

        'id': obj.id,
        'model_name': obj._name,
        'type': _('Expense Request'),
        'sequence': obj.sequence or None,
        'employee_id': obj.employee_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'project_id': obj.project_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'expense_type': obj.expense_type_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'description': obj.description or None,
        'date_from': obj.date_from or None,
        'date_to': obj.date_to or None,
        'amount': obj.amount or None,
        'supportive_doc': obj.supportive_doc or None,
        'state': dict(get_request_states(obj))[obj.state] or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'create_date': obj.create_date,
        'mob_state': get_mob_state(obj) or None,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),

    }


def map_lone_advance(obj):
    return {
        'id': obj.id,
        'model_name': obj._name,
        'type': _('Loan Request'),
        'sequence': obj.sequence or None,
        'employee_id': obj.employee_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'project_id': obj.project_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'amount': obj.amount or None,
        'start_date': obj.start_date or None,
        'number_of_installments': obj.number_of_installments or None,
        'state': dict(get_request_states(obj))[obj.state] or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'create_date': obj.create_date,
        'mob_state': get_mob_state(obj) or None,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': _('This Request us Related to a Loan'),

    }


def map_residency_issuance(obj):
    res_isu_vals = {
        'id': obj.id,
        'model_name': 'residency.issuance',
        'type': _('Residency Issuance'),
        "sequence": obj.sequence or None,
        "residency_id": obj.residency_id.mapped(
            lambda r: {'id': r.id, 'name': r.name, 'residency_type': r.residency_type}) or None,
        "sponsor_name": obj.sponsor_name or None,
        "sponsor_phone": obj.sponsor_phone or None,
        "sponsor_address": obj.sponsor_address or None,
        "name": obj.name or None,
        "arabic_name": obj.arabic_name or None,
        "relation": obj.relation or None,
        "nationality": obj.nationality.mapped(lambda n: {'id': n.id, 'name': n.name}) or None,
        "religion": obj.religion or None,
        "date_of_birth": obj.date_of_birth or None,
        "job_title": obj.job_title or None,
        "state": obj.state or None,
        "gender": obj.gender or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'create_date': obj.create_date,
        'mob_state': get_mob_state(obj) or None,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': _('This Request us Related to a Residency Issuance'),

    }
    if obj.state == 'approve':
        res_isu_vals.update({'issued_residency': {
            "expiration_date_in_hijri": obj.expiration_date_in_hijri or None,
            "number": obj.number or None,
            "serial_number": obj.serial_number or None,
            "re_job_title": obj.re_job_title or None,
            "place_of_issuance": obj.place_of_issuance or None,
            "issuance_date": obj.issuance_date or None,
            "expiration_date": obj.expiration_date or None,
            "arrival_date": obj.arrival_date or None,
            'create_date': obj.create_date
        }})

    return res_isu_vals


def map_residency_renewal(obj):
    res_ren_vals = {

        'id': obj.id,
        'model_name': 'residency.renewal',
        'type': _('Residency Renewal'),
        "sequence": obj.sequence or None,
        "residency_id": obj.residency_id.mapped(
            lambda r: {'id': r.id, 'name': r.name, 'residency_type': r.residency_type}) or None,
        "sponsor_name": obj.sponsor_name or None,
        "sponsor_phone": obj.sponsor_phone or None,
        "sponsor_address": obj.sponsor_address or None,
        "name": obj.name or None,
        "arabic_name": obj.arabic_name or None,
        "relation": obj.relation or None,
        "nationality": obj.nationality.mapped(lambda n: {'id': n.id, 'name': n.name}) or None,
        "religion": obj.religion or None,
        "date_of_birth": obj.date_of_birth or None,
        "job_title": obj.job_title or None,
        "state": obj.state or None,
        "gender": obj.gender or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'create_date': obj.create_date,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': _('This Request us Related to a Residency Renewal'),

        'mob_state': get_mob_state(obj) or None,
        "old_residency": {
            "expiration_date_in_hijri": obj.expiration_date_in_hijri or None,
            "number": obj.number or None,
            "serial_number": obj.serial_number or None,
            "re_job_title": obj.re_job_title or None,
            "place_of_issuance": obj.place_of_issuance or None,
            "issuance_date": obj.issuance_date or None,
            "expiration_date": obj.expiration_date or None,
            "arrival_date": obj.arrival_date or None,

        }
    }
    if obj.state == 'approve':
        res_ren_vals.update({'new_residency': {
            'employee_renewal_residency_number': obj.employee_renewal_residency_number or None,
            'renewal_expiration_date': obj.renewal_expiration_date or None,
            'amount': obj.amount or None,
            'renewal_reason': obj.renewal_reason or None,

        }})
    return res_ren_vals


def map_residency_job_title(obj):
    res_job_val = {
        'id': obj.id,
        'model_name': obj._name,
        'type': _('Residency Job Request'),
        'sequence': obj.sequence or None,
        'employee_id': obj.employee_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'project_id': obj.project_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'residency_number': obj.residency_number or None,
        'serial_number': obj.serial_number or None,
        'employee_position_id': obj.employee_position_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'old_job_title': obj.old_job_title or None,
        'change_reason': obj.change_reason or None,
        'supportive_document_1': obj.supportive_document_1 or None,
        'supportive_document_2': obj.supportive_document_2 or None,
        'amount': obj.amount,
        'state': dict(get_request_states(obj))[obj.state] or None,
        'expiration_date': obj.expiration_date or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'create_date': obj.create_date,
        'mob_state': get_mob_state(obj) or None,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': obj.change_reason or None,

    }
    if obj.state == 'approved':
        res_job_val.update({'new_job_title': obj.new_job_title or None})

    return res_job_val


def map_salary_transfer(obj):
    salt_val = {
        'id': obj.id,
        'model_name': obj._name,
        'type': _('Salary Transfer Request'),
        'sequence': obj.sequence or None,
        'employee_id': obj.employee_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'project_id': obj.project_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'bank_clearance_letter': obj.bank_clearance_letter or None,
        'international_bank': obj.international_bank or None,
        'bank_name': obj.bank_name or None,
        'iban_number': obj.iban_number or None,
        'state': dict(get_request_states(obj))[obj.state] or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'create_date': obj.create_date,
        'mob_state': get_mob_state(obj) or None,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': _('This Request us Related to a Salary Transfer'),

    }

    if not obj.international_bank:
        salt_val.update({'bank_id': obj.bank_id.mapped(lambda t: {'id': t.id, 'name': t.bank_name}) or None,
                         })
    if obj.international_bank:
        salt_val.update({
            'bank_name': obj.bank_name or None,
            'branch_name': obj.branch_name or None,
            'bank_country_id': obj.bank_country_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        })
    return salt_val


def map_travel_tickets(obj):
    trat_val = {
        'id': obj.id,
        'model_name': obj._name,
        'type': _('Travel Ticket Request'),
        'sequence': obj.sequence or None,
        'employee_id': obj.employee_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'project_id': obj.project_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'purpose': dict(obj._fields['purpose'].selection)[obj.purpose] or None,
        'travel_type': dict(obj._fields['travel_type'].selection)[obj.travel_type] or None,
        'origin': obj.origin or None,
        'destination': obj.destination or None,
        'date_from': obj.date_from or None,
        'date_to': obj.date_to or None,
        'travel_class': dict(obj._fields['travel_class'].selection)[obj.travel_class] or None,
        'other_travelers': obj.other_travelers or None,
        'amount': obj.amount or None,
        'state': dict(get_request_states(obj))[obj.state] or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'create_date': obj.create_date,
        'mob_state': get_mob_state(obj) or None,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': obj.purpose or None,

    }
    if obj.other_travelers:
        trat_val.update({"other_travelers_ids": [{
            'name': x.traveler_name,
            'relation': x.relation
        } for x in obj.other_travelers_ids]})
    return trat_val


def map_visit_visa_attestation(obj):
    return {
        'id': obj.id,
        'model_name': obj._name,
        'type': _('Visit Visa Attestation'),
        'sequence': obj.sequence or None,
        'employee_id': obj.employee_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'project_id': obj.project_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'details': obj.details or None,
        'mofa_template': obj.mofa_template or None,
        'amount': obj.amount,
        'state': dict(get_request_states(obj))[obj.state] or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'create_date': obj.create_date,
        'mob_state': get_mob_state(obj) or None,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': obj.details or None,

    }


def map_salary_identification(obj):
    return {
        'id': obj.id,
        'model_name': obj._name,
        'type': _('Salary Identification'),
        'sequence': obj.sequence or None,
        'employee_id': obj.employee_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'project_id': obj.project_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'identity_name': obj.identity_name or None,
        'unknown': obj.unknown or None,
        'whom_name': obj.whom_name or None,
        'e_stamp': obj.e_stamp or None,
        'state': obj.state or None,
        'can_cancel': False,
        'can_approve': False,
        'create_date': obj.create_date,
        'mob_state': 'approve' or None,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': obj.identity_name or None,

    }


def map_leave_request(obj):
    return {
        'id': obj.id,
        'model_name': obj._name,
        'type': _('Leave Request'),
        'sequence': obj.sequence or None,
        'employee_id': obj.employee_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'project_id': obj.project_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'leave_type_id': obj.leave_type_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'date_from': obj.date_from or None,
        'date_to': obj.date_to or None,
        'number_of_days': obj.number_of_days or None,
        'desc': obj.desc or None,
        'leave_current_balance': obj.leave_current_balance or None,
        'balance_after_leave': obj.balance_after_leave or None,
        'allow_extend': obj.allow_extend or None,
        'supportive_document': obj.supportive_document or None,
        'state': obj.state or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': obj.leave_type_id.name or None,

    }


def map_resignation_request(obj):
    return {
        'id': obj.id,
        'model_name': obj._name,
        'type': _('Resignation Request'),
        'sequence': obj.sequence or None,
        'employee_id': obj.employee_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'project_id': obj.project_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'resignation_reason_id': obj.resignation_reason_id.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
        'reason_desc': obj.reason_desc or None,
        'end_date': obj.end_date or None,
        'state': obj.state or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'mob_state': get_mob_state(obj) or None,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': obj.reason_desc or None,

    }


def map_benefit_request(obj):
    return {
        'id': obj.id,
        'model_name': obj._name,
        'type': _('Benefit Request'),
        'sequence': obj.sequence or None,
        'employee_id': obj.employee_id.mapped(lambda c: {'id': c.id, 'name': c.name}) or None,
        'project_id': obj.project_id.mapped(lambda c: {'id': c.id, 'name': c.name}) or None,
        'benefit_id': obj.benefit_id.mapped(lambda c: {'id': c.id, 'name': c.name}) or None,
        'other': obj.other or None,
        'benefit_name': obj.benefit_name or None,
        'benefit_type': obj.benefit_type or None,
        'desc': obj.desc or None,
        'purpose': obj.purpose or None,
        'state': obj.state or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'mob_state': get_mob_state(obj) or None,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': obj.desc or None,

    }


def map_salary_confirm(obj):
    return {
        'id': obj.id,
        'model_name': obj._name,
        'type': _('Salary Confirmation'),
        'sequence': obj.sequence or None,
        'employee_id': obj.employee_id.mapped(lambda c: {'id': c.id, 'name': c.name}) or None,
        'project_id': obj.project_id.mapped(lambda c: {'id': c.id, 'name': c.name}) or None,

        'desc': obj.desc or None,
        'bank_id': obj.bank_id.mapped(lambda c: {'id': c.id, 'name': c.bank_name}) or None,
        'state': obj.state or None,
        'can_cancel': obj.can_cancel,
        'can_approve': get_po_can_approve(obj),
        'mob_state': get_mob_state(obj) or None,
        'create_by': obj.create_uid.mapped(lambda c: {'id': c.id, 'name': c.name}),
        'description': obj.desc or None,

    }
