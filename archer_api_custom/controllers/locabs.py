import functools
import json

from odoo.addons.archer_api_custom.controllers.common import validate_token
from odoo import http, tools,_
from odoo.http import request, Response


class Locabs(http.Controller):
    @validate_token
    @http.route("/api/locabs/residency_types", methods=["POST"], type="json", auth="none", csrf=False)
    def get_residency_type(self):
        try:
            if request.httprequest.accept_languages:
                lang = request.httprequest.accept_languages
            else:
                lang = 'en_US'

            residency_type_ids = request.env['residency.residency'].with_context(lang=str(lang)).sudo().search(
                []).mapped(
                lambda t: {'id': t.id, 'name': t.name, 'residency_type': t.residency_type}) or None
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(residency_type_ids, indent=4, sort_keys=True, default=str),
            )
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))

    @validate_token
    @http.route("/api/locabs/benefits_types", methods=["POST"], type="json", auth="none", csrf=False)
    def get_benefits_ids_types(self):
        try:

            if request.httprequest.accept_languages:
                lang = request.httprequest.accept_languages
            else:
                lang = 'en_US'

            benefits_ids = request.env['employee.monthly.eos'].with_context(lang=str(lang)).sudo().search([]).mapped(
                lambda t: {'id': t.id, 'name': t.name}) or None
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(benefits_ids, indent=4, sort_keys=True, default=str),
            )
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))

    @validate_token
    @http.route("/api/locabs/get_expense_type", methods=["POST"], type="json", auth="none", csrf=False)
    def get_expense_type(self):
        try:

            if request.httprequest.accept_languages:
                lang = request.httprequest.accept_languages
            else:
                lang = 'en_US'

            expense_types = request.env['expense.request.type'].with_context(lang=str(lang)).sudo().search([]).mapped(
                lambda t: {'id': t.id, 'name': t.name})
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(expense_types, indent=4, sort_keys=True, default=str),
            )
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))

    @validate_token
    @http.route("/api/locabs/get_expense_products", methods=["POST"], type="json", auth="none", csrf=False)
    def get_expense_products(self):
        try:

            if request.httprequest.accept_languages:
                lang = request.httprequest.accept_languages
            else:
                lang = 'en_US'

            products = request.env['product.template'].with_context(lang=str(lang)).sudo().search(
                [('detailed_type', '=', 'service'), ('provide_service', '=', True)]).mapped(
                lambda t: {'id': t.id, 'name': t.name})
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(products, indent=4, sort_keys=True, default=str),
            )
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))

    @validate_token
    @http.route("/api/locabs/get_eos_types", methods=["POST"], type="json", auth="none", csrf=False)
    def get_eos_types(self):
        try:

            if request.httprequest.accept_languages:
                lang = request.httprequest.accept_languages
            else:
                lang = 'en_US'

            types = request.env['eos.type'].with_context(lang=str(lang)).sudo().search([]).mapped(
                lambda t: {'id': t.id, 'name': t.name})
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(types, indent=4, sort_keys=True, default=str),
            )
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))

    @validate_token
    @http.route("/api/locabs/countries", methods=["POST"], type="json", auth="none", csrf=False)
    def get_countries(self):
        try:
            if request.httprequest.accept_languages:
                lang = request.httprequest.accept_languages
            else:
                lang = 'en_US'

            country_ids = request.env['res.country'].with_context(lang=str(lang)).sudo().search([]).mapped(
                lambda t: {'id': t.id, 'name': t.name, 'code': t.code}) or None
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(country_ids, indent=4, sort_keys=True, default=str),
            )
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(ex)

    @validate_token
    @http.route("/api/locabs/cities", methods=["POST"], type="json", auth="none", csrf=False)
    def get_cities(self, **kw):
        try:

            if request.httprequest.accept_languages:
                lang = request.httprequest.accept_languages
            else:
                lang = 'en_US'

            cities_ids = request.env['res.country.state'].with_context(lang=str(lang)).sudo().search(
                [('country_id', '=', kw['country_id'])]).mapped(
                lambda t: {'id': t.id, 'name': t.name, 'code': t.code})
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps(cities_ids, indent=4, sort_keys=True, default=str),
            )
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))

    @validate_token
    @http.route("/api/locabs/gender", methods=["POST"], type="json", auth="none", csrf=False)
    def get_gender(self):
        try:
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps([{"male": "Male", "female": "Female"}], indent=4, sort_keys=True, default=str),
            )
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))

    @validate_token
    @http.route("/api/locabs/religion", methods=["POST"], type="json", auth="none", csrf=False)
    def get_religion(self):
        try:
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps([{"muslim": "Muslim",
                                      "not_muslim": "Not Muslim"}], indent=4, sort_keys=True, default=str),
            )
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))

    @validate_token
    @http.route("/api/locabs/residency_static_type", methods=["POST"], type="json", auth="none", csrf=False)
    def get_residency_static_type(self):
        try:
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps([{
                    "employee": _("Employee"),
                    "family_member": _("Family Member"),
                    "newborn_out": _("Newborn (Born Outside KSA)"),
                    "newborn_in": _("Newborn (Born Inside KSA)"),
                }], indent=4, sort_keys=True, default=str),
            )
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))

    @validate_token
    @http.route("/api/locabs/employee_family_relation", methods=["POST"], type="json", auth="none", csrf=False)
    def get_employee_family_relation(self):
        try:
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps([{
                    "spouse": _("Spouse"),
                    "child": _("Child"),
                    "father": _("Father"),
                    "mother": _("Mothe")
                }], indent=4, sort_keys=True, default=str),
            )
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))

    @validate_token
    @http.route("/api/locabs/get_banks", methods=["POST"], type="json", auth="none", csrf=False)
    def get_banks(self):
        try:

            if request.httprequest.accept_languages:
                lang = request.httprequest.accept_languages
            else:
                lang = 'en_US'

            banks = request.env['bank.bank'].with_context(lang=str(lang)).sudo().search([])
            response = Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
                response=json.dumps([banks.mapped(lambda b: {'id': b.id, 'name': b.bank_name})], indent=4,
                                    sort_keys=True, default=str),
            )
            return json.loads(response.data)
        except Exception as ex:
            raise Exception(_('Invalid Operation'))
