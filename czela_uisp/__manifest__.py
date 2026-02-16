# -*- coding: utf-8 -*-
{
    'name': 'CZELA UISP Integration',
    'version': '18.0.1.0.0',
    'category': 'Operations/Inventory',
    'summary': 'Integration with UISP (Ubiquiti Network Management System) for ISP operations',
    'description': """
UISP Integration Module
=======================

This module integrates Odoo with UISP (Ubiquiti ISP management platform) to:

* Synchronize network devices from UISP
* Display device status, metrics (CPU, RAM, signal strength)
* Manage sites (network locations) hierarchy
* Link UISP devices to customers via network inventory
* Generate ČTÚ ART252 compliance reports
* Provide map view with GPS device locations

Key Features:
-------------
* Automatic periodic sync (devices every 15 min, sites hourly)
* Manual sync wizard for on-demand updates
* MAC address-based device matching
* Technology classification (FTTH/WiFi/FWA) for regulatory reporting
* Real-time device metrics and status monitoring

Configuration:
--------------
Set UISP connection parameters in Settings > Technical > Parameters > System Parameters:
* uisp.base_url - UISP server URL (e.g., https://10.93.9.8)
* uisp.api_key - UISP API authentication key
* uisp.verify_ssl - SSL certificate verification (true/false)
    """,
    'author': 'CZELA',
    'website': 'https://is-dev.czela.net',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'contacts',
    ],
    'external_dependencies': {
        'python': ['requests', 'urllib3'],
    },
    'data': [
        # Security
        'security/uisp_security.xml',
        'security/ir.model.access.csv',

        # Data
        'data/ir_config_parameter.xml',
        'data/uisp_cron.xml',

        # Views
        'views/uisp_device_views.xml',
        'views/uisp_site_views.xml',
        'views/partner_views.xml',

        # Wizards
        'wizards/uisp_sync_wizard_views.xml',
        'wizards/ctu_export_wizard_views.xml',

        # Menu (last - depends on actions)
        'views/uisp_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
