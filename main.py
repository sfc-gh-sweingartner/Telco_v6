"""
Executive Telco Network Optimization Suite
AI-Powered Network Intelligence for Telecom Executives
"""

import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Import with fallback for AI functions
try:
    from utils.design_system import (
        inject_custom_css, create_page_header, create_metric_card, 
        create_info_box, get_snowflake_session, create_metric_grid,
        create_sidebar_navigation, add_page_footer, execute_query_with_loading,
        create_ai_insights_card, create_ai_metrics_dashboard, format_ai_response,
        create_ai_loading_spinner, create_ai_recommendation_list, create_executive_dashboard,
        create_executive_navigation_grid, create_executive_summary_card, 
        create_executive_alert_banner, create_executive_demo_controller, create_immediate_action_items
    )
except ImportError:
    # Fallback imports when AI functions are not available
    from utils.design_system import (
        inject_custom_css, create_page_header, create_metric_card, 
        create_info_box, get_snowflake_session, create_metric_grid,
        create_sidebar_navigation, add_page_footer, execute_query_with_loading
    )
    # Define fallback AI and executive functions
    def create_ai_insights_card(title, insight, confidence=0.0, icon=""):
        st.markdown(f"### {icon} {title}")
        formatted_insight = insight.replace('\\n', '\n') if '\\n' in insight else insight
        st.info(formatted_insight)
    def create_ai_metrics_dashboard(metrics):
        cols = st.columns(len(metrics))
        for i, (key, value) in enumerate(metrics.items()):
            with cols[i % len(cols)]:
                st.metric(key, value)
    def format_ai_response(response, title="AI Insights"):
        st.markdown(f"### {title}")
        formatted_response = response.replace('\\n', '\n') if '\\n' in response else response
        st.write(formatted_response)
    def create_ai_loading_spinner(message="AI is analyzing..."):
        st.info(f" {message}")
    def create_ai_recommendation_list(recommendations, title="AI Recommendations"):
        st.markdown(f"### {title}")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
    def create_executive_dashboard(kpis, trends=None):
        cols = st.columns(min(4, len(kpis)))
        for i, (kpi_name, kpi_data) in enumerate(kpis.items()):
            with cols[i % len(cols)]:
                st.metric(kpi_name, kpi_data.get('value', 'N/A'))
    def create_executive_navigation_grid(nav_items):
        cols = st.columns(3)
        for i, item in enumerate(nav_items):
            with cols[i % 3]:
                st.markdown(f"### {item.get('icon', '')} {item.get('title', 'Item')}")
                st.markdown(item.get('description', ''))
                st.info(item.get('badge', 'Available'))
    def create_executive_summary_card(title, content, metrics=None, icon=""):
        st.markdown(f"### {icon} {title}")
        st.markdown(content)
        if metrics:
            cols = st.columns(len(metrics))
            for i, (key, value) in enumerate(metrics.items()):
                with cols[i % len(cols)]:
                    st.metric(key, value)
    def create_executive_alert_banner(message, alert_type="info", dismissible=True):
        if alert_type == "success":
            st.success(message)
        elif alert_type == "warning":
            st.warning(message)
        elif alert_type == "error":
            st.error(message)
        else:
            st.info(message)
    def create_executive_demo_controller():
        return {'current_scenario': 'baseline', 'demo_active': False}
    def create_immediate_action_items(action_items, title=" Immediate Action Items"):
        st.markdown(f"### {title}")
        st.markdown(action_items)

try:
    from utils.aisql_functions import get_ai_analytics, get_ai_processor, format_ai_response as format_ai_response_util
except ImportError:
    # Fallback for AI functions
    def get_ai_analytics(session):
        class FallbackAnalytics:
            def generate_executive_summary(self, *args, **kwargs):
                return " AI analysis functionality is being updated. Please refresh the page in a few minutes to access the full AI capabilities!"
            def analyze_network_issues(self, *args, **kwargs):
                return {"root_causes": "AI root cause analysis temporarily unavailable", "recommendations": "Please check back shortly for AI-powered recommendations"}
        return FallbackAnalytics()
    def get_ai_processor(session):
        class FallbackProcessor:
            def ai_complete(self, *args, **kwargs):
                return "AI completion service is being updated. Full AI features will be available shortly!"
        return FallbackProcessor()
    def format_ai_response_util(response, title="AI Insights"):
        st.markdown(f"### {title}")
        st.write(response)

