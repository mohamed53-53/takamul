# -*- coding: utf-8 -*-
# Copyright 2018 Openinside co. W.L.L.
{
    "name": "Client Action Refresh",
    "summary": "Refresh, Reload, Auto Refresh, Auto Reload, Client",
    "version": "15.0.1.1.3",
    'category': 'Extra Tools',
    "website": "https://www.open-inside.com",
	"description": """
		Client Action Refresh 
		 
    """,
	'images':[
        'static/description/cover.png'
	],
    "author": "Openinside",
    "license": "OPL-1",
    "price" : 9,
    "currency": 'USD',
    "installable": True,
    "depends": [
        'web'
    ],
    "data": [
        
    ],    
    'installable': True,
    'auto_install': True,    
    'odoo-apps' : True,
    'images':[
        'static/description/cover.png'
    ],       
    'assets': {
        'web.assets_backend': [
            'oi_action_trigger_reload/static/src/js/trigger_reload.js',
            'oi_action_trigger_reload/static/src/js/action_menu.js',
        ],
        'web.assets_qweb': [
            'oi_action_trigger_reload/static/src/xml/templates.xml'
        ],
    },         
}

