# -*- coding: utf-8 -*-

{
    'name': 'Employee Project Transfer',
    'summary': """Employee Project Transfer""",
    'description': """Employee Project Transfer""",
    'category': 'Generic Modules/Human Resources',
    'depends': [
        'base',
        'hr',
        'project'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
        'views/employee_project_transfer.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
