
{
    'name': 'Open HRMS Employee Documents Expiry',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': """Manages Employee Documents With Expiry Notifications.""",
    'description': """OH Addon: Manages Employee Related Documents with Expiry
     Notifications. As such dates approach, the system is programmed to send
     automated alerts to relevant employees.These timely notifications are
     essential for ensuring that necessary actions can be taken to update 
     or renew documents before they lapse, thereby avoiding potential legal,
     regulatory, or operational complications that may arise from expired 
     documentation.""",
    'author': ' MY HRMS DASHBOARD',
    'company': 'SAKSHATH TECHNOLOGIES',
    'maintainer': 'HARSHINI G Y ',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/document_type_views.xml',
        'views/hr_document_views.xml',
        'views/hr_employee_document_views.xml',
    ],
    'demo': [
        'data/document_type_demo.xml',
        'data/hr_work_location_demo.xml',
        'data/hr_employee_demo.xml',
        'data/hr_employee_document_demo.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
