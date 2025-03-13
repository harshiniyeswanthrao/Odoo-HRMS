# __manifest__.py
{
    'name': 'Shift Planner',
    'version': '1.0',
    'category': 'Human Resources',
    'author': 'Your Name',
    'website': 'http://www.yourcompany.com',
    'depends': ['hr', 'base'],
    'data': [
         'security/ir.model.access.csv',
        'views/employee_view.xml',
        'views/shift_view.xml',
        'views/shift_swap_views.xml',
        "views/menu.xml",
         "views/action.xml",
    ],
    'installable': True,
    'application': True,
}
