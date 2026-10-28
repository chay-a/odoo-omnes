from odoo import http
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.http import request


class TrainingPortal(CustomerPortal):
    @http.route(['/my/training_hours'], website=True, auth="user")
    def my_training_hours(self, **kwargs):
        return request.render("training_hours.portal_my_training")