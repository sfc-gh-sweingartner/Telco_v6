"""
AI Cache Utility Module
=======================

Provides caching functionality for AI-generated insights to improve user experience.
Handles cache reads, writes, and key generation for all AI action buttons.

Cache Strategy:
- Manual refresh only (no automatic expiration)
- Single-user mode (all users see same cached results)
- Unique cache keys based on all user selections
"""

import hashlib
import json
from datetime import datetime
from typing import Optional, Dict, Any
import streamlit as st


class AICache:
    """Main cache manager for AI-generated content"""
    
    def __init__(self, session):
        """
        Initialize cache manager with Snowflake session
        
        Args:
            session: Snowflake session object
        """
        self.session = session
        self.cache_schema = "TELCO_NETWORK_OPTIMIZATION_PROD.AI_CACHE"
    
    def _get_cache_key_params(self, table_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract only the parameters that should be used for cache key generation.
        Excludes metadata fields that don't affect uniqueness.
        
        Args:
            table_name: Name of the cache table
            params: All parameters passed
            
        Returns:
            Filtered parameters for cache key
        """
        # Define which parameters should be used for cache key (user-selectable values only)
        cache_key_params_map = {
            'MAIN_PAGE_CACHE': ['report_type'],
            'AI_INSIGHTS_CACHE': ['report_type', 'sub_type', 'time_horizon', 'category', 'urgency_level'],
            'CUSTOMER_PROFILE_CACHE': ['customer_id', 'analysis_type', 'recommendation_type'],
            'EXECUTIVE_SUMMARY_CACHE': ['report_type', 'analysis_period', 'financial_focus',
                                        'opportunity_scope', 'time_horizon', 'risk_category'],
            'PREDICTIVE_ANALYTICS_CACHE': ['analysis_type', 'forecast_metric', 'forecast_horizon',
                                           'anomaly_focus', 'sensitivity_level', 'maintenance_focus',
                                           'maintenance_window', 'behavior_metric', 'customer_segment']
        }
        
        key_params = cache_key_params_map.get(table_name, [])
        return {k: v for k, v in params.items() if k in key_params}
    
    def _generate_cache_key(self, table_name: str, **params) -> str:
        """
        Generate a unique cache key from parameters
        
        Args:
            table_name: Name of the cache table
            **params: All parameters that make this request unique
            
        Returns:
            MD5 hash of sorted parameters
        """
        # Filter to only cache-key parameters
        key_params = self._get_cache_key_params(table_name, params)
        # Sort parameters for consistent key generation
        sorted_params = json.dumps(key_params, sort_keys=True)
        return hashlib.md5(sorted_params.encode()).hexdigest()
    
    def _format_age(self, created_at) -> str:
        """
        Format cache age for display
        
        Args:
            created_at: Timestamp when cache was created
            
        Returns:
            Human-readable age string (e.g., "2 hours ago", "1 day ago")
        """
        if not created_at:
            return "Unknown"
        
        # Handle both string and datetime types
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            except:
                return "Unknown"
        
        now = datetime.now()
        diff = now - created_at
        
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            weeks = int(seconds / 604800)
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    
    def get_cached_result(self, table_name: str, **params) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached result if it exists
        
        Args:
            table_name: Name of the cache table (without schema)
            **params: Parameters that uniquely identify this cached item
            
        Returns:
            Dictionary with cached data or None if not found
        """
        try:
            cache_key = self._generate_cache_key(table_name, **params)
            
            query = f"""
            SELECT 
                AI_CONTENT,
                AI_MODEL,
                CONFIDENCE_SCORE,
                CREATED_AT,
                UPDATED_AT
            FROM {self.cache_schema}.{table_name}
            WHERE CACHE_KEY = '{cache_key}'
            """
            
            result = self.session.sql(query).collect()
            
            if result and len(result) > 0:
                row = result[0]
                return {
                    'content': row['AI_CONTENT'],
                    'model': row['AI_MODEL'],
                    'confidence': row['CONFIDENCE_SCORE'],
                    'created_at': row['CREATED_AT'],
                    'updated_at': row['UPDATED_AT'],
                    'cache_key': cache_key,
                    'age': self._format_age(row['CREATED_AT'])
                }
            
            return None
            
        except Exception as e:
            st.warning(f"Cache read error: {e}")
            return None
    
    def save_to_cache(self, table_name: str, ai_content: str, ai_model: str, 
                     confidence_score: float, **params) -> bool:
        """
        Save AI-generated content to cache
        
        Args:
            table_name: Name of the cache table (without schema)
            ai_content: The AI-generated text to cache
            ai_model: Name of the AI model used
            confidence_score: Confidence score of the result
            **params: All parameters including metadata fields
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cache_key = self._generate_cache_key(table_name, **{k: v for k, v in params.items() 
                                                    if k not in ['ai_content', 'ai_model', 'confidence_score']})
            
            # Escape single quotes in content
            escaped_content = ai_content.replace("'", "''")
            
            # Build column list and values based on table
            columns, values = self._build_insert_params(table_name, params)
            
            # Build column names for SELECT with AS aliases
            select_columns = self._build_select_columns(table_name, params)
            
            # Create the MERGE statement for upsert behavior
            merge_query = f"""
            MERGE INTO {self.cache_schema}.{table_name} AS target
            USING (
                SELECT 
                    '{cache_key}' AS CACHE_KEY,
                    '{escaped_content}' AS AI_CONTENT,
                    '{ai_model}' AS AI_MODEL,
                    {confidence_score} AS CONFIDENCE_SCORE,
                    CURRENT_TIMESTAMP() AS UPDATED_AT{select_columns}
            ) AS source
            ON target.CACHE_KEY = source.CACHE_KEY
            WHEN MATCHED THEN
                UPDATE SET
                    AI_CONTENT = source.AI_CONTENT,
                    AI_MODEL = source.AI_MODEL,
                    CONFIDENCE_SCORE = source.CONFIDENCE_SCORE,
                    UPDATED_AT = source.UPDATED_AT
            WHEN NOT MATCHED THEN
                INSERT (CACHE_KEY, AI_CONTENT, AI_MODEL, CONFIDENCE_SCORE{columns})
                VALUES (source.CACHE_KEY, source.AI_CONTENT, source.AI_MODEL, source.CONFIDENCE_SCORE{columns.replace(',', ', source.')})
            """
            
            self.session.sql(merge_query).collect()
            return True
            
        except Exception as e:
            st.error(f"Cache write error: {e}")
            return False
    
    def _build_select_columns(self, table_name: str, params: Dict[str, Any]) -> str:
        """
        Build SELECT column list with AS aliases for the MERGE source
        
        Args:
            table_name: Name of the cache table
            params: Dictionary of parameters
            
        Returns:
            String of columns with AS aliases for SELECT
        """
        select_cols = []
        
        # Map common parameters to table columns
        param_mapping = {
            'MAIN_PAGE_CACHE': ['report_type'],
            'AI_INSIGHTS_CACHE': ['report_type', 'sub_type', 'time_horizon', 'metric', 
                                 'category', 'urgency_level', 'customers_analyzed'],
            'CUSTOMER_PROFILE_CACHE': ['customer_id', 'analysis_type', 'recommendation_type',
                                       'ticket_count', 'avg_sentiment', 'risk_score'],
            'EXECUTIVE_SUMMARY_CACHE': ['report_type', 'analysis_period', 'financial_focus',
                                        'opportunity_scope', 'time_horizon', 'risk_category',
                                        'total_towers', 'total_customers', 'network_health_score',
                                        'customer_satisfaction'],
            'PREDICTIVE_ANALYTICS_CACHE': ['analysis_type', 'forecast_metric', 'forecast_horizon',
                                           'anomaly_focus', 'sensitivity_level', 'maintenance_focus',
                                           'maintenance_window', 'behavior_metric', 'customer_segment',
                                           'data_quality', 'prediction_accuracy']
        }
        
        if table_name in param_mapping:
            for col in param_mapping[table_name]:
                col_upper = col.upper()
                if col in params and params[col] is not None:
                    value = params[col]
                    if isinstance(value, str):
                        value = value.replace("'", "''")
                        select_cols.append(f", '{value}' AS {col_upper}")
                    else:
                        select_cols.append(f", {value} AS {col_upper}")
        
        return ''.join(select_cols)
    
    def _build_insert_params(self, table_name: str, params: Dict[str, Any]) -> tuple:
        """
        Build column names and values for INSERT based on table structure
        
        Args:
            table_name: Name of the cache table
            params: Dictionary of parameters
            
        Returns:
            Tuple of (column_string, value_string) for SQL INSERT
        """
        columns = []
        values = []
        
        # Map common parameters to table columns
        param_mapping = {
            'MAIN_PAGE_CACHE': ['report_type'],
            'AI_INSIGHTS_CACHE': ['report_type', 'sub_type', 'time_horizon', 'metric', 
                                 'category', 'urgency_level', 'customers_analyzed'],
            'CUSTOMER_PROFILE_CACHE': ['customer_id', 'analysis_type', 'recommendation_type',
                                       'ticket_count', 'avg_sentiment', 'risk_score'],
            'EXECUTIVE_SUMMARY_CACHE': ['report_type', 'analysis_period', 'financial_focus',
                                        'opportunity_scope', 'time_horizon', 'risk_category',
                                        'total_towers', 'total_customers', 'network_health_score',
                                        'customer_satisfaction'],
            'PREDICTIVE_ANALYTICS_CACHE': ['analysis_type', 'forecast_metric', 'forecast_horizon',
                                           'anomaly_focus', 'sensitivity_level', 'maintenance_focus',
                                           'maintenance_window', 'behavior_metric', 'customer_segment',
                                           'data_quality', 'prediction_accuracy']
        }
        
        if table_name in param_mapping:
            for col in param_mapping[table_name]:
                col_upper = col.upper()
                if col in params and params[col] is not None:
                    columns.append(f", {col_upper}")
                    value = params[col]
                    if isinstance(value, str):
                        value = value.replace("'", "''")
                        values.append(f", '{value}'")
                    else:
                        values.append(f", {value}")
        
        return (''.join(columns), ''.join(values))
    
    def display_cache_indicator(self, cached_result: Optional[Dict[str, Any]], 
                                show_refresh_hint: bool = True):
        """
        Display visual indicator for cached results
        
        Args:
            cached_result: The cached result dictionary (or None)
            show_refresh_hint: Whether to show hint about refresh button
        """
        if cached_result:
            age = cached_result.get('age', 'Unknown')
            model = cached_result.get('model', 'Unknown')
            
            hint = " Click 'Run/Refresh' to update." if show_refresh_hint else ""
            
            st.info(f" **Cached Result** • Generated {age} using {model}.{hint}")


# Convenience functions for each page

def get_main_page_cache(session) -> AICache:
    """Get cache manager for main page"""
    return AICache(session)


def get_ai_insights_cache(session) -> AICache:
    """Get cache manager for AI Insights page"""
    return AICache(session)


def get_customer_profile_cache(session) -> AICache:
    """Get cache manager for Customer Profile page"""
    return AICache(session)


def get_executive_summary_cache(session) -> AICache:
    """Get cache manager for Executive Summary page"""
    return AICache(session)


def get_predictive_analytics_cache(session) -> AICache:
    """Get cache manager for Predictive Analytics page"""
    return AICache(session)


# Example usage:
"""
from utils.ai_cache import get_ai_insights_cache

# In your Streamlit page:
cache = get_ai_insights_cache(session)

# Try to get cached result
cached = cache.get_cached_result(
    'AI_INSIGHTS_CACHE',
    report_type='executive_report',
    sub_type=None
)

if cached:
    # Display cached result
    cache.display_cache_indicator(cached)
    st.write(cached['content'])
else:
    # Generate new result
    if st.button("Generate Report"):
        result = ai_processor.ai_complete(prompt)
        
        # Save to cache
        cache.save_to_cache(
            'AI_INSIGHTS_CACHE',
            ai_content=result,
            ai_model=selected_model,
            confidence_score=0.89,
            report_type='executive_report',
            sub_type=None
        )
        st.write(result)
"""
