# Changelog

All notable changes to the CZELA UISP Integration module.

## [1.0.0] - 2025-02-16

### Added - Complete Module Implementation

**Core Models:**
- `uisp.device` - UISP network devices with metrics and status
- `uisp.site` - Network sites with hierarchical structure
- `uisp.sync` - Synchronization service for UISP data
- `uisp.config.helper` - UISP connection configuration helper
- Extended `res.partner` with UISP device relationship

**User Interface:**
- Device views (tree, form, kanban, search)
- Site views (tree, form, search)
- Partner smart button showing UISP device count
- UISP root menu with organized submenus
- Color-coded device status in tree view
- Comprehensive search filters (status, technology type)

**Wizards:**
- Manual synchronization wizard (devices + sites)
- ČTÚ ART252 export wizard for compliance reporting

**Automation:**
- Cron job: Sync devices every 15 minutes
- Cron job: Sync sites every hour
- Automatic ČTÚ technology classification

**ČTÚ Classification:**
- `s2_ftth` - FTTH/Fiber (OLT, ONU, GPON devices)
- `s2_wifi` - WiFi/Unlicensed (LiteBeam, NanoBeam, Rocket, etc.)
- `s2_fwa` - FWA/Licensed (airFiber, LTU devices)

**Security:**
- UISP / User group (view-only access)
- UISP / Manager group (full sync and config access)

**Documentation:**
- README.md (complete module documentation)
- INSTALL.md (installation guide)
- DEPLOYMENT.md (is-dev.czela.net deployment)
- TODO.md (future enhancements)
- CHANGELOG.md (this file)

### Technical Specifications

**Compatibility:**
- Odoo 14.0, 15.0, 16.0+
- UISP API v2.1

**Dependencies:**
- Python: requests, urllib3
- Odoo: base, contacts

**Configuration Parameters:**
- `uisp.base_url` - UISP server URL (e.g., https://10.93.9.8)
- `uisp.api_key` - UISP API authentication key
- `uisp.verify_ssl` - SSL verification (true/false)

**Device Metrics Synced:**
- Status (active/inactive/disabled)
- CPU and RAM usage (%)
- Signal strength (dBm)
- Temperature (°C)
- Uptime (seconds)
- Last seen timestamp
- GPS coordinates (latitude/longitude)
- IP address, MAC address, firmware version

### Known Limitations

1. **ČTÚ Export:** Simplified implementation, requires customization for full RUIAN aggregation based on your specific partner/network.inventory relationship
2. **Map View:** Not yet implemented (planned for v1.1)
3. **Network Inventory:** No built-in network.inventory.device integration (requires separate module)

### Installation

**Package:** `czela_uisp.zip`

**Quick Install (Web Interface):**
1. Odoo → Apps → Upload module
2. Select `czela_uisp.zip`
3. Update Apps List
4. Install "CZELA UISP Integration"
5. Configure System Parameters (uisp.*)
6. Run first sync

**See:** DEPLOYMENT.md for detailed instructions

### Future Roadmap (TODO.md)

- Interactive map view with Leaflet.js
- Enhanced ČTÚ export with production-ready RUIAN logic
- Device action buttons (restart device, view in UISP)
- Dashboard with device statistics and KPIs
- Unit tests for sync logic
- Webhook support for real-time UISP updates

---

**Contributors:** CZELA + Claude Sonnet 4.5
**License:** LGPL-3
**Website:** https://is-dev.czela.net
