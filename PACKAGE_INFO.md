# 📦 Instalační balíčky pro Odoo 18

## Dostupné balíčky

### 1. `czela_uisp_odoo18.zip` (46 KB)
**Minimální instalační balíček**

**Obsah:**
- `czela_uisp/` - kompletní Odoo modul

**Použití:**
- Upload přes Odoo UI (Apps → Upload Module)
- Obsahuje pouze modul bez dokumentace

**Kdy použít:**
- Pro rychlou instalaci přes Odoo webové rozhraní
- Když chcete minimální velikost balíčku

---

### 2. `czela_uisp_odoo18_complete.zip` (56 KB) ⭐ DOPORUČENO
**Kompletní instalační balíček s dokumentací**

**Obsah:**
- `czela_uisp/` - kompletní Odoo modul
- `QUICK_START.md` - rychlý návod (3 kroky)
- `INSTALL_ODOO18.md` - detailní instalační návod
- `README.md` - kompletní dokumentace modulu
- `ODOO18_COMPATIBILITY.md` - technické detaily kompatibility

**Použití:**
1. Rozbalte ZIP
2. Uploadujte složku `czela_uisp/` do Odoo
3. Využijte dokumentaci pro konfiguraci

**Kdy použít:**
- Pro první instalaci (obsahuje veškerou dokumentaci)
- Pro manuální instalaci přes file system
- Když chcete mít dokumentaci offline

---

## 🚀 Rychlá instalace

⚠️ **DŮLEŽITÉ:** Odoo 18 neumožňuje upload Python modulů přes UI.
Musíte použít manuální instalaci přes file system.

### Manuální instalace (jediná metoda pro Odoo 18)

> **💡 TIP:** Pro is-dev.czela.net použijte `/data/is-dev-czela-net/developer-addons`

```bash
# 1. Stáhněte a rozbalte complete balíček
unzip czela_uisp_odoo18_complete.zip

# 2. Zkopírujte modul
cp -r czela_uisp /path/to/odoo/addons/

# 3. Restartujte Odoo
sudo systemctl restart odoo

# 4. Apps → Update Apps List → Install
```

---

## 📋 Co je potřeba po instalaci

### 1. Python závislosti
```bash
pip install requests urllib3
```

### 2. UISP konfigurace
V Odoo: **Settings → Technical → System Parameters**

```
uisp.base_url    = https://your-uisp-server
uisp.api_key     = your-api-key
uisp.verify_ssl  = false
```

### 3. První synchronizace
**UISP → Synchronization → Sync Now**

---

## 🔍 Kontrola instalace

Po instalaci ověřte:

```python
# Odoo shell
odoo-bin shell -d your_database

# Test připojení
result = env['uisp.config.helper'].test_connection()
print(result)
# Expected: {'status': 'success', 'message': '...'}

# Test sync
env['uisp.sync'].sync_devices()
```

---

## 📊 Specifikace modulu

| Vlastnost | Hodnota |
|-----------|---------|
| **Název** | CZELA UISP Integration |
| **Verze** | 18.0.1.0.0 |
| **Odoo verze** | 18.0+ (testováno na 18.0-20251021) |
| **Kategorie** | Operations/Inventory |
| **Licence** | LGPL-3 |
| **Autor** | CZELA |
| **Velikost** | ~46 KB (modul), ~56 KB (s dokumentací) |

---

## 🆕 Co je nového v verzi 18.0.1.0.0

✅ Opraveno chybějící pole `network_device_id`
✅ Modernizace `fields.Datetime.now` → lambda výrazy
✅ Relativní importy místo `sys.path` manipulace
✅ Lazy evaluation v loggingu (lepší performance)
✅ Aktualizovaná verze manifestu na Odoo 18 formát
✅ Kompletní dokumentace pro Odoo 18

---

## 📞 Podpora

**GitHub:** https://github.com/jan362/czela_odoo_uisp
**Issues:** https://github.com/jan362/czela_odoo_uisp/issues

**Dokumentace:**
- `QUICK_START.md` - 3-krokový návod
- `INSTALL_ODOO18.md` - Detailní instalace
- `README.md` - Kompletní dokumentace
- `ODOO18_COMPATIBILITY.md` - Technické detaily

---

**Poslední aktualizace:** 2025-02-16
**Build:** Odoo 18.0-20251021 compatible
