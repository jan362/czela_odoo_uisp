# Opravy aplikované na czela_uisp modul

**Datum:** 2025-02-16
**Verze:** 1.0.0 (s opravami)

## Přehled problémů a řešení

### Problém: Modul se nezobrazoval v Odoo Apps po nahrání

Po nahrání ZIP souboru na is-dev.czela.net a spuštění "Update Apps List" se modul CZELA UISP Integration nezobrazil v seznamu dostupných modulů.

**Root Cause:** Kritický bug v `models/uisp_config.py` způsoboval selhání inicializace modulu.

---

## Aplikované opravy

### ✅ Fix #1: CRITICAL - uisp_config.py Model Definition

**Soubor:** `czela_uisp/models/uisp_config.py`
**Řádek:** 13

**Změna:**
```python
# PŘED (špatně):
class UispConfigHelper(models.AbstractModel):
    """Helper model for UISP configuration and client creation."""
    _name = 'uisp.config.helper'
    _description = 'UISP Configuration Helper'

# PO (správně):
class UispConfigHelper(models.Model):
    """Helper model for UISP configuration and client creation."""
    _name = 'uisp.config.helper'
    _description = 'UISP Configuration Helper'
```

**Důvod:** `AbstractModel` je určen pouze pro mixiny BEZ `_name`. Kombinace `AbstractModel` + `_name` vytváří konflikt v Odoo model registry, což způsobí tiché selhání při načítání modulu.

**Impact:** 🔴 KRITICKÉ - bez této opravy se modul vůbec nezobrazí v Apps

---

### ✅ Fix #2: HIGH - Přidání partner_id pole do uisp.device

**Soubor:** `czela_uisp/models/uisp_device.py`
**Řádky:** 58-68, 185-194

**Přidáno pole:**
```python
# Link to partner (via network device or direct)
partner_id = fields.Many2one(
    'res.partner',
    'Customer',
    compute='_compute_partner_id',
    store=True,
    index=True
)
```

**Přidána compute metoda:**
```python
@api.depends('network_device_id.partner_id')
def _compute_partner_id(self):
    """Get partner from linked network device."""
    for device in self:
        if device.network_device_id and hasattr(device.network_device_id, 'partner_id'):
            device.partner_id = device.network_device_id.partner_id
        else:
            device.partner_id = False
```

**Důvod:** `res_partner.py` odkazoval na `domain=[('partner_id', '=', self.id)]`, ale pole `partner_id` v modelu `uisp.device` neexistovalo.

**Impact:** 🟠 HIGH - bez této opravy nefunguje propojení zákazník ↔ UISP zařízení

---

### ✅ Fix #3: MEDIUM - Bezpečnostní kontrola pro network.inventory.device

**Soubor:** `czela_uisp/models/uisp_device.py`
**Řádky:** 172-184

**Změna v _compute_network_device:**
```python
@api.depends('mac_address')
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
```

**Důvod:** Kód předpokládal existenci modelu `network.inventory.device`, který nemusí být nainstalován.

**Impact:** 🟡 MEDIUM - bez této opravy by modul spadl při instalaci, pokud není network.inventory modul

---

### ✅ Fix #4: HIGH - Oprava počítání UISP devices na partnerovi

**Soubor:** `czela_uisp/models/res_partner.py`
**Řádky:** 16-23

**Změna:**
```python
# PŘED (vracelo vždy 0):
@api.depends('id')
def _compute_uisp_device_count(self):
    """Count UISP devices linked to this partner."""
    for partner in self:
        partner.uisp_device_count = 0

# PO (správně počítá):
@api.depends('id')
def _compute_uisp_device_count(self):
    """Count UISP devices linked to this partner."""
    UispDevice = self.env['uisp.device']
    for partner in self:
        partner.uisp_device_count = UispDevice.search_count([
            ('partner_id', '=', partner.id)
        ])
```

**Důvod:** Původní implementace vracela vždy 0, smart button na partnerovi zobrazoval nesprávný počet.

**Impact:** 🟠 HIGH - smart button nefungoval správně

---

### ✅ Fix #5: MEDIUM - _map_status jako statická metoda

**Soubor:** `czela_uisp/models/uisp_sync.py`
**Řádky:** 131-141, volání na řádcích 66 a 118

