# Telco Network Optimization - SPCS Migration Guide

## Overview

This guide walks through migrating the Telco Network Intelligence Suite from **Warehouse Runtime** to **Snowpark Container Services (SPCS) Runtime** for Streamlit.

## Why Migrate to SPCS?

### Benefits
✅ **Full Streamlit Support** - `st.cache_resource` and `st.cache_data` work perfectly  
✅ **Latest Streamlit** - Use newest versions as soon as they're published on PyPI  
✅ **Any Python Package** - Install any package from PyPI (not limited to Anaconda)  
✅ **Experimental Features** - Access streamlit-nightly for cutting-edge features  
✅ **Long-Running Service** - Faster load times for users (3-day keep-alive)  
✅ **Better Performance** - Single container with persistent state

### Key Differences from Warehouse Runtime

| Feature | Warehouse Runtime | SPCS Container Runtime |
|---------|------------------|----------------------|
| Python Environment | Anaconda channel only | Any PyPI package |
| Streamlit Version | Limited versions | Latest (>=1.49) |
| Cache Support | Limited | Full support |
| Package Management | `requirements.txt` only | `pyproject.toml` + `requirements.txt` |
| Keep-Alive | 15 min (sleep timer) | 3 days |
| Compute | Warehouse | Compute Pool + Warehouse |

## Prerequisites

Before migrating, ensure you have:

1. ✅ **Data Loaded**: CELL_TOWER and SUPPORT_TICKETS tables populated
2. ✅ **ACCOUNTADMIN Role**: Required for creating compute pools and integrations
3. ✅ **Warehouse**: TELCO_WH or similar for query execution
4. ✅ **Git Integration**: Code deployed to Snowflake stage (if using Git)

## Migration Steps

### Step 1: Create Compute Pool

Run: `01_create_compute_pool.sql`

```sql
-- Creates TELCO_STREAMLIT_POOL with 2-5 nodes
-- Each Streamlit app uses one full node
```

**What it does:**
- Creates compute pool with CPU_X64_XS instances
- Configures auto-suspend after 10 minutes of inactivity
- Sets min 2 nodes for fast startup, max 5 for scalability

**Verification:**
```sql
SHOW COMPUTE POOLS LIKE 'TELCO_STREAMLIT_POOL';
-- Status should be IDLE or ACTIVE
```

### Step 2: Create External Access Integrations

Run: `02_create_external_access_integrations.sql`

```sql
-- Creates two integrations:
-- 1. pypi_access_integration - for package installation
-- 2. mapbox_access_integration - for map tiles
```

**What it does:**
- Creates network rules for PyPI and Mapbox
- Creates external access integrations
- Grants necessary privileges

**Why Both Are Required:**
- **PyPI**: SPCS installs packages via uv/pip from PyPI at build time
- **Mapbox**: App uses pydeck and st.map() which need Mapbox tiles

**Verification:**
```sql
SHOW EXTERNAL ACCESS INTEGRATIONS;
-- Should show both pypi_access_integration and mapbox_access_integration
```

### Step 3: Create Streamlit App on SPCS

Run: `03_create_streamlit_app_spcs.sql`

**Option A - Create New App (Recommended):**
```sql
CREATE OR REPLACE STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS
  ROOT_LOCATION = '@TELCO_NETWORK_OPTIMIZATION_PROD.RAW.TELCO_APP_STAGE'
  MAIN_FILE = 'main.py'
  RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
  COMPUTE_POOL = TELCO_STREAMLIT_POOL
  QUERY_WAREHOUSE = TELCO_WH
  EXTERNAL_ACCESS_INTEGRATIONS = (
    pypi_access_integration,
    mapbox_access_integration
  );
```

**Option B - Migrate Existing App:**
```sql
-- First, find your app name
SHOW STREAMLITS;

-- Then migrate it
ALTER STREAMLIT YOUR_EXISTING_APP_NAME
  SET RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
      COMPUTE_POOL = TELCO_STREAMLIT_POOL
      EXTERNAL_ACCESS_INTEGRATIONS = (
        pypi_access_integration,
        mapbox_access_integration
      );
```

**Verification:**
```sql
DESCRIBE STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS;
-- Look for RUNTIME_NAME = SYSTEM$ST_CONTAINER_RUNTIME_PY3_11
```

### Step 4: First Launch