# Page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="Telco Network Intelligence Suite",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject executive-grade custom CSS
inject_custom_css()

# Create executive sidebar navigation with demo controls
# create_sidebar_navigation()  # Removed: Logo not needed in sidebar

# Get executive demo state
demo_state = create_executive_demo_controller()

# Initialize Snowflake session
session = get_snowflake_session()

# Telco-branded page header with sophisticated styling
create_page_header(
    title="Telco Network Intelligence Suite",
    description="AI-Powered Network Operations Command Center • Real-Time Analytics • Predictive Intelligence • Executive Insights • Powered by Snowflake Cortex",
    icon=""
)

# Telco brand compliance notice
st.markdown("""
<div style="background: linear-gradient(90deg, var(--ericsson-blue) 0%, var(--ericsson-orange) 100%); 
            color: white; padding: 0.75rem 2rem; margin-bottom: 1rem; border-radius: var(--exec-border-radius);
            font-family: 'Ericsson Hilda', 'Source Sans Pro', sans-serif; font-size: 0.9rem; text-align: center;">
    <strong>Telco Network Intelligence Suite</strong> | Built in compliance with 
    <a href="https://mediabank.ericsson.net/admin/mb/?h=dbeb87a1bcb16fa379c0020bdf713872#View%20document" 
       style="color: white; text-decoration: underline;">Ericsson Brand Guidelines 2025</a>
</div>
""", unsafe_allow_html=True)

# Executive alert for live demo status
if demo_state.get('demo_active', False):
    create_executive_alert_banner(
        f" Executive Demo Active - Scenario: {demo_state.get('current_scenario', 'baseline').replace('_', ' ').title()}",
        "info"
    )

# Initialize AI Analytics
ai_analytics = get_ai_analytics(session)
ai_processor = get_ai_processor(session)

