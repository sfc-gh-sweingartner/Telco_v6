# SPCS Migration - Quick Reference

##  Quick Start (3 Commands)

```sql
-- 1. Create compute pool
!source 01_create_compute_pool.sql

-- 2. Create external access integrations (PyPI + Mapbox)
!source 02_create_external_access_integrations.sql

-- 3. Create SPCS Streamlit app
!source 03_create_streamlit_app_spcs.sql
```

##  One-Liner Summary

**Migration adds TWO external access integrations:**
1. **`pypi_access_integration`** - Installs Python packages from PyPI
2. **`mapbox_access_integration`** - Loads map tiles for geospatial features

##  The Key Answer: External Access Integrations

### What You Need

| Integration | Purpose | When Used | Without It |
|-------------|---------|-----------|------------|
| **PyPI** | Install packages (streamlit, pandas, plotly, pydeck, etc.) | Container build |  App won't start |
| **Mapbox** | Load map tiles for pydeck/st.map | Runtime (map display) |  Maps show blank |

### Why Both?

```
SPCS App Lifecycle:
┌─────────────────────────────────────────────────┐
│ 1. BUILD TIME (PyPI Integration)                │
│    - Download streamlit>=1.49 from PyPI         │
│    - Download pandas, plotly, pydeck, etc.      │
│    - Build container image                      │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 2. RUNTIME (Mapbox Integration)                 │
│    - User opens Cell Tower Lookup page          │
│    - pydeck requests map tiles                  │
│    - Mapbox serves tiles → map renders          │
└─────────────────────────────────────────────────┘
```

### Network Rules

**PyPI Hosts:**
- `pypi.org` - Main site
- `pypi.python.org` - API
- `pythonhosted.org` - Package hosting
- `files.pythonhosted.org` - Downloads

**Mapbox Hosts:**
- `api.mapbox.com` - API endpoint
- `a.tiles.mapbox.com` - Tile server A
- `b.tiles.mapbox.com` - Tile server B
- `c.tiles.mapbox.com` - Tile server C
- `d.tiles.mapbox.com` - Tile server D

##  Essential Commands

### Check Status
```sql
-- Compute pool
SHOW COMPUTE POOLS LIKE 'TELCO_STREAMLIT_POOL';
DESCRIBE COMPUTE POOL TELCO_STREAMLIT_POOL;

-- External access integrations
SHOW EXTERNAL ACCESS INTEGRATIONS;

-- Streamlit app
SHOW STREAMLITS;
DESCRIBE STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS;
```

### Manage App
```sql
-- Shutdown (free node)
ALTER STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS SHUTDOWN;

-- Check service status
SELECT SYSTEM$GET_SERVICE_STATUS('TELCO_NETWORK_INTELLIGENCE_SPCS');
```

### Revert to Warehouse (if needed)
```sql
ALTER STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS
  SET RUNTIME_NAME = 'SYSTEM$WAREHOUSE_RUNTIME';
```

##  Troubleshooting Checklist

### App Won't Start
- [ ] Compute pool is ACTIVE/IDLE (not ERROR)
- [ ] Both external access integrations exist and are ENABLED
- [ ] `pyproject.toml` exists in ROOT_LOCATION
- [ ] `streamlit>=1.49` in requirements.txt or pyproject.toml
- [ ] QUERY_WAREHOUSE exists and is accessible

### Maps Not Rendering
- [ ] `mapbox_access_integration` in EXTERNAL_ACCESS_INTEGRATIONS
- [ ] Browser console shows no CORS errors
- [ ] `pydeck==0.9.1` installed correctly
- [ ] Network rule includes all Mapbox hosts (a/b/c/d.tiles.mapbox.com)

### Build Failures
- [ ] `pypi_access_integration` exists and is ENABLED
- [ ] Network rule includes all PyPI hosts
- [ ] No conflicting package versions in pyproject.toml
- [ ] All packages support Python 3.11

##  Performance Expectations

| Metric | Expected Value | Notes |
|--------|---------------|-------|
| First startup | 2-5 minutes | Container build + package install |
| Subsequent startups | 10-30 seconds | Cached container |
| Map tile load | 1-3 seconds | Per map, depends on network |
| Query execution | Same as before | Uses warehouse, not compute pool |
| Keep-alive | 3 days | Auto-shutdown after inactivity |

##  Cost Factors

| Resource | Cost Driver | Control |
|----------|-------------|---------|
| Compute Pool | Per-node × time | MIN_NODES, AUTO_SUSPEND_SECS |
| Warehouse | Same as before | Size, auto-suspend |
| Storage | Negligible | Container images cached |

**Recommendation:** Start with MIN_NODES=1 for dev, MIN_NODES=2 for prod

##  File Changes

| File | Change | Required |
|------|--------|----------|
| `pyproject.toml` | **NEW** - Python 3.11 + deps |  Yes |
| `requirements.txt` | Updated - streamlit>=1.49 |  Yes |
| SQL scripts | New migration folder |  Yes |
| `main.py` | No changes | ⬜ No |
| `pages/*.py` | No changes | ⬜ No |
| `utils/*.py` | No changes | ⬜ No |

##  Key Concepts

### Compute Pool vs Warehouse
- **Compute Pool**: Runs Python runtime (Streamlit container)
- **Warehouse**: Executes SQL queries
- **Both needed**: Python runs on pool, SQL on warehouse

### Runtime Name
- **Warehouse**: `SYSTEM$WAREHOUSE_RUNTIME`
- **SPCS**: `SYSTEM$ST_CONTAINER_RUNTIME_PY3_11`
- **Can't change Python version**: Only 3.11 supported

### Dependency Management
- **Preferred**: `pyproject.toml` (SPCS standard)
- **Fallback**: `requirements.txt`
- **Priority**: If both exist, pyproject.toml used first

##  Resources

- Full Guide: `README_SPCS_MIGRATION.md`
- Snowflake Docs: https://docs.snowflake.com/LIMITEDACCESS/streamlit/container-runtime
- Streamlit Docs: https://docs.streamlit.io

---

**TL;DR:** Need TWO integrations (PyPI + Mapbox), run 3 SQL scripts, wait 5 mins, done! 
