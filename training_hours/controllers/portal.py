from odoo import http
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class TrainingPortal(CustomerPortal):
    @http.route(['/my/training_hours', '/my/training_hours/page/<int:page>'], website=True, auth="user")
    def my_training_hours(self, page=0, **kwargs):
        training_sessions = request.env['training_session'].search([('partner_id', '=', request.env.user.partner_id.id)])
        total_hours = self._get_total_hours(training_sessions.mapped('hours'))
        step = 3
        pager = request.website.pager(
            url='/my/training_hours',
            total=len(training_sessions),
            page=page,
            step=step
        )
        offset = pager['offset']
        training_sessions = training_sessions[offset:offset + step]
        values = {
            'training_sessions': training_sessions,
            'total_hours': total_hours,
            'pager': pager,
            'page': 'my_training_hours'
        }
        return request.render("training_hours.portal_my_training", values)

    def _get_total_hours(self, training_hours):
        float_hours = sum(training_hours)
        hours, minutes = divmod(float_hours * 60, 60)
        time_str = "{:02d}h{:02d}".format(int(hours), int(minutes))
        return time_str