"""
Snowflake Cortex AISQL Functions Utility Module
==================================================

This module provides a comprehensive interface to Snowflake Cortex AISQL functions
for AI-powered telco network optimization and analytics.

Based on: https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql

Available Functions:
- AI_COMPLETE: Generate completions using LLMs (GPT, Claude, Mistral, etc.)
- AI_CLASSIFY: Classify text/images into user-defined categories  
- AI_FILTER: Filter content based on natural language conditions
- AI_AGG: Aggregate text and return insights across multiple rows
- AI_EMBED: Generate embedding vectors for similarity search
- AI_EXTRACT: Extract information from text/files
- AI_SENTIMENT: Extract sentiment scores from text
- AI_SUMMARIZE_AGG: Summarize text across multiple rows
- AI_SIMILARITY: Calculate embedding similarity between inputs
- TRANSLATE: Translate text between supported languages
- SUMMARIZE: Return summary of specified text
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional, Union
import json
import time
from datetime import datetime
import hashlib
import logging
from functools import wraps
import threading
import os

class TelcoAISQLProcessor:
    """
    Advanced AI processing for Telco Network Optimization using Snowflake Cortex AISQL
    """
    
    def __init__(self, session):
        """
        Initialize with Snowflake session
        
        Args:
            session: Snowflake session object
        """
        self.session = session
        self.supported_models = [
            # Claude Models (Anthropic)
            'claude-4-sonnet', 'claude-4-opus', 'claude-3-5-sonnet', 'claude-3-7-sonnet',
            
            # Mistral Models
            'mistral-large', 'mistral-large2', 'mistral-7b', 'mixtral-8x7b',
            
            # OpenAI Models 
            'openai-gpt-4.1', 'openai-o4-mini', 'openai-gpt-5', 'openai-gpt-5-mini', 
            'openai-gpt-5-nano', 'openai-gpt-5-chat', 'openai-gpt-oss-120b', 'openai-gpt-oss-20b',
            
            # Llama Models (Meta)
            'llama4-maverick', 'llama4-scout', 'llama2-70b-chat',
            'llama3-8b', 'llama3-70b', 'llama3.1-8b', 'llama3.1-70b', 'llama3.1-405b',
            'llama3.2-1b', 'llama3.2-3b', 'llama3.3-70b',
            
            # Snowflake-Optimized Models
            'snowflake-arctic', 'snowflake-llama-3.3-70b', 'snowflake-llama-3.1-405b',
            'snowflake-arctic-embed-m',
            
            # Specialized Models
            'reka-core', 'reka-flash', 'jamba-instruct', 'jamba-1.5-mini', 'jamba-1.5-large',
            'deepseek-r1', 'gemma-7b',
            
            # Embedding Models
            'e5-base-v2', 'nv-embed-qa-4', 'multilingual-e5-large', 'voyage-multilingual-2'
        ]
        self.default_model = 'claude-3-5-sonnet'  # Fast, highly capable Claude model
        
    def ai_complete(self, prompt: str, model: str = None, max_tokens: int = 150) -> str:
        """
        Generate AI completions using Snowflake Cortex AI_COMPLETE (limited to ~100 words)
        
        Args:
            prompt: The input prompt for completion
            model: LLM model to use (default: claude-3-5-sonnet)
            max_tokens: Maximum tokens to generate (default 150 ≈ 100 words)
            
        Returns:
            Generated completion text (max 100 words)
        """
        if model is None:
            model = self.default_model
            
        try:
            query = f"""
            SELECT SNOWFLAKE.CORTEX.AI_COMPLETE(
                '{model}', 
                '{prompt}',
                {{'max_tokens': {max_tokens}}}
            ) as completion
            """
            result = self.session.sql(query).collect()
            return result[0]['COMPLETION'] if result else ""
        except Exception as e:
            st.error(f"AI Complete Error: {e}")
            return ""
    
    def ai_classify(self, text: str, categories: List[str]) -> str:
        """
        Classify text into predefined categories
        
        Args:
            text: Text to classify
            categories: List of possible categories
            
        Returns:
            Classified category
        """
        try:
            # Properly format categories as SQL array using ARRAY_CONSTRUCT
            categories_escaped = [cat.replace("'", "''") for cat in categories]
            categories_sql = "ARRAY_CONSTRUCT(" + ", ".join([f"'{cat}'" for cat in categories_escaped]) + ")"
            text_escaped = text.replace("'", "''")
            
            query = f"""
            SELECT SNOWFLAKE.CORTEX.AI_CLASSIFY(
                '{text_escaped}', 
                {categories_sql}
            ) as classification
            """
            result = self.session.sql(query).collect()
            return result[0]['CLASSIFICATION'] if result else "Unknown"
        except Exception as e:
            st.error(f"AI Classify Error: {e}")
            return "Unknown"
    
    def ai_filter(self, text: str, condition: str) -> bool:
        """
        Filter text based on natural language condition
        
        Args:
            text: Text to filter
            condition: Natural language condition
            
        Returns:
            True if text matches condition, False otherwise
        """
        try:
            text_escaped = text.replace("'", "''")
            condition_escaped = condition.replace("'", "''")
            
            query = f"""
            SELECT SNOWFLAKE.CORTEX.AI_FILTER(
                '{text_escaped}', 
                '{condition_escaped}'
            ) as matches
            """
            result = self.session.sql(query).collect()
            return bool(result[0]['MATCHES']) if result else False
        except Exception as e:
            st.error(f"AI Filter Error: {e}")
            return False
    
    def ai_agg(self, texts: List[str], prompt: str) -> str:
        """
        Aggregate insights from multiple text inputs using AI_COMPLETE instead of AI_AGG
        
        Args:
            texts: List of text inputs to aggregate
            prompt: Prompt describing what insights to extract
            
        Returns:
            Aggregated insights
        """
        try:
            # Instead of using temporary tables, combine texts and use AI_COMPLETE
            combined_text = "\n\n".join([f"Data Point {i+1}: {text}" for i, text in enumerate(texts[:10])])  # Limit to 10 items
            
            full_prompt = f"""
            {prompt}
            
            Analyze these data points and provide insights in EXACTLY 100 words:
            
            {combined_text}
            
            Be concise, specific, and actionable. LIMIT: 100 words maximum.
            """
            
            # Use AI_COMPLETE with 100-word limit
            return self.ai_complete(full_prompt, max_tokens=150)
        except Exception as e:
            st.error(f"AI Aggregation Error: {e}")
            return ""
    
    def ai_embed(self, text: str) -> List[float]:
        """
        Generate embedding vector for text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        try:
            text_escaped = text.replace("'", "''")
            
            query = f"""
            SELECT SNOWFLAKE.CORTEX.AI_EMBED(
                'e5-base-v2',
                '{text_escaped}'
            ) as embedding
            """
            result = self.session.sql(query).collect()
            if result and result[0]['EMBEDDING']:
                return json.loads(result[0]['EMBEDDING'])
            return []
        except Exception as e:
            st.error(f"AI Embed Error: {e}")
            return []
    
    def ai_extract(self, text: str, question: str) -> str:
        """
        Extract specific information from text
        
        Args:
            text: Source text
            question: What to extract
            
        Returns:
            Extracted information
        """
        try:
            text_escaped = text.replace("'", "''")
            question_escaped = question.replace("'", "''")
            
            query = f"""
            SELECT SNOWFLAKE.CORTEX.AI_EXTRACT(
                '{text_escaped}', 
                '{question_escaped}'
            ) as extracted_info
            """
            result = self.session.sql(query).collect()
            return result[0]['EXTRACTED_INFO'] if result else ""
        except Exception as e:
            st.error(f"AI Extract Error: {e}")
            return ""
    
    def ai_sentiment(self, text: str) -> float:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment score (-1 to 1)
        """
        try:
            text_escaped = text.replace("'", "''")
            
            query = f"""
            SELECT SNOWFLAKE.CORTEX.AI_SENTIMENT('{text_escaped}') as sentiment
            """
            result = self.session.sql(query).collect()
            return float(result[0]['SENTIMENT']) if result else 0.0
        except Exception as e:
            st.error(f"AI Sentiment Error: {e}")
            return 0.0
    
    def ai_summarize_agg(self, texts: List[str]) -> str:
        """
        Summarize multiple texts together using AI_COMPLETE instead of AI_SUMMARIZE_AGG
        
        Args:
            texts: List of texts to summarize
            
        Returns:
            Aggregated summary
        """
        try:
            # Instead of using temporary tables, combine texts and use AI_COMPLETE
            combined_text = "\n\n---\n\n".join(texts[:10])  # Limit to 10 texts, separated clearly
            
            prompt = f"""
            Please provide a comprehensive summary of the following texts. Focus on the key insights, patterns, and important information:
            
            {combined_text}
            
            Summary:"""
            
            # Use AI_COMPLETE instead of AI_SUMMARIZE_AGG to avoid temporary table issues
            return self.ai_complete(prompt, max_tokens=500)
        except Exception as e:
            st.error(f"AI Summarize Aggregation Error: {e}")
            return ""
    
    def ai_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0 to 1)
        """
        try:
            text1_escaped = text1.replace("'", "''")
            text2_escaped = text2.replace("'", "''")
            
            query = f"""
            SELECT SNOWFLAKE.CORTEX.AI_SIMILARITY(
                '{text1_escaped}', 
                '{text2_escaped}'
            ) as similarity
            """
            result = self.session.sql(query).collect()
            return float(result[0]['SIMILARITY']) if result else 0.0
        except Exception as e:
            st.error(f"AI Similarity Error: {e}")
            return 0.0
    
    def translate(self, text: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
        """
        Translate text between languages
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        try:
            text_escaped = text.replace("'", "''")
            
            query = f"""
            SELECT SNOWFLAKE.CORTEX.TRANSLATE(
                '{text_escaped}', 
                '{source_lang}', 
                '{target_lang}'
            ) as translated
            """
            result = self.session.sql(query).collect()
            return result[0]['TRANSLATED'] if result else ""
        except Exception as e:
            st.error(f"Translation Error: {e}")
            return ""
    
    def summarize(self, text: str) -> str:
        """
        Generate summary of text
        
        Args:
            text: Text to summarize
            
        Returns:
            Summary text
        """
        try:
            text_escaped = text.replace("'", "''")
            
            query = f"""
            SELECT SNOWFLAKE.CORTEX.SUMMARIZE('{text_escaped}') as summary
            """
            result = self.session.sql(query).collect()
            return result[0]['SUMMARY'] if result else ""
        except Exception as e:
            st.error(f"Summarize Error: {e}")
            return ""


class TelcoAIAnalytics:
    """
    High-level AI analytics specifically designed for Telco Network Optimization
    """
    
    def __init__(self, session, aisql_processor: TelcoAISQLProcessor):
        """
        Initialize with Snowflake session and AISQL processor
        
        Args:
            session: Snowflake session object
            aisql_processor: TelcoAISQLProcessor instance
        """
        self.session = session
        self.ai = aisql_processor
    
    def analyze_network_issues(self, cell_tower_data: pd.DataFrame) -> Dict[str, Any]:
        """
        AI-powered analysis of network issues from cell tower data
        
        Args:
            cell_tower_data: DataFrame with cell tower performance metrics
            
        Returns:
            Dictionary with AI insights about network issues
        """
        try:
            # Extract key metrics for analysis
            issues = []
            if not cell_tower_data.empty:
                for _, row in cell_tower_data.head(10).iterrows():  # Analyze top 10 problematic towers
                    issue_text = f"""
                    Cell Tower {row.get('CELL_ID', 'Unknown')} issues:
                    - Location: {row.get('BID_DESCRIPTION', 'Unknown')}
                    - Connection Success: {row.get('PM_RRC_CONN_ESTAB_SUCC', 0)}/{row.get('PM_RRC_CONN_ESTAB_ATT', 1)}
                    - Abnormal Releases: {row.get('PM_ERAB_REL_ABNORMAL_ENB', 0)}
                    - Failure Codes: {row.get('CAUSE_CODE_SHORT_DESCRIPTION', 'Unknown')}
                    """
                    issues.append(issue_text.strip())
            
            # Generate AI insights
            insights = {}
            if issues:
                # Root cause analysis (100 words max)
                insights['root_causes'] = self.ai.ai_agg(
                    issues,
                    "Identify top 3 root causes of network failures in EXACTLY 100 words. Be specific and technical."
                )
                
                # Priority recommendations (100 words max)  
                insights['recommendations'] = self.ai.ai_agg(
                    issues,
                    "List 3 priority technical recommendations to fix network issues. Format: 1) Action 2) Timeline 3) Impact. LIMIT: 100 words."
                )
                
                # Risk assessment (100 words max)
                insights['risk_assessment'] = self.ai.ai_complete(
                    f"Assess business risk from network issues in EXACTLY 100 words: customer impact, revenue risk, mitigation priorities: {issues[0][:300]}"
                )
            
            return insights
        except Exception as e:
            st.error(f"Network Analysis Error: {e}")
            return {}
    
    def classify_support_tickets(self, tickets_data: pd.DataFrame) -> pd.DataFrame:
        """
        AI-powered classification of support tickets
        
        Args:
            tickets_data: DataFrame with support ticket data
            
        Returns:
            DataFrame with additional AI classification columns
        """
        try:
            if tickets_data.empty:
                return tickets_data
            
            # Define classification categories
            urgency_categories = ["Critical", "High", "Medium", "Low"]
            issue_categories = [
                "Network Outage", "Billing Issue", "Service Quality", 
                "Technical Support", "Account Management", "Hardware Issue"
            ]
            
            # Add AI classifications
            enhanced_tickets = tickets_data.copy()
            
            # Sample classification for first 20 tickets (to manage costs)
            sample_size = min(20, len(enhanced_tickets))
            
            for i in range(sample_size):
                request_text = enhanced_tickets.iloc[i].get('REQUEST', '')
                
                if request_text:
                    # Classify urgency
                    urgency = self.ai.ai_classify(request_text, urgency_categories)
                    enhanced_tickets.loc[enhanced_tickets.index[i], 'AI_URGENCY'] = urgency
                    
                    # Classify issue type
                    issue_type = self.ai.ai_classify(request_text, issue_categories)
                    enhanced_tickets.loc[enhanced_tickets.index[i], 'AI_ISSUE_TYPE'] = issue_type
                    
                    # Extract key issues
                    key_issue = self.ai.ai_extract(
                        request_text, 
                        "What is the main technical problem or concern mentioned?"
                    )
                    enhanced_tickets.loc[enhanced_tickets.index[i], 'AI_KEY_ISSUE'] = key_issue
            
            return enhanced_tickets
        except Exception as e:
            st.error(f"Ticket Classification Error: {e}")
            return tickets_data
    
    def generate_executive_summary(self, network_data: Dict[str, Any], ticket_data: Dict[str, Any]) -> str:
        """
        Generate AI-powered executive summary of network status
        
        Args:
            network_data: Summary of network performance metrics
            ticket_data: Summary of support ticket metrics
            
        Returns:
            Executive summary text
        """
        try:
            context = f"""
            Network Performance Summary:
            - Total Cell Towers Analyzed: {network_data.get('total_towers', 0)}
            - Average Connection Success Rate: {network_data.get('avg_success_rate', 0):.2%}
            - Critical Issues Identified: {network_data.get('critical_issues', 0)}
            
            Customer Support Summary:
            - Total Tickets: {ticket_data.get('total_tickets', 0)}
            - Average Sentiment Score: {ticket_data.get('avg_sentiment', 0):.2f}
            - Critical Tickets: {ticket_data.get('critical_tickets', 0)}
            """
            
            prompt = f"""
            As a senior telco network analyst, provide a CRISP executive summary in EXACTLY 100 words based on this data:
            
            {context}
            
            Cover: 1) Network health status 2) Key metrics 3) Critical issues 4) Customer satisfaction 5) Top 2 strategic actions
            
            Format: Professional, concise, actionable. LIMIT: 100 words maximum.
            """
            
            return self.ai.ai_complete(prompt, max_tokens=150)
        except Exception as e:
            st.error(f"Executive Summary Error: {e}")
            return "Unable to generate executive summary at this time."
    
    def predict_network_failures(self, historical_data: pd.DataFrame) -> Dict[str, Any]:
        """
        AI-powered prediction of potential network failures
        
        Args:
            historical_data: Historical network performance data
            
        Returns:
            Predictions and risk analysis
        """
        try:
            # Analyze trends in the data
            if historical_data.empty:
                return {"predictions": "No data available for analysis"}
            
            # Create trend analysis text
            trend_texts = []
            for _, row in historical_data.head(10).iterrows():
                trend_text = f"""
                Cell {row.get('CELL_ID', 'Unknown')}: 
                Success Rate Trend: {row.get('PM_RRC_CONN_ESTAB_SUCC', 0)} successful / {row.get('PM_RRC_CONN_ESTAB_ATT', 1)} attempts
                Error Pattern: {row.get('CAUSE_CODE_SHORT_DESCRIPTION', 'None')}
                Location: {row.get('BID_DESCRIPTION', 'Unknown')}
                """
                trend_texts.append(trend_text.strip())
            
            # Generate predictions
            predictions = self.ai.ai_agg(
                trend_texts,
                "Based on these network performance patterns, predict which cell towers are most likely to experience failures in the next 30 days and why"
            )
            
            # Risk mitigation strategies
            mitigation = self.ai.ai_complete(
                f"Based on these network trends, recommend 5 proactive measures to prevent network failures: {predictions[:300]}...",
                max_tokens=600
            )
            
            return {
                "predictions": predictions,
                "mitigation_strategies": mitigation,
                "analysis_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            st.error(f"Prediction Error: {e}")
            return {"predictions": "Unable to generate predictions at this time."}
    
    def analyze_customer_churn_risk(self, customer_data: pd.DataFrame, ticket_data: pd.DataFrame) -> Dict[str, Any]:
        """
        AI-powered customer churn risk analysis
        
        Args:
            customer_data: Customer information
            ticket_data: Support ticket history
            
        Returns:
            Churn risk analysis and recommendations
        """
        try:
            # Combine customer and ticket data for analysis
            analysis_texts = []
            
            if not ticket_data.empty:
                # Group tickets by customer
                customer_tickets = ticket_data.groupby('CUSTOMER_NAME').agg({
                    'SENTIMENT_SCORE': 'mean',
                    'TICKET_ID': 'count',
                    'REQUEST': 'first'
                }).head(10)
                
                for customer, data in customer_tickets.iterrows():
                    analysis_text = f"""
                    Customer: {customer}
                    Ticket Count: {data['TICKET_ID']} tickets
                    Average Sentiment: {data['SENTIMENT_SCORE']:.2f}
                    Recent Issue: {data['REQUEST'][:200]}...
                    """
                    analysis_texts.append(analysis_text.strip())
            
            if analysis_texts:
                # Identify high-risk customers
                churn_risk = self.ai.ai_agg(
                    analysis_texts,
                    "Identify the top 5 customers most at risk of churning based on their support ticket patterns and sentiment. Explain why each is at risk."
                )
                
                # Retention strategies
                retention_strategies = self.ai.ai_complete(
                    f"Based on this churn risk analysis, provide specific retention strategies for high-risk telco customers: {churn_risk[:300]}...",
                    max_tokens=700
                )
                
                return {
                    "churn_risk_analysis": churn_risk,
                    "retention_strategies": retention_strategies,
                    "customers_analyzed": len(analysis_texts)
                }
            else:
                return {"churn_risk_analysis": "Insufficient data for churn analysis"}
                
        except Exception as e:
            st.error(f"Churn Analysis Error: {e}")
            return {"churn_risk_analysis": "Unable to perform churn analysis at this time."}


# Utility functions for common AI operations
def get_ai_processor(session) -> TelcoAISQLProcessor:
    """
    Get initialized AI processor instance
    
    Args:
        session: Snowflake session
        
    Returns:
        TelcoAISQLProcessor instance
    """
    return TelcoAISQLProcessor(session)

def get_ai_analytics(session) -> TelcoAIAnalytics:
    """
    Get initialized AI analytics instance
    
    Args:
        session: Snowflake session
        
    Returns:
        TelcoAIAnalytics instance
    """
    ai_processor = get_ai_processor(session)
    return TelcoAIAnalytics(session, ai_processor)

def format_ai_response(response: str, title: str = "AI Insights") -> None:
    """
    Format and display AI response in Streamlit
    
    Args:
        response: AI generated response
        title: Title for the response section
    """
    if response:
        st.markdown(f"### 🤖 {title}")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%); 
                    padding: 1.5rem; border-radius: 12px; margin: 1rem 0; 
                    border-left: 4px solid #2196f3; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
            <div style="color: #1565c0; line-height: 1.6;">{response}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(f"No {title.lower()} available at this time.")

def create_ai_metric_card(title: str, value: str, description: str = "", icon: str = "🤖") -> None:
    """
    Create AI-specific metric card
    
    Args:
        title: Card title
        value: Main value to display
        description: Additional description
        icon: Icon to display
    """
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #4caf50; margin-bottom: 1rem;">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
            <h4 style="margin: 0; color: #2e7d32; font-weight: 600;">{title}</h4>
        </div>
        <div style="font-size: 1.25rem; font-weight: 500; color: #1565c0; margin-bottom: 0.5rem;">{value}</div>
        {f'<div style="color: #6c757d; font-size: 0.9rem;">{description}</div>' if description else ''}
    </div>
    """, unsafe_allow_html=True)

