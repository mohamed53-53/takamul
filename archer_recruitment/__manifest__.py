# -*- coding: utf-8 -*-
{
    'name': "archer_recruitment",

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
    'depends': ['base','hr','archer_dynamic_allowance','social_insurance','archer_base_hr','hr_recruitment_survey','hr_recruitment','archer_project_custom','mail','archer_hr_custom'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/offer_template.xml',
        'data/app_template.xml',
        'views/application.xml',
        'views/customer_application.xml',
        'views/hr_applicant.xml',
        'views/hr_contract_wait.xml',
        'views/res_config_settings.xml',
        'views/menu.xml',
    ],

}
