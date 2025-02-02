# -*- coding: utf-8 -*-
{
    'name': "Archer Project Custom",
    'version': '15.0.0.0.1',
    'summary': "",
    'description': "",
    'category': 'project',
    'author': "Archer Solutions",
    'website': "http://archer.solutions",
    'license': 'OPL-1',
    'depends': ['base', 'utm', 'account', 'account_accountant', 'analytic', 'project', 'oi_workflow', 'archer_base_hr'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "security/project_security.xml",
        "data/sequence.xml",
        "data/logistic_request_workflow.xml",
        "data/headhunting_request_workflow.xml",
        "data/employee_project_close_template.xml",
        "data/project_close_template.xml",
        "data/cron.xml",
        "wizards/generate_coc_wizard.xml",
        "views/headhunting_views.xml",
        "views/logistic_views.xml",
        "views/project_cost_views.xml",
        "views/project_request_views.xml",
        "views/view_project_change_request.xml",
        "views/product_views.xml",
        "views/view_res_partner.xml",
        "views/employee.xml",
        "views/hr_contract.xml",
        "views/view_res_users.xml",
        "views/view_coc_template.xml",
        "views/view_project.xml",
        "views/view_coc.xml",
        "views/account_tax_view.xml",
        "views/analytic_account.xml",
        "views/account_service.xml",
        "views/account_expense_revision.xml",
        "views/res_config_settings.xml",
        "reports/forecaste_report.xml",
        "views/menu.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'archer_project_custom/static/src/css/style.css',
            'archer_project_custom/static/src/js/action_manager.js',
        ]
    }
}
