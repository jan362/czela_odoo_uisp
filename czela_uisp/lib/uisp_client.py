# -*- coding: utf-8 -*-
"""
UISP API Client for NMS (Network Management System).

This module provides a client for interacting with the UISP API v2.1.
API Documentation: {UISP_BASE_URL}/nms/api-docs/

Authentication: Uses x-auth-token header with API key.
Adapted for Odoo - credentials loaded from ir.config_parameter.
"""

from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


@dataclass
class UISPConfig:
    """Configuration for UISP API client."""

    base_url: str
    api_key: str
    verify_ssl: bool = False  # Self-signed cert
    timeout: int = 30


class UISPClient:
    """
    Client for UISP NMS API v2.1.

    Usage in Odoo:
        config = UISPConfig(
            base_url=env['ir.config_parameter'].get_param('uisp.base_url'),
            api_key=env['ir.config_parameter'].get_param('uisp.api_key'),
            verify_ssl=env['ir.config_parameter'].get_param('uisp.verify_ssl') == 'true',
        )
        client = UISPClient(config)

        # Get all sites
        sites = client.get_sites()

        # Get all devices
        devices = client.get_devices()

        # Get specific device
        device = client.get_device("device-uuid-here")
    """

    API_VERSION = "v2.1"

    def __init__(self, config: UISPConfig):
        self.config = config
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create configured requests session with retries."""
        session = requests.Session()

        # Set auth header
        session.headers.update({
            "x-auth-token": self.config.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

        # Configure retries for transient errors
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        return session

    def _url(self, endpoint: str) -> str:
        """Build full URL for API endpoint."""
        base = f"{self.config.base_url}/nms/api/{self.API_VERSION}/"
        return urljoin(base, endpoint.lstrip("/"))

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        json: dict = None,
    ) -> Any:
        """Make HTTP request to API."""
        url = self._url(endpoint)

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            verify=self.config.verify_ssl,
            timeout=self.config.timeout,
        )

        response.raise_for_status()

        if response.content:
            return response.json()
        return None

    def get(self, endpoint: str, params: dict = None) -> Any:
        """GET request."""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: dict = None) -> Any:
        """POST request."""
        return self._request("POST", endpoint, json=json)

    def put(self, endpoint: str, json: dict = None) -> Any:
        """PUT request."""
        return self._request("PUT", endpoint, json=json)

    def patch(self, endpoint: str, json: dict = None) -> Any:
        """PATCH request."""
        return self._request("PATCH", endpoint, json=json)

    def delete(self, endpoint: str) -> Any:
        """DELETE request."""
        return self._request("DELETE", endpoint)

    # ==================== Sites ====================

    def get_sites(self) -> list:
        """
        Get all sites.

        Returns:
            List of site objects with identification, description, endpoints.
        """
        return self.get("sites") or []

    def get_site(self, site_id: str) -> dict:
        """Get specific site by ID."""
        return self.get(f"sites/{site_id}")

    # ==================== Devices ====================

    def get_devices(self) -> list:
        """
        Get all devices.

        Returns:
            List of device objects with identification, overview, location, etc.
        """
        return self.get("devices") or []

    def get_device(self, device_id: str) -> dict:
        """Get specific device by ID."""
        return self.get(f"devices/{device_id}")

    def get_device_detail(self, device_id: str) -> dict:
        """Get detailed device info including interfaces."""
        return self.get(f"devices/{device_id}/detail")

    def get_device_statistics(
        self,
        device_id: str,
        interval: str = "hour",
    ) -> dict:
        """
        Get device statistics.

        Args:
            device_id: Device UUID
            interval: Time interval (hour, day, week, month)
        """
        return self.get(f"devices/{device_id}/statistics", params={"interval": interval})

    # ==================== Interfaces ====================

    def get_interfaces(self) -> list:
        """Get all interfaces."""
        return self.get("interfaces") or []

    # ==================== Outages ====================

    def get_outages(self) -> list:
        """Get all outages."""
        return self.get("outages") or []

    # ==================== Logs ====================

    def get_logs(self, limit: int = 100) -> list:
        """Get system logs."""
        return self.get("logs", params={"limit": limit}) or []

    # ==================== Data Links ====================

    def get_data_links(self) -> list:
        """Get all data links between devices."""
        return self.get("data-links") or []