**Initial Startup (2-5 minutes):**
1. Navigate to app in Snowsight (Projects > Streamlit)
2. First launch builds container and installs dependencies
3. Watch progress in Snowsight (shows build logs)
4. Once ready, app loads automatically

**What Happens During First Launch:**
- Container image is created
- Python 3.11 environment is set up
- Dependencies from `pyproject.toml` are installed via uv
- Streamlit app starts

**Subsequent Launches (10-30 seconds):**
- Container is cached
- Dependencies are cached
- Much faster startup

## External Access Integration - Detailed Explanation

### Why Two Integrations?

Your app needs to communicate with **two external services**:

#### 1. PyPI Access (pypi_access_integration)
**Purpose:** Install Python packages during container build  
**Hosts:**
- `pypi.org` - PyPI website
- `pypi.python.org` - PyPI API
- `pythonhosted.org` - Package hosting
- `files.pythonhosted.org` - Package file downloads

**When Used:** Container build time only (not runtime)  
**What Installs:**
- streamlit >= 1.49.0
- pandas, numpy, plotly
- pydeck, h3-py, matplotlib
- All packages from pyproject.toml

**Without This:** ❌ Container build fails, app won't start

#### 2. Mapbox Access (mapbox_access_integration)
**Purpose:** Load map tiles for geospatial visualizations  
**Hosts:**
- `api.mapbox.com` - Mapbox API
- `*.tiles.mapbox.com` - Map tile servers (a/b/c/d subdomains)

**When Used:** Runtime (every time map is displayed)  
**What Uses It:**
- `pydeck` maps in Cell Tower Lookup
- `st.map()` in Geospatial Analysis
- H3 hexagon overlays

**Without This:** ❌ Maps show blank, no tiles load

### How They Work Together

```
App Startup Flow:
1. Compute pool allocates node
2. PyPI integration downloads packages → Container builds
3. App starts on container
4. User views page with map
5. Mapbox integration loads tiles → Map renders
```

## File Structure for SPCS

### Required Files

```
Telco_v6/
├── main.py                    # Entry point (MAIN_FILE)
├── pyproject.toml             # NEW: Python 3.11 + dependencies
├── requirements.txt           # Updated: streamlit>=1.49.0
├── pages/                     # Multi-page app
│   ├── 0_AI_Insights_and_Recommendations.py
│   ├── 1_Customer_Profile.py
│   ├── 2_Cell_Tower_Lookup.py
│   └── ...
└── utils/                     # Utility modules
    ├── design_system.py
    └── aisql_functions.py
```

### pyproject.toml (NEW)
Primary dependency management for SPCS:
- Specifies Python 3.11
- Lists all dependencies
- Preferred over requirements.txt for SPCS

### requirements.txt (Updated)
Fallback for dependencies:
- Updated to require streamlit>=1.49.0
- SPCS uses pyproject.toml first, then requirements.txt

## Monitoring and Management

### Check App Status
```sql
-- View all Streamlit apps
SHOW STREAMLITS;

-- Check specific app
DESCRIBE STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS;

-- Check service status
SELECT SYSTEM$GET_SERVICE_STATUS('TELCO_NETWORK_INTELLIGENCE_SPCS');
```

### Check Compute Pool
```sql
-- View compute pools
SHOW COMPUTE POOLS;

-- Check pool status
DESCRIBE COMPUTE POOL TELCO_STREAMLIT_POOL;

-- See which apps are using nodes
SELECT * FROM TABLE(
  INFORMATION_SCHEMA.COMPUTE_POOL_STATUS('TELCO_STREAMLIT_POOL')
);
```

### Manual Shutdown
```sql
-- Free up compute pool node
ALTER STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS SHUTDOWN;

-- Note: App will auto-restart on next access
```

## Troubleshooting

### App Won't Start

**Symptom:** Container fails to build or app shows error

**Solutions:**

1. **Check Compute Pool**
```sql
DESCRIBE COMPUTE POOL TELCO_STREAMLIT_POOL;
-- Ensure status is ACTIVE or IDLE, not ERROR
```

2. **Verify External Access Integrations**
```sql
SHOW EXTERNAL ACCESS INTEGRATIONS;
-- Both pypi_access_integration and mapbox_access_integration should exist
```

