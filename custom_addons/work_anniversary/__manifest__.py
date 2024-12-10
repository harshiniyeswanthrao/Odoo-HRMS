{
    'name': 'Work Anniversary',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Displays upcoming work anniversaries for employees',
    'depends': ['hr','base'],
    'data': [
        'security/ir.model.access.csv',
        'views/work_anniversary_view.xml',
    ],
    'installable': True,
    'application': True,
}


