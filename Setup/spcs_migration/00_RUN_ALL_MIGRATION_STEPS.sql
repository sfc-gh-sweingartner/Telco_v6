-- =============================================================================
-- MASTER MIGRATION SCRIPT: Telco Network Optimization to SPCS
-- =============================================================================
-- This script executes all migration steps in sequence
-- Run this ONLY if you want to execute all steps at once
-- Otherwise, run individual scripts (01, 02, 03) for better control
-- Date: 2025-10-06
-- =============================================================================

-- =============================================================================
-- PREREQUISITES CHECKLIST
-- =============================================================================
-- Before running this script, verify:
-- [ ] You have ACCOUNTADMIN role
-- [ ] TELCO_NETWORK_OPTIMIZATION_PROD database exists
-- [ ] RAW schema exists with CELL_TOWER and SUPPORT_TICKETS tables
-- [ ] TELCO_WH warehouse exists and is running
-- [ ] Your code is deployed to a Snowflake stage (if using Git)
-- [ ] You have reviewed README_SPCS_MIGRATION.md

-- =============================================================================
-- SET CONTEXT
-- =============================================================================

USE ROLE ACCOUNTADMIN;
USE DATABASE TELCO_NETWORK_OPTIMIZATION_PROD;
USE SCHEMA RAW;
USE WAREHOUSE TELCO_WH;

-- =============================================================================
-- STEP 1: CREATE COMPUTE POOL
-- =============================================================================

SELECT '========================================' AS STEP;
SELECT 'STEP 1: CREATING COMPUTE POOL' AS STATUS;
SELECT '========================================' AS STEP;

CREATE COMPUTE POOL IF NOT EXISTS TELCO_STREAMLIT_POOL
  MIN_NODES = 2
  MAX_NODES = 5
  INSTANCE_FAMILY = CPU_X64_XS
  AUTO_RESUME = TRUE
  AUTO_SUSPEND_SECS = 600
  COMMENT = 'Compute pool for Telco Network Optimization Streamlit SPCS apps';

-- Grant usage
GRANT USAGE ON COMPUTE POOL TELCO_STREAMLIT_POOL TO ROLE ACCOUNTADMIN;

-- Verify
SELECT '✓ Compute pool created' AS STATUS;
SHOW COMPUTE POOLS LIKE 'TELCO_STREAMLIT_POOL';

-- Wait for compute pool to become active
SELECT SYSTEM$WAIT(10);

-- =============================================================================
-- STEP 2: CREATE EXTERNAL ACCESS INTEGRATIONS
-- =============================================================================

SELECT '========================================' AS STEP;
SELECT 'STEP 2: CREATING EXTERNAL ACCESS INTEGRATIONS' AS STATUS;
SELECT '========================================' AS STEP;

-- PyPI Network Rule and Integration
CREATE OR REPLACE NETWORK RULE pypi_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = (
    'pypi.org',
    'pypi.python.org',
    'pythonhosted.org',
    'files.pythonhosted.org'
  )
  COMMENT = 'Network rule for PyPI package installation in SPCS';

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION pypi_access_integration
  ALLOWED_NETWORK_RULES = (pypi_network_rule)
  ENABLED = TRUE
  COMMENT = 'External access integration for PyPI package installation';

GRANT USAGE ON INTEGRATION pypi_access_integration TO ROLE ACCOUNTADMIN;

SELECT '✓ PyPI integration created' AS STATUS;

-- Mapbox Network Rule and Integration
CREATE OR REPLACE NETWORK RULE mapbox_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = (
    'api.mapbox.com',
    'a.tiles.mapbox.com',
    'b.tiles.mapbox.com',
    'c.tiles.mapbox.com',
    'd.tiles.mapbox.com'
  )
  COMMENT = 'Network rule for Mapbox map tiles';

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION mapbox_access_integration
  ALLOWED_NETWORK_RULES = (mapbox_network_rule)
  ENABLED = TRUE
  COMMENT = 'External access integration for Mapbox map tiles';

GRANT USAGE ON INTEGRATION mapbox_access_integration TO ROLE ACCOUNTADMIN;

SELECT '✓ Mapbox integration created' AS STATUS;

-- Verify
SHOW EXTERNAL ACCESS INTEGRATIONS;

