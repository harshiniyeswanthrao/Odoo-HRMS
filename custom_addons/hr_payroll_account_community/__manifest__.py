
{
    'name': 'Odoo18 Payroll Accounting',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': """Odoo 17 HR Payroll, payroll, Odoo17 Payroll, Odoo Payroll, 
     Payroll, Odoo17 Payslips, Employee Payroll, HR Payroll,Odoo17, Odoo17 HR, 
     odoo hr,odoo17, Accounting,Odoo Apps""",
    'description': """ This module helps you to manage payroll and 
     accounting.""",
    'author': ' MY HRMS DASHBOARD',
    'company': 'SAKSHATH TECHNOLOGIES',
    'maintainer': 'HARSHINI G Y ',
    'depends': ['hr_payroll_community', 'account'],
    'data': ['views/hr_contract_views.xml',
             'views/hr_payslip_run_views.xml',
             'views/hr_payslip_views.xml',
             'views/hr_salary_rule_views.xml', ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
