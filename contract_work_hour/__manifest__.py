
{
    'name': 'Contract Day & Hour Value',
    'summary': 'Contract Day & Hour Value',
    'author': 'Archer Solutions',
    'company': 'Archer Solutions',
    'website': "http://www.archersolutions.com",
    'version': '13.0.0.1.0',
    'category': '',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'hr_contract',
        'hr_payroll',
    ],
    'data': [
        'views/hr_contract.xml',
        # 'views/res_config_settings.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

