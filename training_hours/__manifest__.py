{
   'name': 'Training Hours',
   'version': '18.0.0.0.1',
   'depends': ['base','portal', 'membership'],
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "data/training_year_data.xml",
        "data/nextcloud_folder.xml",
        "views/training_technique_views.xml",
        "views/training_year_views.xml",
        "views/training_session_views.xml",
        "views/menu_views.xml",
        "views/res_config_settings_views.xml",
        "views/portal_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "training_hours/static/src/public_components/**/*",
        ],
    },
    "icon": "/training_hours/static/description/icon.png",
}