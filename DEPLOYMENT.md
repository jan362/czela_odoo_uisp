# 🚀 Deployment na is-dev.czela.net

## Metoda 1: Manualni instalace pres SSH (Doporuceno)

### Pozadavky

- SSH pristup na is-dev.czela.net
- Uzivatelske ucto s sudo opravnenimi

### Krok za krokem

```bash
# 1. Pripojte se na server
ssh your_username@is-dev.czela.net

# 2. Presunete se do /tmp
cd /tmp

# 3. Nahrajte ZIP soubor (pres SCP/WinSCP)
# Z lokalniho PC:
scp czela_uisp_odoo18_complete.zip your_username@is-dev.czela.net:/tmp/

# 4. Rozbalte ZIP
cd /tmp
unzip czela_uisp_odoo18_complete.zip

# 5. Vytvorte zalohu (pokud modul uz existuje)
sudo cp -r /data/is-dev-czela-net/developer-addons/czela_uisp \
     /data/is-dev-czela-net/developer-addons/czela_uisp_backup_$(date +%Y%m%d_%H%M%S)

# 6. Smazte stary modul
sudo rm -rf /data/is-dev-czela-net/developer-addons/czela_uisp

# 7. Zkopiruejte novy modul
sudo cp -r czela_uisp /data/is-dev-czela-net/developer-addons/

# 8. Nastavte spravna opravneni
sudo chown -R odoo:odoo /data/is-dev-czela-net/developer-addons/czela_uisp
sudo chmod -R 755 /data/is-dev-czela-net/developer-addons/czela_uisp

# 9. Instalujte Python zavislosti
sudo pip3 install requests urllib3

# 10. Restartujte Odoo
sudo systemctl restart odoo

# 11. Zkontrolujte status
sudo systemctl status odoo

# 12. Sledujte logy
sudo tail -f /var/log/odoo/odoo-server.log
```

---

## Metoda 2: Deployment pres WinSCP + SSH

### 1. Nahrani souboru pres WinSCP

```
1. Otevrete WinSCP
2. Pripojte se na is-dev.czela.net
3. Nahrajte czelauisp / do /tmp/
```

### 2. Instalace pres SSH

Pouzijte prikazy z Metody 1, krok 5-12.

---

## Po Deploymentu - Aktivace v Odoo

### 1. Prihlaste se do Odoo

```
https://is-dev.czela.net
Username: admin
Password: ***
```

### 2. Aktualizujte seznam aplikaci

```
Apps → ⋮ (tri tecky vpravo nahore) → Update Apps List
```

### 3. Nainstalujte modul

```
Apps → Vyhledejte "CZELA UISP" → Install
```

### 4. Nakonfigurujte UISP pripojeni

```
Settings → Technical → System Parameters

Pridejte tyto parametry:

Key: uisp.base_url
Value: https://10.93.9.8

Key: uisp.api_key
Value: your-api-key-here

Key: uisp.verify_ssl
Value: false
```

### 5. Spustte prvni synchronizaci

```
UISP → Synchronization → Sync Now
```

### 6. Aktivujte automatickou synchronizaci

```
Settings → Technical → Automation → Scheduled Actions

Aktivujte:
- "UISP: Sync Devices" (kazdych 15 min)
- "UISP: Sync Sites" (kazdou hodinu)
```

---

## Reseni problemu

### Modul neni videt v Apps

```bash
# Zkontrolujte addons_path
ssh your_username@is-dev.czela.net
sudo cat /etc/odoo/odoo.conf | grep addons_path

# Melo by obsahovat: /data/is-dev-czela-net/developer-addons

# Pokud ne, pridejte:
sudo nano /etc/odoo/odoo.conf

# Pridejte do addons_path:
# addons_path = /usr/lib/python3/dist-packages/odoo/addons,/data/is-dev-czela-net/developer-addons

# Restartujte
sudo systemctl restart odoo
```

### Permission denied

```bash
# Opravte opravneni
sudo chown -R odoo:odoo /data/is-dev-czela-net/developer-addons/czela_uisp
sudo chmod -R 755 /data/is-dev-czela-net/developer-addons/czela_uisp
```

### ModuleNotFoundError: requests

```bash
# Instalujte Python zavislosti
sudo pip3 install requests urllib3
```

### Odoo se nespusti po deploymentu

```bash
# Zkontrolujte logy
sudo tail -f /var/log/odoo/odoo-server.log

# Rollback na zalohu
sudo rm -rf /data/is-dev-czela-net/developer-addons/czela_uisp
sudo mv /data/is-dev-czela-net/developer-addons/czela_uisp_backup_* \
     /data/is-dev-czela-net/developer-addons/czela_uisp
sudo systemctl restart odoo
```

---

## Rollback

### Vraceni na predchozi verzi

```bash
ssh your_username@is-dev.czela.net

# Najdete posledni zalohu
ls -lt /data/is-dev-czela-net/developer-addons/ | grep czela_uisp_backup

# Obnovte zalohu
sudo rm -rf /data/is-dev-czela-net/developer-addons/czela_uisp
sudo cp -r /data/is-dev-czela-net/developer-addons/czela_uisp_backup_20250216_083000 \
     /data/is-dev-czela-net/developer-addons/czela_uisp

# Restartujte
sudo systemctl restart odoo
```

---

## Monitoring

### Kontrola stavu modulu

```bash
# SSH pripojeni
ssh your_username@is-dev.czela.net

# Status Odoo
sudo systemctl status odoo

# Live logy
sudo tail -f /var/log/odoo/odoo-server.log | grep -i czela

# Kontrola instalace modulu v DB
sudo -u postgres psql
\c your_database
SELECT name, state FROM ir_module_module WHERE name = 'czela_uisp';
\q
```

---

## 📞 Podpora

**Deployment problemy:**
- Zkontrolujte logy: `/var/log/odoo/odoo-server.log`
- GitHub Issues: https://github.com/jan362/czela_odoo_uisp/issues

**Server pristup:**
- Kontaktujte CZELA IT tym pro SSH pristup

---

**Posledni aktualizace:** 2025-02-16
**Cilovy server:** is-dev.czela.net
**Odoo verze:** 18.0
**Addons cesta:** `/data/is-dev-czela-net/developer-addons`
