# CZELA UISP Integration for Odoo

Integrace mezi Odoo a UISP (Ubiquiti Network Management System) pro ISP operace.

## 📋 Popis

Tento Odoo modul umožňuje:

- **Synchronizaci síťových zařízení** z UISP do Odoo
- **Zobrazení statusu a metrik** zařízení (CPU, RAM, signal strength, uptime)
- **Správu síťových lokalit** (sites) s hierarchickou strukturou
- **Propojení UISP zařízení se zákazníky** přes network inventory
- **Generování ČTÚ ART252 reportů** pro compliance reporting
- **Mapové zobrazení** zařízení s GPS lokacemi

## 🚀 Klíčové funkce

### Automatická synchronizace
- Devices: každých 15 minut
- Sites: každou hodinu
- Ruční sync na vyžádání přes wizard

### Klasifikace technologií (ČTÚ)
- **FTTH (s2_ftth)** - optická přípojka (OLT, ONU, GPON)
- **WiFi (s2_wifi)** - bezdrát ve volných pásmech (2.4/5/60 GHz)
- **FWA (s2_fwa)** - bezdrát v licencovaných pásmech (airFiber, LTU)

### Real-time metriky
- CPU a RAM využití
- Signal strength (dBm)
- Uptime a last seen timestamp
- Teplota a firmware verze

## 📦 Instalace

### Požadavky

**Odoo verze:** 14.0+

**Python závislosti:**
```bash
pip install requests urllib3
```

### Instalace modulu

1. **Zkopírujte modul** do Odoo addons adresáře:
   ```bash
   cp -r czela_uisp /path/to/odoo/addons/
   ```

2. **Restartujte Odoo server**:
   ```bash
   sudo systemctl restart odoo
   ```

3. **Aktualizujte seznam modulů** v Odoo:
   - Nastavení → Apps → Update Apps List

4. **Nainstalujte modul**:
   - Vyhledejte "CZELA UISP Integration"
   - Klikněte na "Install"

## ⚙️ Konfigurace

### 1. Nastavení UISP připojení

Přejděte na **Settings → Technical → Parameters → System Parameters** a nastavte:

| Klíč | Hodnota | Příklad |
|------|---------|---------|
| `uisp.base_url` | URL vašeho UISP serveru | `https://10.93.9.8` |
| `uisp.api_key` | UISP API klíč | `your-api-key-here` |
| `uisp.verify_ssl` | SSL verifikace (true/false) | `false` |

### 2. Získání UISP API klíče

1. Přihlaste se do UISP
2. Přejděte na **Settings → Users**
3. Vytvořte nového uživatele nebo upravte existujícího
4. Vygenerujte API klíč v sekci "API Keys"
5. Zkopírujte klíč do Odoo system parameters

### 3. První synchronizace

1. Přejděte na **UISP → Synchronization → Sync Now**
2. Spusťte manuální sync pro ověření připojení
3. Po úspěšné synchronizaci aktivujte cron jobs:
   - **Settings → Technical → Automation → Scheduled Actions**
   - Najděte "UISP: Sync Devices" a "UISP: Sync Sites"
   - Aktivujte obě akce (toggle "Active")

## 🔐 Oprávnění

Modul definuje dvě skupiny uživatelů:

- **UISP / User** - Může prohlížet UISP data (devices, sites)
- **UISP / Manager** - Může spouštět sync, konfigurovat nastavení

Přiřaďte oprávnění v **Settings → Users & Companies → Users**.

## 📊 Použití

### Zobrazení zařízení

**UISP → Devices** zobrazí všechna synchronizovaná zařízení:

- **List view** - přehled všech zařízení s filtry
- **Kanban view** - kartičkový přehled
- **Form view** - detail zařízení s metrikami
- **Map view** - mapa zařízení podle GPS

### Filtrování podle technologie

Použijte filtry pro zobrazení zařízení podle typu:
- FTTH (optika)
- WiFi (volné pásmo)
- FWA (licencované pásmo)

### Propojení se zákazníky

Zařízení jsou automaticky propojována se zákazníky (res.partner) přes:
- **MAC adresa matching** s network.inventory.device
- Smart button na partner form zobrazuje počet UISP zařízení

### ČTÚ Export

**UISP → Reports → ČTÚ ART252 Export**

1. Vyberte technologii (WiFi/FTTH/FWA)
2. Klikněte na "Export CSV"
3. Získejte CSV soubor pro reporting

Formát exportu obsahuje:
- RUIAN kódy
- Aktivní připojení
- Pokrytí
- Rychlosti download/upload
- VHCN třída

## 🏗️ Architektura

### Data modely

