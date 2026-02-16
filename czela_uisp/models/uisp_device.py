# -*- coding: utf-8 -*-

from odoo import api, fields, models


class UispDevice(models.Model):
    """UISP Network Device - cache of devices from UISP."""

    _name = 'uisp.device'
    _description = 'UISP Network Device'
    _order = 'name'

    # Identification (from UISP API)
    uisp_id = fields.Char('UISP ID', required=True, index=True, readonly=True)
    name = fields.Char('Device Name', index=True)
    hostname = fields.Char('Hostname')
    mac_address = fields.Char('MAC Address', index=True)
    serial_number = fields.Char('Serial Number')

    # Model and type
    model = fields.Char('Model')  # e.g., "LiteBeam 5AC Gen2"
    model_name = fields.Char('Model Name')
    platform = fields.Char('Platform')  # e.g., "UBNT"
    category = fields.Char('Category')  # e.g., "Wireless Access Point"

    # ČTÚ classification (computed from model)
    ctu_type = fields.Selection([
        ('s2_ftth', 'FTTH (optika)'),
        ('s2_wifi', 'WiFi (volné pásmo)'),
        ('s2_fwa', 'FWA (licencované)')
    ], string='ČTÚ Technologie', compute='_compute_ctu_type', store=True)

    # Status and metrics
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('disabled', 'Disabled'),
        ('unknown', 'Unknown')
    ], default='unknown')
    authorized = fields.Boolean('Authorized')

    # Performance metrics (from overview)
    uptime = fields.Integer('Uptime (seconds)')
    cpu_percent = fields.Float('CPU %', digits=(5, 2))
    ram_percent = fields.Float('RAM %', digits=(5, 2))
    signal_dbm = fields.Float('Signal (dBm)', digits=(5, 2))
    temperature = fields.Float('Temperature (°C)')
    last_seen = fields.Datetime('Last Seen')

    # Location
    site_id = fields.Many2one('uisp.site', 'Site', index=True, ondelete='set null')
    latitude = fields.Float('Latitude', digits=(10, 7))
    longitude = fields.Float('Longitude', digits=(10, 7))

    # Network
    ip_address = fields.Char('IP Address')
    firmware = fields.Char('Firmware Version')

    # Link to network inventory device
    network_device_id = fields.Many2one(
        'network.inventory.device',
        'Network Device',
        compute='_compute_network_device',
        store=True,
        index=True
    )

    # Link to partner (via network device or direct)
    partner_id = fields.Many2one(
        'res.partner',
        'Customer',
        compute='_compute_partner_id',
        store=True,
        index=True
    )

    # Metadata
    sync_date = fields.Datetime('Last Synced', default=lambda self: fields.Datetime.now(), readonly=True)

    @api.depends('model', 'category')
    def _compute_ctu_type(self):
        """Determine ČTÚ type based on device model (ported from server.py:108-167)."""
        for device in self:
            device.ctu_type = self._get_ctu_type_for_model(device.model, device.category)

    def _get_ctu_type_for_model(self, model, category=None):
        """
        Determine CTU technology type based on device model and category.

        Returns:
            s2_ftth - optická přípojka (FTTH/GPON)
            s2_wifi - bezdrátový přístup ve volných pásmech (2.4/5/60 GHz)
            s2_fwa - bezdrátový přístup v licencovaných pásmech
            None - nelze určit nebo není relevantní (switch, router apod.)
        """
        if not model:
            return None

        model_lower = model.lower()

        # Switche, routery - nelze přiřadit typ ČTÚ (check first)
        network_devices = ['switch', 'router', 'edgerouter']
        for nd in network_devices:
            if nd in model_lower:
                return None

        # FWA - licencovaná pásma (10/11/17/24 GHz apod.) - check BEFORE wifi
        # airFiber devices use licensed spectrum
        if 'airfiber' in model_lower or 'af24' in model_lower or 'af5x' in model_lower:
            return 's2_fwa'
        if 'powerbridge m10' in model_lower:
            return 's2_fwa'
        if 'ltu rocket' in model_lower or 'ltu' in model_lower:
            return 's2_fwa'

        # FTTH/GPON - optická zařízení (UISP Fiber, OLT, ONU)
        ftth_keywords = ['fiber', 'olt', 'onu', 'gpon']
        for kw in ftth_keywords:
            if kw in model_lower:
                return 's2_ftth'

        # WiFi - bezdrátová zařízení ve volných pásmech (2.4/5/60 GHz)
        # Většina Ubiquiti zařízení pracuje v 5GHz volném pásmu
        wifi_models = [
            # 5GHz WiFi (volné pásmo)
            'liteap', 'litebeam', 'nanobeam', 'nanostation', 'powerbeam',
            'prismstation', 'rocket', 'wave ap', 'wave nano', 'wave pico',
            'wave pro', 'wave mlo',
            # 60GHz (volné pásmo)
            '60ad', 'lhgg-60',
            # 2.4GHz
            '2ac', 'm2',
        ]
        for wm in wifi_models:
            if wm in model_lower:
                return 's2_wifi'

        # Fallback based on category if available
        if category:
            cat_lower = category.lower()
            if 'optical' in cat_lower:
                return 's2_ftth'
            if 'wireless' in cat_lower:
                return 's2_wifi'

        return None

    @api.depends('network_device_id.partner_id')
    def _compute_partner_id(self):
        """Get partner from linked network device."""
        for device in self:
            if device.network_device_id and hasattr(device.network_device_id, 'partner_id'):
                device.partner_id = device.network_device_id.partner_id
            else:
                device.partner_id = False

    def _compute_network_device(self):
        """Match UISP device to network.inventory.device by MAC."""
        # Safety: Check if network.inventory module is installed
        if 'network.inventory.device' not in self.env:
            for device in self:
                device.network_device_id = False
            return

        NetworkDevice = self.env['network.inventory.device']
        for device in self:
            if device.mac_address:
                mac_norm = device.mac_address.upper().replace(':', '').replace('-', '')
                net_dev = NetworkDevice.search([
                    ('mac_address', 'ilike', mac_norm)
                ], limit=1)
                device.network_device_id = net_dev
            else:
                device.network_device_id = False

    def action_refresh_from_uisp(self):
        """Refresh device data from UISP (single device)."""
        self.ensure_one()

        client = self.env['uisp.config.helper'].get_uisp_client()
        device_data = client.get_device(self.uisp_id)

        if device_data:
            ident = device_data.get('identification', {})
            overview = device_data.get('overview', {})
            location = device_data.get('location', {})

            self.write({
                'name': ident.get('displayName') or ident.get('name'),
                'hostname': ident.get('hostname'),
                'mac_address': ident.get('mac'),
                'model': ident.get('model'),
                'category': ident.get('category'),
                'status': self._map_status(overview.get('status')),
                'cpu_percent': overview.get('cpu'),
                'ram_percent': overview.get('ram'),
                'signal_dbm': overview.get('signal'),
                'uptime': overview.get('uptime'),
                'last_seen': overview.get('lastSeen'),
                'latitude': location.get('latitude'),
                'longitude': location.get('longitude'),
                'ip_address': ident.get('ipAddress'),
                'firmware': ident.get('firmwareVersion'),
                'sync_date': fields.Datetime.now(),
            })

        return True

    def _map_status(self, uisp_status):
        """Map UISP status to Odoo selection."""
        status_map = {
            'active': 'active',
            'inactive': 'inactive',
            'disabled': 'disabled',
        }
        return status_map.get(uisp_status, 'unknown')
