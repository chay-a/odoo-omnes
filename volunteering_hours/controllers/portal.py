from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class VolunteeringPortal(CustomerPortal):
    @http.route("/my/volunteering", auth="user", website=True)
    def volunteering(self, **kwargs):
        partner = request.env.user.partner_id
        volunteering_times = request.env['volunteering_time'].search([('partner_id', '=', partner.id)])
        values = {
            "partner": partner,
            "volunteering_times": volunteering_times,
        }
        return request.render("volunteering_hours.portal_my_volunteering", values)
