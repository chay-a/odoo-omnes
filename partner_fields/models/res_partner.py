from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    naturopath_school = fields.Char(
        string="Naturopath School"
    )

    naturopath_qualification = fields.Char(
        string="Naturopath qualification"
    )