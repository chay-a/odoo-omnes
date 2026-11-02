from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    nextcloud_initial_training_folder_path = fields.Char(string="Nextcloud initial training folder path", required=True, config_parameter="training_hours.nextcloud_initial_training_folder_path")
    nextcloud_lifelong_training_folder_path = fields.Char(string="Nextcloud initial lifelong folder path", required=True, config_parameter="training_hours.nextcloud_lifelong_training_folder_path")