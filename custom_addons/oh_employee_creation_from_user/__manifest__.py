
{
    'name': 'Open HRMS Employees From User',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Automatically creates employee while creating user',
    'description': "This module facilitates the automatic creation of "
                   "employee records when users are being created.",
    'author': ' MY HRMS DASHBOARD',
    'company': 'SAKSHATH TECHNOLOGIES',
    'maintainer': 'HARSHINI G Y ',
    'depends': ['hr'],
    'data': [
        'views/res_users_views.xml'
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
