# -*- coding: utf-8 -*-
{
    'name': "archer_petty_cash",

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
    'depends': ['base','account','project','archer_project_custom','mail','oi_workflow'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/petty_cash_request_workflow.xml',
        'data/payment_request_workflow.xml',
        'data/petty_cash_settlement_workflow.xml',
        'views/account_journal.xml',
        'views/petty_cash_request.xml',
        'views/account_payment.xml',
        'views/petty_cash_settlement.xml',
        'wizards/petty_cash_payment_register.xml',
        'views/menus.xml',

    ],
}
