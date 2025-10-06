-- =============================================================================
-- Migrate Existing Streamlit App to SPCS
-- =============================================================================
-- App: OMNOPM_OLUQ7ORZM (Network Optimisation)
-- Generated: 2025-10-06
-- =============================================================================

USE ROLE ACCOUNTADMIN;
USE DATABASE TELCO_NETWORK_OPTIMIZATION_PROD;
USE SCHEMA RAW;
USE WAREHOUSE MYWH;

-- =============================================================================
-- Migrate existing app to SPCS Container Runtime
-- =============================================================================

SELECT 'Migrating app OMNOPM_OLUQ7ORZM to SPCS...' AS STATUS;

-- Migrate to SPCS runtime
ALTER STREAMLIT OMNOPM_OLUQ7ORZM
  SET RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
      COMPUTE_POOL = TELCO_STREAMLIT_POOL
      EXTERNAL_ACCESS_INTEGRATIONS = (
        pypi_access_integration,
        mapbox_access_integration
      );

SELECT '✅ Migration complete!' AS STATUS;

-- =============================================================================
-- Verify migration
-- =============================================================================

SELECT 'Verifying app configuration...' AS STATUS;
DESCRIBE STREAMLIT OMNOPM_OLUQ7ORZM;

SELECT 'App is now running on SPCS!' AS STATUS;
SELECT 'First startup will take 2-5 minutes to build container and install packages.' AS NOTE;
SELECT 'Subsequent launches will be much faster (10-30 seconds).' AS NOTE;
