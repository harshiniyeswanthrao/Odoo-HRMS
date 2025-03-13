
{
    'name': 'Open HRMS Leave Request Aliasing',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': """Automated Leave Request generation from Incoming Emails.""",
    'description': """This module simplifies leave request creation by 
     seamlessly generating requests from incoming emails, making the process 
     efficient, saving time, and enhancing employee experience.""",
    'author': ' MY HRMS DASHBOARD',
    'company': 'SAKSHATH TECHNOLOGIES',
    'maintainer': 'HARSHINI G Y ',
    'depends': ['hr_holidays'],
    'data': [
        'data/mail_alias_data.xml',
        'views/res_config_settings_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
