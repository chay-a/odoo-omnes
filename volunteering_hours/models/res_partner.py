from odoo import models, fields
from odoo.api import depends


class ResPartner(models.Model):
    _inherit = "res.partner"

    volunteering_time_ids = fields.One2many("volunteering_time", "partner_id")
    total_volunteering_hours = fields.Float(compute="_compute_total_volunteering_hours")

    @depends("volunteering_time_ids.hours")
    def _compute_total_volunteering_hours(self):
        for record in self:
            for hours in record.volunteering_time_ids.mapped("hours"):
                record.total_volunteering_hours = record.total_volunteering_hours + hours