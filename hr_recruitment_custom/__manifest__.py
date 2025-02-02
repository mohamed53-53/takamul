# -*- coding: utf-8 -*-

{
    'name': "Hr Recruitment Customization",

    'summary': """
        Hr Recruitment Customization
        """,
    'description': """
        Hr Recruitment Customization        
    """,

    'author': "Archer Solutions",
    'website': "http://archer.solutions",
    'category': 'hr',
    'version': '13.0.0',
    # any module necessary for this one to work correctly
    'depends': [
        'base','hr','hr_recruitment','hr_recruitment_survey','hr_contract','hr_payroll','tax_calculation'
    ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hr_applicant.xml',
        'views/salary_breakdown.xml',
        'views/hr_contract.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
