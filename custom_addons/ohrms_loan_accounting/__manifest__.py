
{
    'name': 'Open HRMS Loan Accounting',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Open HRMS Loan Accounting',
    'description': """Create accounting entries for loan requests.""",
    'author': ' MY HRMS DASHBOARD',
    'company': 'SAKSHATH TECHNOLOGIES',
    'maintainer': 'HARSHINI G Y ',
    'depends': [
        'hr_payroll_community', 'hr', 'account', 'ohrms_loan',
    ],
    'data': [
        'security/ohrms_loan_accounting_security.xml',
        'views/res_config_settings_views.xml',
        'views/hr_loan_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
