# Troubleshooting Guide

## Common Issues and Solutions

### ImportError: cannot import name 'DAY_IN_SECONDS'

**Error Message:**
```
ImportError: cannot import name 'DAY_IN_SECONDS' from 'snowflake.connector.constants'
```

**Cause:**
This error occurs when Snowflake's Streamlit environment has cached an old version of the code that used `@st.cache_resource` decorator on session initialization functions.

**Solution:**

1. **Clear Streamlit Cache in Snowflake:**
   - Open your Streamlit app in Snowsight
   - Click the three dots menu (⋮) in the top right
   - Select "Settings"
   - Click "Clear Cache"
   - Restart the app

2. **Force Code Refresh:**
   ```sql
   -- Recreate the Streamlit app to force refresh
   ALTER STREAMLIT TELCO_NETWORK_OPTIMIZATION_PROD.RAW.YOUR_APP_NAME
     SET QUERY_TAG = 'refresh';
   ```

3. **Restart the App:**
   - In Snowsight, stop and start the Streamlit app
   - Or refresh your browser with Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)

4. **Verify Latest Code is Deployed:**
   - Check that you're pulling from the correct branch
   - Verify the Git integration is pointing to main branch
   - Check commit hash matches latest: `3b0afe4`

---

## Map Not Displaying

**Problem:** Interactive maps (PyDeck) not showing in Cell Tower Lookup

**Solutions:**

1. **Configure External Access Integration:**
```sql
-- Run connectMapBoxNoKey.sql
USE DATABASE TELCO_NETWORK_OPTIMIZATION_PROD;
USE SCHEMA RAW;

-- Create integration
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION map_access_int
  ALLOWED_NETWORK_RULES = (mapbox_network_rule)
  ENABLED = TRUE;

-- Apply to Streamlit app
ALTER STREAMLIT YOUR_APP_NAME
  SET EXTERNAL_ACCESS_INTEGRATIONS = (map_access_int);
```

2. **Verify Integration:**
```sql
SHOW EXTERNAL ACCESS INTEGRATIONS;
DESC STREAMLIT YOUR_APP_NAME;
```

---

## Data Not Loading / Empty Tables

**Problem:** No data showing in dashboards

**Solutions:**

1. **Verify Tables Exist:**
```sql
USE DATABASE TELCO_NETWORK_OPTIMIZATION_PROD;
USE SCHEMA RAW;

SHOW TABLES;
```

2. **Check Row Counts:**
```sql
SELECT 'CELL_TOWER' AS table_name, COUNT(*) as rows FROM CELL_TOWER
UNION ALL
SELECT 'SUPPORT_TICKETS', COUNT(*) FROM SUPPORT_TICKETS
UNION ALL  
SELECT 'CUSTOMER_LOYALTY', COUNT(*) FROM CUSTOMER_LOYALTY;
```

Expected results:
- CELL_TOWER: ~2.6M rows
- SUPPORT_TICKETS: ~180K rows
- CUSTOMER_LOYALTY: ~thousands of rows

3. **Reload Data:**
```sql
-- Run setup script
@Setup/create_tables.sql
```

---

## Performance Issues / Slow Queries

**Problem:** App is slow or queries timeout

**Solutions:**

1. **Increase Warehouse Size:**
```sql
ALTER WAREHOUSE YOUR_WAREHOUSE SET WAREHOUSE_SIZE = 'MEDIUM';
```

2. **Enable Query Result Caching:**
```sql
ALTER SESSION SET USE_CACHED_RESULT = TRUE;
```

3. **Check Warehouse State:**
```sql
SHOW WAREHOUSES LIKE 'YOUR_WAREHOUSE';
```

4. **Optimize Queries:**
   - Ensure tables are clustered on frequently queried columns
   - Check query history for long-running queries
   - Consider materialized views for complex aggregations

---

## Cortex Search Not Working

**Problem:** Natural language queries not returning results

**Solutions:**

1. **Verify Cortex Search Services:**
```sql
SHOW CORTEX SEARCH SERVICES IN SCHEMA RAW;
```

2. **Resume Services if Suspended:**
```sql
@CortexSearch/resume_cortex_searches.sql
```

3. **Recreate Services:**
```sql
@CortexSearch/create_cortex_searches.sql
```

4. **Check Service Status:**
```sql
SELECT SYSTEM$CORTEX_SEARCH_SERVICE_STATUS(
  'NETWORK_OPTIMISE_SUPPORT_TICKETS_REQUEST'
);
```

---

## AI Features Not Working

