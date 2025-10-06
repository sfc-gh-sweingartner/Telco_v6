# 🚀 Quick Create Guide - "Network Optimisation v6"

## Why Create in UI?
✅ **Snowsight UI handles Git integration and stages automatically**  
❌ SQL creation has issues with source locations for SPCS

---

## ⚡ Quick Steps

### 1️⃣ Create App (2 minutes)
**Snowsight → Projects → Streamlit → + Streamlit App**

```
App title:     Network Optimisation v6
Database:      TELCO_NETWORK_OPTIMIZATION_PROD
Schema:        RAW
Python:        ⭐ Run on container (NOT warehouse!)
Compute pool:  TELCO_STREAMLIT_POOL
Warehouse:     MYWH
```

### 2️⃣ Enable External Access ⭐ CRITICAL!
**App menu (⋮) → App settings → External networks tab**

Enable BOTH:
- ✅ `PYPI_ACCESS_INTEGRATION` (for Python packages)
- ✅ `MAPBOX_ACCESS_INTEGRATION` (for Carto map tiles)

Click **Save**

### 3️⃣ Connect Your Code
- **If Git:** Select repo → main branch → main.py
- **If no Git:** Upload your files

### 4️⃣ Launch & Wait
- Click **Run** or open app
- **Wait 2-5 minutes** for first build
- ✅ Done!

---

## ⚠️ CRITICAL Settings

| Setting | MUST BE | Why |
|---------|---------|-----|
| Python environment | **Run on container** | SPCS requires this |
| Compute pool | `TELCO_STREAMLIT_POOL` | Already created ✅ |
| PyPI integration | **✅ Enabled** | Or build fails! |
| Mapbox integration | **✅ Enabled** | Or Carto maps blank! |

---

## 🎯 What You Already Have Ready

✅ Compute pool: `TELCO_STREAMLIT_POOL` (2 idle nodes)  
✅ PyPI integration: `PYPI_ACCESS_INTEGRATION`  
✅ Carto integration: `MAPBOX_ACCESS_INTEGRATION` (19 tile servers)  
✅ Dependencies: `pyproject.toml` + `requirements.txt`  
✅ All code: `main.py` + pages + utils  
✅ Carto basemaps: Public, no API key required

**Just create the app in UI and connect it!**

---

## 🐛 If Something Goes Wrong

### Can't select "Run on container"
→ Check your account has SPCS access

### Build fails
→ Enable `PYPI_ACCESS_INTEGRATION` in External networks

### Maps blank / no background tiles
→ Enable `MAPBOX_ACCESS_INTEGRATION` in External networks
→ Restart the app after enabling
→ See `MAPBOX_FIX_SUMMARY.md` for troubleshooting

### Can't find compute pool
→ Refresh page or run:
```sql
GRANT USAGE ON COMPUTE POOL TELCO_STREAMLIT_POOL TO ROLE ACCOUNTADMIN;
```

---

## ✨ After It Works

Test these:
1. Maps in Cell Tower Lookup (should show Carto basemap tiles!)
2. Geospatial Analysis maps (light gray background with roads)
3. AI features
4. All pages load
5. H3 hexagon overlays display correctly

Then delete old app:
```sql
DROP STREAMLIT OMNOPM_OLUQ7ORZM;
```

---

**Ready? Go to Snowsight and create it now! Takes ~7 minutes total (2 min create + 5 min first build)**
