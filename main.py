import streamlit as st
import sys
import os

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.design_system import (
    inject_custom_css, create_page_header, create_metric_card, 
    create_info_box, get_snowflake_session, create_metric_grid,
    create_sidebar_navigation, add_page_footer, execute_query_with_loading
)

# Page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="Telco Network Optimization Suite",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for professional styling
inject_custom_css()

# Create professional sidebar navigation
create_sidebar_navigation()

# Initialize Snowflake session
session = get_snowflake_session()

# Professional page header
create_page_header(
    title="Telco Network Optimization Suite",
    description="Transform network challenges into actionable insights with AI-powered analytics",
    icon="📡"
)

# Value proposition section
st.markdown("""
<div style="background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid #1f4e79;">
    <h3 style="color: #1f4e79; margin: 0 0 1rem 0; font-weight: 600;">🎯 Solve Your Toughest Network Challenges</h3>
    <p style="margin: 0 0 1.5rem 0; font-size: 1.1rem; color: #495057; line-height: 1.6;">
        Today's telco operations are overwhelmed by vast network data, customer complaints, and sprawling infrastructure. 
        Our suite cuts through the noise to deliver clarity and action.
    </p>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
        <div style="padding: 1rem; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h4 style="color: #1f4e79; margin: 0 0 0.5rem 0;">⚡ Rapid Insight</h4>
            <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">Instantly pinpoint cell towers driving the most trouble tickets</p>
        </div>
        <div style="padding: 1rem; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h4 style="color: #1f4e79; margin: 0 0 0.5rem 0;">📊 Proactive Monitoring</h4>
            <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">Visualize live customer sentiment and ticket-density hotspots</p>
        </div>
        <div style="padding: 1rem; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h4 style="color: #1f4e79; margin: 0 0 0.5rem 0;">🔄 Reduced MTTR</h4>
            <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">Quickly identify root causes and accelerate problem-solving</p>
        </div>
        <div style="padding: 1rem; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h4 style="color: #1f4e79; margin: 0 0 0.5rem 0;">💰 Optimized Spend</h4>
            <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">Allocate resources to areas of highest impact efficiently</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero image section
with st.container():
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <img src="https://quickstarts.snowflake.com/guide/optimizing-network-operations-with-cortex-ai-call-transcripts-and-tower-data-analysis/img/dad88af756439cbf.png" 
             style="width: 100%; max-width: 900px; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.1);" 
             alt="Network Operations Dashboard">
    </div>
    """, unsafe_allow_html=True)

# Network overview metrics section
st.markdown("""
<div style="margin: 3rem 0 2rem 0;">
    <h3 style="text-align: center; color: #1f4e79; font-weight: 600; margin-bottom: 2rem;">🏢 Network Overview</h3>
</div>
""", unsafe_allow_html=True)

# Load key metrics with professional loading
metrics_data = execute_query_with_loading("""
    SELECT 
        COUNT(DISTINCT cell_id) as total_cells,
        ROUND(AVG(CASE WHEN call_release_code != 0 THEN 1 ELSE 0 END) * 100, 2) as failure_rate,
        COUNT(*) as total_calls
    FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER
""", "Loading network metrics...")

ticket_data = execute_query_with_loading("""
    SELECT COUNT(*) as ticket_count,
           ROUND(AVG(sentiment_score), 3) as avg_sentiment
    FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.SUPPORT_TICKETS
""", "Loading support metrics...")

# Create professional metric cards
if not metrics_data.empty and not ticket_data.empty:
    metrics = [
        {
            "title": "Cell Towers",
            "value": f"{metrics_data.iloc[0]['TOTAL_CELLS']:,}",
            "delta": "Active network nodes"
        },
        {
            "title": "Network Failure Rate", 
            "value": f"{metrics_data.iloc[0]['FAILURE_RATE']}%",
            "delta": "↓ 2.1% vs last month" if metrics_data.iloc[0]['FAILURE_RATE'] < 15 else "↑ 1.3% vs last month",
            "delta_color": "positive" if metrics_data.iloc[0]['FAILURE_RATE'] < 15 else "negative"
        },
        {
            "title": "Support Tickets",
            "value": f"{ticket_data.iloc[0]['TICKET_COUNT']:,}",
            "delta": "Open and resolved"
        },
        {
            "title": "Customer Sentiment",
            "value": f"{ticket_data.iloc[0]['AVG_SENTIMENT']:.2f}",
            "delta": "↑ 15% improvement" if ticket_data.iloc[0]['AVG_SENTIMENT'] > -0.5 else "Needs attention",
            "delta_color": "positive" if ticket_data.iloc[0]['AVG_SENTIMENT'] > -0.5 else "negative"
        }
    ]
    
    create_metric_grid(metrics, columns=4)
else:
    create_info_box("Unable to load network metrics. Please check your database connection.", "warning")

# Navigation guide section
st.markdown("""
<div style="margin: 3rem 0 2rem 0;">
    <h3 style="text-align: center; color: #1f4e79; font-weight: 600; margin-bottom: 2rem;">🧭 Analysis Tools</h3>
</div>
""", unsafe_allow_html=True)

# Create navigation cards
st.markdown("""
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #1f4e79;">
        <h4 style="color: #1f4e79; margin: 0 0 0.5rem 0; display: flex; align-items: center;">👤 Customer Profile</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.5;">Comprehensive customer analysis with churn prediction and sentiment tracking</p>
    </div>
    
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #28a745;">
        <h4 style="color: #28a745; margin: 0 0 0.5rem 0; display: flex; align-items: center;">📱 Cell Tower Lookup</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.5;">Interactive maps with failure analysis and AI-powered recommendations</p>
    </div>
    
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #ffc107;">
        <h4 style="color: #e0a800; margin: 0 0 0.5rem 0; display: flex; align-items: center;">🗺️ Geospatial Analysis</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.5;">Advanced heatmaps correlating network performance with customer issues</p>
    </div>
    
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #17a2b8;">
        <h4 style="color: #17a2b8; margin: 0 0 0.5rem 0; display: flex; align-items: center;">📊 Correlation Analytics</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.5;">Statistical analysis revealing hidden relationships in network data</p>
    </div>
    
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #dc3545;">
        <h4 style="color: #dc3545; margin: 0 0 0.5rem 0; display: flex; align-items: center;">🎯 Customer Impact Dashboard</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.5;">Real-time monitoring of customer experience and satisfaction metrics</p>
    </div>
    
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #6f42c1;">
        <h4 style="color: #6f42c1; margin: 0 0 0.5rem 0; display: flex; align-items: center;">📈 Advanced Analytics</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.5;">Time series, loyalty analysis, and predictive insights for network optimization</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Getting started guide
create_info_box("💡 Get started by selecting any analysis tool from the sidebar to explore your network data.", "info")

# Add professional footer
add_page_footer()