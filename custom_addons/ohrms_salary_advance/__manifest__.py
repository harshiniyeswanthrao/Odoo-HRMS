
{
    'name': 'Open HRMS Advance Salary',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Advance Salary In Open HRMS.',
    'description': """THis module is a component of Open HRMS suit. It module 
     helps the user to manage salary advance requests from employees. You can 
     configure advance salary rules, set advance salary limit, minimum number 
     of days, and provide advance salary to employees.""",
    'author': ' MY HRMS DASHBOARD',
    'company': 'SAKSHATH TECHNOLOGIES',
    'maintainer': 'HARSHINI G Y ',
    'depends': ['hr_payroll_community', 'hr', 'account',
                'hr_contract', 'ohrms_loan',],
    'data': [
        'security/ir.model.access.csv',
        'security/salary_advance_security.xml',
        'data/ir_sequence_data.xml',
        'data/hr_salary_rule_data.xml',
        'views/salary_advance_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
