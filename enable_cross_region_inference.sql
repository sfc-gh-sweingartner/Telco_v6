-- Enable Cross-Region Inference for Snowflake Cortex AISQL
-- This allows access to models from other AWS regions

-- 1. Enable cross-region inference at account level (requires ACCOUNTADMIN)
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION_INFERENCE = TRUE;

-- 2. Set cross-region policy to access AWS US regions and any region
-- This enables access to claude-3-5-sonnet (default) and other premium models
ALTER ACCOUNT SET CORTEX_GLOBAL_INFERENCE_REGIONS = 'AWS_US, ANY_REGION';

-- 3. Verify the settings
SHOW PARAMETERS LIKE 'CORTEX_ENABLED_CROSS_REGION_INFERENCE' IN ACCOUNT;
SHOW PARAMETERS LIKE 'CORTEX_GLOBAL_INFERENCE_REGIONS' IN ACCOUNT;

-- 4. Test claude-3-5-sonnet availability (our default model)
SELECT snowflake.cortex.complete('claude-3-5-sonnet', 'Hello, can you respond?') as test_response;

-- Alternative: Test with specific region specification
SELECT snowflake.cortex.complete('claude-3-5-sonnet', 'Hello from cross-region inference!', {'region': 'AWS_US'}) as test_response;

-- 5. List available models in your environment
-- Note: This is a conceptual query - actual implementation may vary
-- SHOW CORTEX MODELS;