class AIPerformanceMonitor:
    """
    Performance monitoring and cost tracking for AI operations
    """
    
    def __init__(self):
        self.metrics = {
            'total_calls': 0,
            'total_tokens': 0,
            'total_time': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'errors': 0,
            'model_usage': {},
            'cost_estimate': 0.0
        }
        self.lock = threading.Lock()
    
    def log_operation(self, model: str, tokens: int, duration: float, cached: bool = False, error: bool = False):
        """Log an AI operation for monitoring"""
        with self.lock:
            self.metrics['total_calls'] += 1
            self.metrics['total_tokens'] += tokens
            self.metrics['total_time'] += duration
            
            if cached:
                self.metrics['cache_hits'] += 1
            else:
                self.metrics['cache_misses'] += 1
            
            if error:
                self.metrics['errors'] += 1
            
            if model not in self.metrics['model_usage']:
                self.metrics['model_usage'][model] = 0
            self.metrics['model_usage'][model] += 1
            
            # Rough cost estimation (tokens * $0.002 per 1K tokens average)
            self.metrics['cost_estimate'] += (tokens / 1000) * 0.002
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        with self.lock:
            metrics = self.metrics.copy()
            metrics['cache_hit_rate'] = (
                metrics['cache_hits'] / max(1, metrics['cache_hits'] + metrics['cache_misses'])
            ) * 100
            metrics['avg_response_time'] = metrics['total_time'] / max(1, metrics['total_calls'])
            metrics['error_rate'] = (metrics['errors'] / max(1, metrics['total_calls'])) * 100
            return metrics
    
    def reset_metrics(self):
        """Reset all performance metrics"""
        with self.lock:
            self.metrics = {
                'total_calls': 0,
                'total_tokens': 0,
                'total_time': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'errors': 0,
                'model_usage': {},
                'cost_estimate': 0.0
            }

