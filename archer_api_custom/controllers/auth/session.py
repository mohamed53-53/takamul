import functools
import json

import odoo
from odoo.addons.archer_api_custom.controllers.common import validate_token
from odoo import http, _
from odoo.exceptions import AccessError, AccessDenied, ValidationError
from odoo.http import request, Response
import re

db = "db_takamul_mob"
# db = "db_takamul"
# db = "db_takamul_stage"


regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


def email_validate(email):
    if re.fullmatch(regex, email):
        return True
    else:
        raise ValidationError(_("Invalid Email"))


def mobile_validate(mobile):
    if mobile.strip()[:2] == '05' and len(mobile.strip()) == 10:
        return True
    else:
        raise ValidationError(_("Invalid Mobile Number"))


def passwd_validate(password):
    if re.fullmatch(r"[A-Za-z0-9_@.!#$%&'*+-/=?^`{|}~]{8,32}", password):
        return True
    else:
        raise ValidationError(_("Invalid Password"))


class Session(http.Controller):
    @http.route("/api/auth/login", type="json", auth="none",csrf=False)
    def api_auth_login(self, login, password, fmc_key):
        email_validate(login)
        try:
            request.env.context = dict(request.env.context)
            request.env.context.update({'from_mobile': True})
            auth = request.session.authenticate(db, login, password)
            uid = request.session.uid

            request.env.user.sudo().write({'fmc_key': fmc_key})
            # odoo login failed:
            if not uid:
                return Response(status=401)

            # Generate tokens
            access_token = request.env["api.access_token"].find_or_create_token(user_id=uid, create=True)
            # Successful response:
            Response.status = str(200)
            response = Response(
                status=str(200),
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(
                    {
                        "uid": uid,
                        "access_token": access_token,
                        "company_id": request.env.user.company_id.id if uid else None,
                        "company_ids": request.env.user.company_ids.ids if uid else None,
                        "company_name": request.env.user.company_name or None,
                        "country": request.env.user.country_id.name or None,
                        "country_code": request.env.user.country_id.code or None,
                        "partner_id": request.env.user.partner_id.id or None,
                        "project_ids": request.env.user.project_ids.mapped(lambda t: {'id': t.id, 'name': t.name}) or None,
                        "employee_id": request.env.user.employee_id.id or None,
                        "international_bank": request.env.user.employee_id.international_bank or None,
                        "is_locked": request.env.user.employee_id.is_locked or None,
                        "name": request.env.user.name or None,
                        'fmc_key': request.env.user.fmc_key or None,
                        'login_status': request.env.user.login_status or None,
                        'web_login': request.env.user.web_login,
                        'user_type': request.env.user.user_type or None,
                    }
                ),
            )
            return json.loads(response.data)
        except Exception as ae:
            Response.status = str(401)
            raise AccessDenied(_('Access Denied'))

    @validate_token
    @http.route('/api/auth/logout', methods=["POST"], type="json", auth="none", csrf=False)
    def api_auth_logout(self):
        try:
            access_token = request.env["api.access_token"].sudo().search(
                [("user_id", "=", request.env.uid), ("token", "=", request.httprequest.headers.get('Access-Token'))], order="id DESC",
                limit=1)
            if access_token:
                access_token.sudo().write({'active': False})
                request.env.cr.commit()
            request.session.logout()
            response = Response(
                status=str(200),
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(True),
            )
            return json.loads(response.data)

        except Exception as ex:
            raise Exception(_('Failed Logout'))

    @http.route("/api/auth/generate_otp", methods=["POST"], type="json", auth="none", csrf=False)
    def api_auth_generate_otp(self, email, mobile):
        email_validate(email)
        mobile_validate(mobile.strip())
        try:
            user = request.env['res.users'].sudo().search([('login', '=', email), ('partner_id.mobile', '=', mobile.strip())], limit=1)

            otp = user.sudo().generate_otp()
            response = Response(
                status=str(200),
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(otp),
            )

            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Field generate OTP'))

    @http.route("/api/auth/verify_otp", methods=["POST"], type="json", auth="none", csrf=False)
    def api_auth_verify_otp(self, email, mobile, otp):
        email_validate(email)
        mobile_validate(mobile.strip())
        try:
            user = request.env['res.users'].sudo().search([('login', '=', email), ('partner_id.mobile', '=', mobile.strip())], limit=1)
            if user:
                result_otp = user.sudo().verify_otp(int(otp))
                response = Response(
                    status=str(200),
                    content_type="application/json; charset=utf-8",
                    headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                    response=json.dumps(result_otp, indent=4, sort_keys=True, default=str),
                )
                return json.loads(response.data)
            else:
                raise ValidationError(_('User not found'))
        except ValidationError as ve:
            raise ValidationError(_('Field verify otp'))

    @validate_token
    @http.route('/api/auth/change_password', methods=["POST"], type="json", auth="none", csrf=False)
    def api_auth_change_password(self, old_passwd, new_passwd):
        passwd_validate(new_passwd)
        try:
            passwd = request.env.user.change_password(old_passwd, new_passwd)
            response = Response(
                status=str(200),
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(passwd),
            )
            return json.loads(response.data)
        except ValidationError as ve:
            raise ValidationError(_('Failed Change Password'))

    @http.route("/api/auth/reset_passwd", methods=["POST"], type="json", auth="none", csrf=False)
    def api_auth_reset_passwd(self, email, mobile, new_passwd, tmp_passwd, fmc_key):
        email_validate(email)
        mobile_validate(mobile.strip())
        passwd_validate(new_passwd)
        try:
            user = request.env['res.users'].sudo().search([('login', '=', email), ('partner_id.mobile', '=', mobile.strip())], limit=1)
            if user.tmp_passwd == tmp_passwd:
                passwd = user.sudo().write({'password': new_passwd,'fmc_key': fmc_key})
                request.env.cr.commit()     # as authenticate will use its own cursor we need to commit the current transaction
                access_token = request.env["api.access_token"].sudo().search([("user_id", "=", user.id)], order="id DESC", limit=1)
                if access_token:
                    access_token.sudo().write({'active': False})
                    access_token = request.env["api.access_token"].sudo().find_or_create_token(user_id=user.id, create=True)
                # Successful response:
                response = Response(
                    status=str(200),
                    content_type="application/json; charset=utf-8",
                    headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                    response=json.dumps(
                        {
                            "uid": user.id,
                            "access_token": access_token,
                            "company_id": user.company_id.id if user else None,
                            "company_ids": user.company_ids.ids if user else None,
                            "company_name": user.company_name or None,
                            "country": user.country_id.name or None,
                            "partner_id": user.partner_id.id or None,
                            "employee_id": user.employee_id.id or None,
                            "name": user.name or None,
                            'fmc_key': user.fmc_key or None,
                            'login_status': user.login_status or None,
                            'web_login': user.web_login,
                            'user_type': user.user_type or None,
                        }
                    ),
                )
                return json.loads(response.data)

            else:
                raise ValidationError(_('Invalid Password'))

        except ValidationError as ve:
            raise ValidationError(_('Invalid Password'))
