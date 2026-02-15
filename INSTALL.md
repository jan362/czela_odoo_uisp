# Instalační návod - CZELA UISP Integration

## 🚀 Rychlá instalace

### 1. Zkopírovat modul do Odoo

```bash
# Zkopírovat modul do Odoo addons adresáře
cp -r czela_uisp /opt/odoo/addons/

# Nastavit vlastníka (pokud běží Odoo pod odoo uživatelem)
sudo chown -R odoo:odoo /opt/odoo/addons/czela_uisp
```

### 2. Instalovat Python závislosti

```bash
# Aktivovat Odoo virtualenv (pokud používáte)
source /opt/odoo/venv/bin/activate

# Instalovat požadované balíčky
pip install requests urllib3
```

### 3. Restartovat Odoo

```bash
sudo systemctl restart odoo
```

### 4. Nainstalovat modul v Odoo

1. Přihlaste se do Odoo jako administrátor
2. Přejděte na **Apps** (Aplikace)
3. Klikněte na **Update Apps List** (Aktualizovat seznam aplikací)
4. Vyhledejte "**CZELA UISP**"
5. Klikněte na **Install** (Instalovat)

### 5. Konfigurovat UISP připojení

1. Přejděte na **Settings → Technical → Parameters → System Parameters**
2. Nastavte následující parametry:

| Parametr | Hodnota | Příklad |
|----------|---------|---------|
| `uisp.base_url` | URL UISP serveru | `https://10.93.9.8` |
| `uisp.api_key` | UISP API klíč | `váš-api-klíč` |
| `uisp.verify_ssl` | SSL verifikace | `false` |

**Získání API klíče z UISP:**
1. Přihlaste se do UISP
2. Settings → Users → [váš uživatel]
3. API Keys → Generate New Key
4. Zkopírujte klíč do Odoo

### 6. První synchronizace

1. Přejděte na **UISP → Synchronization → Sync Now**
2. Klikněte na **Sync Devices** a **Sync Sites**
3. Zkontrolujte, že synchronizace proběhla úspěšně
4. Otevřete **UISP → Devices** pro zobrazení zařízení

### 7. Aktivovat automatickou synchronizaci

1. Přejděte na **Settings → Technical → Automation → Scheduled Actions**
2. Najděte a aktivujte:
   - **UISP: Sync Devices** (každých 15 minut)
   - **UISP: Sync Sites** (každou hodinu)

## ✅ Ověření instalace

### Test UISP připojení

V Odoo shell:

```python
# Spustit Odoo shell
/opt/odoo/odoo-bin shell -d your_database

# Testovat připojení
env['uisp.config.helper'].test_connection()
```

Očekávaný výstup:
```python
{
    'status': 'success',
    'message': 'Connection successful! Found X sites.',
    'site_count': X
}
```

### Zkontrolovat logy

```bash
# Sledovat Odoo logy
tail -f /var/log/odoo/odoo-server.log | grep UISP

# Měli byste vidět:
# INFO ... UISP device sync completed. Synced X devices.
# INFO ... UISP site sync completed. Synced X sites.
```

## 🔐 Oprávnění uživatelů

Přiřaďte uživatelům oprávnění:

1. **Settings → Users & Companies → Users**
2. Vyberte uživatele
3. V záložce **Access Rights** přiřaďte:
   - **UISP / User** - pro zobrazení dat
   - **UISP / Manager** - pro správu synchronizace

## 🐛 Řešení problémů

### Modul se neobjevuje v Apps

```bash
# Zkontrolujte addons_path v odoo.conf
cat /etc/odoo/odoo.conf | grep addons_path

# Měla by obsahovat cestu k modulu
addons_path = /opt/odoo/addons,...

# Restartujte Odoo
sudo systemctl restart odoo
```

### Chyba při synchronizaci: "UISP base URL not configured"

Zkontrolujte System Parameters:
```sql
-- V PostgreSQL
SELECT key, value FROM ir_config_parameter
WHERE key LIKE 'uisp.%';
```

### SSL Certificate Verify Failed

Nastavte `uisp.verify_ssl` na `false` pro self-signed certifikáty.

### ImportError: No module named 'requests'

```bash
# Instalujte requests v Odoo virtualenv
source /opt/odoo/venv/bin/activate
pip install requests urllib3
sudo systemctl restart odoo
```

## 📝 Co dál?

1. **Prozkoumejte UISP menu** - Devices, Sites, Reports
2. **Nastavte filtry** - podle technologie (FTTH/WiFi/FWA)
3. **Vyzkoušejte ČTÚ export** - UISP → Reports → ČTÚ ART252 Export
4. **Propojte se zákazníky** - přes network.inventory.device

## 🔗 Další zdroje

- [README.md](README.md) - Kompletní dokumentace
- [UISP API Documentation](https://uisp.ui.com/api-docs/) - UISP API reference
- [Odoo Documentation](https://www.odoo.com/documentation/) - Odoo development guide

---

**Potřebujete pomoc?** Kontaktujte CZELA IT tým.
