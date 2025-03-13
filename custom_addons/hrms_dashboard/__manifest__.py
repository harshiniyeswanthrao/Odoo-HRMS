
{
    'name': "Open HRMS HR Dashboard",
    'version': '18.0.1.0.0',
    'summary': """Open HRMS - HR Dashboard""",
    'description': """Open HRMS - HR Dashboard""",
    'category': 'Generic Modules/Human Resources',
    'author': ' MY HRMS DASHBOARD',
    'company': 'SAKSHATH TECHNOLOGIES',
    'maintainer': 'HARSHINI G Y ',
    'depends': ['hr', 'hr_holidays', 'hr_timesheet', 'hr_payroll_community',
                'hr_attendance', 'hr_timesheet_attendance',
                'hr_recruitment', 'hr_resignation', 'event',
                'hr_reward_warning','hr_expense'],
    'external_dependencies': {
        'python': ['pandas'],
    },
    'data': [
        'security/ir.model.access.csv',
        'report/broadfactor.xml',
        'views/hr_leave_views.xml',
        'views/hrms_dashboard_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hrms_dashboard/static/src/css/dashboard.css',
            'hrms_dashboard/static/src/js/dashboard.js',
            'hrms_dashboard/static/src/xml/dashboard.xml',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js',
        ],
    },
    'images': ["static/description/banner.jpg"],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
