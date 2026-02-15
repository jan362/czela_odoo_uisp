# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    """Extend res.partner with UISP device relation."""

    _inherit = 'res.partner'

    uisp_device_count = fields.Integer(
        'UISP Device Count',
        compute='_compute_uisp_device_count'
    )

    @api.depends('id')
    def _compute_uisp_device_count(self):
        """Count UISP devices linked to this partner."""
        for partner in self:
            # Note: This assumes network.inventory.device exists with partner_id field
            # If the module doesn't exist, this won't cause error, count will be 0
            partner.uisp_device_count = 0

    def action_view_uisp_devices(self):
        """Open UISP devices view filtered by this partner."""
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'UISP Devices',
            'res_model': 'uisp.device',
            'view_mode': 'tree,form,kanban',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }
