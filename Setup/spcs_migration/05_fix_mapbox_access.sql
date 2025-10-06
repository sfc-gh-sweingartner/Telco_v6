-- =============================================================================
-- Fix Mapbox Access for Background Map Tiles
-- =============================================================================
-- This adds additional hosts needed for map rendering
-- Date: 2025-10-06
-- =============================================================================

USE ROLE ACCOUNTADMIN;
USE DATABASE TELCO_NETWORK_OPTIMIZATION_PROD;
USE SCHEMA RAW;

-- =============================================================================
-- Update Mapbox Network Rule with Additional Hosts
-- =============================================================================

-- Drop and recreate with expanded host list
DROP NETWORK RULE IF EXISTS MAPBOX_NETWORK_RULE;

CREATE NETWORK RULE MAPBOX_NETWORK_RULE
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = (
    -- Mapbox API and tiles
    'api.mapbox.com',
    'events.mapbox.com',
    'a.tiles.mapbox.com',
    'b.tiles.mapbox.com',
    'c.tiles.mapbox.com',
    'd.tiles.mapbox.com',
    -- Mapbox styles and fonts
    'api.mapbox.com:443',
    '*.mapbox.com',
    -- Carto basemaps (alternative, no auth needed)
    'a.basemaps.cartocdn.com',
    'b.basemaps.cartocdn.com',
    'c.basemaps.cartocdn.com',
    'd.basemaps.cartocdn.com',
    'cartodb-basemaps-a.global.ssl.fastly.net',
    'cartodb-basemaps-b.global.ssl.fastly.net',
    'cartodb-basemaps-c.global.ssl.fastly.net',
    'cartodb-basemaps-d.global.ssl.fastly.net',
    -- OpenStreetMap (fallback)
    'a.tile.openstreetmap.org',
    'b.tile.openstreetmap.org',
    'c.tile.openstreetmap.org'
  )
  COMMENT = 'Network rule for Mapbox and Carto map tiles - expanded for PyDeck';

-- Recreate the integration with the updated network rule
DROP EXTERNAL ACCESS INTEGRATION IF EXISTS MAPBOX_ACCESS_INTEGRATION;

CREATE EXTERNAL ACCESS INTEGRATION MAPBOX_ACCESS_INTEGRATION
  ALLOWED_NETWORK_RULES = (MAPBOX_NETWORK_RULE)
  ENABLED = TRUE
  COMMENT = 'External access integration for Mapbox and Carto map tiles';

-- Grant usage
GRANT USAGE ON INTEGRATION MAPBOX_ACCESS_INTEGRATION TO ROLE ACCOUNTADMIN;

-- Verify
SELECT '✅ Updated Mapbox network rule with additional hosts' AS STATUS;
SHOW NETWORK RULES LIKE 'MAPBOX_NETWORK_RULE';
SHOW EXTERNAL ACCESS INTEGRATIONS LIKE 'MAPBOX_ACCESS_INTEGRATION';

-- =============================================================================
-- Important: You must restart your Streamlit app for changes to take effect
-- =============================================================================
SELECT 'Note: Restart your Streamlit app in Snowsight for changes to take effect' AS NOTE;