```
uisp.device          - UISP zařízení (cache)
uisp.site            - UISP lokality (hierarchie)
uisp.config.helper   - Helper pro UISP klient
uisp.sync            - Synchronizační služba
res.partner          - Extended: UISP device count
```

### Synchronizační flow

```
UISP API
   ↓ (cron job / manual)
uisp.sync.sync_devices()
   ↓
uisp.device (create/update)
   ↓ (computed field)
Match by MAC address
   ↓
network.inventory.device
   ↓
res.partner
```

### CTU klasifikace

Zařízení jsou automaticky klasifikována podle modelu:

```python
FTTH: 'fiber', 'olt', 'onu', 'gpon'
WiFi: 'litebeam', 'nanobeam', 'rocket', 'wave ap', '60ad'
FWA:  'airfiber', 'af24', 'ltu'
```

## 🔧 Vývoj

### Struktura projektu

```
czela_uisp/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── uisp_config.py       # UISP client helper
│   ├── uisp_device.py       # Device model
│   ├── uisp_site.py         # Site model
│   ├── uisp_sync.py         # Sync service
│   └── res_partner.py       # Partner extension
├── wizards/
│   ├── uisp_sync_wizard.py
│   └── ctu_export_wizard.py
├── views/
│   ├── uisp_menu.xml
│   ├── uisp_device_views.xml
│   ├── uisp_site_views.xml
│   ├── uisp_config_views.xml
│   └── partner_views.xml
├── data/
│   ├── ir_config_parameter.xml
│   └── uisp_cron.xml
├── security/
│   ├── ir.model.access.csv
│   └── uisp_security.xml
└── lib/
    └── uisp_client.py       # UISP API v2.1 client
```

### UISP API Client

Modul obsahuje kompletní UISP API v2.1 klienta:

```python
from odoo.addons.czela_uisp.lib.uisp_client import UISPClient, UISPConfig

# V Odoo modelu
client = self.env['uisp.config.helper'].get_uisp_client()

# Získat všechna zařízení
devices = client.get_devices()

# Získat konkrétní zařízení
device = client.get_device('device-uuid')

# Získat lokality
sites = client.get_sites()
```

### Rozšíření modulu

Pro přidání vlastních polí do `uisp.device`:

```python
from odoo import fields, models

class UispDevice(models.Model):
    _inherit = 'uisp.device'

    custom_field = fields.Char('Custom Field')
```

## 🐛 Troubleshooting

### Synchronizace selhává

1. **Zkontrolujte UISP připojení**:
   ```python
   # V Odoo shell
   env['uisp.config.helper'].test_connection()
   ```

2. **Zkontrolujte logy**:
   ```bash
   tail -f /var/log/odoo/odoo-server.log | grep UISP
   ```

3. **Ověřte SSL certifikát**:
   - Pro self-signed cert nastavte `uisp.verify_ssl = false`

### Zařízení se nepárují se zákazníky

1. Ověřte, že existuje model `network.inventory.device`
2. Zkontrolujte MAC adresy - musí být v databázi
3. MAC matching je case-insensitive, normalizuje separátory

### Cron job neběží

1. Zkontrolujte, že cron je aktivní:
   - Settings → Technical → Scheduled Actions
   - "UISP: Sync Devices" - toggle Active

2. Ověřte Odoo cron worker:
   ```bash
   ps aux | grep odoo | grep cron
   ```

## 📝 Changelog

### Version 1.0.0 (2025-02-16)
- ✨ Iniciální release
- ✅ UISP device a site synchronizace
- ✅ ČTÚ technology classification
- ✅ MAC address matching
- ✅ ČTÚ ART252 export
- ✅ Cron jobs pro auto-sync
- ✅ Security groups (User, Manager)

## 🤝 Přispívání

Projekt je vyvíjen pro CZELA ISP operace. Pro přispění:

1. Fork repository
2. Vytvořte feature branch (`git checkout -b feature/amazing-feature`)
3. Commit změny (`git commit -m 'Add amazing feature'`)
4. Push do branch (`git push origin feature/amazing-feature`)
5. Otevřete Pull Request

## 📄 Licence

LGPL-3

## 👥 Autoři

- **CZELA** - [is-dev.czela.net](https://is-dev.czela.net)

## 🔗 Související projekty

- [czela_ctu](https://github.com/czela/czela_ctu) - Standalone UISP integration server (Python)
- [UISP](https://ui.com/unifi/unifi-isp-manager) - Ubiquiti ISP management platform

## 📞 Podpora

Pro podporu kontaktujte CZELA IT tým nebo vytvořte issue v GitHub repository.

---

**Made with ❤️ for Czech ISP operations**
