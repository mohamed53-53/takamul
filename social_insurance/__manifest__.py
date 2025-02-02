# -*- coding: utf-8 -*-
{
    'name': 'Social Insurence',
    'version': '15.0.1.0.0',
    'category': 'Hr',
    'author': "Archer Solutions",
    'website': "www.archersolutions.com",
    'summary': 'this app manage social insurence of employees',
    'sequence': 1,
    'depends': [
        'base', 'hr','hr_payroll', 'hr_contract','archer_hr_custom','archer_project_custom', 'contract_work_hour', 'archer_base_hr', 'saudi_hr_eos'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/social_insurence.xml',
        'views/hr_contract.xml',
        'views/hr_employee.xml',
        'views/res_config_setting.xml',
        'views/view_gosi_hire.xml',
        'views/gosi_eos.xml',
        'wizard/insurance_wizard.xml',
        'wizard/report.xml',
        'views/payslip.xml',
        'views/menu.xml',

    ],
    'installable': True,
}
