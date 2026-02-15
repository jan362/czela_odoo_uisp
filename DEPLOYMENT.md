# Nasazení modulu na is-dev.czela.net

## 📦 Instalace přes Odoo Web Interface

### Krok 1: Příprava modulu

✅ **Hotovo** - Modul je zabalen jako `czela_uisp.zip`

Umístění: `H:\Sdílené disky\jsemit-EXT\_code\czela_odoo_uisp\czela_uisp.zip`

### Krok 2: Přihlášení do Odoo

1. Otevřete prohlížeč a přejděte na: **https://is-dev.czela.net**
2. Přihlaste se jako **administrátor** (uživatel s právy "Settings")

### Krok 3: Aktivace Developer Mode

1. V Odoo přejděte na **Settings** (Nastavení)
2. Scroll dolů na **Developer Tools**
3. Klikněte na **Activate the developer mode**

   Případně přidejte `?debug=1` do URL:
   ```
   https://is-dev.czela.net/web?debug=1
   ```

### Krok 4: Upload modulu

**Metoda A: Přes Apps menu (doporučeno pro Odoo 16+)**

1. Přejděte na **Apps** (Aplikace)
2. V pravém horním rohu klikněte na **⚙️ ikonu** nebo tři tečky
3. Vyberte **Upload module** nebo **Import module**
4. Vyberte soubor `czela_uisp.zip`
5. Klikněte na **Import**

**Metoda B: Ruční nahrání na server (pokud A nefunguje)**

Pokud web interface neumožňuje upload, budete potřebovat:
- SSH/SFTP přístup, nebo
- Požádat server administrátora o nahrání modulu do `/opt/odoo/addons/`

### Krok 5: Update Apps List

1. V **Apps** menu klikněte na **Update Apps List** (Aktualizovat seznam aplikací)
2. Potvrďte akci
3. Počkejte na dokončení (může trvat několik sekund)

### Krok 6: Instalace modulu

1. V Apps vyhledejte "**CZELA UISP**" nebo "**uisp**"
2. Měli byste vidět modul s názvem "CZELA UISP Integration"
3. Klikněte na **Install** (Instalovat)
4. Počkejte na dokončení instalace

⚠️ **Poznámka:** Instalace může zobrazit chybu, pokud chybí závislosti (viz níže).

### Krok 7: Konfigurace UISP připojení

1. Přejděte na **Settings → Technical → Parameters → System Parameters**
2. Klikněte na **Create** (Vytvořit)
3. Přidejte následující parametry:

| Key | Value | Příklad |
|-----|-------|---------|
| `uisp.base_url` | `https://10.93.9.8` | URL vašeho UISP serveru |
| `uisp.api_key` | `your-api-key` | API klíč z UISP |
| `uisp.verify_ssl` | `false` | Pro self-signed certifikáty |

