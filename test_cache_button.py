"""
Test Cache Button Functionality
================================
Simulate button clicks to debug why cache isn't being saved
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from snowflake.snowpark import Session

# Connection parameters from ~/.snowsql/config  
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Load private key
with open(os.path.expanduser("~/.ssh/rsa_key.p8"), "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password="cLbz!g3hmZGa!Jan".encode(),
        backend=default_backend()
    )

pkb = private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

connection_params = {
    "account": "rxb32947",
    "user": "STEPHEN_PYTHON",
    "private_key": pkb,
    "database": "TELCO_NETWORK_OPTIMIZATION_PROD",
    "schema": "AI_CACHE",
    "warehouse": "MYWH",
    "role": "ACCOUNTADMIN"
}

print("🔍 Testing AI Cache Button Functionality\n")
print("=" * 60)

# Create session
print("\n1️⃣ Connecting to Snowflake...")
try:
    session = Session.builder.configs(connection_params).create()
    print("   ✅ Connected successfully!")
except Exception as e:
    print(f"   ❌ Connection failed: {e}")
    sys.exit(1)

# Import AI functions
print("\n2️⃣ Loading AI functions...")
try:
    from aisql_functions import TelcoAISQLProcessor
    ai_processor = TelcoAISQLProcessor(session)
    print("   ✅ AI processor loaded!")
except Exception as e:
    print(f"   ❌ Failed to load AI functions: {e}")
    sys.exit(1)

# Import cache functions
print("\n3️⃣ Loading cache functions...")
try:
    from ai_cache import get_main_page_cache
    main_cache = get_main_page_cache(session)
    print("   ✅ Cache module loaded!")
except Exception as e:
    print(f"   ❌ Failed to load cache module: {e}")
    sys.exit(1)

# Test 1: Generate a simple AI response
print("\n4️⃣ Testing AI completion...")
try:
    test_prompt = "In 50 words, explain network optimization."
    test_response = ai_processor.ai_complete(test_prompt, max_tokens=100)
    
    if test_response:
        print(f"   ✅ AI response received ({len(test_response)} chars)")
        print(f"   Preview: {test_response[:100]}...")
    else:
        print("   ❌ AI response was empty!")
        print("   This is why cache isn't being saved - AI returns empty string on error")
except Exception as e:
    print(f"   ❌ AI completion failed: {e}")

# Test 2: Try to save to cache
print("\n5️⃣ Testing cache save...")
try:
    test_content = "This is a test strategic report with network metrics and business intelligence."
    
    result = main_cache.save_to_cache(
        'MAIN_PAGE_CACHE',
        ai_content=test_content,
        ai_model='claude-4-sonnet',
        confidence_score=0.92,
        report_type='strategic_report'
    )
    
    if result:
        print("   ✅ Cache save successful!")
        
        # Verify it was saved
        print("\n6️⃣ Verifying cache entry...")
        cached = main_cache.get_cached_result(
            'MAIN_PAGE_CACHE',
            report_type='strategic_report'
        )
        if cached:
            print(f"   ✅ Cache entry verified!")
            print(f"   Content length: {len(cached['content'])} chars")
            print(f"   Created: {cached.get('created_at')}")
        else:
            print("   ❌ Cache entry not found after save!")
    else:
        print("   ❌ Cache save failed!")
        print("   Check error messages above for details")
        
except Exception as e:
    print(f"   ❌ Cache save exception: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Check current cache status
print("\n7️⃣ Checking all cache tables...")
try:
    query = """
    SELECT 
        'MAIN_PAGE_CACHE' AS TABLE_NAME, COUNT(*) AS ROW_COUNT 
    FROM MAIN_PAGE_CACHE
    UNION ALL
    SELECT 'AI_INSIGHTS_CACHE', COUNT(*) FROM AI_INSIGHTS_CACHE
    UNION ALL  
    SELECT 'CUSTOMER_PROFILE_CACHE', COUNT(*) FROM CUSTOMER_PROFILE_CACHE
    UNION ALL
    SELECT 'EXECUTIVE_SUMMARY_CACHE', COUNT(*) FROM EXECUTIVE_SUMMARY_CACHE
    UNION ALL
    SELECT 'PREDICTIVE_ANALYTICS_CACHE', COUNT(*) FROM PREDICTIVE_ANALYTICS_CACHE
    """
    
    results = session.sql(query).collect()
    total = 0
    for row in results:
        count = row['ROW_COUNT']
        total += count
        status = "✅" if count > 0 else "❌"
        print(f"   {status} {row['TABLE_NAME']:30s}: {count} rows")
    
    print(f"\n   Total cached entries: {total}")
    
except Exception as e:
    print(f"   ❌ Error checking cache: {e}")

print("\n" + "=" * 60)
print("\n✅ Test complete! Check output above for issues.\n")

session.close()

