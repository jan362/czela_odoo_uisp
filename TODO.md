# TODO - Zbývající implementace

## ✅ Hotovo

- [x] Module foundation (structure, manifest)
- [x] UISP API client (lib/uisp_client.py)
- [x] Core models (device, site, config, sync)
- [x] Partner extension (smart button)
- [x] Security (groups, access rights)
- [x] Cron jobs configuration
- [x] README documentation
- [x] Git repository initialization

## 🚧 Zbývá implementovat

### High Priority

- [ ] **XML Views** - Device views, site views, menu
  - czela_uisp/views/uisp_menu.xml
  - czela_uisp/views/uisp_device_views.xml
  - czela_uisp/views/uisp_site_views.xml
  - czela_uisp/views/uisp_config_views.xml
  - czela_uisp/views/partner_views.xml

- [ ] **Wizards** - Sync wizard, ČTÚ export wizard
  - czela_uisp/wizards/uisp_sync_wizard.py
  - czela_uisp/wizards/uisp_sync_wizard_views.xml
  - czela_uisp/wizards/ctu_export_wizard.py
  - czela_uisp/wizards/ctu_export_wizard_views.xml

- [ ] **Network Inventory Extension** - pokud existuje modul
  - czela_uisp/models/network_inventory_device.py
  - Extend network.inventory.device s UISP device linkem
  - MAC matching computed field

### Medium Priority

- [ ] **Map Widget** - Leaflet.js integration pro GPS view
  - czela_uisp/static/src/js/uisp_map_widget.js
  - Map view definition v device views

- [ ] **Icon & Description** - Module assets
  - czela_uisp/static/description/icon.png
  - czela_uisp/static/description/index.html

- [ ] **Unit Tests**
  - tests/__init__.py
  - tests/test_uisp_client.py
  - tests/test_uisp_sync.py
  - tests/test_ctu_classification.py

### Low Priority

- [ ] **Dashboard/KPI** - Statistics kanban
  - Device count by status
  - Technology breakdown (FTTH/WiFi/FWA)
  - Sync status indicator

- [ ] **Webhooks** - Real-time UISP updates
  - Webhook receiver controller
  - UISP webhook configuration guide

- [ ] **Device Actions**
  - Restart device (UISP API call)
  - View in UISP (redirect to UISP web)
  - Show device statistics graph

## 📝 Notes

### Views Implementation

XML views jsou kritické pro použitelnost modulu. Struktura:

```xml
<!-- uisp_menu.xml -->
UISP (top menu)
├── Devices
│   ├── All Devices
│   ├── By Technology (filters)
├── Sites
├── Synchronization
│   ├── Sync Now (wizard)
│   ├── Configuration
├── Reports
    └── ČTÚ ART252 Export (wizard)
```

### ČTÚ Export Wizard

Port logiky z `czela_ctu/server.py:1359-1531`:

1. Získat partnery s RUIAN kódem
2. Získat network devices s partner_id
3. Match s UISP devices přes MAC
4. Filtrovat podle CTU typu
5. Agregovat podle RUIAN
6. Generovat CSV (delimiter ';')

Formát CSV:
```
ADM;kategorie;aktivni_pripojeni;nepodnikatelske;pokryti;download;upload;download_max;upload_max;trida_vhcn
```

### Network Inventory Dependency

Pokud modul `network.inventory` neexistuje v Odoo instalaci:

- Udělat `network.inventory.device` dependency optional
- Computed fields v res_partner vrátí 0 pokud model neexistuje
- MAC matching nebude fungovat → dokumentovat jako limitation

## 🔍 Testing Checklist

Po dokončení views & wizards:

- [ ] Instalace modulu bez chyb
- [ ] UISP connection test přes wizard
- [ ] Manual sync devices & sites
- [ ] Device list view zobrazuje data
- [ ] Device form view zobrazuje všechna pole
- [ ] Kanban view funguje
- [ ] CTU classification je správná (FTTH/WiFi/FWA)
- [ ] Cron jobs běží automaticky
- [ ] ČTÚ export generuje CSV
- [ ] Partner smart button zobrazuje device count
- [ ] Security groups fungují (User vs Manager)

## 📦 Release Checklist

Před verzí 1.0.0:

- [ ] Všechny views implementovány
- [ ] Wizards funkční
- [ ] Unit tests pokrývají sync logiku
- [ ] Documentation kompletní
- [ ] Icon a description vytvořeny
- [ ] Testováno na Odoo 14.0, 15.0, 16.0
- [ ] GitHub repository public
- [ ] CHANGELOG.md vytvořen

---

**Poznámka:** V současné době je vytvořen základ modulu (models, security, cron).
Pro plnou funkcionalitu je potřeba implementovat XML views a wizards.
