# -*- coding: utf-8 -*-

from odoo import api, models
import sys
import os

# Add lib directory to Python path for UISP client import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from uisp_client import UISPClient, UISPConfig


class UispConfigHelper(models.AbstractModel):
    """Helper model for UISP configuration and client creation."""

    _name = 'uisp.config.helper'
    _description = 'UISP Configuration Helper'

    @api.model
    def get_uisp_client(self):
        """
        Create and return configured UISP client.

        Loads configuration from ir.config_parameter:
        - uisp.base_url: UISP server URL (e.g., https://10.93.9.8)
        - uisp.api_key: UISP API authentication key
        - uisp.verify_ssl: SSL certificate verification (true/false)

        Returns:
            UISPClient: Configured UISP API client instance

        Raises:
            UserError: If required configuration parameters are missing
        """
        ICP = self.env['ir.config_parameter'].sudo()

        base_url = ICP.get_param('uisp.base_url', '').strip()
        api_key = ICP.get_param('uisp.api_key', '').strip()
        verify_ssl_str = ICP.get_param('uisp.verify_ssl', 'false').lower()
        verify_ssl = verify_ssl_str == 'true'

        if not base_url:
            from odoo.exceptions import UserError
            raise UserError(
                'UISP base URL not configured. '
                'Please set "uisp.base_url" in System Parameters.'
            )

        if not api_key:
            from odoo.exceptions import UserError
            raise UserError(
                'UISP API key not configured. '
                'Please set "uisp.api_key" in System Parameters.'
            )

        config = UISPConfig(
            base_url=base_url,
            api_key=api_key,
            verify_ssl=verify_ssl,
        )

        return UISPClient(config)

    @api.model
    def test_connection(self):
        """
        Test UISP connection.

        Returns:
            dict: Connection test result with status and message
        """
        try:
            client = self.get_uisp_client()
            sites = client.get_sites()

            return {
                'status': 'success',
                'message': f'Connection successful! Found {len(sites)} sites.',
                'site_count': len(sites),
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
            }
