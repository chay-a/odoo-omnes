from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    nextcloud_initial_training_folder_url = fields.Char(string="Nextcloud initial training folder URL", required=True, config_parameter="training_hours.nextcloud_initial_training_folder_url")