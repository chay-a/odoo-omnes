from odoo import models, fields


class VolunteeringPlace(models.Model):
    _name = "volunteering_place"

    name = fields.Char(required=True)