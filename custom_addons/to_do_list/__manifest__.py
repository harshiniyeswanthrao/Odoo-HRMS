{
    "name": "To-Do App",
    "version": "1.0",
    "depends": ["base", "web"],
    "author": "Your Name",
    "category": "Productivity",
    "description": "A simple to-do app built with OWL framework.",
    "data": [
        "security/ir.model.access.csv",
        "views/to_do_task_views.xml",
        # "views/assets.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/to_do_app/static/src/js/to_do_app.js",
        ],
    },
    "installable": True,
    "application": True,
}
