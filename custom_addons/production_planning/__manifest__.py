{
    'name': 'Product Process Matrix(PPM)',
    'version': '1.0',
    'summary': 'Custom module for Production Planning',
    'description': 'This module helps with the planning of production processes by selecting machine, parts, and production cell.',
    'category': 'Manufacturing',
    'depends':[
        'mail', 'web',
    ],
    'assets': {
                'web.assets_backend': [
                    'production_planning/static/src/css/custom_styles.css',
                    'production_planning/static/src/js/graph.js',
                    'production_planning/static/src/xml/graph_temp.xml',
                    'https://cdn.jsdelivr.net/npm/chart.js',
                ],
            },
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/production_planning_views.xml',
        'views/plantmain_views.xml',
        'views/plantline_main_views.xml',
        'views/machine_part_views.xml',
        'views/actions.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
