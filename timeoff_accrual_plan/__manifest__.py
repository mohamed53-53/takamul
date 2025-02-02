# -*- coding: utf-8 -*-
{
    'name': 'TimeOff Accrual Plan',
    'version': '15.0.1.0.0',
    'category': 'Hr',
    'author': "Archer Solutions",
    'website': "www.archersolutions.com",
    'summary': 'Timeoff Accrual Plan',
    'sequence': 1,
    'depends': [
        'base', 'hr_holidays', 'archer_project_custom',
    ],
    'data': [
        'views/accrual_view.xml',
        'views/res_config.xml',
    ],
    'installable': True,
}
