import logging
import requests
import xml.etree.ElementTree as ET
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
    share_file_source = fields.Char(string="Share file source")


    def upload_file(self, file, training_year = False):
        file_name = file.filename
        file_content = file.read()
        if self.type == "initial_learning":
            base_url_field = "training_hours.nextcloud_initial_training_folder_path"
            nextcloud_base_url = self._get_nextcloud_base_file_upload_url(base_url_field)
            file_path = f"/{self.env['ir.config_parameter'].sudo().get_param(base_url_field)}/{self._get_partner_folder_url("",self.partner_id)}"
        else :
            base_url_field = "training_hours.nextcloud_lifelong_training_folder_path"
            nextcloud_base_url = f"{self._get_nextcloud_base_file_upload_url(base_url_field)}/{requote_uri(f"{training_year}")}"
            file_path = f"/{self.env['ir.config_parameter'].sudo().get_param(base_url_field)}/{requote_uri(f"{training_year}")}{self._get_partner_folder_url("",self.partner_id)}"
        url = self._get_partner_folder_url(nextcloud_base_url, self.partner_id)
        response = requests.put(
            f"{url}/{requote_uri(file_name)}",
            data=file_content,
            headers={"OCS-APIRequest": "true"},
            timeout=10,
        )
        try:
            response.raise_for_status()
            file_path = f"{file_path}/{requote_uri(file_name)}"
            self._share_file(file_path, self.partner_id.user_ids.oauth_uid, share_type="0", share_permissions="1")
            self._share_file(file_path, 'admin', share_type="1", share_permissions="31")
            self.write({'nextcloud_file_url': f"{url}/{requote_uri(file_name)}"})
        except requests.exceptions.HTTPError as e:
            _logger.error(f"Error creating nextcloud file {url}: {e}")

    def _get_nextcloud_base_file_upload_url(self, base_url_field) -> str:
        nextcloud_initial_training_folder_url = requote_uri(self.env['ir.config_parameter'].sudo().get_param(
            base_url_field))
        nextcloud_base_url = self._get_nextcloud_base_url()
        return f"{nextcloud_base_url}/remote.php/dav/files/{self.env['ir.config_parameter'].sudo().get_param("nextcloud_teams.nextcloud_admin_username")}/{nextcloud_initial_training_folder_url}"

    def _get_nextcloud_base_url(self) -> str:
        params = self.env['ir.config_parameter'].sudo()
        nextcloud_url = params.get_param('nextcloud_teams.nextcloud_url').replace("https://", "").replace("http://", "")
        nextcloud_admin_username = params.get_param('nextcloud_teams.nextcloud_admin_username')
        nextcloud_admin_password = params.get_param('nextcloud_teams.nextcloud_admin_password')
        nextcloud_base_url = f"https://{nextcloud_admin_username}:{nextcloud_admin_password}@{nextcloud_url}"
        return nextcloud_base_url

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

    def _share_file(self, file_path: str, share_with: str, share_type: str ="0", share_permissions = "1"):
        nextcloud_base_url = self._get_nextcloud_base_url()
        url = f"{nextcloud_base_url}/ocs/v2.php/apps/files_sharing/api/v1/shares"
        
        response = requests.post(
            url,
            data=dict(
                path=file_path,
                shareType=share_type,
                shareWith=share_with,
                permissions=share_permissions,
            ),
            headers={"OCS-APIRequest": "true"},
            timeout=10,
        )
        try:
            response.raise_for_status()
            _logger.info(f"Nextcloud share created: {response.text}")
            response_text = ET.fromstring(response.text)
            data = response_text.find("data")
            self.share_file_source = data.find('file_source').text
        except requests.exceptions.HTTPError as e:
            _logger.error(f"Error creating nextcloud share {url} / {file_path}: {e}")

    def get_share_url(self):
        return f"{self.env['ir.config_parameter'].sudo().get_param('nextcloud_teams.nextcloud_url')}/f/{self.share_file_source}"

    def delete_file(self):
        response = requests.delete(
            self.nextcloud_file_url,
            headers={"OCS-APIRequest": "true"},
            timeout=10,
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            _logger.error(f"Error deleting nextcloud file {self.nextcloud_file_url}: {e}")