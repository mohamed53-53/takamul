# -*- coding: utf-8 -*-
# Part of odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "End Of Service",
    'summary': """
        End Of Service""",
    'description': """
        It calculate End of Services.
EOS will be divide in two ways
1. Termination
2. Resignation

EOS required joined date and leaving date of employee.
EOS calculated depends on Last Salary.
For EOS Calculation (as per provided Excel sheet)
EOS amount
+ Current Salary (days depends on leave date)
+ total annual Leave balance amount
+ other (for any addition)
- other (for any deduction)

    """,

    'author': 'Synconics Technologies Pvt. Ltd.',
    'website': 'http://www.synconics.com',
    'category': 'Human Resources',
    'version': '1.0',
    'license': 'OPL-1',
    'depends': [
        'hr',
        'hr_contract',
        'hr_payroll_account',
        'contract_work_hour',
        'hr_holidays',
        'hr_payroll',
        'oi_workflow',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'data/hr_eos_data.xml',
        'data/employee_eos_workflow.xml',
        'data/payroll_batch_workflow.xml',
        'views/other_benefits.xml',
        'views/hr_employee_eos_view.xml',
        'views/hr_employee_termination_view.xml',
        'menu.xml',
        'views/categ.xml',
        'views/res_config_settings.xml',
        'views/monthly_eos.xml',
        'views/hr_leave.xml',
        'views/eos_type.xml',
        'register_qweb_report_eos.xml',
        'report/emp_experience_letter_maleqweb.xml',
        'report/emp_experience_letter_femaleqweb.xml',
    ],
    'demo': [
        'demo/demo.xml'
    ],
    'installable': True,
    'auto_install': False,
}