class AITestSuite:
    """
    Comprehensive testing suite for AISQL integrations
    """
    
    def __init__(self, processor: TelcoAISQLProcessor, analytics: TelcoAIAnalytics):
        self.processor = processor
        self.analytics = analytics
        self.test_results = []
    
    def run_basic_tests(self) -> Dict[str, Any]:
        """Run basic functionality tests"""
        results = {
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'details': []
        }
        
        # Test AI Complete
        try:
            response = self.processor.ai_complete("Say 'Hello' in one word", max_tokens=10)
            success = len(response) > 0 and response.lower().find('hello') >= 0
            results['details'].append({
                'test': 'AI Complete Basic',
                'status': 'PASS' if success else 'FAIL',
                'response_length': len(response)
            })
            if success:
                results['tests_passed'] += 1
            else:
                results['tests_failed'] += 1
        except Exception as e:
            results['details'].append({
                'test': 'AI Complete Basic',
                'status': 'ERROR',
                'error': str(e)
            })
            results['tests_failed'] += 1
        
        results['tests_run'] += 1
        
        # Test AI Classify
        try:
            result = self.processor.ai_classify("This is excellent service!", ["positive", "negative", "neutral"])
            success = result in ["positive", "negative", "neutral"]
            results['details'].append({
                'test': 'AI Classify Basic',
                'status': 'PASS' if success else 'FAIL',
                'result': result
            })
            if success:
                results['tests_passed'] += 1
            else:
                results['tests_failed'] += 1
        except Exception as e:
            results['details'].append({
                'test': 'AI Classify Basic',
                'status': 'ERROR',
                'error': str(e)
            })
            results['tests_failed'] += 1
        
        results['tests_run'] += 1
        
        # Test AI Sentiment
        try:
            sentiment = self.processor.ai_sentiment("I love this service!")
            success = isinstance(sentiment, float) and -1 <= sentiment <= 1
            results['details'].append({
                'test': 'AI Sentiment Basic',
                'status': 'PASS' if success else 'FAIL',
                'sentiment_score': sentiment
            })
            if success:
                results['tests_passed'] += 1
            else:
                results['tests_failed'] += 1
        except Exception as e:
            results['details'].append({
                'test': 'AI Sentiment Basic',
                'status': 'ERROR',
                'error': str(e)
            })
            results['tests_failed'] += 1
        
        results['tests_run'] += 1
        return results
    
    def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance and load tests"""
        results = {
            'response_times': [],
            'cache_performance': {},
            'model_comparison': {}
        }
        
        test_prompt = "Analyze network performance in one sentence."
        
        # Test response times
        for i in range(3):
            start_time = time.time()
            try:
                self.processor.ai_complete(test_prompt, max_tokens=50)
                response_time = time.time() - start_time
                results['response_times'].append(response_time)
            except Exception:
                results['response_times'].append(None)
        
        # Test caching
        start_time = time.time()
        self.processor.ai_complete("Cache test query", max_tokens=20)
        first_time = time.time() - start_time
        
        start_time = time.time()
        self.processor.ai_complete("Cache test query", max_tokens=20)
        second_time = time.time() - start_time
        
        results['cache_performance'] = {
            'first_call': first_time,
            'second_call': second_time,
            'improvement': max(0, first_time - second_time)
        }
        
        return results

def create_ai_cost_dashboard(monitor: AIPerformanceMonitor):
    """Create a cost monitoring dashboard"""
    metrics = monitor.get_metrics()
    
    st.markdown("### 💰 AI Cost & Performance Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total AI Calls", f"{metrics['total_calls']:,}")
    
    with col2:
        st.metric("Total Tokens", f"{metrics['total_tokens']:,}")
    
    with col3:
        st.metric("Est. Cost", f"${metrics['cost_estimate']:.2f}")
    
    with col4:
        st.metric("Cache Hit Rate", f"{metrics['cache_hit_rate']:.1f}%")
    
    # Performance metrics
    st.markdown("#### 📊 Performance Metrics")
    perf_col1, perf_col2, perf_col3 = st.columns(3)
    
    with perf_col1:
        st.metric("Avg Response Time", f"{metrics['avg_response_time']:.2f}s")
    
    with perf_col2:
        st.metric("Error Rate", f"{metrics['error_rate']:.1f}%")
    
    with perf_col3:
        st.metric("Total Operations", f"{metrics['cache_hits'] + metrics['cache_misses']:,}")

@st.cache_resource
def get_performance_monitor() -> AIPerformanceMonitor:
    """Get cached performance monitor instance"""
    return AIPerformanceMonitor()

@st.cache_resource
def get_ai_test_suite(session) -> AITestSuite:
    """
    Get cached AI test suite instance
    
    Args:
        session: Snowflake session
        
    Returns:
        AITestSuite: Test suite instance
    """
    processor = get_ai_processor(session)
    analytics = get_ai_analytics(session)
    return AITestSuite(processor, analytics)
