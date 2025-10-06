-- =============================================================================
-- Create NEW Streamlit App on SPCS: "Network Optimisation v6"
-- =============================================================================
-- This creates a brand new SPCS app alongside the old warehouse app
-- Date: 2025-10-06
-- =============================================================================

USE ROLE ACCOUNTADMIN;
USE DATABASE TELCO_NETWORK_OPTIMIZATION_PROD;
USE SCHEMA RAW;
USE WAREHOUSE MYWH;

-- =============================================================================
-- Create New SPCS Streamlit App
-- =============================================================================

SELECT 'Creating new SPCS Streamlit app: Network Optimisation v6...' AS STATUS;

-- Create new Streamlit app with SPCS runtime
CREATE STREAMLIT NETWORK_OPTIMISATION_V6
  ROOT_LOCATION = '@"TELCO_NETWORK_OPTIMIZATION_PROD"."RAW"."NETWORK_OPTMISE"/branches/"main"/'
  MAIN_FILE = 'main.py'
  RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
  COMPUTE_POOL = TELCO_STREAMLIT_POOL
  QUERY_WAREHOUSE = MYWH
  EXTERNAL_ACCESS_INTEGRATIONS = (
    pypi_access_integration,
    mapbox_access_integration
  )
  TITLE = 'Network Optimisation v6'
  COMMENT = 'Telco Network Intelligence Suite - SPCS Version';

SELECT '✅ App created successfully!' AS STATUS;

-- Add live version
SELECT 'Adding live version...' AS STATUS;
ALTER STREAMLIT NETWORK_OPTIMISATION_V6 ADD LIVE VERSION FROM LAST;

SELECT '✅ Live version added!' AS STATUS;

-- =============================================================================
-- Verify new app
-- =============================================================================

SELECT 'Verifying new app configuration...' AS STATUS;
DESCRIBE STREAMLIT NETWORK_OPTIMISATION_V6;

-- Show all Streamlit apps
SELECT 'All Streamlit apps in schema:' AS STATUS;
SHOW STREAMLITS IN SCHEMA TELCO_NETWORK_OPTIMIZATION_PROD.RAW;

-- =============================================================================
-- Next Steps
-- =============================================================================

SELECT '✅ NEW APP CREATED: Network Optimisation v6' AS STATUS;
SELECT 'Old app (OMNOPM_OLUQ7ORZM) is still available as backup' AS NOTE;
SELECT 'New app will take 2-5 minutes to build on first launch' AS NOTE;
SELECT 'Access in Snowsight: Projects > Streamlit > "Network Optimisation v6"' AS NOTE;