**Problem:** AI-powered insights or recommendations not generating

**Solutions:**

1. **Verify Cortex AI is Enabled:**
   - Check your Snowflake edition supports Cortex
   - Verify cross-region inference is enabled (if needed)

2. **Check Model Availability:**
```sql
-- Test Cortex completion
SELECT SNOWFLAKE.CORTEX.COMPLETE(
  'mistral-large',
  'Hello, this is a test. Respond with OK.'
) as test_response;
```

3. **Enable Cross-Region Inference (if needed):**
```sql
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ALL';
```

---

## Page Navigation Issues

**Problem:** Pages not showing in sidebar or navigation broken

**Solutions:**

1. **Check Page Naming Convention:**
   - Files must be in `pages/` directory
   - Prefix with numbers for ordering: `1_Page_Name.py`
   - No special characters in filenames

2. **Verify File Structure:**
```
pages/
├── 0_AI_Insights_and_Recommendations.py
├── 1_Customer_Profile.py
├── 2_Cell_Tower_Lookup.py
└── ...
```

3. **Check Page Configuration:**
   - Each page should have `st.set_page_config()` at the top
   - Ensure no syntax errors in page files

---

## Git Integration Issues

**Problem:** Can't deploy from GitHub or code not updating

**Solutions:**

1. **Verify API Integration:**
```sql
SHOW API INTEGRATIONS LIKE 'git_telco_v4';
```

2. **Recreate Integration:**
```sql
CREATE OR REPLACE API INTEGRATION git_telco_v4
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com/Deepjyoti-ricky/')
  ENABLED = TRUE;
```

3. **Update Streamlit Repository:**
   - In Snowsight, go to Projects > Streamlit
   - Click your app settings
   - Update repository URL if needed
   - Force refresh by recreating the app

---

## Package Import Errors

**Problem:** `ModuleNotFoundError` for packages

**Solutions:**

1. **Add Missing Packages:**
   - In Streamlit editor, click "Packages" dropdown
   - Add: `altair`, `branca`, `h3-py`, `matplotlib`, `numpy`, `pandas`, `plotly`, `pydeck`, `scipy`

2. **Verify requirements.txt:**
   - Check that requirements.txt exists in root
   - Verify package versions are compatible

3. **Restart App:**
   - Changes to packages require app restart
   - Click "Stop" then "Run" in Streamlit editor

---

## Authentication / Permission Errors

**Problem:** Access denied or insufficient privileges

**Solutions:**

1. **Required Roles:**
   - Database: SELECT on all tables
   - Warehouse: USAGE
   - Schema: USAGE
   - Streamlit: OWNERSHIP or USAGE

2. **Grant Permissions:**
```sql
-- For a specific role
GRANT USAGE ON DATABASE TELCO_NETWORK_OPTIMIZATION_PROD TO ROLE YOUR_ROLE;
GRANT USAGE ON SCHEMA RAW TO ROLE YOUR_ROLE;
GRANT SELECT ON ALL TABLES IN SCHEMA RAW TO ROLE YOUR_ROLE;
GRANT USAGE ON WAREHOUSE YOUR_WAREHOUSE TO ROLE YOUR_ROLE;
```

---

## Demo Mode Issues

**Problem:** Live demo not generating data

**Solutions:**

1. **Verify Tasks are Running:**
```sql
SHOW TASKS IN SCHEMA RAW;
SELECT * FROM INFORMATION_SCHEMA.TASK_HISTORY
WHERE SCHEMA_NAME = 'RAW'
ORDER BY SCHEDULED_TIME DESC
LIMIT 10;
```

2. **Start Demo Mode:**
```sql
@Setup/START_DEMO.sql
-- Or manually
CALL MANAGE_DATA_GENERATORS('START');
```

3. **Check Task State:**
```sql
-- Tasks should be in 'started' state
SELECT name, state, schedule 
FROM INFORMATION_SCHEMA.TASKS
WHERE schema_name = 'RAW';
```

---

## Getting Additional Help

If issues persist:

1. **Check Snowflake Status:** https://status.snowflake.com/
2. **Snowflake Documentation:** https://docs.snowflake.com/
3. **Contact:** deepjyoti.dev@snowflake.com
4. **GitHub Issues:** https://github.com/Deepjyoti-ricky/Telco_v4/issues

---

## Debug Mode

Enable debug logging in your Streamlit app:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check Snowflake Query History:
```sql
SELECT *
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE QUERY_TEXT ILIKE '%CELL_TOWER%'
ORDER BY START_TIME DESC
LIMIT 10;
```
