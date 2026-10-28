from odoo import models, fields


class TrainingSession(models.Model):
    _name = "training_session"

    organisation = fields.Char(string="Organisation", required=True)
    type = fields.Selection(string="Type", selection=[("lifelong_learning", "Lifelong Learning"), ("initial_learning", "Initial Learning")], required=True)
    hours = fields.Float(string="Hours", required=True, help="ex. 2,5 for 2 hours and 30 minutes")
    year = fields.Char(string="Year", required=True)
    training_technique_ids = fields.Many2one(
        "training_technique", string="Training techniques", required=True,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)