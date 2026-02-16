# 🔄 UPDATE GUIDE - CZELA UISP Integration

Průvodce aktualizací modulu CZELA UISP Integration na serveru is-dev.czela.net.

> **📅 Verze:** 18.0.1.0.0
> **🎯 Server:** is-dev.czela.net
> **📦 Balíčky:** czela_uisp_odoo18.zip, czela_uisp_odoo18_complete.zip

---

## 📖 Kdy použít tento průvodce

- ✅ **UPDATE:** Modul je již nainstalován a chceš aktualizovat na novou verzi
- ❌ **FRESH INSTALL:** Pro novou instalaci použij [INSTALL_ODOO18.md](INSTALL_ODOO18.md)

---

## ⚙️ Prerekvizity

Před zahájením aktualizace ověř, že máš:

- [x] SSH přístup na server is-dev.czela.net
- [x] Sudo oprávnění na serveru
- [x] Nové ZIP balíčky připravené (`czela_uisp_odoo18_complete.zip`)
- [x] Modul `network_inventory` je nainstalován v Odoo (⚠️ NOVÁ ZÁVISLOST!)

---

## ⚠️ PŘED AKTUALIZACÍ - KRITICKÉ!

### 1. Vytvoř zálohu současného modulu

```bash
ssh your_username@is-dev.czela.net

# Vytvoř zálohu s timestampem
sudo cp -r /data/is-dev-czela-net/developer-addons/czela_uisp \
     /data/is-dev-czela-net/developer-addons/czela_uisp_backup_$(date +%Y%m%d_%H%M%S)

# Ověř, že záloha byla vytvořena
ls -la /data/is-dev-czela-net/developer-addons/czela_uisp_backup_*
```

### 2. Kontrola network_inventory modulu

```bash
# V Odoo UI:
# Settings → Apps → Vyhledej "network_inventory"
# Ověř, že modul je nainstalován (stav: "Installed")
```

⚠️ **DŮLEŽITÉ:** Pokud `network_inventory` není nainstalován, instaluj ho NYNÍ (před upgradem UISP modulu)!

---

## 🚀 POSTUP AKTUALIZACE

### Krok 1: Nahrání souborů na server

**Z lokálního PC:**

```bash
# Nahraj ZIP balíček na server
scp czela_uisp_odoo18_complete.zip your_username@is-dev.czela.net:/tmp/
```

**Na serveru (SSH):**

```bash
# Přihlas se na server
ssh your_username@is-dev.czela.net

# Extrahuj ZIP
cd /tmp
unzip -o czela_uisp_odoo18_complete.zip

# Odstraň starou verzi
sudo rm -rf /data/is-dev-czela-net/developer-addons/czela_uisp

# Zkopíruj novou verzi
sudo cp -r czela_uisp /data/is-dev-czela-net/developer-addons/

# Ověř, že soubory byly zkopírovány
ls -la /data/is-dev-czela-net/developer-addons/czela_uisp/
```

---

### Krok 2: Nastavení oprávnění

```bash
# Nastav vlastníka na odoo:odoo
sudo chown -R odoo:odoo /data/is-dev-czela-net/developer-addons/czela_uisp

# Nastav oprávnění 755
sudo chmod -R 755 /data/is-dev-czela-net/developer-addons/czela_uisp

# Ověř oprávnění
ls -la /data/is-dev-czela-net/developer-addons/ | grep czela_uisp
```

Očekávaný výstup:
```
drwxr-xr-x  5 odoo odoo  4096 Feb 16 10:30 czela_uisp
```

---

### Krok 3: Restart Odoo služby

⚠️ **KRITICKÉ:** Restart je POVINNÝ pro aplikování Python změn!

```bash
# Restartuj Odoo
sudo systemctl restart odoo

# Počkej 5-10 sekund a zkontroluj status
sudo systemctl status odoo
```

Očekávaný výstup:
```
● odoo.service - Odoo Open Source ERP
   Loaded: loaded (/etc/systemd/system/odoo.service; enabled)
   Active: active (running) since ...
```

**Sleduj logy pro případné errory:**

```bash
sudo tail -f /var/log/odoo/odoo-server.log
```