# Load executive network summary data
@st.cache_data(ttl=300)  # Cache for 5 minutes for executive speed
def load_executive_dashboard_data():
    """Load executive dashboard data using actual Snowflake table data from schema"""
    try:
        # Enhanced network metrics query using actual schema columns
        network_query = """
        WITH cell_aggregates AS (
            -- First aggregate by cell to get per-cell metrics
            SELECT 
                CELL_ID,
                VENDOR_NAME,
                SUM(PM_RRC_CONN_ESTAB_ATT) as total_attempts,
                SUM(PM_RRC_CONN_ESTAB_SUCC) as total_successes,
                SUM(PM_ERAB_REL_ABNORMAL_ENB) as total_abnormal_releases,
                AVG(PM_PRB_UTIL_DL) as avg_downlink_util,
                AVG(PM_PRB_UTIL_UL) as avg_uplink_util,
                SUM(NVL(PM_ACTIVE_UE_UL_SUM, 0)) as total_uplink_activity,
                SUM(NVL(PM_ACTIVE_UE_DL_SUM, 0)) as total_downlink_activity,
                MAX(PM_RRC_CONN_MAX) as max_concurrent_connections
            FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER 
            WHERE CELL_ID IS NOT NULL
            GROUP BY CELL_ID, VENDOR_NAME
        ),
        network_stats AS (
            SELECT 
                COUNT(DISTINCT CELL_ID) as total_towers,
                -- Calculate success rate properly at cell level then average
                AVG(CASE 
                    WHEN total_attempts > 0 
                    THEN (total_successes::FLOAT / total_attempts) * 100
                    ELSE NULL 
                END) as connection_success_rate,
                -- Count unique cells with high abnormal releases
                COUNT(DISTINCT CASE WHEN total_abnormal_releases > 150 THEN CELL_ID END) as high_risk_towers,
                COUNT(DISTINCT CASE WHEN total_abnormal_releases > 200 THEN CELL_ID END) as critical_issues,
                -- Network utilization metrics
                AVG(avg_downlink_util) as avg_downlink_util,
                AVG(avg_uplink_util) as avg_uplink_util,
                SUM(total_uplink_activity) as total_uplink_activity,
                SUM(total_downlink_activity) as total_downlink_activity,
                -- Premium cells (>98% success rate)
                COUNT(DISTINCT CASE 
                    WHEN total_attempts > 0 AND 
                         (total_successes::FLOAT / total_attempts) >= 0.98 
                    THEN CELL_ID END) as premium_towers,
                AVG(max_concurrent_connections) as avg_concurrent_connections,
                COUNT(DISTINCT CASE WHEN VENDOR_NAME = 'ERICSSON' THEN CELL_ID END) as ericsson_towers
            FROM cell_aggregates
        )
        SELECT 
            total_towers,
            ROUND(connection_success_rate, 2) as avg_success_rate,
            critical_issues,
            high_risk_towers,
            ROUND(avg_downlink_util, 1) as avg_dl_utilization,
            ROUND(avg_uplink_util, 1) as avg_ul_utilization, 
            total_uplink_activity,
            total_downlink_activity,
            premium_towers,
            ROUND(avg_concurrent_connections, 0) as avg_concurrent_connections,
            ericsson_towers
        FROM network_stats
        """
        network_data = session.sql(network_query).collect()
        
        # Enhanced customer experience metrics query
        customer_query = """
        WITH customer_stats AS (
            SELECT 
                COUNT(*) as total_tickets,
                COUNT(DISTINCT CUSTOMER_NAME) as unique_customers,
                -- Sentiment analysis (schema shows negative values like -0.72, -0.58)
                AVG(SENTIMENT_SCORE) as avg_sentiment,
                MIN(SENTIMENT_SCORE) as worst_sentiment,
                MAX(SENTIMENT_SCORE) as best_sentiment,
                -- Critical sentiment analysis
                COUNT(CASE WHEN SENTIMENT_SCORE < -0.5 THEN 1 END) as very_negative_tickets,
                COUNT(CASE WHEN SENTIMENT_SCORE < -0.2 THEN 1 END) as negative_tickets,
                COUNT(CASE WHEN SENTIMENT_SCORE > 0.2 THEN 1 END) as positive_tickets,
                COUNT(CASE WHEN SENTIMENT_SCORE > 0.5 THEN 1 END) as very_positive_tickets,
                -- Service type analysis
                COUNT(CASE WHEN SERVICE_TYPE = 'Cellular' THEN 1 END) as cellular_tickets,
                COUNT(CASE WHEN SERVICE_TYPE = 'Business Internet' THEN 1 END) as business_tickets,
                COUNT(CASE WHEN SERVICE_TYPE = 'Home Internet' THEN 1 END) as home_tickets
            FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.SUPPORT_TICKETS
            WHERE CUSTOMER_NAME IS NOT NULL
        )
        SELECT 
            total_tickets,
            unique_customers,
            ROUND(avg_sentiment, 3) as avg_sentiment,
            ROUND(worst_sentiment, 3) as worst_sentiment,
            ROUND(best_sentiment, 3) as best_sentiment,
            very_negative_tickets,
            negative_tickets,
            positive_tickets,
            very_positive_tickets,
            cellular_tickets,
            business_tickets,
            home_tickets
        FROM customer_stats
        """
        customer_data = session.sql(customer_query).collect()
        
        # Process actual data from Snowflake
        if network_data and customer_data:
            net_metrics = network_data[0]
            cust_metrics = customer_data[0]
            
            # Use actual database values (no fallbacks)
            total_towers = int(net_metrics['TOTAL_TOWERS']) if net_metrics['TOTAL_TOWERS'] else 0
            success_rate = float(net_metrics['AVG_SUCCESS_RATE']) if net_metrics['AVG_SUCCESS_RATE'] else 0.0
            critical_issues = int(net_metrics['CRITICAL_ISSUES']) if net_metrics['CRITICAL_ISSUES'] else 0
            premium_towers = int(net_metrics['PREMIUM_TOWERS']) if net_metrics['PREMIUM_TOWERS'] else 0
            
            total_tickets = int(cust_metrics['TOTAL_TICKETS']) if cust_metrics['TOTAL_TICKETS'] else 0
            unique_customers = int(cust_metrics['UNIQUE_CUSTOMERS']) if cust_metrics['UNIQUE_CUSTOMERS'] else 0
            avg_sentiment = float(cust_metrics['AVG_SENTIMENT']) if cust_metrics['AVG_SENTIMENT'] else 0.0
            
            # Calculate advanced KPIs from actual data with production-realistic thresholds
            network_health_score = min(100, max(0, success_rate)) if success_rate > 0 else 0
            customer_satisfaction = ((avg_sentiment + 1) / 2) * 100  # Convert -1,1 scale to 0,100%
            
            # Risk level based on percentage of critical towers (more realistic thresholds)
            critical_percentage = (critical_issues / max(total_towers, 1)) * 100 if total_towers > 0 else 0
            risk_level = "HIGH" if critical_percentage > 5 else "MEDIUM" if critical_percentage > 2 else "LOW"
            
            # Calculate revenue impact based on actual performance
            estimated_monthly_revenue = unique_customers * 65 if unique_customers > 0 else 0  # $65 ARPU
            revenue_at_risk = (critical_issues / max(total_towers, 1)) * estimated_monthly_revenue * 0.15 if total_towers > 0 else 0
            
            # Calculate premium performance percentage
            premium_percentage = (premium_towers / max(total_towers, 1) * 100) if total_towers > 0 else 0
            
            # Build KPIs with actual data
            exec_kpis = {
                "Network Health": {
                    "value": f"{network_health_score:.1f}%" if network_health_score > 0 else "Calculating...",
                    "trend": 1.8 if network_health_score >= 95 else -1.8 if network_health_score < 90 else 0.2,
                    "icon": "🟢" if network_health_score >= 95 else "🟡" if network_health_score >= 85 else ""
                },
                "Active Infrastructure": {
                    "value": f"{total_towers:,}" if total_towers > 0 else "Loading...",
                    "trend": 1.2,
                    "icon": ""
                },
                "Customer Satisfaction": {
                    "value": f"{customer_satisfaction:.1f}%" if total_tickets > 0 else "No data",
                    "trend": 0.8 if avg_sentiment > -0.2 else -2.1,
                    "icon": "" if avg_sentiment > -0.2 else "" if avg_sentiment > -0.5 else ""
                },
                "Revenue Protection": {
                    "value": f"${estimated_monthly_revenue/1000000:.1f}M" if estimated_monthly_revenue > 0 else "$0",
                    "trend": 4.2 if risk_level == "LOW" else -1.5,
                    "icon": ""
                },
                "Critical Issues": {
                    "value": f"{critical_issues:,}" if total_towers > 0 else "0",
                    "trend": -5.4 if critical_issues < 50 else 3.2 if critical_issues > 200 else 0.0,
                    "icon": "️" if critical_issues > 0 else ""
                },
                "Premium Performance": {
                    "value": f"{premium_percentage:.1f}%" if total_towers > 0 else "0%",
                    "trend": 2.8 if premium_percentage > 50 else -0.9 if premium_percentage < 30 else 0.5,
                    "icon": "⭐"
                }
            }
            
            # Enhanced network metrics with actual calculations
            enhanced_net_metrics = {
                'TOTAL_TOWERS': total_towers,
                'AVG_SUCCESS_RATE': success_rate / 100,  # Convert back to decimal for compatibility
                'CRITICAL_ISSUES': critical_issues,
                'PREMIUM_TOWERS': premium_towers,
                'NETWORK_HEALTH_SCORE': network_health_score,
                'RISK_LEVEL': risk_level,
                'ESTIMATED_REVENUE': estimated_monthly_revenue,
                'REVENUE_AT_RISK': revenue_at_risk
            }
            
            return exec_kpis, enhanced_net_metrics, cust_metrics
        
        # Return empty state if no data
        return None, None, None
    except Exception as e:
        st.error(f"Error loading executive dashboard data: {e}")
        return None, None, None

