"""
Verify AI Cache Functionality
=============================
Quick script to check if cache tables are being populated correctly.
Run this after clicking buttons in the Streamlit app to verify caching is working.
"""

from snowflake.snowpark import Session
import os
import json

def get_snowflake_session():
    """Create Snowflake session from environment or config"""
    try:
        # Try to load from environment or config
        connection_params = {
            "account": os.getenv("SNOWFLAKE_ACCOUNT", "your_account"),
            "user": os.getenv("SNOWFLAKE_USER", "your_user"),
            "authenticator": "externalbrowser",  # Use SSO/browser auth
            "database": "TELCO_NETWORK_OPTIMIZATION_PROD",
            "schema": "AI_CACHE",
            "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
        }
        
        return Session.builder.configs(connection_params).create()
    except Exception as e:
        print(f"❌ Error connecting to Snowflake: {e}")
        print("\n💡 Tip: Make sure you have snowflake-snowpark-python installed:")
        print("   pip install snowflake-snowpark-python")
        return None

def check_cache_status(session):
    """Check the status of all cache tables"""
    print("\n" + "="*60)
    print("📦 AI CACHE STATUS CHECK")
    print("="*60)
    
    # Check row counts
    print("\n📊 Row Counts by Table:")
    print("-" * 60)
    
    tables = [
        'MAIN_PAGE_CACHE',
        'AI_INSIGHTS_CACHE', 
        'CUSTOMER_PROFILE_CACHE',
        'EXECUTIVE_SUMMARY_CACHE',
        'PREDICTIVE_ANALYTICS_CACHE'
    ]
    
    total_rows = 0
    for table in tables:
        try:
            query = f"SELECT COUNT(*) as cnt FROM TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE.{table}"
            result = session.sql(query).collect()
            count = result[0]['CNT']
            total_rows += count
            
            status = "✅" if count > 0 else "❌"
            print(f"{status} {table:30s} : {count:4d} rows")
        except Exception as e:
            print(f"❌ {table:30s} : ERROR - {e}")
    
    print("-" * 60)
    print(f"{'TOTAL':30s} : {total_rows:4d} rows")
    
    # Show recent cache entries
    print("\n📝 Recent Cache Entries (Last 10):")
    print("-" * 60)
    
    try:
        query = """
        SELECT 
            SOURCE_TABLE,
            REPORT_TYPE,
            SUB_TYPE,
            CREATED_AT,
            DATEDIFF('hour', CREATED_AT, CURRENT_TIMESTAMP()) as HOURS_OLD
        FROM TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE.ALL_CACHED_REPORTS
        ORDER BY CREATED_AT DESC
        LIMIT 10
        """
        results = session.sql(query).collect()
        
        if results:
            for row in results:
                source = row['SOURCE_TABLE']
                report_type = row['REPORT_TYPE']
                sub_type = row['SUB_TYPE'] or ''
                hours = row['HOURS_OLD']
                
                print(f"  • {source:20s} | {report_type:25s} | {sub_type:20s} | {hours}h ago")
        else:
            print("  ❌ No cache entries found!")
    except Exception as e:
        print(f"  ❌ Error querying recent entries: {e}")
    
    # Show cache statistics
    print("\n📈 Cache Statistics:")
    print("-" * 60)
    
    try:
        query = "SELECT * FROM TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE.CACHE_STATISTICS"
        results = session.sql(query).collect()
        
        for row in results:
            table_name = row['TABLE_NAME']
            cached_reports = row['CACHED_REPORTS']
            last_update = row['LAST_CACHE_UPDATE']
            avg_age = row['AVG_AGE_HOURS'] or 0
            
            print(f"  {table_name:30s} : {cached_reports:3d} reports | Avg age: {avg_age:.1f}h")
    except Exception as e:
        print(f"  ❌ Error querying statistics: {e}")
    
    print("\n" + "="*60)
    
    # Recommendations
    if total_rows == 0:
        print("\n⚠️  WARNING: No cache entries found!")
        print("\n💡 Troubleshooting Steps:")
        print("  1. Run the Streamlit app: streamlit run main.py")
        print("  2. Click on AI report generation buttons")
        print("  3. Look for error messages in the Streamlit UI")
        print("  4. Check Snowflake permissions on AI_CACHE schema")
        print("  5. Review Documentation/CACHE_FIX_SUMMARY.md")
    elif total_rows < 10:
        print("\n⚠️  Low cache count detected!")
        print(f"   Only {total_rows} entries found. Expected 20+ after testing all buttons.")
        print("\n💡 Next Steps:")
        print("  1. Test remaining buttons systematically")
        print("  2. Check for error messages when clicking buttons")
        print("  3. Refer to Documentation/CACHE_FIX_SUMMARY.md for testing guide")
    else:
        print("\n✅ Cache appears to be working correctly!")
        print(f"   Found {total_rows} cache entries across all tables.")
        print("\n💡 Continue testing all buttons to ensure full functionality.")
    
    print("\n" + "="*60 + "\n")

def main():
    """Main function"""
    print("\n🔍 Telco Network Optimization - Cache Verification Tool")
    
    session = get_snowflake_session()
    if not session:
        print("\n❌ Failed to connect to Snowflake. Please check your credentials.")
        print("\n💡 This script uses browser-based authentication.")
        print("   A browser window should open for you to sign in.")
        return
    
    try:
        check_cache_status(session)
    except Exception as e:
        print(f"\n❌ Error during cache verification: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()