-- =============================================================================
-- STEP 3: CREATE OR MIGRATE STREAMLIT APP
-- =============================================================================

SELECT '========================================' AS STEP;
SELECT 'STEP 3: CREATING STREAMLIT APP ON SPCS' AS STATUS;
SELECT '========================================' AS STEP;

-- Check for existing Streamlit apps
SELECT 'Checking for existing Streamlit apps...' AS STATUS;
SHOW STREAMLITS IN SCHEMA TELCO_NETWORK_OPTIMIZATION_PROD.RAW;

-- =============================================================================
-- IMPORTANT: Choose ONE of the following options
-- =============================================================================

-- OPTION A: Create new Streamlit app (uncomment if creating new)
-- Recommended if you want to keep old app as backup

/*
CREATE OR REPLACE STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS
  ROOT_LOCATION = '@TELCO_NETWORK_OPTIMIZATION_PROD.RAW.TELCO_APP_STAGE'
  MAIN_FILE = 'main.py'
  RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
  COMPUTE_POOL = TELCO_STREAMLIT_POOL
  QUERY_WAREHOUSE = TELCO_WH
  EXTERNAL_ACCESS_INTEGRATIONS = (
    pypi_access_integration,
    mapbox_access_integration
  )
  COMMENT = 'Telco Network Intelligence Suite running on SPCS - Container Runtime';

-- Add live version
ALTER STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS ADD LIVE VERSION FROM LAST;

SELECT '✓ New SPCS Streamlit app created: TELCO_NETWORK_INTELLIGENCE_SPCS' AS STATUS;
*/

-- OPTION B: Migrate existing app (uncomment and modify)
-- Replace YOUR_EXISTING_APP_NAME with actual name from SHOW STREAMLITS above

/*
ALTER STREAMLIT YOUR_EXISTING_APP_NAME
  SET RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
      COMPUTE_POOL = TELCO_STREAMLIT_POOL
      EXTERNAL_ACCESS_INTEGRATIONS = (
        pypi_access_integration,
        mapbox_access_integration
      );

SELECT '✓ Existing app migrated to SPCS: YOUR_EXISTING_APP_NAME' AS STATUS;
*/

-- =============================================================================
-- VERIFICATION
-- =============================================================================

SELECT '========================================' AS STEP;
SELECT 'VERIFYING MIGRATION' AS STATUS;
SELECT '========================================' AS STEP;

-- Check compute pool
SELECT '--- Compute Pool Status ---' AS INFO;
DESCRIBE COMPUTE POOL TELCO_STREAMLIT_POOL;

-- Check external access integrations
SELECT '--- External Access Integrations ---' AS INFO;
SHOW EXTERNAL ACCESS INTEGRATIONS;

-- Check Streamlit apps
SELECT '--- Streamlit Apps ---' AS INFO;
SHOW STREAMLITS IN SCHEMA TELCO_NETWORK_OPTIMIZATION_PROD.RAW;

-- =============================================================================
-- NEXT STEPS
-- =============================================================================

SELECT '========================================' AS STEP;
SELECT 'MIGRATION COMPLETE!' AS STATUS;
SELECT '========================================' AS STEP;

SELECT 'Next Steps:' AS INFO;
SELECT '1. Uncomment OPTION A or B above to create/migrate your Streamlit app' AS STEP_1;
SELECT '2. Wait 2-5 minutes for container to build on first launch' AS STEP_2;
SELECT '3. Access your app in Snowsight: Projects > Streamlit' AS STEP_3;
SELECT '4. Test all pages, especially maps and AI features' AS STEP_4;
SELECT '5. Monitor compute pool usage and costs' AS STEP_5;

SELECT 'For detailed troubleshooting, see: Setup/spcs_migration/README_SPCS_MIGRATION.md' AS HELP;

-- =============================================================================
-- ROLLBACK (if needed)
-- =============================================================================

/*
-- Uncomment to rollback to warehouse runtime
ALTER STREAMLIT YOUR_APP_NAME
  SET RUNTIME_NAME = 'SYSTEM$WAREHOUSE_RUNTIME';

-- Note: You'll lose SPCS benefits (full cache, latest Streamlit, any PyPI packages)
*/
