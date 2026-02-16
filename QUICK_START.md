# 🚀 Quick Start - CZELA UISP Integration pro Odoo 18

## Rychlá instalace (3 kroky)

### 1️⃣ Upload modulu do Odoo

1. Přihlaste se do Odoo jako **admin**
2. **Apps** → **⋮** → **Upload Module**
3. Nahrajte `czela_uisp_odoo18.zip`
4. Klikněte **Install** u "CZELA UISP Integration"

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
