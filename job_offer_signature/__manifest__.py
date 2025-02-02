# -*- coding: utf-8 -*-
{
    'name': "job Offer Signature",

    'summary': """
        job_offer_signature
        """,
    'description': """
        job_offer_signature       
    """,

    'author': "Archer Solutions",
    'website': "http://archer.solutions",
    'category': 'hr',
    'version': '13.0.0',
    # any module necessary for this one to work correctly
    'depends': [
        'base','sign','hr_recruitment','hr_contract_sign',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/job_offer_mail.xml',
        'views/hr_applicant.xml',
        'views/sign_request_templates.xml',
        'wizard/hr_applicant_sign_document_wizard_view.xml',
    ],

    'assets': {
        'web.assets_common': [
            'job_offer_signature/static/src/js/sign_common.js'
        ]
    }
}
