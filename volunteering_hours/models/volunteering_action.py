from odoo import models, fields


class VolunteeringAction(models.Model):
    _name = "volunteering_action"

    name = fields.Char(required=True, placeholder="Action name")
    sequence = fields.Integer(string='Sequence', default=10)