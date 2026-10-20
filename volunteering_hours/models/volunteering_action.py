from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VolunteeringAction(models.Model):
    _name = "volunteering_action"
    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char(required=True, placeholder="Action name")
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name', recursive=True,
        store=True)
    sequence = fields.Integer(string='Sequence', default=10)
    parent_id = fields.Many2one('volunteering_action', 'Parent Action', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_id = fields.One2many('volunteering_action', 'parent_id', 'Child Actions')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for action in self:
            if action.parent_id:
                action.complete_name = '%s / %s' % (action.parent_id.complete_name, action.name)
            else:
                action.complete_name = action.name

    @api.constrains('parent_id')
    def _check_action_recursion(self):
        if self._has_cycle():
            raise ValidationError(_('You cannot create recursive actions.'))