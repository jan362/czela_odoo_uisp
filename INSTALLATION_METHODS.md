# 📦 Metody instalace pro Odoo 18

⚠️ **DŮLEŽITÉ UPOZORNĚNÍ**

Odoo 18 **NEUMOŽŇUJE** upload Python modulů přes webové rozhraní (Apps → Upload Module).
Chybová hláška: *"Můžete importovat pouze datové moduly (soubory XML a statické prostředky)"*

**Všechny instalace musí probíhat manuálně přes file system.**

---

## 📋 Přehled metod

| Metoda | Platforma | Obtížnost | Čas |
|--------|-----------|-----------|-----|
| [Linux Server](#metoda-1-linux-server-standardní-instalace) | Linux | Snadná | 5 min |
| [Windows Server](#metoda-2-windows-server) | Windows | Střední | 10 min |
| [Docker](#metoda-3-docker) | Linux/Win/Mac | Snadná | 5 min |
| [Odoo.sh](#metoda-4-odoo-sh-cloud) | Cloud | Snadná | 3 min |
| [Development](#metoda-5-development-vývojářský-režim) | Linux/Win | Snadná | 5 min |

---

## Metoda 1: Linux Server (Standardní instalace)

> **📌 NOTE pro is-dev.czela.net:**
> Na serveru is-dev.czela.net použijte cestu:
> `/data/is-dev-czela-net/developer-addons`
> místo `/opt/odoo/custom/addons`

### Krok za krokem

```bash
# 1. Přihlaste se jako root nebo použijte sudo
ssh user@your-server

# 2. Stáhněte balíček (nebo nahrajte přes SCP/FTP)
wget https://github.com/jan362/czela_odoo_uisp/releases/download/v18.0.1.0.0/czela_uisp_odoo18_complete.zip
# NEBO
scp czela_uisp_odoo18_complete.zip user@server:/tmp/

# 3. Rozbalte
cd /tmp
unzip czela_uisp_odoo18_complete.zip

# 4. Najděte Odoo addons cestu
# Zkontrolujte /etc/odoo/odoo.conf, hledejte řádek "addons_path"
cat /etc/odoo/odoo.conf | grep addons_path
# Výsledek např: addons_path = /usr/lib/python3/dist-packages/odoo/addons,/opt/odoo/custom/addons

# 5. Zkopírujte modul do CUSTOM addons (doporučeno)
sudo cp -r czela_uisp /opt/odoo/custom/addons/

# 6. Nastavte správná oprávnění
sudo chown -R odoo:odoo /opt/odoo/custom/addons/czela_uisp
sudo chmod -R 755 /opt/odoo/custom/addons/czela_uisp

# 7. Instalujte Python závislosti
sudo pip3 install requests urllib3

# 8. Restartujte Odoo
sudo systemctl restart odoo
# NEBO
sudo service odoo restart

# 9. Zkontrolujte logy pro chyby
sudo tail -f /var/log/odoo/odoo-server.log
```

### V Odoo UI

1. Přihlaste se jako **administrátor**
2. **Apps** → Klikněte na **⋮** (tři tečky vpravo nahoře)
3. **Update Apps List**
4. Vyhledejte: **"CZELA UISP"**
5. Klikněte **Install**

---

## Metoda 2: Windows Server

### Krok za krokem

```powershell
# 1. Otevřete PowerShell jako Administrator

# 2. Rozbalte ZIP (nebo použijte Windows Explorer)
Expand-Archive -Path "C:\Downloads\czela_uisp_odoo18_complete.zip" -DestinationPath "C:\temp\"

# 3. Najděte Odoo addons cestu
# Zkontrolujte C:\Program Files\Odoo 18\server\odoo.conf
# Nebo: C:\odoo\server\odoo.conf
notepad "C:\Program Files\Odoo 18\server\odoo.conf"
# Hledejte řádek: addons_path = ...

# 4. Zkopírujte modul do custom addons
# Obvykle: C:\Program Files\Odoo 18\server\odoo\addons
# Nebo: C:\odoo\custom\addons
Copy-Item -Path "C:\temp\czela_uisp" -Destination "C:\Program Files\Odoo 18\server\odoo\addons\" -Recurse

# 5. Instalujte Python závislosti
# Najděte Python v Odoo instalaci
cd "C:\Program Files\Odoo 18\python"
.\python.exe -m pip install requests urllib3

# 6. Restartujte Odoo službu
Restart-Service -Name "odoo-server-18.0"
# NEBO přes Services.msc GUI

# 7. Zkontrolujte logy
# C:\Program Files\Odoo 18\server\odoo.log
```

### V Odoo UI

1. Otevřete prohlížeč: `http://localhost:8069`
2. Přihlaste se jako admin
3. **Apps → Update Apps List**
4. Vyhledejte a instalujte **"CZELA UISP Integration"**

---

## Metoda 3: Docker

### Varianta A: Volume mount (Doporučeno)

```bash
# 1. Rozbalte ZIP
unzip czela_uisp_odoo18_complete.zip

# 2. Zkopírujte do custom addons volume
# Pokud používáte docker-compose s volume:
docker cp czela_uisp odoo:/mnt/extra-addons/

# 3. Nastavte oprávnění (pokud potřeba)
docker exec -u root odoo chown -R odoo:odoo /mnt/extra-addons/czela_uisp

# 4. Instalujte závislosti v containeru
docker exec -it odoo pip install requests urllib3

# 5. Restartujte container
docker restart odoo

# 6. Update Apps List v UI a instalujte
```

### Varianta B: Rebuild image

```dockerfile
# Přidejte do Dockerfile
FROM odoo:18.0

# Zkopírujte custom modul
COPY ./czela_uisp /mnt/extra-addons/czela_uisp

# Instalujte závislosti
RUN pip install requests urllib3

USER odoo
```

```bash
# Build a spusťte
docker build -t odoo-czela:18.0 .
docker-compose up -d
```

### docker-compose.yml příklad

```yaml
version: '3.8'
services:
  odoo:
    image: odoo:18.0
    ports:
      - "8069:8069"
    volumes:
      - ./addons:/mnt/extra-addons
      - odoo-data:/var/lib/odoo
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=odoo
volumes:
  odoo-data:
```

```bash
# Zkopírujte modul do ./addons/
cp -r czela_uisp ./addons/

# Restartujte
docker-compose restart odoo
```

---

## Metoda 4: Odoo.sh (Cloud)

### Instalace přes Git

```bash
# 1. Připojte se k vašemu Odoo.sh repository
git clone git@github.com:odoo/your-instance.git
cd your-instance

# 2. Zkopírujte modul do addons/
cp -r czela_uisp addons/

# 3. Přidejte do requirements.txt (pokud existuje)
echo "requests" >> requirements.txt
echo "urllib3" >> requirements.txt

# 4. Commit a push
git add addons/czela_uisp
git add requirements.txt
git commit -m "Add CZELA UISP Integration module"
git push origin main

# 5. Odoo.sh automaticky nasadí změny
# Sledujte build v Odoo.sh dashboardu

# 6. Po deployi: Apps → Update Apps List → Install
```

---

## Metoda 5: Development (Vývojářský režim)

### Pro vývoj a testování

```bash
# 1. Klonujte nebo rozbalte modul
unzip czela_uisp_odoo18_complete.zip

# 2. Spusťte Odoo s --addons-path
odoo-bin \
  --addons-path=/path/to/odoo/addons,/path/to/czela_uisp \
  --database=test_db \
  --db-filter=test_db \
  --dev=all

# 3. V prohlížeči: http://localhost:8069
# Apps → Update Apps List → Install
```

### S virtualenv

```bash
# 1. Vytvořte virtualenv
python3 -m venv odoo-venv
source odoo-venv/bin/activate

# 2. Instalujte Odoo a závislosti
pip install odoo
pip install requests urllib3

# 3. Spusťte Odoo
odoo --addons-path=./czela_uisp,./odoo/addons
```

---

## 🔍 Ověření instalace

### Po instalaci zkontrolujte:

```bash
# 1. Zkontrolujte, že soubory jsou na místě
ls -la /opt/odoo/custom/addons/czela_uisp/

# 2. Zkontrolujte oprávnění
ls -l /opt/odoo/custom/addons/ | grep czela_uisp
# Mělo by být: drwxr-xr-x odoo odoo

# 3. Zkontrolujte Python import
python3 -c "import requests; import urllib3; print('OK')"

# 4. Zkontrolujte Odoo logy
sudo tail -f /var/log/odoo/odoo-server.log | grep -i czela
# Neměly by být žádné ERROR zprávy

# 5. V Odoo UI zkontrolujte Apps
# Měl by být vidět "CZELA UISP Integration"
```

---

## ❌ Řešení problémů

### Modul není vidět v Apps

**Problém:** Po restartu modul není v seznamu Apps

**Řešení:**
```bash
# 1. Zkontrolujte addons_path v config
cat /etc/odoo/odoo.conf | grep addons_path

# 2. Ověřte, že cesta k modulu je v addons_path
# Pokud ne, přidejte:
sudo nano /etc/odoo/odoo.conf
# addons_path = /usr/lib/.../odoo/addons,/opt/odoo/custom/addons

# 3. Restartujte
sudo systemctl restart odoo

# 4. Update Apps List (klikněte na ⋮ v Apps)
```

### Permission denied

**Problém:** Chyba při načítání modulu - oprávnění

**Řešení:**
```bash
# Nastavte správného vlastníka a oprávnění
sudo chown -R odoo:odoo /opt/odoo/custom/addons/czela_uisp
sudo chmod -R 755 /opt/odoo/custom/addons/czela_uisp
```

### ModuleNotFoundError: requests

**Problém:** Python závislosti chybí

**Řešení:**
```bash
# Instalujte do Odoo Python prostředí
sudo -H -u odoo pip3 install requests urllib3

# NEBO pro virtualenv
source /path/to/odoo-venv/bin/activate
pip install requests urllib3
```

---

## 📞 Potřebujete pomoc?

**Dokumentace:**
- `QUICK_START.md` - Rychlý návod
- `INSTALL_ODOO18.md` - Detailní instalace
- `README.md` - Kompletní dokumentace

**GitHub:** https://github.com/jan362/czela_odoo_uisp/issues

---

**Poslední aktualizace:** 2025-02-16
**Verze:** 18.0.1.0.0
