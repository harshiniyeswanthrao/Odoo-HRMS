
{
    'name': 'Work Anniversary Reminder',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': """Send work anniversary emails to employees.""",
    'description': """This Module helps to automatically send work anniversary
    emails to employees based on their joining date in the contract form.""",
    'author': ' MY HRMS DASHBOARD',
    'company': 'SAKSHATH TECHNOLOGIES',
    'maintainer': 'HARSHINI G Y ',
    'depends': ['mail', 'hr_contract'],
    'data': [
        'data/ir_cron_data.xml',
        'data/mail_template_data.xml',
        'views/hr_employee_views.xml'
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