Hledej řádky s "czela_uisp" - neměly by obsahovat ERROR ani WARNING.

---

### Krok 4: Upgrade přes Odoo UI

1. **Login do Odoo:**
   - Otevři https://is-dev.czela.net
   - Přihlas se jako admin

2. **Update Apps List:**
   - Přejdi na **Apps**
   - Klikni na menu (tři tečky) → **"Update Apps List"**
   - Potvrď akci

3. **Najdi CZELA UISP modul:**
   - Vyhledej "CZELA UISP" nebo "UISP"
   - Modul by měl zobrazovat tlačítko **"Upgrade"** (ne "Install")

4. **Spusť upgrade:**
   - Klikni na **"Upgrade"**
   - Počkej na dokončení (může trvat 10-30 sekund)

5. **Ověř úspěch:**
   - Modul by měl zobrazovat **"Installed"**
   - Verze: **18.0.1.0.0**

---

## ✅ OVĚŘENÍ ÚSPĚŠNÉ AKTUALIZACE

### Checklist

- [ ] **Záloha vytvořena** s timestampem
- [ ] **network_inventory** modul je nainstalován
- [ ] **Soubory zkopírovány** do `/data/is-dev-czela-net/developer-addons/czela_uisp`
- [ ] **Oprávnění nastavena** (odoo:odoo, 755)
- [ ] **Odoo restart úspěšný** (status = active)
- [ ] **V logu nejsou Python errory** týkající se czela_uisp
- [ ] **UI: Update Apps List** proběhl
- [ ] **CZELA UISP modul** zobrazuje "Upgrade" tlačítko
- [ ] **Upgrade proběhl** bez chyb
- [ ] **Module state = 'installed'** v databázi
- [ ] **Computed fields fungují** (viz níže)

### Kontrola module state v databázi

```bash
# Na serveru
sudo -u postgres psql

# V PostgreSQL konzoli
\c your_database_name
SELECT name, state, latest_version FROM ir_module_module WHERE name = 'czela_uisp';
\q
```

Očekávaný výstup:
```
    name     |  state    | latest_version
-------------+-----------+----------------
 czela_uisp  | installed | 18.0.1.0.0
```

### Test computed fields

1. Přejdi na **UISP → Devices**
2. Otevři libovolné UISP zařízení, které má MAC adresu
3. Zkontroluj pole:
   - **Network Device:** Mělo by být vyplněno (pokud existuje matching MAC v network_inventory)
   - **Partner:** Mělo by se automaticky vyplnit z Network Device

**Očekávané chování:**
- UISP device s MAC `AA:BB:CC:DD:EE:FF` se automaticky spáruje s network.inventory.device se stejnou MAC
- Partner se automaticky doplní z network device

---

## 🔧 ŘEŠENÍ PROBLÉMŮ

### ❌ Error: "Module network_inventory not found"

**Příčina:** Modul network_inventory není nainstalován.

**Řešení:**
1. V Odoo UI: Apps → Vyhledej "network_inventory"
2. Klikni "Install"
3. Počkej na instalaci
4. Opakuj upgrade CZELA UISP modulu

---

### ❌ Error: "Compute method cannot depend on field 'id'"

**Příčina:** Stará verze modulu s chybou v `res_partner.py`.

**Řešení:**
- Tato chyba byla opravena v commit `6d02b7c`
- Ujisti se, že používáš aktuální ZIP balíček (`czela_uisp_odoo18_complete.zip`)
- Pokud problém přetrvává, zkontroluj soubor `czela_uisp/models/res_partner.py` - metoda `_compute_uisp_device_count` NESMÍ mít `@api.depends('id')`

---

### ❌ Odoo restart selhal

**Symptomy:**
```bash
sudo systemctl status odoo
# Výstup: Active: failed
```

**Řešení:**

1. **Zkontroluj logy:**
   ```bash
   sudo journalctl -u odoo -n 100
   ```

2. **Hledej chybové hlášky:**
   - Python syntax errors
   - Missing dependencies
   - Permission denied errors

3. **Časté příčiny:**
   - Chybějící Python závislosti: `sudo pip3 install requests urllib3`
   - Špatná oprávnění: Opakuj Krok 2 (chown/chmod)
   - Syntax error v kódu: Rollback na předchozí verzi (viz níže)

