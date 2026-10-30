{
   'name': 'Training Hours',
   'version': '18.0.0.0.1',
   'depends': ['base','portal'],
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "data/training_year_data.xml",
        "views/training_technique_views.xml",
        "views/training_year_views.xml",
        "views/training_session_views.xml",
        "views/menu_views.xml",
        "views/portal_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "training_hours/static/src/public_components/**/*",
        ],
    },
}