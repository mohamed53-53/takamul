# -*- coding: utf-8 -*-
{
    'name': "archer_vendor_coc",

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
    'depends': ['base','oi_certification_of_completion','archer_project_custom'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/account_coc_workflow.xml',
        'views/account_coc_view.xml',
        'views/account_coc_utils_view.xml',
        'wizards/vendor_coc_payment_register.xml'
    ],
}
