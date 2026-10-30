import datetime

from odoo import models, fields


class TrainingYear(models.Model):
    _name = "training_year"

    name = fields.Char(required=True)
    sequence = fields.Integer(string='Sequence', default=10)

    def _add_current_year(self):
        if not self.search([('name', '=', datetime.datetime.now().year)]):
            try:
                self.create([{'name': datetime.datetime.now().year}])
            except Exception:
                raise Exception("Error while creating Training Year")