# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

{
    'name': 'TDS or Withholding Tax Advanced CV',
    'version': '15.0.0.5',
    'category': 'Accounting & Finance',
    'sequence': 1,
    'summary': 'Advanced Tax Deducted at Source(TDS) or Withholding Tax.',
    'description': """
Manage Tax Deducted at Source(TDS) or Withholding Tax
===========================================================

This application allows you to apply TDS or withholding tax at the time of invoice or payment.
     * We can add multiple Tds on payments and invoices.
     * Tds Option in Register payments.
     * Journal Item filtered by Tds

    """,
    'website': 'http://www.technaureus.com/',
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'depends': ['account'],
    'price': 80,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'data': [
        'security/ir.model.access.csv',
        'views/account_view.xml',
        'views/res_partner_view.xml',
        'views/account_payment_view.xml',
        'views/account_invoice_view.xml',
        'report/report_invoice.xml',
    ],
    'demo': [],
    'css': [],
    'images': ['images/tds_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
