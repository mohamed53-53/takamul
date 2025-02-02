{
    "name": "Certification of Completion",
    "summary": "Certification of Completion, Certificate of Completion, COC, Completion Certificate, Service Delivery Certificate",    
    'category': 'Accounting',
    "description": """
        Manage Certification of Completion
         
    """,
    
    "author": "Openinside",
    "license": "OPL-1",
    'website': "https://www.open-inside.com",
    "version": "15.0.0.0.1",
    "price" : 60,
    "currency": 'USD',
    "installable": True,
    "depends": [
        'account',
        'purchase',
        'hr',
        'oi_workflow',
        'oi_purchase_requisition_request'
    ],
    "data": [
        'security/res_groups.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',        
        'views/account_analytic_account.xml',
        'views/purchase_order.xml',
        'views/account_coc.xml',
        'views/action.xml',
        'views/menu.xml',
        'data/ir_sequence.xml',
        'report/templates.xml',
        'report/action.xml'
    ],
    'images': [
        'static/description/cover.png'
    ],

    'odoo-apps' : True      
}