---

### ❌ Computed fields nefungují

**Symptomy:**
- Network Device field je prázdné i když existuje matching MAC
- Partner field se nevyplňuje

**Možné příčiny:**

1. **network_inventory není nainstalován:**
   - Řešení: Instaluj network_inventory přes UI

2. **MAC adresy se neshodují:**
   - V UISP device: `AA:BB:CC:DD:EE:FF`
   - V network device: `aa-bb-cc-dd-ee-ff`
   - Normalizace by měla fungovat, ale zkontroluj formát

3. **Computed field nebyl přepočítán:**
   ```bash
   # V Odoo UI:
   # Otevři UISP device → Edit → Změň MAC adresu → Save
   # To vynutí přepočítání computed field
   ```

---

## 🔙 ROLLBACK NA PŘEDCHOZÍ VERZI

Pokud aktualizace selže nebo způsobí problémy:

```bash
# Na serveru (SSH)
ssh your_username@is-dev.czela.net

# Odstraň novou verzi
sudo rm -rf /data/is-dev-czela-net/developer-addons/czela_uisp

# Obnov zálohu (nahraď TIMESTAMP skutečným timestampem)
sudo cp -r /data/is-dev-czela-net/developer-addons/czela_uisp_backup_YYYYMMDD_HHMMSS \
     /data/is-dev-czela-net/developer-addons/czela_uisp

# Restartuj Odoo
sudo systemctl restart odoo

# Ověř status
sudo systemctl status odoo
```

**V Odoo UI:**
- Apps → Update Apps List
- Najdi CZELA UISP → Klikni "Upgrade" (pro obnovení předchozího stavu v DB)

---

## 🆕 CO JE NOVÉHO V TÉTO VERZI (18.0.1.0.0)

### 1. Nová závislost: network_inventory

**Před:**
- Modul volitelně kontroloval, zda network_inventory existuje
- Pokud neexistoval, tiše selhal

**Po:**
- `network_inventory` je **povinná závislost**
- Modul nelze nainstalovat bez network_inventory
- Zajištěna konzistence dat

### 2. Automatické párování UISP devices s network devices

**Před:**
- Computed field `_compute_network_device()` neměl `@api.depends`
- Nikdy se automaticky nepřepočítával
- Partner vztahy nefungovaly

**Po:**
- Přidán `@api.depends('mac_address')`
- Při změně MAC adresy se automaticky spáruje s network device
- Partner se automaticky doplní z network device

**Vztahový řetězec:**
```
uisp.device (MAC: AA:BB:CC:DD:EE:FF)
    ↓ _compute_network_device()
network.inventory.device (MAC: AA:BB:CC:DD:EE:FF)
    ↓ _compute_partner_id()
res.partner (Customer)
```

### 3. Odstraněn safety check

**Před:**
```python
if 'network.inventory.device' not in self.env:
    # Tiše selže
    return
```

**Po:**
- Safety check odstraněn
- network_inventory je garantován (díky depends)
- Jednodušší a spolehlivější kód

---

## 📚 Další dokumentace

- [INSTALL_ODOO18.md](INSTALL_ODOO18.md) - Instalace nového modulu
- [DEPLOYMENT.md](DEPLOYMENT.md) - Obecný deployment guide pro is-dev.czela.net
- [QUICK_START.md](QUICK_START.md) - Rychlý start po instalaci
- [README.md](README.md) - Přehled funkcí a konfigurace
- [ODOO18_COMPATIBILITY.md](ODOO18_COMPATIBILITY.md) - Kompatibilita s Odoo 18

---

## 🆘 Pomoc

Pokud narazíš na problém, který není pokryt v tomto průvodci:

1. Zkontroluj Odoo logy: `sudo tail -f /var/log/odoo/odoo-server.log`
2. Zkontroluj systemd logy: `sudo journalctl -u odoo -n 100`
3. Prohledej GitHub Issues: https://github.com/jan362/czela_odoo_uisp/issues
4. Vytvoř nový Issue s:
   - Popisem problému
   - Relevantními logy
   - Kroky k reprodukci

---

**✅ Hotovo!** Modul je aktualizován a připraven k použití.
