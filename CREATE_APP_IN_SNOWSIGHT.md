# ✅ Create "Network Optimisation v6" in Snowsight

**Why through UI?** Snowsight automatically sets up Git integration and stages properly for SPCS apps.

---

## 📋 Step-by-Step Instructions

### 1. Open Snowsight
Navigate to your Snowflake account in browser

### 2. Go to Streamlit Apps
- Click **Projects** in left sidebar
- Click **Streamlit**
- Click **+ Streamlit App** button (top right)

### 3. Configure New App

**Fill in these fields:**

| Field | Value |
|-------|-------|
| **App title** | `Network Optimisation v6` |
| **App location** | |
| └─ Database | `TELCO_NETWORK_OPTIMIZATION_PROD` |
| └─ Schema | `RAW` |
| **Python environment** | **⭐ Run on container** (Critical!) |
| **Compute pool** | `TELCO_STREAMLIT_POOL` |
| **Query warehouse** | `MYWH` |

### 4. Configure Source

**Option A - If you have Git integration:**
- Select your Git repository
- Branch: `main`
- Root folder: (leave default or specify if needed)
- Main file: `main.py`

**Option B - If no Git (upload files):**
- Choose "Upload files"
- You'll upload your code after creation

### 5. Configure External Access ⭐ CRITICAL!

**After creating the app, immediately:**

1. Click the **⋮** (three dots) menu → **App settings**
2. Go to **External networks** tab
3. **Enable BOTH:**
   - ✅ `PYPI_ACCESS_INTEGRATION` (required for packages)
   - ✅ `MAPBOX_ACCESS_INTEGRATION` (required for maps)
4. Click **Save**

### 6. Configure Dependencies

If the app has a code editor, ensure these files exist in root:

**`pyproject.toml`** (exists in your repo ✅)
```toml
[project]
requires-python = "==3.11.*"
dependencies = [
    "streamlit>=1.49.0",
    "pandas==2.3.1",
    "numpy==2.2.5",
    "plotly==5.22.0",
    "pydeck==0.9.1",
    "h3-py==3.7.6",
    "matplotlib==3.10.0",
    "branca==0.6.0",
    "scipy==1.15.3",
    "altair==5.5.0",
]
```

**`requirements.txt`** (exists in your repo ✅)
```
streamlit>=1.49.0
pandas==2.3.1
numpy==2.2.5
# ... (all other dependencies)
```

### 7. First Launch

1. Click **Run** in the editor, or just open the app
2. **Wait 2-5 minutes** for first build:
   - Container builds
   - Python 3.11 environment created
   - Packages install from PyPI
   - App starts
3. ✅ App loads!

### 8. Test

Verify these work:
- [ ] Dashboard loads
- [ ] **Maps display with tiles** (Cell Tower Lookup, Geospatial Analysis)
- [ ] AI features work
- [ ] All pages load

---

## ⚙️ Configuration Checklist

**MUST HAVE for SPCS:**
- ✅ Python environment: **Run on container**
- ✅ Compute pool: `TELCO_STREAMLIT_POOL`
- ✅ External access: **PYPI_ACCESS_INTEGRATION** (critical!)
- ✅ External access: **MAPBOX_ACCESS_INTEGRATION** (for maps!)
- ✅ Main file: `main.py`
- ✅ Dependencies: `pyproject.toml` or `requirements.txt` with streamlit>=1.49

---

## 🎯 Key Settings

### Python Environment
**MUST select:** "Run on container" (not "Run on warehouse")

### Compute Pool
**Use:** `TELCO_STREAMLIT_POOL` (already created ✅)

### External Access Integrations
**Enable BOTH in App Settings → External networks:**
1. `PYPI_ACCESS_INTEGRATION` - Without this, container won't build!
2. `MAPBOX_ACCESS_INTEGRATION` - Without this, maps won't load!

### Query Warehouse
**Use:** `MYWH` (or any warehouse you have)
- This is for SQL queries only, not the Python runtime

---

## 🐛 Common Issues

### Can't see app in Snowsight
- **Fix:** Create through UI, not SQL
- UI handles Git integration automatically

### Container build fails
- **Fix:** Ensure `PYPI_ACCESS_INTEGRATION` is enabled
- Check `pyproject.toml` or `requirements.txt` exists

### Maps are blank
- **Fix:** Enable `MAPBOX_ACCESS_INTEGRATION` in App Settings
- Go to: App menu (⋮) → App settings → External networks

### "Run on container" not available
- **Check:** Compute pool exists and is accessible
- **Check:** Your account has SPCS enabled

---

## 📝 Summary

**Create in Snowsight UI because:**
✅ Handles Git integration automatically  
✅ Creates proper stages and connections  
✅ Better for SPCS apps  
✅ Easier to configure external access  
✅ Visual interface for all settings  

**Critical settings:**
1. **Run on container** (not warehouse)
2. Compute pool: `TELCO_STREAMLIT_POOL`
3. **Enable BOTH external access integrations!**

---

## ✨ After Creation

Once created and running:

1. **Test maps** - Most important! They should show Mapbox tiles
2. **Test AI features** - Should work with Snowflake Cortex
3. **Check performance** - Should be responsive
4. **Verify all pages** - Make sure nothing breaks

Then you can safely delete the old app:
```sql
DROP STREAMLIT OMNOPM_OLUQ7ORZM;  -- After v6 works perfectly
```

---

## 🎉 You're Ready!

**Go to Snowsight now and create your app following these steps!**

The UI will handle everything properly, and your app will be running on SPCS with all the benefits! 🚀
