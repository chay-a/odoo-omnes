{
   'name': 'Training Hours',
   'version': '18.0.0.0.1',
   'depends': ['base','portal'],
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/training_technique_views.xml",
        "views/training_session_views.xml",
        "views/menu_views.xml",
    ],
}