**Získání UISP API klíče:**
1. Přihlaste se do UISP (https://10.93.9.8)
2. Settings → Users → [váš user]
3. API Keys → Generate New Key
4. Zkopírujte klíč

### Krok 8: První synchronizace

1. V Odoo přejděte na **UISP → Synchronization → Sync Now**
   - ⚠️ **Poznámka:** Pokud menu UISP není vidět, views nejsou implementovány (viz níže)

2. Pokud views nejsou hotové, můžete syncnout přes Python:
   ```python
   # V Odoo shell nebo přes Technical → Execute Code (developer mode)
   env['uisp.sync'].sync_devices()
   env['uisp.sync'].sync_sites()
   ```

### Krok 9: Aktivace automatické synchronizace

1. **Settings → Technical → Automation → Scheduled Actions**
2. Najděte:
   - **UISP: Sync Devices**
   - **UISP: Sync Sites**
3. Pro každou akci:
   - Otevřete detail
   - Zaškrtněte **Active**
   - Uložte

---

## ⚠️ Známé problémy a řešení

### ❌ Chyba při instalaci: "Module czela_uisp depends on..."

**Příčina:** Modul vyžaduje závislosti, které nejsou nainstalované.

**Řešení:**

V `__manifest__.py` je zatím minimal dependencies:
```python
'depends': [
    'base',
    'contacts',
],
```

Pokud používáte **network.inventory.device** model, přidejte příslušný modul do `depends`.

### ❌ ImportError: No module named 'requests'

**Příčina:** Python balíček `requests` není nainstalován na serveru.

**Řešení (vyžaduje SSH přístup):**
```bash
# SSH na server
ssh user@is-dev.czela.net

# Aktivovat Odoo virtualenv (zjistit cestu od admina)
source /opt/odoo/venv/bin/activate

# Instalovat requests
pip install requests urllib3

# Restartovat Odoo
sudo systemctl restart odoo
```

**Alternativa (bez SSH):** Požádejte server administrátora.

### ❌ Menu "UISP" se nezobrazuje

**Příčina:** XML views nejsou implementovány (viz TODO.md).

**Řešení:**

1. **Krátkodobě:** Použijte Python shell pro sync:
   ```python
   env['uisp.sync'].sync_devices()
   ```

2. **Dlouhodobě:** Implementujte XML views:
   - `views/uisp_menu.xml`
   - `views/uisp_device_views.xml`
   - atd.

### ❌ SSL Certificate Verify Failed

**Příčina:** UISP používá self-signed certifikát.

**Řešení:** Nastavte `uisp.verify_ssl = false` v System Parameters.

---

## 🧪 Testování instalace

### Test 1: Ověření modulu v databázi

```python
# Technical → Execute Code (developer mode)
module = env['ir.module.module'].search([('name', '=', 'czela_uisp')])
print(f"Module state: {module.state}")
# Očekáváno: 'installed'
```

### Test 2: Test UISP připojení

```python
# Execute Code
result = env['uisp.config.helper'].test_connection()
print(result)
# Očekáváno: {'status': 'success', 'message': '...', 'site_count': X}
```

### Test 3: Manuální sync

```python
# Execute Code
result = env['uisp.sync'].sync_devices()
print(f"Synced {result['synced_count']} devices")
```

### Test 4: Zobrazení dat

```python
# Execute Code
devices = env['uisp.device'].search([])
print(f"Total devices: {len(devices)}")

for device in devices[:5]:
    print(f"- {device.name} ({device.model}) - {device.status}")
```

---

## 📋 Checklist před nasazením

- [ ] ZIP balíček vytvořen (`czela_uisp.zip`)
- [ ] Přihlášen do Odoo jako admin
- [ ] Developer mode aktivován
- [ ] Modul nahrán přes Apps → Upload module
- [ ] Apps list aktualizován
- [ ] Modul nainstalován
- [ ] System Parameters nastaveny (base_url, api_key)
- [ ] Test connection úspěšný
- [ ] První sync devices + sites proběhl
- [ ] Cron jobs aktivovány
- [ ] Data zobrazena v Odoo (nebo přes Python shell)

---

## 🚀 Po nasazení

### Pokud vše funguje:

1. ✅ Devices jsou synchronizovány z UISP
2. ✅ Sites jsou v databázi
3. ✅ Cron jobs běží automaticky
4. ✅ Můžete procházet data přes Python shell

### Další kroky:

1. **Implementovat views** (viz TODO.md)
   - Pro zobrazení dat v UI
   - Menu UISP → Devices, Sites, atd.

2. **Implementovat wizards**
   - Sync wizard (UI pro manuální sync)
   - ČTÚ export wizard

3. **Otestovat na production data**
   - Ověřit MAC matching s network.inventory.device
   - Zkontrolovat CTU classification

---

## 📞 Potřebujete pomoc?

- **Views nejsou implementovány?** → Viz TODO.md pro seznam zbývajících souborů
- **Chyby při instalaci?** → Zkontrolujte Odoo logy: `/var/log/odoo/odoo-server.log`
- **Python závislosti chybí?** → Kontaktujte server administrátora

---

**Soubor k nahrání:** `czela_uisp.zip` (v root adresáři projektu)
