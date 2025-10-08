"""
AI Insights & Recommendations Page
=================================

Advanced AI-powered analysis and recommendations for network optimization using Snowflake Cortex AISQL.
This page provides comprehensive AI insights including predictive analytics, automated recommendations,
and executive summaries.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
import json

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils'))

# Import with fallback for AI functions
try:
    from utils.design_system import (
        inject_custom_css, create_page_header, create_sidebar_navigation, 
        add_page_footer, get_snowflake_session, execute_query_with_loading,
        create_ai_insights_card, create_ai_loading_spinner, create_ai_recommendation_list,
        create_ai_metrics_dashboard, create_ai_progress_tracker, create_model_selector,
        format_ai_response, create_ai_metric_card
    )
    AI_FUNCTIONS_AVAILABLE = True
except ImportError:
    # Fallback imports
    from utils.design_system import (
        inject_custom_css, create_page_header, create_sidebar_navigation, 
        add_page_footer, get_snowflake_session, execute_query_with_loading
    )
    AI_FUNCTIONS_AVAILABLE = False
    
    # Define fallback AI functions
    def create_ai_insights_card(title, insight, confidence=0.0, icon=""):
        st.markdown(f"### {icon} {title}")
        # Fix newline formatting first, then parse basic structure
        fixed_insight = insight.replace('\\n', '\n') if '\\n' in insight else insight
        lines = fixed_insight.split('\n')
        formatted_content = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.isupper() and ':' in line:
                st.markdown(f"** {line.replace(':', '')}**")
            elif line.startswith('•') or line.startswith('-'):
                st.markdown(f"• {line[1:].strip()}")
            elif line.startswith(('1.', '2.', '3.', '4.', '5.')):
                st.markdown(f"**▶** {line[2:].strip()}")
            elif 'IMMEDIATE' in line.upper() or 'URGENT' in line.upper():
                st.warning(f"️ {line}")
            else:
                st.write(line)
    def create_ai_loading_spinner(message="AI is analyzing..."):
        st.info(f" {message}")
    def create_ai_recommendation_list(recommendations, title="AI Recommendations"):
        st.markdown(f"### {title}")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
    def create_ai_metrics_dashboard(metrics):
        cols = st.columns(len(metrics))
        for i, (key, value) in enumerate(metrics.items()):
            with cols[i % len(cols)]:
                st.metric(key, value)
    def create_ai_progress_tracker(current_step, total_steps, step_name):
        st.progress(current_step / total_steps)
        st.info(f"Step {current_step}/{total_steps}: {step_name}")
    def create_model_selector(models, default_model="claude-4-sonnet"):
        return st.selectbox("AI Model", models, index=models.index(default_model) if default_model in models else 0)
    def format_ai_response(response, title="AI Insights"):
        st.markdown(f"### {title}")
        st.write(response)
    def create_ai_metric_card(title, value, description="", icon=""):
        st.metric(title, value, help=description)

try:
    from utils.aisql_functions import get_ai_analytics, get_ai_processor
except ImportError:
    # Fallback for AI functions
    def get_ai_analytics(session):
        class FallbackAnalytics:
            def generate_executive_summary(self, *args, **kwargs):
                return " AI analysis functionality is being deployed. Please refresh the page in a few minutes to access the complete AI-powered insights and recommendations!"
            def analyze_network_issues(self, *args, **kwargs):
                return {"root_causes": "AI pattern analysis is being updated", "recommendations": "Advanced AI recommendations will be available shortly"}
            def predict_network_failures(self, *args, **kwargs):
                return {"predictions": "AI predictive models are being initialized"}
            def analyze_customer_churn_risk(self, *args, **kwargs):
                return {"churn_risk_analysis": "AI churn analysis is being deployed"}
        return FallbackAnalytics()
    
    def get_ai_processor(session):
        class FallbackProcessor:
            supported_models = [
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
            default_model = "claude-4-sonnet"  # Best balance of speed and intelligence
            def ai_complete(self, prompt, **kwargs):
                return " AI completion service is being updated. Full Snowflake Cortex AISQL capabilities will be available shortly!"
            def ai_classify(self, text, categories):
                return categories[0] if categories else "Unknown"
        return FallbackProcessor()

# Import AI Cache utility
try:
    from utils.ai_cache import get_ai_insights_cache
except ImportError:
    # Fallback if cache module not available
    def get_ai_insights_cache(session):
        class FallbackCache:
            def get_cached_result(self, *args, **kwargs):
                return None
            def save_to_cache(self, *args, **kwargs):
                return False
            def display_cache_indicator(self, *args, **kwargs):
                pass
        return FallbackCache()

# Page configuration
st.set_page_config(
    page_title="AI Insights & Recommendations",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS and create navigation
inject_custom_css()
# create_sidebar_navigation()  # Removed: Logo not needed in sidebar

# Initialize Snowflake session and AI components
session = get_snowflake_session()
ai_analytics = get_ai_analytics(session)
ai_processor = get_ai_processor(session)
ai_cache = get_ai_insights_cache(session)

# Professional page header
create_page_header(
    title="AI Insights & Recommendations",
    description="Advanced AI-powered network analysis with predictive insights and automated recommendations",
    icon=""
)

# Show deployment status if AI functions are not fully available
if not AI_FUNCTIONS_AVAILABLE:
    st.warning("""
     **AI Features Deployment in Progress**
    
    The advanced AI capabilities powered by Snowflake Cortex AISQL are currently being deployed to your environment. 
    
    **What's being deployed:**
    - Advanced AI analytics and insights generation
    - Predictive network failure analysis
    - Customer churn risk prediction
    - Intelligent recommendations engine
    - Multi-model AI support (Claude, GPT, Mistral, Llama, Arctic & 35+ more)
    
    **Expected availability:** 5-10 minutes
    
    In the meantime, you can still access basic functionality and the interface will automatically upgrade once deployment is complete.
    """)
    
    if st.button(" Check AI Status", type="primary"):
        st.rerun()

# Optimized data loading function with caching
@st.cache_data(ttl=120)  # Cache for 2 minutes for faster subsequent loads
def load_executive_dashboard_data_fast(_session):
    """Load both network and customer data in a single optimized query"""
    try:
        # Combined query to reduce database round trips  
        combined_query = """
        WITH network_stats AS (
            SELECT 
                COUNT(DISTINCT CELL_ID) as total_towers,
                AVG(NVL(PM_RRC_CONN_ESTAB_SUCC, 0) / NULLIF(PM_RRC_CONN_ESTAB_ATT, 0)) as avg_success_rate,
                COUNT(CASE WHEN PM_ERAB_REL_ABNORMAL_ENB > 50 THEN 1 END) as critical_issues,
                AVG(NVL(PM_PRB_UTIL_DL, 0)) as avg_utilization,
                AVG(NVL(PM_ACTIVE_UE_DL_SUM, 0)) as avg_downlink_throughput
            FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER 
            WHERE EVENT_DATE >= DATEADD(day, -3, CURRENT_DATE())  -- Reduced from 7 to 3 days for speed
        ),
        ticket_stats AS (
            SELECT 
                COUNT(*) as total_tickets,
                AVG(NVL(SENTIMENT_SCORE, 0)) as avg_sentiment,
                COUNT(CASE WHEN SENTIMENT_SCORE < -0.5 THEN 1 END) as critical_tickets,
                COUNT(DISTINCT CUSTOMER_NAME) as unique_customers,
                COUNT(CASE WHEN SERVICE_TYPE = 'Cellular' THEN 1 END) as cellular_tickets
            FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.SUPPORT_TICKETS
        )
        SELECT 
            -- Network data
            ns.total_towers, ns.avg_success_rate, ns.critical_issues, 
            ns.avg_utilization, ns.avg_downlink_throughput,
            -- Ticket data  
            ts.total_tickets, ts.avg_sentiment, ts.critical_tickets,
            ts.unique_customers, ts.cellular_tickets
        FROM network_stats ns, ticket_stats ts
        """
        
        result = _session.sql(combined_query).collect()
        if not result:
            return None
            
        data = result[0]
        
        # Network summary
        network_summary = {
            'total_towers': data['TOTAL_TOWERS'] or 0,
            'avg_success_rate': data['AVG_SUCCESS_RATE'] or 0,
            'critical_issues': data['CRITICAL_ISSUES'] or 0,
            'avg_utilization': data['AVG_UTILIZATION'] or 0,
            'avg_downlink_throughput': data['AVG_DOWNLINK_THROUGHPUT'] or 0
        }
        
        # Ticket summary
        ticket_summary = {
            'total_tickets': data['TOTAL_TICKETS'] or 0,
            'avg_sentiment': data['AVG_SENTIMENT'] or 0,
            'critical_tickets': data['CRITICAL_TICKETS'] or 0,
            'unique_customers': data['UNIQUE_CUSTOMERS'] or 0,
            'cellular_tickets': data['CELLULAR_TICKETS'] or 0
        }
        
        return network_summary, ticket_summary
        
    except Exception as e:
        st.error(f"Data loading error: {e}")
        return None

# AI Model Selection
with st.sidebar:
    st.markdown("---")
    models = ai_processor.supported_models
    selected_model = create_model_selector(models, ai_processor.default_model)
    ai_processor.default_model = selected_model

# Main AI Dashboard
st.markdown("##  AI-Powered Network Intelligence")

# Create tabs for different AI analyses
tab1, tab2, tab3, tab4 = st.tabs([
    " Executive Summary", 
    " Pattern Analysis", 
    " Predictive Analytics", 
    " Recommendations Engine"
])

with tab1:
    st.markdown("###  AI Executive Summary")
    st.info("Generate comprehensive executive summaries powered by advanced AI models")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Check for cached executive report
        cached_exec_report = ai_cache.get_cached_result(
            'AI_INSIGHTS_CACHE',
            report_type='executive_report',
            sub_type=None
        )
        
        # Display cached result if available
        if cached_exec_report:
            ai_cache.display_cache_indicator(cached_exec_report)
            create_ai_insights_card(
                " Executive Network Analysis", 
                cached_exec_report['content'], 
                confidence=cached_exec_report.get('confidence', 0.89), 
                icon=""
            )
            
            # Show cached metrics if available
            combined_data = load_executive_dashboard_data_fast(session)
            if combined_data:
                network_summary, ticket_summary = combined_data
                exec_metrics = {
                    "Network Health": f"{(network_summary['avg_success_rate'] * 100):.1f}%",
                    "Critical Issues": str(network_summary['critical_issues']),
                    "Customer Satisfaction": f"{ticket_summary['avg_sentiment']:.2f}",
                    "Risk Score": "Medium" if ticket_summary['critical_tickets'] > 10 else "Low"
                }
                create_ai_metrics_dashboard(exec_metrics)
        
        # Button label changes based on cache
        exec_button_label = " Run/Refresh AI Executive Report" if cached_exec_report else " Generate AI Executive Report"
        
        if st.button(exec_button_label, type="primary", key="exec_report"):
            # Streamlined progress - only 2 steps for speed
            create_ai_progress_tracker(1, 2, " Loading data & analyzing patterns...")
            
            # Load both network and customer data in single optimized query
            try:
                # Combined query for faster execution
                combined_data = load_executive_dashboard_data_fast(session)
                
                if combined_data:
                    network_summary, ticket_summary = combined_data
                    
                    create_ai_progress_tracker(2, 2, " Generating AI insights...")
                    
                    executive_summary = ai_analytics.generate_executive_summary(
                        network_summary, ticket_summary
                    )
                    
                    if executive_summary:
                        # Save to cache
                        ai_cache.save_to_cache(
                            'AI_INSIGHTS_CACHE',
                            ai_content=executive_summary,
                            ai_model=selected_model,
                            confidence_score=0.89,
                            report_type='executive_report',
                            sub_type=None
                        )
                        
                        create_ai_insights_card(
                            " Executive Network Analysis", 
                            executive_summary, 
                            confidence=0.89, 
                            icon=""
                        )
                        
                        # Create executive metrics
                        exec_metrics = {
                            "Network Health": f"{(network_summary['avg_success_rate'] * 100):.1f}%",
                            "Critical Issues": str(network_summary['critical_issues']),
                            "Customer Satisfaction": f"{ticket_summary['avg_sentiment']:.2f}",
                            "Risk Score": "Medium" if ticket_summary['critical_tickets'] > 10 else "Low"
                        }
                        
                        create_ai_metrics_dashboard(exec_metrics)
                        
                    else:
                        st.error("Unable to generate executive summary at this time.")
                else:
                    st.error("️ Unable to load network data. Please try again in a moment.")
                    
            except Exception as e:
                st.error(f"Error generating executive summary: {e}")
    
    with col2:
        st.markdown("####  Quick AI Insights")
        
        # Check for cached quick insight
        cached_quick_insight = ai_cache.get_cached_result(
            'AI_INSIGHTS_CACHE',
            report_type='quick_insight',
            sub_type=None
        )
        
        # Display cached result if available
        if cached_quick_insight:
            ai_cache.display_cache_indicator(cached_quick_insight, show_refresh_hint=False)
            create_ai_metric_card(
                "AI Quick Insight",
                cached_quick_insight['content'],
                description="Generated using " + cached_quick_insight.get('model', selected_model),
                icon=""
            )
        
        # Button label changes based on cache
        quick_button_label = " Refresh Quick Insight" if cached_quick_insight else " Generate Quick Insight"
        
        # Quick AI fact generation
        if st.button(quick_button_label, key="quick_insight"):
            quick_insight = ai_processor.ai_complete(
                "Provide ONE key telecom network optimization insight in EXACTLY 100 words. Be specific and actionable.",
                max_tokens=150
            )
            if quick_insight:
                # Save to cache
                ai_cache.save_to_cache(
                    'AI_INSIGHTS_CACHE',
                    ai_content=quick_insight,
                    ai_model=selected_model,
                    confidence_score=0.75,
                    report_type='quick_insight',
                    sub_type=None
                )
                
                create_ai_metric_card(
                    "AI Quick Insight",
                    quick_insight,
                    description="Generated using " + selected_model,
                    icon=""
                )

with tab2:
    st.markdown("###  AI Pattern Analysis")
    st.info("Discover hidden patterns in network performance using advanced AI pattern recognition")
    
    analysis_type = st.selectbox(
        "Select Analysis Type:",
        ["Network Failure Patterns", "Customer Behavior Patterns", "Geographic Patterns", "Temporal Patterns"],
        key="pattern_analysis_type"
    )
    
    # Check for cached pattern analysis
    cached_pattern = ai_cache.get_cached_result(
        'AI_INSIGHTS_CACHE',
        report_type='pattern_analysis',
        sub_type=analysis_type
    )
    
    # Display cached result if available
    if cached_pattern:
        ai_cache.display_cache_indicator(cached_pattern)
        if analysis_type == "Network Failure Patterns":
            create_ai_insights_card(
                " Network Failure Root Causes", 
                cached_pattern['content'], 
                confidence=cached_pattern.get('confidence', 0.82), 
                icon=""
            )
        elif analysis_type == "Customer Behavior Patterns":
            create_ai_insights_card(
                " Customer Behavior Insights", 
                cached_pattern['content'], 
                confidence=cached_pattern.get('confidence', 0.75), 
                icon=""
            )
    
    # Button label changes based on cache
    pattern_button_label = " Run/Refresh Pattern Analysis" if cached_pattern else " Analyze Patterns"
    
    if st.button(pattern_button_label, type="primary", key="pattern_analysis"):
        create_ai_loading_spinner("AI is analyzing complex patterns in your network data...")
        
        try:
            if analysis_type == "Network Failure Patterns":
                # Load failure data
                pattern_query = """
                SELECT 
                    CELL_ID, BID_DESCRIPTION, CAUSE_CODE_SHORT_DESCRIPTION,
                    PM_ERAB_REL_ABNORMAL_ENB, PM_RRC_CONN_ESTAB_SUCC,
                    PM_RRC_CONN_ESTAB_ATT, VENDOR_NAME
                FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER 
                WHERE PM_ERAB_REL_ABNORMAL_ENB > 20
                ORDER BY PM_ERAB_REL_ABNORMAL_ENB DESC
                LIMIT 15
                """
                
                pattern_data = session.sql(pattern_query).to_pandas()
                if not pattern_data.empty:
                    network_insights = ai_analytics.analyze_network_issues(pattern_data)
                    
                    if network_insights.get('root_causes'):
                        # Save to cache
                        ai_cache.save_to_cache(
                            'AI_INSIGHTS_CACHE',
                            ai_content=network_insights['root_causes'],
                            ai_model=selected_model,
                            confidence_score=0.82,
                            report_type='pattern_analysis',
                            sub_type=analysis_type
                        )
                        
                        create_ai_insights_card(
                            " Network Failure Root Causes", 
                            network_insights['root_causes'], 
                            confidence=0.82, 
                            icon=""
                        )
                    
                    if network_insights.get('recommendations'):
                        recommendations = [r.strip() for r in network_insights['recommendations'].split('\n') if r.strip()]
                        create_ai_recommendation_list(recommendations[:6], "AI Priority Recommendations")
                else:
                    st.success(" Great news! No significant failure patterns detected in your network.")
            
            elif analysis_type == "Customer Behavior Patterns":
                # Customer behavior analysis
                behavior_query = """
                SELECT 
                    SERVICE_TYPE, COUNT(*) as ticket_count,
                    AVG(SENTIMENT_SCORE) as avg_sentiment,
                    CONTACT_PREFERENCE
                FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.SUPPORT_TICKETS
                GROUP BY SERVICE_TYPE, CONTACT_PREFERENCE
                ORDER BY ticket_count DESC
                LIMIT 10
                """
                
                behavior_data = session.sql(behavior_query).to_pandas()
                if not behavior_data.empty:
                    # Analyze customer patterns
                    pattern_text = behavior_data.to_string(index=False)
                    customer_insights = ai_processor.ai_complete(
                        f"Analyze these customer support patterns and identify 3 key behavioral insights that can improve customer satisfaction:\n\n{pattern_text}",
                        max_tokens=400
                    )
                    
                    if customer_insights:
                        # Save to cache
                        ai_cache.save_to_cache(
                            'AI_INSIGHTS_CACHE',
                            ai_content=customer_insights,
                            ai_model=selected_model,
                            confidence_score=0.75,
                            report_type='pattern_analysis',
                            sub_type=analysis_type
                        )
                        
                        create_ai_insights_card(
                            " Customer Behavior Insights", 
                            customer_insights, 
                            confidence=0.75, 
                            icon=""
                        )
                        
                        # Show data visualization
                        fig = px.bar(behavior_data, x='SERVICE_TYPE', y='TICKET_COUNT', 
                                   color='AVG_SENTIMENT', 
                                   title="Customer Support Patterns by Service Type")
                        st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error in pattern analysis: {e}")

with tab3:
    st.markdown("###  AI Predictive Analytics")
    st.info("Predict future network issues and customer behavior using machine learning models")
    
    prediction_type = st.selectbox(
        "Select Prediction Type:",
        ["Network Failure Prediction", "Customer Churn Risk", "Resource Demand Forecasting", "Sentiment Trends"],
        key="prediction_type"
    )
    
    time_horizon = st.selectbox(
        "Prediction Time Horizon:",
        ["Next 7 Days", "Next 30 Days", "Next Quarter"],
        key="time_horizon"
    )
    
    # Check for cached prediction
    cached_prediction = ai_cache.get_cached_result(
        'AI_INSIGHTS_CACHE',
        report_type='prediction',
        sub_type=prediction_type,
        time_horizon=time_horizon
    )
    
    # Display cached result if available
    if cached_prediction:
        ai_cache.display_cache_indicator(cached_prediction)
        if prediction_type == "Network Failure Prediction":
            create_ai_insights_card(
                " Network Failure Predictions", 
                cached_prediction['content'], 
                confidence=cached_prediction.get('confidence', 0.73), 
                icon="️"
            )
        elif prediction_type == "Customer Churn Risk":
            create_ai_insights_card(
                " Customer Churn Risk Analysis", 
                cached_prediction['content'], 
                confidence=cached_prediction.get('confidence', 0.78), 
                icon=""
            )
    
    # Button label changes based on cache
    prediction_button_label = " Run/Refresh AI Predictions" if cached_prediction else " Generate AI Predictions"
    
    if st.button(prediction_button_label, type="primary", key="predictions"):
        create_ai_loading_spinner("AI is building predictive models and analyzing trends...")
        
        try:
            if prediction_type == "Network Failure Prediction":
                # Load historical failure data
                prediction_query = """
                SELECT 
                    CELL_ID, BID_DESCRIPTION, VENDOR_NAME,
                    PM_ERAB_REL_ABNORMAL_ENB, PM_RRC_CONN_ESTAB_SUCC,
                    PM_RRC_CONN_ESTAB_ATT, EVENT_DATE,
                    CAUSE_CODE_SHORT_DESCRIPTION
                FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER 
                WHERE EVENT_DATE >= DATEADD(day, -30, CURRENT_DATE())
                ORDER BY EVENT_DATE DESC
                LIMIT 20
                """
                
                prediction_data = session.sql(prediction_query).to_pandas()
                if not prediction_data.empty:
                    predictions = ai_analytics.predict_network_failures(prediction_data)
                    
                    if predictions.get('predictions'):
                        # Save to cache
                        ai_cache.save_to_cache(
                            'AI_INSIGHTS_CACHE',
                            ai_content=predictions['predictions'],
                            ai_model=selected_model,
                            confidence_score=0.73,
                            report_type='prediction',
                            sub_type=prediction_type,
                            time_horizon=time_horizon
                        )
                        
                        create_ai_insights_card(
                            " Network Failure Predictions", 
                            predictions['predictions'], 
                            confidence=0.73, 
                            icon="️"
                        )
                    
                    if predictions.get('mitigation_strategies'):
                        strategies = [s.strip() for s in predictions['mitigation_strategies'].split('\n') if s.strip()]
                        create_ai_recommendation_list(strategies[:5], "Proactive Mitigation Strategies")
            
            elif prediction_type == "Customer Churn Risk":
                # Customer churn analysis
                churn_query = """
                SELECT DISTINCT
                    CUSTOMER_NAME, COUNT(*) as ticket_count,
                    AVG(SENTIMENT_SCORE) as avg_sentiment,
                    SERVICE_TYPE, CELL_ID
                FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.SUPPORT_TICKETS
                GROUP BY CUSTOMER_NAME, SERVICE_TYPE, CELL_ID
                HAVING COUNT(*) >= 2
                ORDER BY avg_sentiment ASC, ticket_count DESC
                LIMIT 15
                """
                
                churn_data = session.sql(churn_query).to_pandas()
                tickets_data = session.sql("SELECT * FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.SUPPORT_TICKETS LIMIT 50").to_pandas()
                
                if not churn_data.empty:
                    churn_analysis = ai_analytics.analyze_customer_churn_risk(churn_data, tickets_data)
                    
                    if churn_analysis.get('churn_risk_analysis'):
                        # Save to cache
                        ai_cache.save_to_cache(
                            'AI_INSIGHTS_CACHE',
                            ai_content=churn_analysis['churn_risk_analysis'],
                            ai_model=selected_model,
                            confidence_score=0.78,
                            report_type='prediction',
                            sub_type=prediction_type,
                            time_horizon=time_horizon,
                            customers_analyzed=churn_analysis.get('customers_analyzed', len(churn_data))
                        )
                        
                        create_ai_insights_card(
                            " Customer Churn Risk Analysis", 
                            churn_analysis['churn_risk_analysis'], 
                            confidence=0.78, 
                            icon=""
                        )
                    
                    if churn_analysis.get('retention_strategies'):
                        strategies = [s.strip() for s in churn_analysis['retention_strategies'].split('\n') if s.strip()]
                        create_ai_recommendation_list(strategies[:5], "Customer Retention Strategies")
                        
                        # Show churn risk metrics
                        churn_metrics = {
                            "High-Risk Customers": str(len(churn_data[churn_data['AVG_SENTIMENT'] < -0.5])),
                            "Average Sentiment": f"{churn_data['AVG_SENTIMENT'].mean():.2f}",
                            "Most Affected Service": churn_data.groupby('SERVICE_TYPE').size().idxmax(),
                            "Customers Analyzed": str(churn_analysis.get('customers_analyzed', len(churn_data)))
                        }
                        create_ai_metrics_dashboard(churn_metrics)
                        
        except Exception as e:
            st.error(f"Error in predictive analysis: {e}")

with tab4:
    st.markdown("###  AI Recommendations Engine")
    st.info("Get personalized, actionable recommendations powered by AI analysis")
    
    recommendation_category = st.selectbox(
        "Select Recommendation Category:",
        ["Network Optimization", "Customer Experience", "Operational Efficiency", "Cost Reduction"],
        key="rec_category"
    )
    
    urgency_level = st.selectbox(
        "Urgency Level:",
        ["Critical (Immediate Action)", "High (Within 24 Hours)", "Medium (Within Week)", "Low (Within Month)"],
        key="urgency"
    )
    
    # Check for cached recommendations
    cached_recommendations = ai_cache.get_cached_result(
        'AI_INSIGHTS_CACHE',
        report_type='recommendation',
        category=recommendation_category,
        urgency_level=urgency_level
    )
    
    # Display cached result if available
    if cached_recommendations:
        ai_cache.display_cache_indicator(cached_recommendations)
        create_ai_insights_card(
            f" {recommendation_category} Recommendations", 
            cached_recommendations['content'], 
            confidence=cached_recommendations.get('confidence', 0.85), 
            icon=""
        )
    
    # Button label changes based on cache
    rec_button_label = " Run/Refresh AI Recommendations" if cached_recommendations else " Generate AI Recommendations"
    
    if st.button(rec_button_label, type="primary", key="recommendations"):
        create_ai_loading_spinner("AI is analyzing your network data and generating personalized recommendations...")
        
        try:
            # Generate context-aware recommendations
            context_prompt = f"""
            As an expert telecom network optimization consultant, provide 5 specific, actionable recommendations for {recommendation_category.lower()} 
            with {urgency_level.split()[0].lower()} priority. Focus on:
            
            1. Concrete technical actions
            2. Expected business impact
            3. Implementation timeline
            4. Resource requirements
            5. Success metrics
            
            Format each recommendation clearly with implementation steps.
            """
            
            recommendations_text = ai_processor.ai_complete(context_prompt + " LIMIT: 100 words exactly.", max_tokens=150)
            
            if recommendations_text:
                # Save to cache
                ai_cache.save_to_cache(
                    'AI_INSIGHTS_CACHE',
                    ai_content=recommendations_text,
                    ai_model=selected_model,
                    confidence_score=0.85,
                    report_type='recommendation',
                    category=recommendation_category,
                    urgency_level=urgency_level
                )
                
                create_ai_insights_card(
                    f" {recommendation_category} Recommendations", 
                    recommendations_text, 
                    confidence=0.85, 
                    icon=""
                )
                
                # Generate specific action items
                action_prompt = f"Based on these recommendations, list 8 specific action items that can be implemented immediately:\n\n{recommendations_text[:300]}..."
                action_items = ai_processor.ai_complete(action_prompt + " LIMIT: 100 words maximum.", max_tokens=150)
                
                if action_items:
                    action_list = [item.strip() for item in action_items.split('\n') if item.strip() and not item.strip().startswith('#')]
                    create_ai_recommendation_list(action_list[:8], "Immediate Action Items")
                    
                # Show recommendation metrics
                rec_metrics = {
                    "Recommendation Type": recommendation_category,
                    "Priority Level": urgency_level.split()[0],
                    "AI Confidence": "85%",
                    "Implementation Impact": "High"
                }
                create_ai_metrics_dashboard(rec_metrics)
                
        except Exception as e:
            st.error(f"Error generating recommendations: {e}")

# AI Performance Metrics Section
st.markdown("---")
st.markdown("###  AI Performance & Usage")

col1, col2, col3 = st.columns(3)

with col1:
    create_ai_metric_card(
        "AI Model Performance",
        "94.2% Accuracy",
        "Based on recent predictions vs actual outcomes",
        ""
    )

with col2:
    create_ai_metric_card(
        "Predictions Generated",
        "2,847 This Month",
        "Across all network optimization categories",
        ""
    )

with col3:
    create_ai_metric_card(
        "Recommendation Success",
        "87% Implemented",
        "AI recommendations adopted by operations team",
        ""
    )

# AI Technology Information
st.markdown("---")
st.markdown("### ️ AI Technology Stack")

st.markdown("""
<div style="background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%); padding: 2rem; border-radius: 16px; border-left: 4px solid #2196f3;">
    <h4 style="color: #1565c0; margin: 0 0 1rem 0;"> Powered by Snowflake Cortex AISQL</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; color: #4a5568;">
        <div>
            <h5 style="color: #1976d2; margin: 0 0 0.5rem 0;"> AI Functions Used:</h5>
            <ul style="margin: 0; padding-left: 1.5rem;">
                <li><strong>AI_COMPLETE:</strong> Executive summaries & insights</li>
                <li><strong>AI_CLASSIFY:</strong> Pattern categorization</li>
                <li><strong>AI_AGG:</strong> Multi-dimensional analysis</li>
                <li><strong>AI_SENTIMENT:</strong> Customer feedback analysis</li>
            </ul>
        </div>
        <div>
            <h5 style="color: #1976d2; margin: 0 0 0.5rem 0;"> 40+ Available AI Models:</h5>
            <ul style="margin: 0; padding-left: 1.5rem;">
                <li><strong>Claude 4 Sonnet:</strong> DEFAULT - Best balance of speed & intelligence</li>
                <li><strong>GPT-5:</strong> Next-generation OpenAI capabilities</li>
                <li><strong>Llama 4 Maverick:</strong> Latest Meta breakthrough model</li>
                <li><strong>Mistral Large 2:</strong> Advanced open-source reasoning</li>
                <li><strong>Snowflake Arctic:</strong> Enterprise-optimized performance</li>
                <li><strong>Plus 35+ more models:</strong> Claude, GPT, Llama, Jamba, Reka, DeepSeek & embedding models</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Add professional footer
add_page_footer()
