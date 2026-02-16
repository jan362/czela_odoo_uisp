# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class UispSync(models.TransientModel):
    """UISP Synchronization Service."""

    _name = 'uisp.sync'
    _description = 'UISP Synchronization Service'

    @api.model
    def sync_devices(self):
        """Synchronize devices from UISP to Odoo."""
        _logger.info('Starting UISP device sync...')

        try:
            client = self.env['uisp.config.helper'].get_uisp_client()
            devices_data = client.get_devices()

            UispDevice = self.env['uisp.device']
            UispSite = self.env['uisp.site']
            synced_ids = []

            for device in devices_data:
                ident = device.get('identification', {})
                overview = device.get('overview', {})
                location = device.get('location', {})
                site_data = ident.get('site', {})

                # Get or create site first
                site_id = None
                if site_data and site_data.get('id'):
                    site = UispSite.search([('uisp_id', '=', site_data['id'])], limit=1)
                    if not site:
                        site = UispSite.create({
                            'uisp_id': site_data['id'],
                            'name': site_data.get('name', 'Unknown Site'),
                        })
                    site_id = site.id

                vals = {
                    'uisp_id': ident.get('id'),
                    'name': ident.get('displayName') or ident.get('name'),
                    'hostname': ident.get('hostname'),
                    'mac_address': ident.get('mac'),
                    'model': ident.get('model'),
                    'model_name': ident.get('modelName'),
                    'platform': ident.get('platformId'),
                    'category': ident.get('category'),
                    'serial_number': ident.get('serialNumber'),
                    'status': UispSync._map_status(overview.get('status')),
                    'authorized': ident.get('authorized', False),
                    'cpu_percent': overview.get('cpu'),
                    'ram_percent': overview.get('ram'),
                    'signal_dbm': overview.get('signal'),
                    'uptime': overview.get('uptime'),
                    'temperature': overview.get('temperature'),
                    'last_seen': overview.get('lastSeen'),
                    'latitude': location.get('latitude'),
                    'longitude': location.get('longitude'),
                    'ip_address': ident.get('ipAddress'),
                    'firmware': ident.get('firmwareVersion'),
                    'site_id': site_id,
                    'sync_date': fields.Datetime.now(),
                }

                existing = UispDevice.search([('uisp_id', '=', vals['uisp_id'])], limit=1)
                if existing:
                    existing.write(vals)
                    synced_ids.append(existing.id)
                else:
                    new_device = UispDevice.create(vals)
                    synced_ids.append(new_device.id)

            _logger.info('UISP device sync completed. Synced %d devices.', len(synced_ids))

            return {
                'synced_count': len(synced_ids),
                'device_ids': synced_ids
            }

        except Exception as e:
            _logger.error('UISP device sync failed: %s', str(e))
            raise UserError(f'UISP sync failed: {str(e)}')

    @api.model
    def sync_sites(self):
        """Synchronize sites from UISP."""
        _logger.info('Starting UISP site sync...')

        try:
            client = self.env['uisp.config.helper'].get_uisp_client()
            sites_data = client.get_sites()

            UispSite = self.env['uisp.site']
            synced_count = 0

            for site in sites_data:
                ident = site.get('identification', {})
                desc = site.get('description', {})

                vals = {
                    'uisp_id': ident.get('id'),
                    'name': ident.get('name'),
                    'latitude': desc.get('location', {}).get('latitude'),
                    'longitude': desc.get('location', {}).get('longitude'),
                    'sync_date': fields.Datetime.now(),
                }

                existing = UispSite.search([('uisp_id', '=', vals['uisp_id'])], limit=1)
                if existing:
                    existing.write(vals)
                else:
                    UispSite.create(vals)

                synced_count += 1

            _logger.info('UISP site sync completed. Synced %d sites.', synced_count)

            return {'synced_count': synced_count}

        except Exception as e:
            _logger.error('UISP site sync failed: %s', str(e))
            raise UserError(f'UISP site sync failed: {str(e)}')

    @staticmethod
    def _map_status(uisp_status):
        """Map UISP status to Odoo selection."""
        status_map = {
            'active': 'active',
            'inactive': 'inactive',
            'disabled': 'disabled',
        }
        return status_map.get(uisp_status, 'unknown')
