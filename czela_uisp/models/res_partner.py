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
        UispDevice = self.env['uisp.device']
        for partner in self:
            partner.uisp_device_count = UispDevice.search_count([
                ('partner_id', '=', partner.id)
            ])

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
