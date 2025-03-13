
{
    'name': 'OpenHRMS Employee Info',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': """Adding Advanced Fields In Employee Master""",
    'description': 'This module helps you to add more information '
                   'in employee records.',
    'author': ' MY HRMS DASHBOARD',
    'company': 'SAKSHATH TECHNOLOGIES',
    'maintainer': 'HARSHINI G Y ',
    'depends': ['hr', 'mail', 'hr_gamification', 'hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_employee_relation_data.xml',
        'data/ir_cron_data.xml',
        'views/hr_contract_views.xml',
        'views/res_config_settings_views.xml',
        'views/hr_employee_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
