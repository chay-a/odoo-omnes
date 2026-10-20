from odoo import models, fields


class VolunteeringTime(models.Model):
    _name = "volunteering_time"

    date = fields.Date(string="Date", required=True)
    action_id = fields.Many2one("volunteering_action", string="Action", required=True)
    place_id = fields.Many2one("volunteering_place", string="Place", required=True)