3. **Check Dependencies**
- Ensure `pyproject.toml` exists in root
- Verify streamlit >= 1.49 specified
- Check for conflicting package versions

4. **Review Logs**
- Open app in Snowsight
- Check build logs for error messages
- Look for package installation failures

### Maps Not Displaying

**Symptom:** Blank maps, no tiles loading

**Solutions:**

1. **Verify Mapbox Integration**
```sql
DESCRIBE STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS;
-- Check EXTERNAL_ACCESS_INTEGRATIONS includes mapbox_access_integration
```

2. **Check Browser Console**
- Open browser DevTools (F12)
- Look for network errors to `*.tiles.mapbox.com`
- Check for CORS or connection errors

3. **Verify pydeck Version**
```python
# In app, check installed version
import pydeck
print(pydeck.__version__)  # Should be 0.9.1
```

### Slow Performance

**Symptom:** App takes long to load or respond

**Solutions:**

1. **Check Warehouse Size**
```sql
-- Queries run on warehouse, not compute pool
SHOW WAREHOUSES LIKE 'TELCO_WH';
-- Consider resizing if queries are slow
```

2. **Check Compute Pool**
```sql
-- Ensure pool has available nodes
DESCRIBE COMPUTE POOL TELCO_STREAMLIT_POOL;
-- Consider increasing MIN_NODES if startup is slow
```

3. **Optimize Queries**
- Add `@st.cache_data` to expensive queries
- Use `@st.cache_resource` for persistent objects
- Review query execution plans

### Dependency Installation Fails

**Symptom:** Build fails with package error

**Solutions:**

1. **Check PyPI Integration**
```sql
SHOW EXTERNAL ACCESS INTEGRATIONS LIKE 'pypi_access_integration';
-- Verify it's ENABLED
```

2. **Verify Network Rule**
```sql
SHOW NETWORK RULES LIKE 'pypi_network_rule';
-- Check all PyPI hosts are listed
```

3. **Check Package Compatibility**
- Ensure all packages support Python 3.11
- Check for platform-specific dependencies
- Review package version conflicts

## Cost Considerations

### Compute Pool Costs
- **Per-node pricing** based on instance family (CPU_X64_XS)
- **Auto-suspend** after 10 minutes saves costs
- **Consider MIN_NODES** carefully (more nodes = faster startup but higher minimum cost)

### Warehouse Costs
- **Queries still run on warehouse** (not compute pool)
- **Warehouse size** affects query performance and cost
- **Auto-suspend** on warehouse recommended

### Best Practices
- Set `MIN_NODES = 1` for dev/test environments
- Set `MIN_NODES = 2+` for production (faster startup)
- Use `AUTO_SUSPEND_SECS = 600` to balance availability and cost
- Monitor usage with `QUERY_HISTORY` and `COMPUTE_POOL_HISTORY`

## Migration Checklist

- [ ] Step 1: Create compute pool
- [ ] Step 2: Create external access integrations (PyPI + Mapbox)
- [ ] Step 3: Create or migrate Streamlit app to SPCS
- [ ] Step 4: Verify app starts successfully
- [ ] Step 5: Test all pages load correctly
- [ ] Step 6: Verify maps render with tiles
- [ ] Step 7: Test AI features and queries
- [ ] Step 8: Validate data loads from tables
- [ ] Step 9: Check performance and response times
- [ ] Step 10: Update documentation with new app URL

## Reverting to Warehouse Runtime

If you need to revert (not recommended):

```sql
ALTER STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS
  SET RUNTIME_NAME = 'SYSTEM$WAREHOUSE_RUNTIME';
```

**Note:** You'll lose:
- Full cache support
- Latest Streamlit features
- Any PyPI packages
- Long-running service benefits

## Support and Resources

### Documentation
- [Snowflake SPCS Streamlit Docs](https://docs.snowflake.com/LIMITEDACCESS/streamlit/container-runtime)
- [Streamlit Documentation](https://docs.streamlit.io)
- [PyPI Package Index](https://pypi.org)

### Internal Resources
- TROUBLESHOOTING.md - Common issues and solutions
- README.md - General project documentation
- Setup/connectMapBoxNoKey.sql - Original Mapbox setup

### Questions?
Refer to the Snowflake documentation or consult with your Snowflake account team.

---

**Last Updated:** October 6, 2025  
**Version:** 1.0 - Initial SPCS Migration
