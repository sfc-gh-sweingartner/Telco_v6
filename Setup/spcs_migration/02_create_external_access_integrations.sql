-- =============================================================================
-- Streamlit SPCS Migration: Step 2 - Create External Access Integrations
-- =============================================================================
-- This script creates network rules and external access integrations for:
-- 1. PyPI - for installing Python packages
-- 2. Mapbox - for map tiles (already exists, but recreated for SPCS)
-- Date: 2025-10-06
-- Database: TELCO_NETWORK_OPTIMIZATION_PROD
-- =============================================================================

-- Set context
USE ROLE ACCOUNTADMIN;
USE DATABASE TELCO_NETWORK_OPTIMIZATION_PROD;
USE SCHEMA RAW;

-- =============================================================================
-- 1. PyPI Network Rule and Integration (NEW for SPCS)
-- =============================================================================

-- Create network rule for PyPI package installation
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

-- Create external access integration for PyPI
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION pypi_access_integration
  ALLOWED_NETWORK_RULES = (pypi_network_rule)
  ENABLED = TRUE
  COMMENT = 'External access integration for PyPI package installation';

-- Verify PyPI integration
SHOW NETWORK RULES LIKE 'pypi_network_rule';
SHOW EXTERNAL ACCESS INTEGRATIONS LIKE 'pypi_access_integration';

-- =============================================================================
-- 2. Mapbox Network Rule and Integration (for geospatial features)
-- =============================================================================

-- Create network rule for Mapbox tile servers
-- This is needed for pydeck maps and st.map() functionality
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

-- Create external access integration for Mapbox
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION mapbox_access_integration
  ALLOWED_NETWORK_RULES = (mapbox_network_rule)
  ENABLED = TRUE
  COMMENT = 'External access integration for Mapbox map tiles';

-- Verify Mapbox integration
SHOW NETWORK RULES LIKE 'mapbox_network_rule';
SHOW EXTERNAL ACCESS INTEGRATIONS LIKE 'mapbox_access_integration';

-- =============================================================================
-- 3. Grant Privileges
-- =============================================================================

-- Grant usage on PyPI integration
GRANT USAGE ON INTEGRATION pypi_access_integration TO ROLE ACCOUNTADMIN;

-- Grant usage on Mapbox integration  
GRANT USAGE ON INTEGRATION mapbox_access_integration TO ROLE ACCOUNTADMIN;

-- =============================================================================
-- Verification
-- =============================================================================

-- List all external access integrations
SHOW EXTERNAL ACCESS INTEGRATIONS;

-- List all network rules
SHOW NETWORK RULES;

-- =============================================================================
-- Notes:
-- =============================================================================
-- 1. pypi_access_integration is REQUIRED for SPCS to install packages
-- 2. mapbox_access_integration is REQUIRED for geospatial maps to work
-- 3. Both integrations must be assigned to the Streamlit app
-- 4. Without PyPI access, the app will fail to build
-- 5. Without Mapbox access, maps won't render
-- =============================================================================
