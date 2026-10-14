from odoo.addons.website_membership_extension.controllers.portal import CustomerPortalExtension


class CustomerPortalExtension(CustomerPortalExtension):
    def _get_mandatory_fields(self):
        mandatory_fields = super()._get_mandatory_fields()
        mandatory_fields.append('naturopath_school')
        mandatory_fields.append('naturopath_qualification')
        return mandatory_fields
