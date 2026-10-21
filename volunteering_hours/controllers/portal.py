from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)


class VolunteeringPortal(CustomerPortal):
    @http.route("/my/volunteering", auth="user", website=True)
    def volunteering(self, year='' ,**kwargs):
        partner = request.env.user.partner_id
        domain = [('partner_id', '=', partner.id)]
        volunteering_times = request.env['volunteering_time'].search(domain, order='date desc')
        if year:
            domain.append(('date', '>=', year + '-01-01'))
            domain.append(('date', '<=', year + '-12-31'))
        years = {date.year for date in volunteering_times.mapped('date')}
        volunteering_times = volunteering_times.search(domain, order='date desc')
        values = {
            "partner": partner,
            "volunteering_times": volunteering_times,
            "years": years,
            "year": year
        }
        return request.render("volunteering_hours.portal_my_volunteering", values)
