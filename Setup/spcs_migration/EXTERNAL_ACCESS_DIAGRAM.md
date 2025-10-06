# External Access Integrations - Visual Guide

## 🎯 The Big Picture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    TELCO NETWORK INTELLIGENCE                       │
│                      Streamlit SPCS App                             │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ Needs Access To
                              ▼
        ┌─────────────────────────────────────────────┐
        │         TWO EXTERNAL SERVICES               │
        └─────────────────────────────────────────────┘
                │                        │
                │                        │
        ┌───────┴─────────┐     ┌───────┴──────────┐
        │                 │     │                  │
        ▼                 │     ▼                  │
┌─────────────┐          │  ┌──────────────┐     │
│   PyPI      │          │  │   Mapbox     │     │
│ (Build Time)│          │  │  (Runtime)   │     │
└─────────────┘          │  └──────────────┘     │
        │                │          │             │
        │ Requires       │          │ Requires    │
        ▼                │          ▼             │
┌────────────────────────┴───┐ ┌──────────────────┴────┐
│ pypi_access_integration    │ │mapbox_access_integration│
│ ├─ pypi_network_rule       │ │├─ mapbox_network_rule   │
│ │  ├─ pypi.org             │ ││  ├─ api.mapbox.com      │
│ │  ├─ pypi.python.org      │ ││  ├─ a.tiles.mapbox.com  │
│ │  ├─ pythonhosted.org     │ ││  ├─ b.tiles.mapbox.com  │
│ │  └─ files.pythonhosted...│ ││  ├─ c.tiles.mapbox.com  │
└────────────────────────────┘ ││  └─ d.tiles.mapbox.com  │
                                └─────────────────────────┘
```

## 📦 Integration 1: PyPI Access

### Purpose
Install Python packages during container build

### Timeline
```
Container Build Process (2-5 minutes, ONE TIME)
│
├─ [1] Allocate compute pool node
│      ⏱ 10-30 seconds
│
├─ [2] Create Python 3.11 environment
│      ⏱ 30 seconds
│
├─ [3] Download packages from PyPI ← NEEDS pypi_access_integration
│      ⏱ 1-2 minutes
│      │
│      ├─ streamlit>=1.49.0
│      ├─ pandas==2.3.1
│      ├─ numpy==2.2.5
│      ├─ plotly==5.22.0
│      ├─ pydeck==0.9.1
│      ├─ h3-py==3.7.6
│      ├─ matplotlib==3.10.0
│      ├─ branca==0.6.0
│      ├─ scipy==1.15.3
│      └─ altair==5.5.0
│
├─ [4] Install packages with uv
│      ⏱ 1-2 minutes
│
└─ [5] Start Streamlit app
       ⏱ 10 seconds
       ✅ App Ready!
```

### Network Hosts
```
pypi.org               → Main PyPI website
pypi.python.org        → PyPI API endpoint
pythonhosted.org       → Package hosting CDN
files.pythonhosted.org → Package file downloads
```

### What Happens Without It?
```
❌ Container build fails
❌ Error: "Unable to download packages"
❌ App never starts
❌ Users see error page
```

## 🗺️ Integration 2: Mapbox Access

### Purpose
Load map tiles for geospatial visualizations

### Timeline
```
Every Time User Views a Map
│
├─ User clicks "Cell Tower Lookup"
│  ⏱ Page loads instantly
│
├─ Page renders PyDeck map component
│  ⏱ 100ms
│
├─ PyDeck requests map tiles ← NEEDS mapbox_access_integration
│  ⏱ 1-3 seconds
│  │
│  ├─ Request tile for zoom level 8
│  ├─ Request tile for zoom level 9
│  ├─ Request tile for zoom level 10
│  └─ Request tiles for visible area
│
└─ Map renders with tiles
   ⏱ 200ms
   ✅ Map Visible!
