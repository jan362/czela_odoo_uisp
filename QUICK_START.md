# 🚀 Quick Start - CZELA UISP Integration pro Odoo 18

⚠️ **DŮLEŽITÉ:** Odoo 18 neumožňuje upload Python modulů přes UI. Použijte manuální instalaci.

## Rychlá instalace (3 kroky)

### 1️⃣ Instalace modulu (manuálně)

> **💡 TIP:** Pro is-dev.czela.net použijte `/data/is-dev-czela-net/developer-addons`

```bash
# Rozbalte ZIP
unzip czela_uisp_odoo18_complete.zip

# Zkopírujte do Odoo addons
sudo cp -r czela_uisp /opt/odoo/custom/addons/

# Restartujte Odoo
sudo systemctl restart odoo

# V Odoo UI: Apps → Update Apps List → Install "CZELA UISP Integration"
```

### 2️⃣ Konfigurace UISP připojení

**Settings → Technical → System Parameters**

Přidejte 3 parametry:

```
uisp.base_url    = https://10.93.9.8
uisp.api_key     = your-api-key-here
uisp.verify_ssl  = false
```

### 3️⃣ Spusťte synchronizaci

**UISP → Synchronization → Sync Now**

✅ Hotovo! Data z UISP jsou nyní v Odoo.

---

## 📖 Kompletní dokumentace

- **INSTALL_ODOO18.md** - Detailní instalační návod
- **README.md** - Úplná dokumentace modulu
- **ODOO18_COMPATIBILITY.md** - Technické detaily kompatibility

---

## ⚡ Klíčové funkce

- ✅ Automatická synchronizace devices (15 min) a sites (1 hod)
- ✅ ČTÚ klasifikace (FTTH/WiFi/FWA)
- ✅ GPS mapové zobrazení
- ✅ Propojení se zákazníky (res.partner)
- ✅ ČTÚ ART252 export

---

**Verze:** 18.0.1.0.0 | **Odoo:** 18.0+ | **Licence:** LGPL-3
