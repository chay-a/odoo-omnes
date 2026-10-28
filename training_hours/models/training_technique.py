from odoo import models, fields


class TrainingTechnique(models.Model):
    _name = "training_technique"

    name = fields.Char(required=True)
    sequence = fields.Integer(string='Sequence', default=10)