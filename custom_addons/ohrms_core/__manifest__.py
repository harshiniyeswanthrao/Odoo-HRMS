
{
    'name': 'Open HRMS Core Odoo 18',
    'version': '18.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'summary': """Open HRMS Odoo18, HRMS odoo18, Odoo HR, HR Dashboard, 
     Odoo18 Payroll, HR Management, Odoo Branch, Odoo Loan, Salary Advance, 
     Odoo18,Payroll,Dashboard,Accounting,HR Kit,HR,Odoo Apps""",
    'description': """Openhrms, Main module of Open HRMS,Payroll, Payroll 
     Accounting, Expense, Dashboard,Employees, Employee Document, Resignation, 
     Salary Advance, Loan Management, Gratuity, Service Request, Gosi, 
     WPS Report, Reminder, Multi Company, Shift Management, Employee History, 
     Branch Transfer, Employee Appraisal,Biometric Device, Announcements, 
     Insurance Management, Vacation Management,Employee Appreciations, 
     Asset Custody, Employee Checklist, Entry and Exit Checklist, Disciplinary 
     Actions, openhrms, Open HRMS, hrms, Attrition Rate, Document Expiry, 
     Visa Expiry, Law Suit Management, Employee, Employee Training, payroll, 
     odoo18 payroll""",
    'author': ' MY HRMS DASHBOARD',
    'company': 'SAKSHATH TECHNOLOGIES',
    'maintainer': 'HARSHINI G Y ',
    'depends': [
        'hr',
        'hr_payroll_account_community',
        'hr_gamification',
        'hr_employee_updation',
        'hr_recruitment',
        'hr_attendance',
        'hr_holidays',
        'hr_payroll_community',
        'hr_expense',
        'hr_leave_request_aliasing',
        'hr_timesheet',
        'oh_employee_creation_from_user',
        'oh_employee_documents_expiry',
        'hr_multi_company',
        'ohrms_loan_accounting',
        'ohrms_salary_advance',
        'hr_reward_warning',
        'hrms_dashboard',
        'hr_reminder'
    ],
    'data': [
        'views/menu_arrangement_view.xml',
        'views/hr_config_view.xml',
        'views/ir_ui_menu_views.xml',
        'views/hr_employee_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'ohrms_core/static/src/css/menu_order_alphabets.css',
            'web/static/lib/jquery/jquery.js',
            'ohrms_core/static/src/js/appMenu.js',
            'ohrms_core/static/src/xml/link_view.xml',
            'ohrms_core/static/templates/side_bar.xml'
        ],
    },
    "external_dependencies": {"python": ["pandas"]},
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