```

### Network Hosts
```
api.mapbox.com        → Mapbox API endpoint
a.tiles.mapbox.com    → Tile server A (load balanced)
b.tiles.mapbox.com    → Tile server B (load balanced)
c.tiles.mapbox.com    → Tile server C (load balanced)
d.tiles.mapbox.com    → Tile server D (load balanced)
```

### What Uses Mapbox?
```
📍 Cell Tower Lookup (2_Cell_Tower_Lookup.py)
   └─ PyDeck 3D map with cell tower locations

📍 Geospatial Analysis (3_Geospatial_Analysis.py)
   ├─ st.map() for support ticket heatmap
   └─ H3 hexagon overlays for coverage analysis
```

### What Happens Without It?
```
❌ Maps render as blank white rectangles
❌ Browser console: "Failed to load resource"
❌ Network tab shows 403/blocked for tiles.mapbox.com
❌ Users can't see geographic data
```

## 🔧 How They're Created

### Step 1: Network Rules (Allow Outbound Traffic)
```sql
-- PyPI Network Rule
CREATE NETWORK RULE pypi_network_rule
  MODE = EGRESS                    -- Allow outbound
  TYPE = HOST_PORT                 -- Specify hosts
  VALUE_LIST = (
    'pypi.org',
    'pypi.python.org',
    'pythonhosted.org',
    'files.pythonhosted.org'
  );

-- Mapbox Network Rule
CREATE NETWORK RULE mapbox_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = (
    'api.mapbox.com',
    'a.tiles.mapbox.com',
    'b.tiles.mapbox.com',
    'c.tiles.mapbox.com',
    'd.tiles.mapbox.com'
  );
```

### Step 2: External Access Integrations (Bundle Rules)
```sql
-- PyPI Integration
CREATE EXTERNAL ACCESS INTEGRATION pypi_access_integration
  ALLOWED_NETWORK_RULES = (pypi_network_rule)
  ENABLED = TRUE;

-- Mapbox Integration
CREATE EXTERNAL ACCESS INTEGRATION mapbox_access_integration
  ALLOWED_NETWORK_RULES = (mapbox_network_rule)
  ENABLED = TRUE;
```

### Step 3: Assign to Streamlit App
```sql
CREATE STREAMLIT my_app
  ...
  EXTERNAL_ACCESS_INTEGRATIONS = (
    pypi_access_integration,     -- For build
    mapbox_access_integration    -- For runtime
  );
```

## 🔄 Data Flow Diagrams

### Build Time Flow (PyPI)
```
┌────────────────┐
│ Snowflake      │
│ SPCS Service   │
└────────┬───────┘
         │
         │ 1. Need to install packages
         ▼
┌─────────────────────┐
│ Check External      │
│ Access Integrations │
└──────────┬──────────┘
           │
           │ 2. Found: pypi_access_integration
           ▼
┌──────────────────────┐
│ Check Network Rule:  │
│ pypi_network_rule    │
└──────────┬───────────┘
           │
           │ 3. Allowed hosts:
           │    - pypi.org ✓
           │    - pypi.python.org ✓
           │    - pythonhosted.org ✓
           │    - files.pythonhosted.org ✓
           ▼
┌─────────────────────┐
│ Download packages   │
│ from PyPI           │
└──────────┬──────────┘
           │
           │ 4. Install with uv
           ▼
┌─────────────────────┐
│ ✅ Container Ready  │
└─────────────────────┘
```

### Runtime Flow (Mapbox)
```
┌────────────────┐
│ User's Browser │
└────────┬───────┘
         │
         │ 1. Navigate to Cell Tower Lookup page
         ▼
┌─────────────────────┐
│ Streamlit App       │
│ (in SPCS container) │
└──────────┬──────────┘
           │
           │ 2. Render PyDeck map
           ▼
┌──────────────────────┐
│ PyDeck requests      │
│ map tiles            │
└──────────┬───────────┘
           │
           │ 3. Outbound request to tiles.mapbox.com
           ▼
