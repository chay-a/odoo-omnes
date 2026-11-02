import logging
import requests
from requests.utils import requote_uri

from odoo import models, fields

_logger = logging.getLogger(__name__)

class TrainingSession(models.Model):
    _name = "training_session"

    organisation = fields.Char(string="Organisation", required=True)
    type = fields.Selection(string="Type", selection=[("lifelong_learning", "Lifelong Learning"), ("initial_learning", "Initial Learning")], required=True)
    hours = fields.Float(string="Hours", required=True, help="ex. 2,5 for 2 hours and 30 minutes")
    year_id = fields.Many2one("training_year", string="Year", required=True)
    training_technique_ids = fields.Many2one(
        "training_technique", string="Training techniques", required=True,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    nextcloud_file_url = fields.Char(string="Nextcloud file URL")


    def upload_file(self, file, training_year = False):
        file_name = file.filename
        file_content = file.read()
        if self.type == "initial_learning":
            base_url_field = "training_hours.nextcloud_initial_training_folder_url"
            nextcloud_base_url = self._get_nextcloud_base_url(base_url_field)
        else :
            base_url_field = "training_hours.nextcloud_lifelong_training_folder_url"
            nextcloud_base_url = f"{self._get_nextcloud_base_url(base_url_field)}/{requote_uri(f"{training_year}")}"
        url = self._get_partner_folder_url(nextcloud_base_url, self.partner_id)
        response = requests.put(
            f"{url}/{requote_uri(file_name)}",
            data=file_content,
            headers={"OCS-APIRequest": "true"},
            timeout=10,
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            _logger.error(f"Error creating nextcloud folder {url}: {e}")

    def _get_nextcloud_base_url(self, base_url_field) -> str:
        params = self.env['ir.config_parameter'].sudo()
        nextcloud_initial_training_folder_url = params.get_param(
            base_url_field).replace("https://", "").replace("http://", "")
        nextcloud_admin_username = params.get_param('nextcloud_teams.nextcloud_admin_username')
        nextcloud_admin_password = params.get_param('nextcloud_teams.nextcloud_admin_password')
        return f"https://{nextcloud_admin_username}:{nextcloud_admin_password}@{nextcloud_initial_training_folder_url}"

    def _get_partner_folder_url(self, nextcloud_base_url: str, partner) -> str:
        partner_folder = self._get_partner_folder(partner)
        url = f"{nextcloud_base_url}/{partner_folder}"
        return url

    def _get_partner_folder(self, partner) -> str:
        member_identification = f"{partner.member_identification}-" if partner.member_identification else ''
        partner_lastname = f"{partner.lastname}-" if partner.lastname else ''
        partner_firstname = partner.firstname if partner.firstname else ''
        partner_folder = requote_uri(f"{member_identification}{partner_lastname}{partner_firstname}")
        return partner_folder