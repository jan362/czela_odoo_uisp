# Instalační návod pro Odoo 18.0

## 📦 Rychlá instalace

### Požadavky

- **Odoo 18.0+** (testováno na 18.0-20251021)
- **Python 3.10+**
- **Závislosti:** `requests`, `urllib3`

### Krok 1: Instalace Python závislostí

```bash
pip install requests urllib3
```

### Krok 2: Instalace modulu přes Odoo UI (Doporučeno)

1. **Přihlaste se** do Odoo jako administrátor
2. Přejděte na **Apps** (Aplikace)
3. Klikněte na **⋮** (tři tečky) → **Upload Module**
4. Nahrajte soubor `czela_uisp_odoo18.zip`
5. Klikněte na **Upload**
6. Najděte modul "CZELA UISP Integration" v seznamu
7. Klikněte na **Install**

### Alternativa: Manuální instalace

```bash
# 1. Zkopírujte modul do addons adresáře
cp -r czela_uisp /path/to/odoo/addons/

# 2. Restartujte Odoo server
sudo systemctl restart odoo

# 3. Aktualizujte seznam modulů
# V Odoo UI: Apps → Update Apps List

# 4. Instalujte modul
# V Odoo UI: Apps → Search "CZELA UISP" → Install
```

---

## ⚙️ Konfigurace

### Krok 1: Nastavení UISP připojení

Po instalaci přejděte na:

**Settings → Technical → Parameters → System Parameters**

Nastavte následující parametry:

| Klíč | Popis | Příklad |
|------|-------|---------|
| `uisp.base_url` | URL UISP serveru | `https://10.93.9.8` nebo `https://uisp.example.com` |
| `uisp.api_key` | UISP API klíč | `your-api-key-here` |
| `uisp.verify_ssl` | SSL verifikace | `false` (pro self-signed), `true` (pro platný cert) |

### Krok 2: Získání UISP API klíče

1. Přihlaste se do UISP (Ubiquiti ISP Manager)
2. Přejděte na **Settings → Users**
3. Vyberte uživatele nebo vytvořte nového
4. V sekci **API Keys** klikněte na **Generate New Key**
5. Zkopírujte klíč a vložte do Odoo system parameters

### Krok 3: Test připojení

V Pythonu shell (nebo custom Odoo action):

```python
# Otevřete Odoo shell
odoo-bin shell -d your_database

# Test připojení
result = env['uisp.config.helper'].test_connection()
print(result)
# Expected output: {'status': 'success', 'message': 'Connection successful! Found X sites.'}
```

### Krok 4: První synchronizace

1. Přejděte na **UISP → Synchronization → Sync Now**
2. Spusťte manuální synchronizaci
3. Zkontrolujte logy pro případné chyby

**Nebo přes Python:**

```python
# Sync devices
env['uisp.sync'].sync_devices()

# Sync sites
env['uisp.sync'].sync_sites()
```

### Krok 5: Aktivace automatické synchronizace

1. Přejděte na **Settings → Technical → Automation → Scheduled Actions**
2. Najděte:
   - **UISP: Sync Devices** (každých 15 minut)
   - **UISP: Sync Sites** (každou hodinu)
3. Aktivujte obě akce (toggle "Active")

---

## 🔐 Oprávnění

### Přiřazení rolí uživatelům

1. Přejděte na **Settings → Users & Companies → Users**
2. Vyberte uživatele
3. V sekci **Access Rights** najděte:
   - **UISP / User** - Může prohlížet UISP data
   - **UISP / Manager** - Může spouštět sync a měnit nastavení
4. Zaškrtněte příslušná oprávnění

---

## 📊 Použití

### Zobrazení zařízení

**UISP → Devices**

- **List View** - tabulkový přehled všech zařízení
- **Kanban View** - kartičkový přehled
- **Form View** - detail zařízení s metrikami
- **Map View** - GPS mapa zařízení

### Filtrování

Použijte předdefinované filtry:

- **FTTH** - optická zařízení (OLT, ONU, GPON)
- **WiFi** - bezdrát ve volných pásmech
- **FWA** - bezdrát v licencovaných pásmech

### ČTÚ Export

**UISP → Reports → ČTÚ ART252 Export**

1. Vyberte technologii (FTTH/WiFi/FWA)
2. Klikněte na **Export CSV**
3. Stáhněte CSV soubor pro reporting

---

## 🐛 Řešení problémů

### Modul se nepodaří nainstalovat

**Problém:** Chyba při instalaci modulu

**Řešení:**
```bash
# Zkontrolujte logy
tail -f /var/log/odoo/odoo-server.log

# Zkontrolujte závislosti
pip list | grep -E "requests|urllib3"

# Zkontrolujte, že modul 'contacts' je nainstalován
```

### Synchronizace selhává

**Problém:** UISP sync vrací chyby

**Řešení:**
```bash
# Test připojení
curl -k -H "x-auth-token: YOUR_API_KEY" https://UISP_URL/nms/api/v2.1/sites

# Zkontrolujte SSL
# Pokud používáte self-signed certifikát, nastavte uisp.verify_ssl = false
```

### Zařízení nejsou propojená se zákazníky

**Problém:** `partner_id` je prázdné

**Řešení:**
- Ověřte, že existuje modul `network.inventory.device`
- Zkontrolujte MAC adresy v databázi
- MAC matching je case-insensitive a normalizuje separátory (`:`, `-`)

### Cron job neběží

**Problém:** Automatická synchronizace nefunguje

**Řešení:**
```bash
# Zkontrolujte, že Odoo cron worker běží
ps aux | grep odoo | grep cron

# Zkontrolujte nastavení cron jobs v Odoo
# Settings → Technical → Scheduled Actions

# Manuálně spusťte cron (pro testování)
odoo-bin -c /etc/odoo/odoo.conf --db-filter=your_db -d your_db --stop-after-init --load=base,web,uisp
```

---

## 🔄 Upgrade z verze 1.0.0

Pokud upgradujete z předchozí verze:

1. **Zálohujte databázi**
   ```bash
   pg_dump your_database > backup_$(date +%Y%m%d).sql
   ```

2. **Aktualizujte soubory modulu**
   ```bash
   rm -rf /path/to/odoo/addons/czela_uisp
   unzip czela_uisp_odoo18.zip -d /path/to/odoo/addons/
   ```

3. **Restartujte Odoo**
   ```bash
   sudo systemctl restart odoo
   ```

4. **Update modul v UI**
   - Apps → CZELA UISP Integration → Upgrade

**Poznámka:** Není nutná databázová migrace - všechny změny jsou pouze na úrovni kódu.

---

## 📋 Checklist po instalaci

- [ ] Python závislosti nainstalovány
- [ ] Modul nainstalován v Odoo
- [ ] UISP parametry nakonfigurovány
- [ ] API klíč získán a nastaven
- [ ] Test připojení proběhl úspěšně
- [ ] První manuální sync dokončena
- [ ] Cron jobs aktivovány
- [ ] Oprávnění uživatelům přiřazena
- [ ] Data viditelná v UISP menu

---

## 📞 Podpora

**Issues:** https://github.com/jan362/czela_odoo_uisp/issues

**Email:** IT tým CZELA

**Dokumentace:**
- `README.md` - Kompletní dokumentace
- `ODOO18_COMPATIBILITY.md` - Detaily Odoo 18 kompatibility
- `FIXES_APPLIED.md` - Historie oprav

---

## 📄 Verze

**Modul:** 18.0.1.0.0
**Odoo:** 18.0+
**Datum vydání:** 2025-02-16

---

**Úspěšnou instalaci!** 🚀