┌─────────────────────┐
│ Check External      │
│ Access Integrations │
└──────────┬──────────┘
           │
           │ 4. Found: mapbox_access_integration
           ▼
┌──────────────────────┐
│ Check Network Rule:  │
│ mapbox_network_rule  │
└──────────┬───────────┘
           │
           │ 5. Allowed hosts:
           │    - api.mapbox.com ✓
           │    - *.tiles.mapbox.com ✓
           ▼
┌─────────────────────┐
│ Fetch map tiles     │
│ from Mapbox         │
└──────────┬──────────┘
           │
           │ 6. Return tiles to browser
           ▼
┌─────────────────────┐
│ ✅ Map Renders      │
└─────────────────────┘
```

## ❓ Common Questions

### Q: Why can't I use just one integration?

**A:** They serve different purposes at different times:
- **PyPI** = Build time (installing software)
- **Mapbox** = Runtime (loading data)

You need both, even if you think you don't use maps. The app won't build without PyPI, and maps won't work without Mapbox.

### Q: Can I add more integrations later?

**A:** Yes! You can ALTER the Streamlit app to add more:
```sql
ALTER STREAMLIT my_app
  SET EXTERNAL_ACCESS_INTEGRATIONS = (
    pypi_access_integration,
    mapbox_access_integration,
    my_new_api_integration  -- Add more here
  );
```

### Q: Do these cost money?

**A:** The integrations themselves are free. You only pay for:
- Compute pool nodes (regardless of integrations)
- Warehouse query execution (same as before)
- Data egress (if any, minimal for PyPI/Mapbox)

### Q: Can I use my own Mapbox API key?

**A:** Yes, but not required. Streamlit provides default access. If you want to use your own key:
1. Create a SECRET with your API key
2. Add to EXTERNAL_ACCESS_INTEGRATION
3. Configure in app code

But for this demo, the integration alone (no key) is sufficient.

### Q: What if I forget an integration?

**A:** 
- **No PyPI**: Build fails immediately, clear error message
- **No Mapbox**: App starts but maps are blank, network errors in browser console

Easy to fix: Just ALTER the app to add the missing integration.

## 🎯 Validation Checklist

After creating integrations, verify:

```sql
-- ✓ Both integrations exist
SHOW EXTERNAL ACCESS INTEGRATIONS;
-- Should show: pypi_access_integration, mapbox_access_integration

-- ✓ Both are enabled
DESC INTEGRATION pypi_access_integration;
DESC INTEGRATION mapbox_access_integration;
-- Both should show: enabled = true

-- ✓ Network rules exist
SHOW NETWORK RULES;
-- Should show: pypi_network_rule, mapbox_network_rule

-- ✓ App has both integrations
DESC STREAMLIT my_app;
-- Look for: external_access_integrations = both

-- ✓ Can access PyPI (test)
-- Try building the app - should succeed

-- ✓ Can access Mapbox (test)
-- Open Cell Tower Lookup page - maps should load
```

## 📚 Summary

### The Answer to Your Question

**"What do I need to create an external access integration?"**

**TWO integrations:**

1. **pypi_access_integration**
   - 4 hosts (pypi.org, pypi.python.org, pythonhosted.org, files.pythonhosted.org)
   - For: Installing Python packages during build
   - Used: Once during container build
   - Without: App won't start

2. **mapbox_access_integration**
   - 5 hosts (api.mapbox.com, a/b/c/d.tiles.mapbox.com)
   - For: Loading map tiles during runtime
   - Used: Every time a map is displayed
   - Without: Maps are blank

**Both are created by script:** `02_create_external_access_integrations.sql`

**Both are required in app creation:**
```sql
CREATE STREAMLIT my_app
  ...
  EXTERNAL_ACCESS_INTEGRATIONS = (
    pypi_access_integration,    -- ← Must have both
    mapbox_access_integration   -- ← Must have both
  );
```

---

**Still confused?** See `README_SPCS_MIGRATION.md` section "External Access Integration - Detailed Explanation"
