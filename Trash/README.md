# 🗑️ Trash Folder

This folder contains obsolete files that are no longer needed but kept for reference.

## Files in this folder

### Old Mapbox Setup (Warehouse Runtime)
- **`mapbox_access_setup.sql`** - Original Mapbox integration for warehouse-based Streamlit
- **`connectMapBoxNoKey.sql`** - Mapbox configuration without API key for warehouse runtime

**Why obsolete?** 
- These were for the old warehouse-based Streamlit runtime
- SPCS uses a different external access integration approach
- We now use **Carto basemaps** (public, no auth) instead of Mapbox

### Old SQL-Based App Creation Scripts
- **`00_RUN_ALL_MIGRATION_STEPS.sql`** - Master migration script that tried to automate everything
- **`03_create_streamlit_app_spcs.sql`** - SQL script to create SPCS app
- **`03_migrate_existing_app.sql`** - SQL script to migrate existing app
- **`04_create_new_app_v6.sql`** - SQL script to create new versioned app

**Why obsolete?**
- Creating SPCS Streamlit apps via SQL doesn't work well
- The UI doesn't show SQL-created apps properly
- Git integration and stage setup isn't handled correctly via SQL
- **Must use Snowsight UI** for SPCS app creation (works perfectly!)

### Old Migration Documentation
- **`MIGRATION_COMPLETED.md`** - Early migration documentation that's now outdated

**Why obsolete?**
- Process has been refined and improved
- New documentation is more accurate and complete
- See `CREATE_APP_IN_SNOWSIGHT.md` and `QUICK_CREATE_GUIDE.md` instead

## Current Approach

### For Deployment:
✅ Use Snowsight UI to create SPCS apps  
✅ Use Carto basemaps (no auth needed)  
✅ Use external access integrations for PyPI and Carto  

### Documentation to Use:
- `CREATE_APP_IN_SNOWSIGHT.md` - Complete step-by-step guide
- `QUICK_CREATE_GUIDE.md` - Quick reference
- `Setup/spcs_migration/01_create_compute_pool.sql` - Create compute pool
- `Setup/spcs_migration/02_create_external_access_integrations.sql` - Create integrations
- `Setup/spcs_migration/05_fix_mapbox_access.sql` - Final network rule with Carto

## Should I Delete These?

**No** - Keep them for:
- Historical reference
- Understanding what didn't work
- Learning from the evolution
- Potential future use cases

If you need to restore disk space, these files can be safely deleted.

---

**Last Updated**: October 6, 2025  
**Reason for Archive**: Migration to SPCS with UI-based deployment and Carto basemaps

