# -*- coding: utf-8 -*-
{
    'name': "archer_portal",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'portal', 'website', 'archer_recruitment', 'sign','archer_base_hr'],

    # always loaded
    'data': [
        'views/templates.xml',
        'views/job_offer.xml',
        'views/customer/customer_hire_request.xml',
        'views/employee_app_new.xml',
        'views/thanks.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'archer_portal/static/webclient/navbar/navbar.scss',
        ],
        'web.assets_frontend': [
            # 'archer_portal/static/css/bootstrap.min.css',

            'archer_portal/static/css/jquery-ui.min.css',

            'archer_portal/static/css/datatables.css',
            'archer_portal/static/css/bootstrap-datepicker.css',
            'archer_portal/static/css/smart_wizard.css',
            'archer_portal/static/css/smart_wizard_all.css',
            'archer_portal/static/css/bootstrap-datetimepicker.min.css',
            'archer_portal/static/css/employee_app_new.css',
            'archer_portal/static/js/datatables.js',
            'archer_portal/static/js/bootstrap-datepicker.js',
            'archer_portal/static/js/dexie.min.js',
            'archer_portal/static/js/dexie-export-import.js',
            'archer_portal/static/js/jquery.smartWizard.js',
            'archer_portal/static/js/bootstrap-filestyle.js',
            'archer_portal/static/js/db_util.js',
            'archer_portal/static/js/moment-hijri.js',
            'archer_portal/static/js/employee_app_new.js',
            # 'archer_portal/static/js/scripts.js',
        ],

    },

}
