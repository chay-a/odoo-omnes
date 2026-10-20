from odoo import models, fields


class VolunteeringTime(models.Model):
    _name = "volunteering_time"

    date = fields.Date(string="Date", required=True)
