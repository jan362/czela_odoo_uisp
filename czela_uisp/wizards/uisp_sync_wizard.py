# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class UispSyncWizard(models.TransientModel):
    """Wizard for manual UISP synchronization."""

    _name = 'uisp.sync.wizard'
    _description = 'UISP Synchronization Wizard'

    sync_devices = fields.Boolean('Sync Devices', default=True)
    sync_sites = fields.Boolean('Sync Sites', default=True)
    result_message = fields.Text('Result', readonly=True)
    state = fields.Selection([
        ('draft', 'Ready'),
        ('done', 'Completed'),
    ], default='draft')

    def action_sync(self):
        """Execute synchronization."""
        self.ensure_one()

        messages = []

        try:
            # Test connection first
            test_result = self.env['uisp.config.helper'].test_connection()
            if test_result['status'] != 'success':
                raise UserError(f"UISP connection failed: {test_result['message']}")

            messages.append(f"✓ Connection test: {test_result['message']}\n")

            # Sync devices
            if self.sync_devices:
                result = self.env['uisp.sync'].sync_devices()
                messages.append(f"✓ Devices synced: {result['synced_count']} devices\n")

            # Sync sites
            if self.sync_sites:
                result = self.env['uisp.sync'].sync_sites()
                messages.append(f"✓ Sites synced: {result['synced_count']} sites\n")

            self.write({
                'result_message': ''.join(messages),
                'state': 'done',
            })

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'uisp.sync.wizard',
                'view_mode': 'form',
                'res_id': self.id,
                'target': 'new',
            }

        except Exception as e:
            raise UserError(f'Synchronization failed: {str(e)}')

    def action_close(self):
        """Close wizard."""
        return {'type': 'ir.actions.act_window_close'}

    def action_view_devices(self):
        """Open devices view."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'UISP Devices',
            'res_model': 'uisp.device',
            'view_mode': 'tree,kanban,form',
            'target': 'current',
        }