**Změna metody:**
```python
# PŘED:
def _map_status(self, uisp_status):
    """Map UISP status to Odoo selection."""
    status_map = {
        'active': 'active',
        'inactive': 'inactive',
        'disabled': 'disabled',
    }
    return status_map.get(uisp_status, 'unknown')

# PO:
@staticmethod
def _map_status(uisp_status):
    """Map UISP status to Odoo selection."""
    status_map = {
        'active': 'active',
        'inactive': 'inactive',
        'disabled': 'disabled',
    }
    return status_map.get(uisp_status, 'unknown')
```

**Aktualizace volání:**
```python
# PŘED:
'status': self._map_status(overview.get('status'))

# PO:
'status': UispSync._map_status(overview.get('status'))
```

**Důvod:** V `TransientModel` kontextu mohla metoda způsobovat problémy s bindingem `self`.

**Impact:** 🟡 MEDIUM - preventivní oprava pro stabilitu synchronizace

---

## Další úpravy pro konzistenci

### Security Access Rights

**Soubor:** `czela_uisp/security/ir.model.access.csv`
**Přidáno:** Přístupová práva pro `uisp.config.helper` model (řádek 6)

```csv
access_uisp_config_helper,uisp.config.helper,model_uisp_config_helper,group_uisp_user,1,0,0,0
```

---

## Verifikace oprav

### ✅ Kontrolní seznam před instalací:

- [x] `uisp_config.py` používá `models.Model` (ne AbstractModel)
- [x] `uisp.device` má pole `partner_id` s compute metodou
- [x] `_compute_network_device` kontroluje existenci modelu před použitím
- [x] `res_partner._compute_uisp_device_count` skutečně počítá devices
- [x] `_map_status` je statická metoda s aktualizovanými voláními
- [x] Security access rights obsahují všechny modely
- [x] ZIP balíček vytvořen s opravenými soubory

### 📦 Instalační balíček:

**Soubor:** `H:\Sdílené disky\jsemit-EXT\_code\czela_odoo_uisp\czela_uisp.zip`
**Velikost:** 46 KB
**Datum vytvoření:** 2025-02-16 00:54

---

## Postup instalace na is-dev.czela.net

1. **Upload modulu:**
   - Otevřete: https://is-dev.czela.net
   - Apps → Upload (ikona cloudu s šipkou nahoru)
   - Vyberte: `czela_uisp.zip`
   - Import

2. **Update Apps List:**
   - Apps → ⋮ (tři tečky) → Update Apps List
   - Potvrdit

3. **Najít a nainstalovat:**
   - V Apps vyhledat: "CZELA UISP" nebo "uisp"
   - Modul by se měl zobrazit! ✅
   - Install

4. **Konfigurace:**
   - Settings → Technical → System Parameters
   - Přidat:
     - `uisp.base_url` = `https://10.93.9.8`
     - `uisp.api_key` = `<váš API klíč>`
     - `uisp.verify_ssl` = `false`

5. **První synchronizace:**
   - UISP → Configuration → Synchronization
   - Sync Now
   - Zkontrolovat UISP → Devices

---

## Očekávané výsledky po instalaci

✅ Modul se zobrazí v Apps
✅ Instalace proběhne bez chyb
✅ Menu "UISP" viditelné v hlavním menu
✅ Všechny views se načtou správně
✅ Sync wizard funguje
✅ Smart button na partnerovi ukazuje správný počet devices
✅ Propojení partner ↔ UISP device funguje

---

## Rollback (v případě problémů)

1. **Zkontrolovat logy:**
   ```bash
   tail -f /var/log/odoo/odoo-server.log
   ```

2. **Odinstalovat modul:**
   - Apps → CZELA UISP Integration → Uninstall

3. **Odstranit ze serveru (vyžaduje SSH):**
   ```bash
   rm -rf /opt/odoo/addons/czela_uisp/
   sudo systemctl restart odoo
   ```

---

## Kontakt a podpora

**Projekt:** CZELA UISP Integration
**Verzovací systém:** Git
**Dokumentace:** README.md, DEPLOYMENT.md

Pro další dotazy viz TODO.md a CHANGELOG.md.