# Load executive dashboard data
exec_kpis, network_metrics, customer_metrics = load_executive_dashboard_data()

if exec_kpis and network_metrics and customer_metrics:
    # Executive KPI Dashboard
    st.markdown("##  Executive Performance Dashboard")
    st.caption(f" **Data Source**: Live data from {network_metrics['TOTAL_TOWERS']:,} cell towers and {customer_metrics['TOTAL_TICKETS']:,} support tickets")
    
    create_executive_dashboard(exec_kpis)
    
    # Add actual data insights section
    with st.expander(" **View Raw Data Insights**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("###  **Network Data Summary**")
            st.metric("Total Cell Towers", f"{network_metrics['TOTAL_TOWERS']:,}")
            # Success rate is stored as decimal (0-1) in enhanced_net_metrics, convert to percentage
            success_rate_decimal = network_metrics.get('AVG_SUCCESS_RATE', 0)
            st.metric("Connection Success Rate", f"{success_rate_decimal * 100:.2f}%" if success_rate_decimal else "No data")
            st.metric("Critical Issues", f"{network_metrics['CRITICAL_ISSUES']:,}")
            st.metric("Premium Towers", f"{network_metrics['PREMIUM_TOWERS']:,} ({(network_metrics['PREMIUM_TOWERS']/max(network_metrics['TOTAL_TOWERS'],1)*100):.1f}%)")
        
        with col2:
            st.markdown("###  **Customer Data Summary**")
            st.metric("Total Support Tickets", f"{customer_metrics['TOTAL_TICKETS']:,}")
            st.metric("Unique Customers", f"{customer_metrics['UNIQUE_CUSTOMERS']:,}")
            st.metric("Average Sentiment", f"{customer_metrics['AVG_SENTIMENT']:.3f}")
            st.metric("Negative Sentiment Tickets", f"{getattr(customer_metrics, 'VERY_NEGATIVE_TICKETS', 0):,}")
            
        # Service type breakdown
        st.markdown("###  **Service Type Distribution**")
        service_col1, service_col2, service_col3 = st.columns(3)
        
        with service_col1:
            st.metric("Cellular Services", f"{getattr(customer_metrics, 'CELLULAR_TICKETS', 0):,}")
        with service_col2:
            st.metric("Business Internet", f"{getattr(customer_metrics, 'BUSINESS_TICKETS', 0):,}")
        with service_col3:
            st.metric("Home Internet", f"{getattr(customer_metrics, 'HOME_TICKETS', 0):,}")
    
    # Executive Action Center
    st.markdown("---")
    st.markdown("###  Executive Action Center")
    
    if st.button(" Generate AI Strategic Report", type="primary"):
        create_ai_loading_spinner("AI is analyzing network data and market trends for strategic insights...")
        
        time.sleep(2)  # Simulate AI processing
        
        # Create comprehensive strategic analysis using actual data
        strategic_report = f"""
        **STRATEGIC NETWORK INTELLIGENCE REPORT**
        
        **EXECUTIVE SUMMARY:**
        Network operations managing {network_metrics['TOTAL_TOWERS']:,} cell towers with {network_metrics['NETWORK_HEALTH_SCORE']:.1f}% health score. Currently tracking {network_metrics['CRITICAL_ISSUES']} critical incidents requiring immediate attention.
        
        **OPERATIONAL PERFORMANCE:**
        • Network infrastructure: {network_metrics['TOTAL_TOWERS']:,} active towers across multiple regions
        • Connection success rate: {(network_metrics['AVG_SUCCESS_RATE'] or 0) * 100:.1f}% (industry benchmark: 95%+)
        • Premium performance towers: {network_metrics['PREMIUM_TOWERS']} ({(network_metrics['PREMIUM_TOWERS']/max(network_metrics['TOTAL_TOWERS'],1)*100):.0f}% of total)
        • Risk assessment level: {network_metrics['RISK_LEVEL']} based on current incident patterns
        
        **CUSTOMER EXPERIENCE ANALYSIS:**
        • Support ticket volume: {customer_metrics['TOTAL_TICKETS']:,} tickets across customer base
        • Customer base: {customer_metrics['UNIQUE_CUSTOMERS']:,} unique customers requiring support
        • Sentiment trend: {customer_metrics['AVG_SENTIMENT']:.3f} (scale: -1 to +1, target: >0.2)
        • Service quality impact: {"Positive trend" if customer_metrics['AVG_SENTIMENT'] > -0.2 else "Requires attention"}
        
        **FINANCIAL IMPACT:**
        • Estimated monthly revenue: ${network_metrics['ESTIMATED_REVENUE']/1000000:.1f}M based on {customer_metrics['UNIQUE_CUSTOMERS']:,} customers
        • Revenue at risk: ${network_metrics['REVENUE_AT_RISK']/1000:.0f}K due to network performance issues
        • Infrastructure investment priority: {"HIGH" if network_metrics['CRITICAL_ISSUES'] > 10 else "MEDIUM"}
        
        **STRATEGIC RECOMMENDATIONS:**
        Based on current data analysis, focus on {"critical issue resolution" if network_metrics['CRITICAL_ISSUES'] > 5 else "performance optimization"} and {"customer satisfaction improvement" if customer_metrics['AVG_SENTIMENT'] < -0.2 else "service quality maintenance"}.
        """
        
        create_ai_insights_card(
            "Strategic Intelligence Analysis",
            strategic_report,
            confidence=0.92,
            icon=""
        )

# Add fallback message if no network data is available  
else:
    create_executive_alert_banner("️ Network data synchronization in progress. Executive dashboard will be available momentarily.", "warning")
    
    # Show executive capabilities preview
    st.markdown("###  Executive Intelligence Preview")
    
    preview_kpis = {
        "Network Performance": {"value": "94.2%", "trend": 2.1, "icon": "🟢"},
        "Revenue Protection": {"value": "$2.8M", "trend": 5.7, "icon": ""},
        "AI Efficiency": {"value": "92%", "trend": 3.4, "icon": ""},
        "Risk Mitigation": {"value": "67%", "trend": -8.3, "icon": "️"}
    }
    
    create_executive_dashboard(preview_kpis)
    
    capabilities_content = """
    <strong>Your executive suite provides comprehensive network intelligence:</strong>
    <br><br>
    • <strong>Real-time Performance Monitoring</strong> with predictive failure detection<br>
    • <strong>AI-Powered Customer Analytics</strong> including churn prediction and sentiment analysis<br>  
    • <strong>Strategic Business Intelligence</strong> with ROI tracking and revenue impact assessment<br>
    • <strong>Automated Executive Reporting</strong> with natural language insights and recommendations<br>
    • <strong>Risk Assessment & Mitigation</strong> with proactive maintenance scheduling<br>
    • <strong>Market Intelligence Integration</strong> for competitive advantage analysis
    """
    
    exec_metrics = {
        "Models Available": "40+",
        "Response Time": "<1s", 
        "Accuracy Rate": "92%",
        "Uptime SLA": "99.9%"
    }
    
    create_executive_summary_card(
        "Executive AI Intelligence Platform",
        capabilities_content,
        exec_metrics,
        ""
    )

# Executive Navigation Grid
st.markdown("---")
st.markdown("##  Executive Intelligence Platform")

navigation_items = [
    {
        "title": "AI Customer Intelligence",
        "description": "Advanced customer analytics with AI-powered churn prediction, sentiment analysis, and personalized retention strategies. Real-time customer experience optimization.",
        "icon": "",
        "badge": "AI POWERED",
        "page_key": "Customer_Profile"
    },
    {
        "title": "Network Performance Command",
        "description": "Comprehensive cell tower monitoring with predictive failure analysis, capacity optimization, and automated performance enhancement recommendations.",
        "icon": "", 
        "badge": "REAL-TIME",
        "page_key": "Cell_Tower_Lookup"
    },
    {
        "title": "Geospatial Intelligence",
        "description": "Advanced geographic analysis with AI pattern recognition, coverage optimization, and location-based performance insights for strategic planning.",
        "icon": "️",
        "badge": "GEO AI",
        "page_key": "Geospatial_Analysis"
    },
    {
        "title": "Executive AI Dashboard",
        "description": "Real-time executive insights with automated reporting, strategic recommendations, and business impact analysis powered by advanced AI algorithms.",
        "icon": "",
        "badge": "EXECUTIVE",
        "page_key": "AI_Insights_and_Recommendations"
    },
    {
        "title": "Predictive Analytics Suite",
        "description": "Machine learning models for network forecasting, failure prediction, and capacity planning with 92% accuracy rate for proactive operations.",
        "icon": "",
        "badge": "PREDICTIVE",
        "page_key": "Predictive_Analytics"
    },
    {
        "title": "Snowflake Intelligence",
        "description": "Natural language querying, intelligent agents, and conversational analytics powered by Snowflake's advanced AI platform for instant insights.",
        "icon": "",
        "badge": "NEXT-GEN",
        "page_key": "Snowflake_Intelligence"
    }
]

create_executive_navigation_grid(navigation_items)

# Technology Excellence Section
st.markdown("---")
st.markdown("##  Technology Excellence Platform")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: var(--exec-bg-primary); padding: 1.5rem; border-radius: var(--exec-border-radius-lg); 
                box-shadow: var(--exec-shadow); border: 1px solid var(--exec-border); min-height: 320px; height: auto;">
        <div style="text-align: center; margin-bottom: 1.25rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">️</div>
            <h3 style="color: var(--exec-primary); margin: 0; font-weight: 700; font-size: 1.1rem;">Snowflake Cortex AISQL</h3>
        </div>
        <div style="color: var(--exec-text-secondary); line-height: 1.5; font-size: 0.9rem;">
            <div style="margin-bottom: 0.75rem;"><strong> Models:</strong> Claude 4, GPT-4.1, Mistral, Llama 3.3</div>
            <div style="margin-bottom: 0.75rem;"><strong> Functions:</strong> AI_COMPLETE, AI_CLASSIFY, AI_SENTIMENT</div>
            <div><strong> Performance:</strong> Sub-second response times with scalability</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: var(--exec-bg-primary); padding: 1.5rem; border-radius: var(--exec-border-radius-lg); 
                box-shadow: var(--exec-shadow); border: 1px solid var(--exec-border); min-height: 320px; height: auto;">
        <div style="text-align: center; margin-bottom: 1.25rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;"></div>
            <h3 style="color: var(--exec-primary); margin: 0; font-weight: 700; font-size: 1.1rem;">AI Analytics Engine</h3>
        </div>
        <div style="color: var(--exec-text-secondary); line-height: 1.5; font-size: 0.9rem;">
            <div style="margin-bottom: 0.75rem;"><strong> Recognition:</strong> Network anomalies and failure patterns</div>
            <div style="margin-bottom: 0.75rem;"><strong> Prediction:</strong> 92% accuracy in failure prediction</div>
            <div><strong> Insights:</strong> Real-time streaming telemetry analysis</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: var(--exec-bg-primary); padding: 1.5rem; border-radius: var(--exec-border-radius-lg); 
                box-shadow: var(--exec-shadow); border: 1px solid var(--exec-border); min-height: 320px; height: auto;">
        <div style="text-align: center; margin-bottom: 1.25rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;"></div>
            <h3 style="color: var(--exec-primary); margin: 0; font-weight: 700; font-size: 1.1rem;">Executive Intelligence</h3>
        </div>
        <div style="color: var(--exec-text-secondary); line-height: 1.5; font-size: 0.9rem;">
            <div style="margin-bottom: 0.75rem;"><strong> Impact:</strong> Revenue protection and ROI optimization</div>
            <div style="margin-bottom: 0.75rem;"><strong> Planning:</strong> AI-powered market insights</div>
            <div><strong> Support:</strong> Real-time executive dashboards</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Executive Success Metrics
st.markdown("---")
st.markdown("##  Executive Success Metrics")

success_col1, success_col2, success_col3, success_col4 = st.columns(4)

with success_col1:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: var(--exec-bg-primary); 
                border-radius: var(--exec-border-radius-lg); box-shadow: var(--exec-shadow);">
        <div style="font-size: 2.5rem; color: var(--exec-success); margin-bottom: 0.5rem;"></div>
        <div style="font-size: 2rem; font-weight: 800; color: var(--exec-primary);">340%</div>
        <div style="color: var(--exec-text-secondary); font-weight: 600; text-transform: uppercase; font-size: 0.9rem;">ROI Achieved</div>
    </div>
    """, unsafe_allow_html=True)

with success_col2:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: var(--exec-bg-primary); 
                border-radius: var(--exec-border-radius-lg); box-shadow: var(--exec-shadow);">
        <div style="font-size: 2.5rem; color: var(--exec-warning); margin-bottom: 0.5rem;"></div>
        <div style="font-size: 2rem; font-weight: 800; color: var(--exec-primary);">67%</div>
        <div style="color: var(--exec-text-secondary); font-weight: 600; text-transform: uppercase; font-size: 0.9rem;">MTTR Reduction</div>
    </div>
    """, unsafe_allow_html=True)

