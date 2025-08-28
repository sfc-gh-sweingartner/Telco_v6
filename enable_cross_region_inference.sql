-- Enable Cross-Region Inference for Snowflake Cortex AISQL
-- This allows access to models from other regions

-- 1. Enable cross-region inference at account level (requires ACCOUNTADMIN)
-- Options: 'DISABLED', 'ANY_REGION', or specific regions like 'AWS_US,AWS_EU'
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';

-- 2. Verify the setting
SHOW PARAMETERS LIKE 'CORTEX_ENABLED_CROSS_REGION' IN ACCOUNT;

-- 3. Test claude-3-5-sonnet availability (our default model)
SELECT snowflake.cortex.complete('claude-3-5-sonnet', 'Hello, can you respond? This tests cross-region access.') as test_response;

-- 4. Test other models to verify cross-region access
SELECT snowflake.cortex.complete('mistral-large', 'Hello from Mistral!') as mistral_test;
SELECT snowflake.cortex.complete('llama3.1-8b', 'Hello from Llama!') as llama_test;

-- 5. Alternative regions (if you want to restrict to specific regions instead of ANY_REGION)
-- ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'AWS_US,AWS_EU';
-- ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'AWS_US';

-- 6. To disable cross-region inference (if needed)
-- ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'DISABLED';
