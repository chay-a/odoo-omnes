from odoo import http, _
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class TrainingPortal(CustomerPortal):
    @http.route(['/my/training_hours', '/my/training_hours/page/<int:page>'], website=True, auth="user")
    def my_training_hours(self, selected_year="", page=0, **kwargs):
        domain = [('partner_id', '=', request.env.user.partner_id.id)]
        training_sessions = request.env['training_session'].search(domain)
        years = request.env['training_year'].search([('id', 'in', training_sessions.mapped('year_id').ids)], order='sequence asc')
        if selected_year:
            domain.append(('year_id.id', '=', selected_year))
        training_sessions = training_sessions.search(domain)
        total_hours = self._get_total_hours(training_sessions.mapped('hours'))
        step = 12
        pager = request.website.pager(
            url='/my/training_hours',
            total=len(training_sessions),
            page=page,
            step=step
        )
        offset = pager['offset']
        training_sessions = training_sessions[offset:offset + step]
        years_filter = {
            "0": _("All Years"),
        }
        years_filter.update(dict(zip(years.ids, years.mapped('name'))))
        year_filter_props= {
            "selectedYear": str(selected_year) if selected_year else "",
            "years": years_filter,
            "default" : "0"
        }
        values = {
            'training_sessions': training_sessions,
            'total_hours': total_hours,
            'pager': pager,
            'year_filter_props': year_filter_props,
            'page': 'my_training_hours'
        }
        return request.render("training_hours.portal_my_training", values)

    def _get_total_hours(self, training_hours):
        float_hours = sum(training_hours)
        hours, minutes = divmod(float_hours * 60, 60)
        time_str = "{:02d}h{:02d}".format(int(hours), int(minutes))
        return time_str