/*
AI Cache Tables Setup
=====================
Creates schema and tables for caching AI-generated insights to improve user experience.

Schema: TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE
Cache Strategy: Manual refresh only, no automatic expiration
*/

-- Create AI_CACHE schema
CREATE SCHEMA IF NOT EXISTS TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE;

USE SCHEMA TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE;

-- ============================================================================
-- Main Page Cache
-- ============================================================================
CREATE OR REPLACE TABLE MAIN_PAGE_CACHE (
    CACHE_KEY VARCHAR(500) PRIMARY KEY,
    REPORT_TYPE VARCHAR(100) NOT NULL,
    AI_CONTENT TEXT NOT NULL,
    AI_MODEL VARCHAR(100),
    CONFIDENCE_SCORE FLOAT,
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ============================================================================
-- AI Insights & Recommendations Cache
-- ============================================================================
CREATE OR REPLACE TABLE AI_INSIGHTS_CACHE (
    CACHE_KEY VARCHAR(500) PRIMARY KEY,
    REPORT_TYPE VARCHAR(100) NOT NULL,  -- 'executive_report', 'quick_insight', 'pattern_analysis', 'prediction', 'recommendation'
    SUB_TYPE VARCHAR(100),               -- For analysis types, prediction types, etc.
    TIME_HORIZON VARCHAR(50),            -- For predictions
    METRIC VARCHAR(100),                 -- For forecasts
    CATEGORY VARCHAR(100),               -- For recommendations
    URGENCY_LEVEL VARCHAR(50),           -- For recommendations
    AI_CONTENT TEXT NOT NULL,
    AI_MODEL VARCHAR(100),
    CONFIDENCE_SCORE FLOAT,
    CUSTOMERS_ANALYZED INT,              -- For customer-related analyses
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ============================================================================
-- Customer Profile Cache
-- ============================================================================
CREATE OR REPLACE TABLE CUSTOMER_PROFILE_CACHE (
    CACHE_KEY VARCHAR(500) PRIMARY KEY,
    CUSTOMER_ID VARCHAR(100) NOT NULL,
    ANALYSIS_TYPE VARCHAR(100) NOT NULL,  -- 'customer_insights', 'churn_analysis', 'recommendations'
    RECOMMENDATION_TYPE VARCHAR(100),      -- For recommendations: 'retention', 'service_improvements', etc.
    AI_CONTENT TEXT NOT NULL,
    AI_MODEL VARCHAR(100),
    CONFIDENCE_SCORE FLOAT,
    TICKET_COUNT INT,
    AVG_SENTIMENT FLOAT,
    RISK_SCORE INT,
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ============================================================================
-- Executive AI Summary Cache
-- ============================================================================
CREATE OR REPLACE TABLE EXECUTIVE_SUMMARY_CACHE (
    CACHE_KEY VARCHAR(500) PRIMARY KEY,
    REPORT_TYPE VARCHAR(100) NOT NULL,    -- 'business_performance', 'financial_impact', 'strategic_opportunities', 'risk_assessment'
    ANALYSIS_PERIOD VARCHAR(50),          -- 'Current Quarter', 'Last 30 Days', etc.
    FINANCIAL_FOCUS VARCHAR(100),         -- For financial analysis
    OPPORTUNITY_SCOPE VARCHAR(100),       -- For strategic opportunities
    TIME_HORIZON VARCHAR(50),             -- For strategic opportunities
    RISK_CATEGORY VARCHAR(100),           -- For risk assessment
    AI_CONTENT TEXT NOT NULL,
    AI_MODEL VARCHAR(100),
    CONFIDENCE_SCORE FLOAT,
    TOTAL_TOWERS INT,
    TOTAL_CUSTOMERS INT,
    NETWORK_HEALTH_SCORE FLOAT,
    CUSTOMER_SATISFACTION FLOAT,
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ============================================================================
-- Predictive Analytics Cache
-- ============================================================================
CREATE OR REPLACE TABLE PREDICTIVE_ANALYTICS_CACHE (
    CACHE_KEY VARCHAR(500) PRIMARY KEY,
    ANALYSIS_TYPE VARCHAR(100) NOT NULL,  -- 'forecast', 'anomaly_detection', 'predictive_maintenance', 'customer_behavior'
    FORECAST_METRIC VARCHAR(100),         -- For forecasts
    FORECAST_HORIZON VARCHAR(50),         -- For forecasts
    ANOMALY_FOCUS VARCHAR(100),           -- For anomaly detection
    SENSITIVITY_LEVEL INT,                -- For anomaly detection (1-10)
    MAINTENANCE_FOCUS VARCHAR(100),       -- For predictive maintenance
    MAINTENANCE_WINDOW VARCHAR(50),       -- For predictive maintenance
    BEHAVIOR_METRIC VARCHAR(100),         -- For customer behavior
    CUSTOMER_SEGMENT VARCHAR(100),        -- For customer behavior
    AI_CONTENT TEXT NOT NULL,
    AI_MODEL VARCHAR(100),
    CONFIDENCE_SCORE FLOAT,
    DATA_QUALITY VARCHAR(50),             -- 'Good', 'Limited', etc.
    PREDICTION_ACCURACY FLOAT,
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ============================================================================
-- Create indexes for better query performance
-- ============================================================================

-- AI Insights indexes
CREATE INDEX IF NOT EXISTS IDX_AI_INSIGHTS_TYPE ON AI_INSIGHTS_CACHE(REPORT_TYPE, SUB_TYPE);
CREATE INDEX IF NOT EXISTS IDX_AI_INSIGHTS_CREATED ON AI_INSIGHTS_CACHE(CREATED_AT);

-- Customer Profile indexes
CREATE INDEX IF NOT EXISTS IDX_CUSTOMER_ID ON CUSTOMER_PROFILE_CACHE(CUSTOMER_ID, ANALYSIS_TYPE);
CREATE INDEX IF NOT EXISTS IDX_CUSTOMER_CREATED ON CUSTOMER_PROFILE_CACHE(CREATED_AT);

-- Executive Summary indexes
CREATE INDEX IF NOT EXISTS IDX_EXECUTIVE_TYPE ON EXECUTIVE_SUMMARY_CACHE(REPORT_TYPE);
CREATE INDEX IF NOT EXISTS IDX_EXECUTIVE_CREATED ON EXECUTIVE_SUMMARY_CACHE(CREATED_AT);

-- Predictive Analytics indexes
CREATE INDEX IF NOT EXISTS IDX_PREDICTIVE_TYPE ON PREDICTIVE_ANALYTICS_CACHE(ANALYSIS_TYPE);
CREATE INDEX IF NOT EXISTS IDX_PREDICTIVE_CREATED ON PREDICTIVE_ANALYTICS_CACHE(CREATED_AT);

-- ============================================================================
-- Utility Views for Cache Management
-- ============================================================================

-- View to see all cached reports across all tables
CREATE OR REPLACE VIEW ALL_CACHED_REPORTS AS
SELECT 
    'MAIN_PAGE' AS SOURCE_TABLE,
    REPORT_TYPE,
    NULL AS SUB_TYPE,
    CREATED_AT,
    UPDATED_AT,
    DATEDIFF('hour', CREATED_AT, CURRENT_TIMESTAMP()) AS HOURS_OLD
FROM MAIN_PAGE_CACHE

UNION ALL

SELECT 
    'AI_INSIGHTS' AS SOURCE_TABLE,
    REPORT_TYPE,
    SUB_TYPE,
    CREATED_AT,
    UPDATED_AT,
    DATEDIFF('hour', CREATED_AT, CURRENT_TIMESTAMP()) AS HOURS_OLD
FROM AI_INSIGHTS_CACHE

UNION ALL

SELECT 
    'CUSTOMER_PROFILE' AS SOURCE_TABLE,
    ANALYSIS_TYPE AS REPORT_TYPE,
    CUSTOMER_ID AS SUB_TYPE,
    CREATED_AT,
    UPDATED_AT,
    DATEDIFF('hour', CREATED_AT, CURRENT_TIMESTAMP()) AS HOURS_OLD
FROM CUSTOMER_PROFILE_CACHE

UNION ALL

SELECT 
    'EXECUTIVE_SUMMARY' AS SOURCE_TABLE,
    REPORT_TYPE,
    ANALYSIS_PERIOD AS SUB_TYPE,
    CREATED_AT,
    UPDATED_AT,
    DATEDIFF('hour', CREATED_AT, CURRENT_TIMESTAMP()) AS HOURS_OLD
FROM EXECUTIVE_SUMMARY_CACHE

UNION ALL

SELECT 
    'PREDICTIVE_ANALYTICS' AS SOURCE_TABLE,
    ANALYSIS_TYPE AS REPORT_TYPE,
    FORECAST_METRIC AS SUB_TYPE,
    CREATED_AT,
    UPDATED_AT,
    DATEDIFF('hour', CREATED_AT, CURRENT_TIMESTAMP()) AS HOURS_OLD
FROM PREDICTIVE_ANALYTICS_CACHE
ORDER BY CREATED_AT DESC;

-- View for cache statistics
CREATE OR REPLACE VIEW CACHE_STATISTICS AS
SELECT 
    'MAIN_PAGE' AS TABLE_NAME,
    COUNT(*) AS CACHED_REPORTS,
    MAX(CREATED_AT) AS LAST_CACHE_UPDATE,
    MIN(CREATED_AT) AS OLDEST_CACHE,
    AVG(DATEDIFF('hour', CREATED_AT, CURRENT_TIMESTAMP())) AS AVG_AGE_HOURS
FROM MAIN_PAGE_CACHE

UNION ALL

SELECT 
    'AI_INSIGHTS' AS TABLE_NAME,
    COUNT(*) AS CACHED_REPORTS,
    MAX(CREATED_AT) AS LAST_CACHE_UPDATE,
    MIN(CREATED_AT) AS OLDEST_CACHE,
    AVG(DATEDIFF('hour', CREATED_AT, CURRENT_TIMESTAMP())) AS AVG_AGE_HOURS
FROM AI_INSIGHTS_CACHE

UNION ALL

SELECT 
    'CUSTOMER_PROFILE' AS TABLE_NAME,
    COUNT(*) AS CACHED_REPORTS,
    MAX(CREATED_AT) AS LAST_CACHE_UPDATE,
    MIN(CREATED_AT) AS OLDEST_CACHE,
    AVG(DATEDIFF('hour', CREATED_AT, CURRENT_TIMESTAMP())) AS AVG_AGE_HOURS
FROM CUSTOMER_PROFILE_CACHE

UNION ALL

SELECT 
    'EXECUTIVE_SUMMARY' AS TABLE_NAME,
    COUNT(*) AS CACHED_REPORTS,
    MAX(CREATED_AT) AS LAST_CACHE_UPDATE,
    MIN(CREATED_AT) AS OLDEST_CACHE,
    AVG(DATEDIFF('hour', CREATED_AT, CURRENT_TIMESTAMP())) AS AVG_AGE_HOURS
FROM EXECUTIVE_SUMMARY_CACHE

UNION ALL

SELECT 
    'PREDICTIVE_ANALYTICS' AS TABLE_NAME,
    COUNT(*) AS CACHED_REPORTS,
    MAX(CREATED_AT) AS LAST_CACHE_UPDATE,
    MIN(CREATED_AT) AS OLDEST_CACHE,
    AVG(DATEDIFF('hour', CREATED_AT, CURRENT_TIMESTAMP())) AS AVG_AGE_HOURS
FROM PREDICTIVE_ANALYTICS_CACHE;

-- ============================================================================
-- Grant necessary permissions (adjust role as needed)
-- ============================================================================

-- GRANT USAGE ON SCHEMA TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE TO ROLE YOUR_ROLE;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE TO ROLE YOUR_ROLE;
-- GRANT SELECT ON ALL VIEWS IN SCHEMA TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE TO ROLE YOUR_ROLE;

-- ============================================================================
-- Cleanup procedure (optional - for manual cache clearing)
-- ============================================================================

CREATE OR REPLACE PROCEDURE CLEAR_ALL_CACHES()
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    TRUNCATE TABLE TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE.MAIN_PAGE_CACHE;
    TRUNCATE TABLE TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE.AI_INSIGHTS_CACHE;
    TRUNCATE TABLE TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE.CUSTOMER_PROFILE_CACHE;
    TRUNCATE TABLE TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE.EXECUTIVE_SUMMARY_CACHE;
    TRUNCATE TABLE TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE.PREDICTIVE_ANALYTICS_CACHE;
    RETURN 'All AI caches cleared successfully';
END;
$$;

-- ============================================================================
-- Setup Complete
-- ============================================================================

SELECT 'AI Cache tables created successfully!' AS STATUS;
SELECT * FROM CACHE_STATISTICS;