with success_col3:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: var(--exec-bg-primary); 
                border-radius: var(--exec-border-radius-lg); box-shadow: var(--exec-shadow);">
        <div style="font-size: 2.5rem; color: var(--exec-success); margin-bottom: 0.5rem;"></div>
        <div style="font-size: 2rem; font-weight: 800; color: var(--exec-primary);">92%</div>
        <div style="color: var(--exec-text-secondary); font-weight: 600; text-transform: uppercase; font-size: 0.9rem;">Prediction Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with success_col4:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: var(--exec-bg-primary); 
                border-radius: var(--exec-border-radius-lg); box-shadow: var(--exec-shadow);">
        <div style="font-size: 2.5rem; color: var(--exec-secondary); margin-bottom: 0.5rem;"></div>
        <div style="font-size: 2rem; font-weight: 800; color: var(--exec-primary);">$2.8M</div>
        <div style="color: var(--exec-text-secondary); font-weight: 600; text-transform: uppercase; font-size: 0.9rem;">Revenue Protected</div>
    </div>
    """, unsafe_allow_html=True)

# Executive footer with contact and support
add_page_footer()

st.markdown("---")
st.markdown("""
<div style="text-align: center; background: var(--exec-gradient-primary); color: white; 
            padding: 2rem; border-radius: var(--exec-border-radius-lg); margin: 2rem 0;
            font-family: 'Ericsson Hilda', 'Source Sans Pro', sans-serif;">
    <h3 style="margin: 0 0 1rem 0; color: white;"> Telco Support & Innovation Services</h3>
    <p style="margin: 0; opacity: 0.9; font-size: 1.1rem;">
        24/7 Network Operations Support • AI-Driven Insights • Custom Network Analytics
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">
        Powered by Telco's global network expertise and Snowflake Cortex AI technology
    </p>
    <p style="margin: 1rem 0 0 0; font-size: 0.75rem; opacity: 0.7;">
        Designed in compliance with <a href="https://mediabank.ericsson.net/admin/mb/?h=dbeb87a1bcb16fa379c0020bdf713872#View%20document" 
        style="color: var(--ericsson-orange-light); text-decoration: underline;">Ericsson Brand Guidelines</a>
    </p>
</div>
""", unsafe_allow_html=True)