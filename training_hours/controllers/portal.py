from odoo import http, _
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.exceptions import ValidationError
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
            'training_techniques': request.env['training_technique'].search([]),
            'training_years': request.env['training_year'].search([]),
            'training_types': [("lifelong_learning", _("Lifelong Learning")), ("initial_learning", _("Initial Learning"))],
            'page': 'my_training_hours'
        }
        return request.render("training_hours.portal_my_training", values)

    def _get_total_hours(self, training_hours):
        float_hours = sum(training_hours)
        hours, minutes = divmod(float_hours * 60, 60)
        time_str = "{:02d}h{:02d}".format(int(hours), int(minutes))
        return time_str

    @http.route(["/my/training/delete/<int:id>"], auth="user", website=True, type="json")
    def delete_training_session(self, id=0, **kwargs):
        training_session = request.env['training_session'].browse(id)
        if training_session:
            training_session.unlink()
        return {
            'redirect_url': "/my/training_hours",
        }

    @http.route("/my/training/new", auth="user", website=True, methods=['POST'])
    def new_training_session(self, **kwargs):
        partner = request.env.user.partner_id.id
        missing_fields = self._required_training_fields() - kwargs.keys()
        _logger.info(f"kwargs: {kwargs}")
        if any(missing_fields):
            raise ValidationError(_("Missing required fields: %s", missing_fields))
        training_technique = request.env['training_technique'].search([('id', '=', kwargs['training_technique_ids'])])
        if not training_technique:
            raise ValidationError(_("Invalid technique id: %s", kwargs['training_technique_ids']))
        training_year = request.env['training_year'].search([('id', '=', kwargs['year_id'])])
        if not training_year:
            raise ValidationError(_("Invalid year id: %s", kwargs['year_id']))
        kwargs['partner_id'] = partner
        file = kwargs.pop('file')
        training_session = request.env['training_session'].sudo().create(kwargs)
        if not training_session:
            raise ValidationError(_("Failed to create training session"))
        training_session.upload_file(file, training_year.name)
        return request.redirect("/my/training_hours")

    def _required_training_fields(self):
        return ['organisation', 'type', 'hours', 'training_technique_ids', 'year_id', 'file']