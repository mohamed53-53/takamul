# -*- coding: utf-8 -*-
# Copyright 2018 Openinside co. W.L.L.
{
    "name": "Purchase Requisition for Employee",
    "summary": "Purchase Requisition for Employee, Purchase Request by User, Purchase Request by Employee, Purchase Request Submission For users/employees",
    "version": "15.0.0.0.0",
    'category': 'Purchases',
    "website": "https://www.open-inside.com",
	"description": """
		purchase.requisition changes:
		added fields: Requester(requester_id)
		modified fields: Responsible (Added domain on the field to show Purchase Manager users only)
		
		 
    """,
	'images':[
        'static/description/cover.png'
	],
    "author": "Openinside",
    "license": "OPL-1",
    "price" : 29.99,
    "currency": 'USD',
    "installable": True,
    "depends": [
        'purchase_requisition','hr'
    ],
    "data": [
        'security/group.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'views/purchase_requisition.xml',
        'views/menu.xml',
    ],
    'odoo-apps' : True 
}

