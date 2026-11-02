from odoo import models, fields
import logging
import urllib.parse
import requests

from odoo.http import Response
from odoo.models import BaseModel

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    nextcloud_folder_link = fields.Char(string="Nextcloud Folder Link")


    def _add_nextcloud_folder(self):
        partners = self.env["res.partner"].search([("membership_state", "=", "paid")])

        nextcloud_base_url = self._get_nextcloud_base_url()
        for partner in partners:
            url = self._get_partner_folder_url(nextcloud_base_url, partner)
            self._create_folder(partner, url)

    def _create_folder(self, partner: BaseModel, url: str):
        response = requests.request(
            "PROPFIND",
            url,
            headers={"OCS-APIRequest": "true"},
            timeout=10,
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                self._create_folder_call(partner, url)
            else:
                _logger.error(f"Error getting nextcloud folder {url}: {e}")

    def _get_partner_folder_url(self, nextcloud_base_url: str, partner: BaseModel) -> str:
        if partner.nextcloud_folder_link:
            return partner.nextcloud_folder_link
        member_identification = f"{partner.member_identification}-" if partner.member_identification else ''
        partner_lastname = f"{partner.lastname}-" if partner.lastname else ''
        partner_firstname = partner.firstname if partner.firstname else ''
        partner_folder = urllib.parse.quote_plus(f"{member_identification}{partner_lastname}{partner_firstname}")
        url = f"{nextcloud_base_url}/{partner_folder}"
        return url

    def _get_nextcloud_base_url(self) -> str:
        params = self.env['ir.config_parameter'].sudo()
        nextcloud_initial_training_folder_url = params.get_param(
            'training_hours.nextcloud_initial_training_folder_url').replace("https://", "").replace("http://", "")
        nextcloud_admin_username = params.get_param('nextcloud_teams.nextcloud_admin_username')
        nextcloud_admin_password = params.get_param('nextcloud_teams.nextcloud_admin_password')
        return f"https://{nextcloud_admin_username}:{nextcloud_admin_password}@{nextcloud_initial_training_folder_url}"

    def _create_folder_call(self, partner: BaseModel, url: str):
        response = requests.request(
            "MKCOL",
            url,
            headers={"OCS-APIRequest": "true"},
            timeout=10,
        )
        try:
            response.raise_for_status()
            partner.write({'nextcloud_folder_link': url})
        except requests.exceptions.HTTPError as e:
            _logger.error(f"Error creating nextcloud folder {url}: {e}")
