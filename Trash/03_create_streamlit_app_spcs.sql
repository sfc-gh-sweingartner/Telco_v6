-- =============================================================================
-- Streamlit SPCS Migration: Step 3 - Create Streamlit App on SPCS
-- =============================================================================
-- This script creates the Telco Network Optimization Streamlit app to run
-- on Snowpark Container Services (SPCS) instead of warehouse runtime
-- Date: 2025-10-06
-- Database: TELCO_NETWORK_OPTIMIZATION_PROD
-- =============================================================================

-- Set context
USE ROLE ACCOUNTADMIN;
USE DATABASE TELCO_NETWORK_OPTIMIZATION_PROD;
USE SCHEMA RAW;
USE WAREHOUSE TELCO_WH;

-- =============================================================================
-- Important: Find existing Streamlit app name (if migrating)
-- =============================================================================

-- Run this first to see if you have an existing Streamlit app
SHOW STREAMLITS IN SCHEMA TELCO_NETWORK_OPTIMIZATION_PROD.RAW;

-- If migrating an existing app, note the app name from above
-- You can either DROP the old one or CREATE OR REPLACE

-- =============================================================================
-- Option 1: Create New SPCS Streamlit App (Recommended)
-- =============================================================================

-- Create Streamlit app on SPCS with container runtime
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

-- Add live version from latest code
ALTER STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS ADD LIVE VERSION FROM LAST;

-- =============================================================================
-- Option 2: Migrate Existing App to SPCS (Alternative)
-- =============================================================================

-- Uncomment and modify if migrating an existing app
-- Replace YOUR_EXISTING_APP_NAME with actual name from SHOW STREAMLITS

/*
ALTER STREAMLIT YOUR_EXISTING_APP_NAME
  SET RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
      COMPUTE_POOL = TELCO_STREAMLIT_POOL
      EXTERNAL_ACCESS_INTEGRATIONS = (
        pypi_access_integration,
        mapbox_access_integration
      );
*/

-- =============================================================================
-- Verification
-- =============================================================================

-- Check Streamlit app configuration
SHOW STREAMLITS LIKE 'TELCO_NETWORK_INTELLIGENCE_SPCS';

-- Describe the app to see full configuration
DESCRIBE STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS;

-- Check app status (should show SPCS runtime)
-- Look for: RUNTIME_NAME = SYSTEM$ST_CONTAINER_RUNTIME_PY3_11

-- =============================================================================
-- Access the App
-- =============================================================================

-- The app will be available at:
-- https://<your-account>.snowflakecomputing.com/streamlit/TELCO_NETWORK_OPTIMIZATION_PROD/RAW/TELCO_NETWORK_INTELLIGENCE_SPCS

-- Note: First startup will take 2-5 minutes while container builds and 
-- installs dependencies from pyproject.toml/requirements.txt

-- =============================================================================
-- Monitoring and Management
-- =============================================================================

-- Check compute pool status
SHOW COMPUTE POOLS LIKE 'TELCO_STREAMLIT_POOL';
DESCRIBE COMPUTE POOL TELCO_STREAMLIT_POOL;

-- Check if app is running
SELECT SYSTEM$GET_SERVICE_STATUS('TELCO_NETWORK_INTELLIGENCE_SPCS');

-- Manually shutdown app to free compute pool node
-- (Apps auto-shutdown after 3 days of inactivity)
-- ALTER STREAMLIT TELCO_NETWORK_INTELLIGENCE_SPCS SHUTDOWN;

-- =============================================================================
-- Troubleshooting
-- =============================================================================

-- If app fails to start:
-- 1. Check compute pool has available nodes
-- 2. Verify external access integrations are properly configured
-- 3. Check that pyproject.toml exists in ROOT_LOCATION
-- 4. Verify streamlit >= 1.49 in requirements.txt or pyproject.toml
-- 5. Check app logs in Snowsight
-- 6. Ensure QUERY_WAREHOUSE has proper permissions

-- If maps don't render:
-- 1. Verify mapbox_access_integration is included
-- 2. Check browser console for network errors
-- 3. Verify pydeck version is compatible

-- =============================================================================
-- Notes:
-- =============================================================================
-- 1. RUNTIME_NAME must be 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
-- 2. COMPUTE_POOL is where the Python runtime runs (not queries)
-- 3. QUERY_WAREHOUSE is where SQL queries execute
-- 4. Both PyPI and Mapbox integrations are required
-- 5. Dependencies install from pyproject.toml (preferred) or requirements.txt
-- 6. First launch takes longer due to dependency installation
-- 7. Subsequent launches are faster (cached environment)
-- 8. Each app uses one full node from the compute pool
-- 9. Apps stay running for 3 days after last use (no sleep timer)
-- 10. Python 3.11 is the only supported version for SPCS
-- =============================================================================
