import json

from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)


class VolunteeringPortal(CustomerPortal):
    @http.route("/my/volunteering", auth="user", website=True)
    def volunteering(self, selected_year='', **kwargs):
        partner = request.env.user.partner_id
        domain = [('partner_id', '=', partner.id)]
        volunteering_times = request.env['volunteering_time'].search(domain, order='date desc')
        if selected_year:
            domain.append(('date', '>=', selected_year + '-01-01'))
            domain.append(('date', '<=', selected_year + '-12-31'))
        volunteering_years = {date.year for date in volunteering_times.mapped('date')}
        volunteering_times = volunteering_times.search(domain, order='date desc')
        years_filter = {
            "0": "All Years",
        }
        for volunteering_year in volunteering_years:
            years_filter[volunteering_year] = volunteering_year
        year_filter_props = {
            "selectedYear": str(selected_year) if selected_year else "",
            "years": years_filter,
            "default" : "0"
        }
        values = {
            "partner": partner,
            "volunteering_times": volunteering_times,
            "year_filter_props": year_filter_props
        }
        return request.render("volunteering_hours.portal_my_volunteering", values)
