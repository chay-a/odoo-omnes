from datetime import datetime

from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request, route

import logging
_logger = logging.getLogger(__name__)


class VolunteeringPortal(CustomerPortal):
    @http.route(["/my/volunteering", "/my/volunteering/page/<int:page>"], auth="user", website=True)
    def volunteering(self, selected_year='', page=0,  **kwargs):
        partner = request.env.user.partner_id
        domain = [('partner_id', '=', partner.id)]
        volunteering_times = request.env['volunteering_time'].search(domain, order='date desc')
        if selected_year:
            domain.append(('date', '>=', selected_year + '-01-01'))
            domain.append(('date', '<=', selected_year + '-12-31'))
        volunteering_years = {date.year for date in volunteering_times.mapped('date')}
        volunteering_times = volunteering_times.search(domain, order='date desc')
        total_hours = self._get_total_hours(volunteering_times.mapped("hours"))
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
        selected_year_query = {}
        if selected_year:
            selected_year_query = {"selected_year": selected_year}
        step = 6
        pager = request.website.pager(
            url='/my/volunteering',
            total=len(volunteering_times),
            page=page,
            step=step,
            url_args=selected_year_query
        )
        offset = pager['offset']
        volunteering_times = volunteering_times[offset:offset + step]
        values = {
            "partner": partner,
            "volunteering_times": volunteering_times,
            "year_filter_props": year_filter_props,
            "total_hours": total_hours,
            "currentYear": datetime.now().year,
            'pager': pager,
        }
        return request.render("volunteering_hours.portal_my_volunteering", values)

    def _get_total_hours(self, volunteering_hours):
        float_hours = sum(volunteering_hours)
        hours, minutes = divmod(float_hours * 60, 60)
        time_str = "{:02d}h{:02d}".format(int(hours), int(minutes))
        return time_str

    @route(["/my/volunteering/delete/<int:id>"], auth="user", website=True, type="json")
    def delete_volunteering_time(self, id=0, **kwargs):
        volunteering_time = request.env['volunteering_time'].browse(id)
        if volunteering_time:
            volunteering_time.sudo().unlink()
        return {
            'redirect_url': "/my/volunteering",
        }
