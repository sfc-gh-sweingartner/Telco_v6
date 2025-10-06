-- =============================================================================
-- Streamlit SPCS Migration: Step 1 - Create Compute Pool
-- =============================================================================
-- This script creates a compute pool for running Streamlit apps on containers
-- Date: 2025-10-06
-- Database: TELCO_NETWORK_OPTIMIZATION_PROD
-- =============================================================================

-- Set context
USE ROLE ACCOUNTADMIN;
USE DATABASE TELCO_NETWORK_OPTIMIZATION_PROD;
USE SCHEMA RAW;

-- =============================================================================
-- Create Compute Pool for Streamlit SPCS
-- =============================================================================

-- Create a compute pool with 2-5 nodes for Streamlit apps
-- Each Streamlit app uses one full node, so this supports 2-5 concurrent apps
CREATE COMPUTE POOL IF NOT EXISTS TELCO_STREAMLIT_POOL
  MIN_NODES = 2
  MAX_NODES = 5
  INSTANCE_FAMILY = CPU_X64_XS
  AUTO_RESUME = TRUE
  AUTO_SUSPEND_SECS = 600
  COMMENT = 'Compute pool for Telco Network Optimization Streamlit SPCS apps';

-- Verify compute pool creation
SHOW COMPUTE POOLS LIKE 'TELCO_STREAMLIT_POOL';

-- Check compute pool status (should be IDLE or ACTIVE)
DESCRIBE COMPUTE POOL TELCO_STREAMLIT_POOL;

-- Grant usage on compute pool to appropriate role
GRANT USAGE ON COMPUTE POOL TELCO_STREAMLIT_POOL TO ROLE ACCOUNTADMIN;

-- =============================================================================
-- Notes:
-- =============================================================================
-- 1. MIN_NODES = 2 ensures fast app startup for testing
-- 2. MAX_NODES = 5 allows for future expansion
-- 3. CPU_X64_XS is cost-effective for most Streamlit apps
-- 4. AUTO_SUSPEND_SECS = 600 (10 minutes) helps control costs
-- 5. Each Streamlit app takes one full node
-- =============================================================================
