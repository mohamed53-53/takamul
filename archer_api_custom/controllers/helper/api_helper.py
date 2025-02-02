from odoo.addons.archer_api_custom.controllers.common import validate_token
from odoo.addons.archer_api_custom.controllers.helper.objects_map import *
from odoo.addons.archer_api_custom.controllers.utils.utils import jsonfy_response

from odoo import http, _
from odoo.exceptions import ValidationError
from odoo.http import request, Response


class ApiHelper(http.Controller):
    @validate_token
    @http.route("/api/helper/get_all_requests", methods=["POST"], type="json", auth="none", csrf=False)
    def get_all_requests(self, **kw):
        domain = []
        limit = False
        user = request.env['res.users'].sudo().browse(request.session['uid'])
        if user.user_type == 'external_employee':
            domain.extend([('employee_id.user_id', '=', user.id)])
        if user.user_type == 'project_owner':
            if not user.project_ids:
                raise ValidationError(_('User Not Assigned to  Projects'))
            else:
                domain.extend([('project_id', 'in', user.project_ids.ids)])
        if 'limit' in kw:
            limit = int(kw['limit'])
        models_names = [
            'business.trip',
            're.entry.visa',
            'expense.request',
            'lone.advance',
            'residency.issuance',
            'residency.renewal',
            'residency.job.title',
            'salary.transfer',
            'travel.tickets',
            'visit.visa.attestation',
            'leave.request',
            'salary.identification',
            'resignation.request',
            'benefit.request',
            'salary.confirmation'
        ]
        requests_vals = []

        if request.httprequest.accept_languages:
            lang = request.httprequest.accept_languages
        else:
            lang = 'en_US'

        for model in models_names:
            if model == 'business.trip':
                business_trip_list = []

                objs = request.env[model].with_context(lang=str(lang)).sudo().search(domain, limit=limit,
                                                                                     order='create_date desc').with_user(
                    user).sudo()
                for trip in objs:
                    business_trip_list.append(
                        map_generic_object(obj=trip, desc=trip.occasion_or_purpose or _('This Request is Related to a '
                                                                                        'Business Trip')))
                requests_vals += business_trip_list

            if model == 're.entry.visa':
                re_entry_visa_list = []
                objs = request.env[model].with_context(lang=str(lang)).sudo().search(domain, limit=limit,
                                                                                     order='create_date desc').with_user(
                    user).sudo()
                for re_entry_visa in objs:
                    re_entry_visa_list.append(
                        map_generic_object(obj=re_entry_visa,
                                           desc=_('This Request is Related to a Exit & Re-Entry Visa')))
                requests_vals += re_entry_visa_list

            if model == 'expense.request':
                expense_list = []
                objs = request.env[model].with_context(lang=str(lang)).sudo().search(domain, limit=limit,
                                                                                     order='create_date desc').with_user(
                    user).sudo()
                for expense in objs:
                    expense_list.append(map_generic_object(obj=expense,
                                                           desc=expense.description or _(
                                                               'This Request is Related to a Expense '
                                                               'Clim')))
                requests_vals += expense_list

            if model == 'lone.advance':
                loan_list = []
                objs = request.env[model].with_context(lang=str(lang)).sudo().search(domain, limit=limit,
                                                                                     order='create_date desc').with_user(
                    user).sudo()
                for loan in objs:
                    loan_list.append(map_generic_object(obj=loan, desc=_('This Request is Related to a Loan')))
                requests_vals += loan_list

            if model == 'residency.issuance':
                res_isu_list = []
                res_domain = domain + [('request_type', '=', 'residency_issuance')]
                objs = request.env['residency.issuance'].with_context(lang=str(lang)).sudo().search(res_domain,
                                                                                                    limit=limit,
                                                                                                    order='create_date desc').with_user(
                    user).sudo()
                for res_isu in objs:
                    res_isu_list.append(
                        map_generic_object(obj=res_isu, desc=_('This Request is Related to a Residency Issuance')))
                requests_vals += res_isu_list

            if model == 'residency.renewal':
                res_ren_list = []
                ren_domain = domain + [('request_type', '=', 'residency_renewal')]
                objs = request.env['residency.issuance'].with_context(lang=str(lang)).sudo().search(ren_domain,
                                                                                                    limit=limit,
                                                                                                    order='create_date desc').with_user(
                    user).sudo()
                for res_ren in objs:
                    res_ren_list.append(
                        map_generic_object(obj=res_ren, desc=_('This Request is Related to a Residency Renewal')))
                requests_vals += res_ren_list

            if model == 'residency.job.title':
                res_job_list = []
                objs = request.env[model].with_context(lang=str(lang)).sudo().search(domain, limit=limit,
                                                                                     order='create_date desc').with_user(
                    user).sudo()
                for res_job in objs:
                    res_job_list.append(map_generic_object(obj=res_job,
                                                           desc=res_job.change_reason or _(
                                                               'This Request is Related to a Change Residency Job Title')))
                requests_vals += res_job_list

            if model == 'salary.transfer':
                salt_list = []
                objs = request.env[model].with_context(lang=str(lang)).sudo().search(domain, limit=limit,
                                                                                     order='create_date desc').with_user(
                    user).sudo()
                for salt in objs:
                    salt_list.append(
                        map_generic_object(obj=salt, desc=_('This Request is Related to a Salary Transfer')))
                requests_vals += salt_list

            if model == 'travel.tickets':
                trat_list = []
                objs = request.env[model].with_context(lang=str(lang)).sudo().search(domain, limit=limit,
                                                                                     order='create_date desc').with_user(
                    user).sudo()
                for trat in objs:
                    trat_list.append(map_generic_object(obj=trat, desc=dict(trat._fields['purpose'].selection)[
                                                                           trat.purpose] or _(
                        'This Request is Related to a Travel Ticket ')))
                requests_vals += trat_list

            if model == 'visit.visa.attestation':
                vivis_list = []
                objs = request.env[model].with_context(lang=str(lang)).sudo().search(domain, limit=limit,
                                                                                     order='create_date desc').with_user(
                    user).sudo()
                for vivis in objs:
                    vivis_list.append(
                        map_generic_object(obj=vivis,
                                           desc=vivis.details or _(
                                               'This Request is Related to a visit Visa Attestation')))
                requests_vals += vivis_list

            if model == 'leave.request':
                leave_list = []
                objs = request.env[model].with_context(lang=str(lang)).sudo().search(domain, limit=limit,
                                                                                     order='create_date desc').with_user(
                    user).sudo()
                for leave in objs:
                    leave_list.append(
                        map_generic_object(obj=leave,
                                           desc=leave.desc or _('This Request is Related to a visit Visa Attestation')))
                requests_vals += leave_list

            if model == 'salary.identification':
                salary_ids_list = []
                objs = request.env[model].with_context(lang=str(lang)).sudo().search(domain, limit=limit,
                                                                                     order='create_date desc').with_user(
                    user).sudo()
                for salary in objs:
                    salary_ids_list.append(
                        map_generic_object(obj=salary,
                                           desc=salary.identity_name or _(
                                               'This Request is Related to a vSalary Identification')))
                requests_vals += salary_ids_list

            if model == 'resignation.request':
                request_ids_list = []
                objs = request.env[model].with_context(lang=str(lang)).sudo().search(domain, limit=limit,
                                                                                     order='create_date desc').with_user(
                    user).sudo()
                for req in objs:
                    request_ids_list.append(
                        map_generic_object(obj=req,
                                           desc=req.reason_desc or _(
                                               'This Request is Related to a Resignation Request')))
                requests_vals += request_ids_list

            if model == 'benefit.request':
                request_ids_list = []
                objs = request.env[model].with_context(lang=str(lang)).sudo().search(domain, limit=limit,
                                                                                     order='create_date desc').with_user(
                    user).sudo()
                for req in objs:
                    request_ids_list.append(
                        map_generic_object(obj=req,
                                           desc=req.desc or _('This Request is Related to a Benefit Request')))
                requests_vals += request_ids_list

            if model == 'salary.confirmation':
                request_ids_list = []
                objs = request.env[model].with_context(lang=str(lang)).sudo().search(domain, limit=limit,
                                                                                     order='create_date desc').with_user(
                    user).sudo()
                for req in objs:
                    request_ids_list.append(
                        map_generic_object(obj=req,
                                           desc=req.desc or _('This Request is Related to a Salary Confirmation')))
                requests_vals += request_ids_list

        sorted_list = sorted(requests_vals, key=lambda i: i['create_date'], reverse=True)
        return jsonfy_response(sorted_list)

    @validate_token
    @http.route("/api/helper/get_request_by_id", methods=["POST"], type="json", auth="none", csrf=False)
    def get_request_by_id(self, **kw):
        try:
            domain = []
            if not 'model_name' in kw:
                raise ValidationError('model_name is required')
            else:
                model_name = kw['model_name']
            if not 'request_id' in kw:
                raise ValidationError((_('request_id is required')))
            else:
                domain.extend([('id', '=', kw['request_id'])])
            user = request.env['res.users'].sudo().browse(request.session['uid'])
            if user.user_type == 'external_employee':
                domain.extend([('employee_id.user_id', '=', user.id)])

            if user.user_type == 'project_owner':
                if not user.project_ids:
                    raise ValidationError(_('User Not Assigned to  Projects'))
                else:
                    domain.extend([('project_id', 'in', user.project_ids.ids)])

            if request.httprequest.accept_languages:
                lang = request.httprequest.accept_languages
            else:
                lang = 'en_US'

            if model_name == 'business.trip':
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_business_trip(obj))
                else:
                    raise Exception('No Data')

            if model_name == 're.entry.visa':
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_re_entry_visa(obj))
                else:
                    raise Exception('No Data')

            if model_name == 'expense.request':
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_expense_request(obj))

                else:
                    raise Exception('No Data')

            if model_name == 'lone.advance':
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_lone_advance(obj))
                else:
                    raise Exception('No Data')

            if model_name == 'residency.issuance':
                res_domain = domain + [('request_type', '=', 'residency_issuance')]
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(res_domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_residency_issuance(obj))
                else:
                    raise Exception('No Data')

            if model_name == 'residency.renewal':
                model_name = 'residency.issuance'
                ren_domain = domain + [('request_type', '=', 'residency_renewal')]
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(ren_domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_residency_renewal(obj))
                else:
                    raise Exception('No Data')

            if model_name == 'residency.job.title':
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_residency_job_title(obj))
                else:
                    raise Exception('No Data')

            if model_name == 'salary.transfer':
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_salary_transfer(obj))
                else:
                    raise Exception('No Data')

            if model_name == 'travel.tickets':
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_travel_tickets(obj))
                else:
                    raise Exception('No Data')

            if model_name == 'visit.visa.attestation':
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_visit_visa_attestation(obj))
                else:
                    raise Exception('No Data')

            if model_name == 'salary.identification':
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_salary_identification(obj))
                else:
                    raise Exception('No Data')

            if model_name == 'leave.request':
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_leave_request(obj))
                else:
                    raise Exception('No Data')

            if model_name == 'resignation.request':
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_resignation_request(obj))
                else:
                    raise Exception('No Data')

            if model_name == 'benefit.request':
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_benefit_request(obj))
                else:
                    raise Exception('No Data')

            if model_name == 'salary.confirmation':
                obj = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain, limit=1).with_user(
                    user).sudo()
                if obj:
                    return jsonfy_response(map_salary_confirm(obj))
                else:
                    raise Exception(_('No Data'))

        except Exception as ex:
            raise Exception(_('Failed Operation'))

    @validate_token
    @http.route("/api/helper/get_all_requests_by_model", methods=["POST"], type="json", auth="none", csrf=False)
    def get_all_requests_by_model(self, **kw):
        domain = []
        if not 'model_name' in kw:
            raise ValidationError(_('model_name is required'))
        else:
            model_name = kw['model_name']
        user = request.env['res.users'].sudo().browse(request.session['uid'])

        if user.user_type == 'external_employee':
            domain.extend([('employee_id.user_id', '=', user.id)])
        if user.user_type == 'project_owner':
            if not user.project_ids:
                raise ValidationError(_('User Not Assigned to  Projects'))
            else:
                domain.extend([('project_id', 'in', user.project_ids.ids)])
        if request.httprequest.accept_languages:
            lang = request.httprequest.accept_languages
        else:
            lang = 'en_US'

        requests_vals = []
        if model_name == 'business.trip':
            business_trip_list = []
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for trip in objs:
                business_trip_list.append(map_business_trip(trip))
            requests_vals = business_trip_list

        if model_name == 're.entry.visa':
            re_entry_visa_list = []
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for re_entry_visa in objs:
                re_entry_visa_list.append(map_re_entry_visa(re_entry_visa))
            requests_vals = re_entry_visa_list

        if model_name == 'expense.request':
            expense_list = []
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for expense in objs:
                expense_list.append(map_expense_request(expense))
            requests_vals = expense_list

        if model_name == 'lone.advance':
            loan_list = []
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for loan in objs:
                loan_list.append(map_lone_advance(loan))
            requests_vals = loan_list

        if model_name == 'residency.issuance':
            res_isu_list = []
            res_domain = domain + [('request_type', '=', 'residency_issuance')]
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(res_domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for res_isu in objs:
                res_isu_list.append(map_residency_issuance(res_isu))
            requests_vals = res_isu_list

        if model_name == 'residency.renewal':
            model_name = 'residency.issuance'
            res_ren_list = []
            ren_domain = domain + [('request_type', '=', 'residency_renewal')]
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(ren_domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for res_ren in objs:
                res_ren_list.append(map_residency_renewal(res_ren))
            requests_vals = res_ren_list

        if model_name == 'residency.job.title':
            res_job_list = []
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for res_job in objs:
                res_job_list.append(map_residency_job_title(res_job))
            requests_vals = res_job_list

        if model_name == 'salary.transfer':
            salt_list = []
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for salt in objs:
                salt_list.append(map_salary_transfer(salt))
            requests_vals = salt_list

        if model_name == 'travel.tickets':
            trat_list = []
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for trat in objs:
                trat_list.append(map_travel_tickets(trat))
            requests_vals = trat_list

        if model_name == 'visit.visa.attestation':
            vivis_list = []
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for vivis in objs:
                vivis_list.append(map_visit_visa_attestation(vivis))
            requests_vals = vivis_list

        if model_name == 'salary.identification':
            salary_ids_list = []
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for salary in objs:
                salary_ids_list.append(
                    map_salary_identification(salary))
            requests_vals = salary_ids_list

        if model_name == 'leave.request':
            leaves_list = []
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for leave in objs:
                leaves_list.append(
                    map_leave_request(leave))
            requests_vals = leaves_list

        if model_name == 'resignation.request':
            resign_list = []
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for resig in objs:
                resign_list.append(
                    map_resignation_request(resig))
            requests_vals = resign_list
        if model_name == 'benefit.request':
            benefit_list = []
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for bene in objs:
                benefit_list.append(
                    map_benefit_request(bene))
            requests_vals = benefit_list
        if model_name == 'salary.confirmation':
            confirm_list = []
            objs = request.env[model_name].with_context(lang=str(lang)).sudo().search(domain,
                                                                                      order='create_date desc').with_user(
                user).sudo()
            for conf in objs:
                confirm_list.append(
                    map_salary_confirm(conf))
            requests_vals = confirm_list
        return jsonfy_response(requests_vals)

    @validate_token
    @http.route("/api/helper/acton_cancel", methods=["POST"], type="json", auth="none", csrf=False)
    def action_api_cancel(self, **kw):
        try:
            user = request.env['res.users'].sudo().browse(request.session['uid'])
            if not 'request_id' in kw:
                raise ValidationError(_('request_id is required'))
            else:
                if kw['model_name'] == 'residency.renewal':
                    kw['model_name'] = 'residency.issuance'
                model_name = kw['model_name']
                obj = request.env[model_name].sudo().browse(kw['request_id']).with_user(user).sudo()
                if obj:
                    if obj.state == 'submit':
                        obj.sudo().write({'active': False})
                        return jsonfy_response(True)
                    else:
                        raise ValidationError(_('This Request Had Action before from Manager Side'))
        except Exception as ex:
            raise ValidationError(ex)

    @validate_token
    @http.route("/api/helper/acton_approve", methods=["POST"], type="json", auth="none", csrf=False)
    def action_api_approve(self, **kw):
        try:
            user = request.env['res.users'].sudo().browse(request.session['uid'])

            if not 'model_name' in kw:
                raise ValidationError(_('model_name is required'))
            else:
                if kw['model_name'] == 'residency.renewal':
                    kw['model_name'] = 'residency.issuance'
                model_name = kw['model_name']
            if not 'request_id' in kw:
                raise ValidationError('request_id is required')
            if not 'action' in kw:
                raise ValidationError('action is required')
            obj = request.env[model_name].sudo().browse(kw['request_id']).with_user(user).sudo()
            if obj:
                if obj.active:
                    if kw['action'] == 'approve':
                        obj.sudo()._action_approve()
                    elif kw['action'] == 'reject':
                        if not 'reject_reason' in kw:
                            raise ValidationError('Reject Reason Required')
                        else:
                            obj.action_reject(reason=kw['reject_reason'])
                    return jsonfy_response(True)
                else:
                    raise ValidationError(_('This Request Had Action before from Employee Side'))
            else:
                raise ValidationError(_('Field Approve'))
        except Exception as ex:
            raise ValidationError(_("Field Operation"))

    @validate_token
    @http.route("/api/helper/dashboard", methods=["POST"], type="json", auth="none", csrf=False)
    def get_dashboard(self, **kw):
        try:
            domain = []
            user = request.env['res.users'].sudo().browse(request.session['uid'])
            user = request.env['res.users'].sudo().browse(request.session['uid'])
            if user.user_type == 'external_employee':
                domain.extend([('employee_id.user_id', '=', user.id)])
            if user.user_type == 'project_owner':
                if not user.project_ids:
                    raise ValidationError(_('User Not Assigned to  Projects'))
                else:
                    domain.extend([('project_id', 'in', user.project_ids.ids)])
            models_names = [
                'business.trip',
                're.entry.visa',
                'expense.request',
                'lone.advance',
                'residency.issuance',
                'residency.job.title',
                'salary.transfer',
                'travel.tickets',
                'visit.visa.attestation',
            ]
            pendding_total = 0
            rejected_total = 0
            approved_total = 0
            for model in models_names:
                pendding_total += request.env[model].sudo().search_count(
                    domain + [('state', 'not in', ['draft', 'approved'])])
            for model in models_names:
                rejected_total += request.env[model].sudo().search_count(domain + [('state', '=', 'rejected')])
            for model in models_names:
                approved_total += request.env[model].sudo().search_count(domain + [('state', '=', 'approved')])
            return {
                'pending': int(pendding_total),
                'rejected': int(rejected_total),
                'approved': int(approved_total)
            }
        except Exception as ex:
            raise ValidationError(_('Failed Operation'))

    @http.route("/api/helper/action_send_fmc", methods=["POST"], type="json", auth="none", csrf=False)
    def action_send_fmc(self, **kw):
        user = request.env['res.users'].sudo().browse(request.session['uid'])
        model_string = request.env['ir.model'].sudo().search([('model', '=', self._name)]).name
        msg = request.env['archer.fcm.notify'].sudo().send_fcm_notify(client_key=[user.fmc_key],
                                                                      msg_header='%s' % model_string,
                                                                      msg_body=_('[%s]%s:% Create New Request'))
        return jsonfy_response(True)
