
{
    'name': 'Open HRMS Branch Transfer',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Employee transfer between branches',
    'description': 'This modules allows the user to transfer an employee from '
                   'one branch to another branch',
    'author': ' MY HRMS DASHBOARD',
    'company': 'SAKSHATH TECHNOLOGIES',
    'maintainer': 'HARSHINI G Y ',
    'depends': ['hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'security/hr_employee_security.xml',
        'views/employee_transfer_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
