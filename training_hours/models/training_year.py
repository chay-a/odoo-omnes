from odoo import models, fields


class TrainingYear(models.Model):
    _name = "training_year"

    name = fields.Char(required=True)
    sequence = fields.Integer(string='Sequence', default=10)