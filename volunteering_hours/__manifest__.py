{
   'name': 'Volunteering Hours',
   'version': '18.0.0.0.1',
   'depends': ['base','portal'],
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/volunteering_time_views.xml",
        "views/volunteering_action_views.xml",
        "views/volunteering_place_views.xml",
        "views/menu_views.xml"
    ]
}