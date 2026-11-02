from odoo import models, fields
import logging
import requests
from requests.utils import requote_uri

from odoo.models import BaseModel

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    nextcloud_folder_link = fields.Char(string="Nextcloud Folder Link")


    def _add_nextcloud_folder(self):
        partners = self.env["res.partner"].search([("membership_state", "=", "paid")])

        nextcloud_base_url = self._get_nextcloud_base_url('training_hours.nextcloud_initial_training_folder_url')
        for partner in partners:
            if partner.nextcloud_folder_link:
                nextcloud_base_url = partner.nextcloud_folder_link
            url = self._get_partner_folder_url(nextcloud_base_url, partner)
            created = self._create_folder(url)
            if created and not partner.nextcloud_folder_link:
                partner.write({'nextcloud_folder_link': url})

    def _add_nextcloud_folder_for_lifelong_training(self):
        partners = self.env["res.partner"].search([("membership_state", "=", "paid")])
        training_years = self.env["training_year"].search([])
        nextcloud_base_url = self._get_nextcloud_base_url('training_hours.nextcloud_lifelong_training_folder_url')
        for partner in partners:
            for training_year in training_years:
                training_year_url = requote_uri(f"{training_year.name}")
                nextcloud_base_url_with_year = f"{nextcloud_base_url}/{training_year_url}"
                self._create_folder(nextcloud_base_url_with_year)
                url = self._get_partner_folder_url(nextcloud_base_url_with_year, partner)
                self._create_folder(url)

    def _create_folder(self, url: str):
        response = requests.request(
            "PROPFIND",
            url,
            headers={"OCS-APIRequest": "true"},
            timeout=10,
        )
        try:
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                self._create_folder_call(url)
            else:
                _logger.error(f"Error getting nextcloud folder {url}: {e}")

    def _get_partner_folder_url(self, nextcloud_base_url: str, partner: BaseModel) -> str:
        partner_folder = self._get_partner_folder(partner)
        url = f"{nextcloud_base_url}/{partner_folder}"
        return url

    def _get_partner_folder(self, partner: BaseModel) -> str:
        member_identification = f"{partner.member_identification}-" if partner.member_identification else ''
        partner_lastname = f"{partner.lastname}-" if partner.lastname else ''
        partner_firstname = partner.firstname if partner.firstname else ''
        partner_folder = requote_uri(f"{member_identification}{partner_lastname}{partner_firstname}")
        return partner_folder

    def _get_nextcloud_base_url(self, base_url_field) -> str:
        params = self.env['ir.config_parameter'].sudo()
        nextcloud_initial_training_folder_url = params.get_param(
            base_url_field).replace("https://", "").replace("http://", "")
        nextcloud_admin_username = params.get_param('nextcloud_teams.nextcloud_admin_username')
        nextcloud_admin_password = params.get_param('nextcloud_teams.nextcloud_admin_password')
        return f"https://{nextcloud_admin_username}:{nextcloud_admin_password}@{nextcloud_initial_training_folder_url}"

    def _create_folder_call(self, url: str):
        response = requests.request(
            "MKCOL",
            url,
            headers={"OCS-APIRequest": "true"},
            timeout=10,
        )
        try:
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            _logger.error(f"Error creating nextcloud folder {url}: {e}")
