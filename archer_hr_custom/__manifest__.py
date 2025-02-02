{
    'name': 'Archer HR Customisation',
    'version': '15.0.0',
    'summary': 'HR Improvements',
    'description': '',
    'category': 'hr',
    'author': "Archer Solutions",
    'website': "http://archer.solutions",
    'license': 'OPL-1',
    'depends': ['base','hr','hr_holidays','hr_payroll','hr_contract','saudi_hr_eos','archer_base_hr','archer_project_custom'],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_documents.xml',
        'views/hr_plan.xml',
        'views/hr_employee_views.xml',
        'views/hr_payroll.xml',
        'views/hr_leave.xml',
        'views/project_views.xml',
        'views/hr_document.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False
}
