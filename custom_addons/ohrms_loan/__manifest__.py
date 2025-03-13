
{
    'name': 'Open HRMS Loan Management',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Manage Employee Loan Requests',
    'description': """This module facilitates the creation and management of 
     employee loan requests. The loan amount is automatically deducted from the 
     salary""",
    'author': ' MY HRMS DASHBOARD',
    'company': 'SAKSHATH TECHNOLOGIES',
    'maintainer': 'HARSHINI G Y ',
    'depends': ['hr', 'account', 'hr_payroll_community'],
    'data': [
        'security/hr_loan_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/hr_loan_views.xml',
        'views/hr_payslip_views.xml',
        'views/hr_employee_views.xml',
    ],
    'demo': ['data/hr_salary_rule_demo.xml',
             'data/hr_rule_input_demo.xml', ],
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
