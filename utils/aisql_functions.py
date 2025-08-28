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
            'mistral-large', 'mistral-7b', 'mixtral-8x7b',
            'llama3.1-8b', 'llama3.1-70b', 'llama3.1-405b',
            'reka-core', 'reka-flash',
            'snowflake-arctic',
            'gemma-7b'
        ]
        self.default_model = 'mistral-large'
        
    def ai_complete(self, prompt: str, model: str = None, max_tokens: int = 500) -> str:
        """
        Generate AI completions using Snowflake Cortex AI_COMPLETE
        
        Args:
            prompt: The input prompt for completion
            model: LLM model to use (default: mistral-large)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated completion text
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
            categories_str = str(categories).replace("'", "''")
            text_escaped = text.replace("'", "''")
            
            query = f"""
            SELECT SNOWFLAKE.CORTEX.AI_CLASSIFY(
                '{text_escaped}', 
                {categories_str}
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
        Aggregate insights from multiple text inputs
        
        Args:
            texts: List of text inputs to aggregate
            prompt: Prompt describing what insights to extract
            
        Returns:
            Aggregated insights
        """
        try:
            # Create temporary table with texts
            text_data = [{"text": text} for text in texts]
            temp_df = self.session.create_dataframe(text_data)
            temp_table = f"temp_agg_table_{int(time.time())}"
            temp_df.write.save_as_table(temp_table, mode="overwrite", table_type="temporary")
            
            prompt_escaped = prompt.replace("'", "''")
            
            query = f"""
            SELECT SNOWFLAKE.CORTEX.AI_AGG(
                text, 
                '{prompt_escaped}'
            ) as aggregated_insights
            FROM {temp_table}
            """
            result = self.session.sql(query).collect()
            return result[0]['AGGREGATED_INSIGHTS'] if result else ""
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
        Summarize multiple texts together
        
        Args:
            texts: List of texts to summarize
            
        Returns:
            Aggregated summary
        """
        try:
            # Create temporary table with texts
            text_data = [{"text": text} for text in texts]
            temp_df = self.session.create_dataframe(text_data)
            temp_table = f"temp_summary_table_{int(time.time())}"
            temp_df.write.save_as_table(temp_table, mode="overwrite", table_type="temporary")
            
            query = f"""
            SELECT SNOWFLAKE.CORTEX.AI_SUMMARIZE_AGG(text) as summary
            FROM {temp_table}
            """
            result = self.session.sql(query).collect()
            return result[0]['SUMMARY'] if result else ""
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
                # Root cause analysis
                insights['root_causes'] = self.ai.ai_agg(
                    issues,
                    "Identify the top 3 root causes of network failures based on the technical metrics provided"
                )
                
                # Priority recommendations
                insights['recommendations'] = self.ai.ai_agg(
                    issues,
                    "Provide 5 specific technical recommendations to resolve these network issues, prioritized by impact"
                )
                
                # Risk assessment
                insights['risk_assessment'] = self.ai.ai_complete(
                    f"Based on these network issues, provide a risk assessment for customer impact and business continuity: {issues[0][:500]}..."
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
            As a senior telco network analyst, provide an executive summary based on this data:
            
            {context}
            
            Include:
            1. Overall network health status
            2. Key performance indicators
            3. Critical issues requiring immediate attention
            4. Customer satisfaction insights
            5. Strategic recommendations for the next quarter
            
            Keep it concise, executive-level, and actionable.
            """
            
            return self.ai.ai_complete(prompt, max_tokens=800)
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
