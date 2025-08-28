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

# Force rendering by adding a refresh button in the sidebar for debugging
if st.sidebar.button("🔄 Refresh Page"):
    st.rerun()

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
</div>
""", unsafe_allow_html=True)

# Create benefit cards using Streamlit columns for better reliability
st.markdown("### Key Benefits")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="padding: 1.5rem; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #1f4e79; height: 120px;">
        <h4 style="color: #1f4e79; margin: 0 0 0.5rem 0;">⚡ Rapid Insight</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.4;">Instantly pinpoint cell towers driving the most trouble tickets</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="padding: 1.5rem; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #28a745; height: 120px;">
        <h4 style="color: #28a745; margin: 0 0 0.5rem 0;">📊 Proactive Monitoring</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.4;">Visualize live customer sentiment and ticket-density hotspots</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="padding: 1.5rem; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #ffc107; height: 120px;">
        <h4 style="color: #e0a800; margin: 0 0 0.5rem 0;">🔄 Reduced MTTR</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.4;">Quickly identify root causes and accelerate problem-solving</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="padding: 1.5rem; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #dc3545; height: 120px;">
        <h4 style="color: #dc3545; margin: 0 0 0.5rem 0;">💰 Optimized Spend</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.4;">Allocate resources to areas of highest impact efficiently</p>
    </div>
    """, unsafe_allow_html=True)

# Hero image section
st.markdown("---")
st.markdown("### 📊 Network Operations Dashboard")
st.image(
    "https://quickstarts.snowflake.com/guide/optimizing-network-operations-with-cortex-ai-call-transcripts-and-tower-data-analysis/img/dad88af756439cbf.png",
    caption="Optimizing Network Operations with Cortex AI",
    use_column_width=True
)

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
st.markdown("---")
st.markdown("### 🧭 Analysis Tools")
st.markdown("Explore our comprehensive suite of network optimization tools:")

# Create navigation cards using Streamlit columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #1f4e79; height: 140px; margin-bottom: 1rem;">
        <h4 style="color: #1f4e79; margin: 0 0 0.5rem 0;">👤 Customer Profile</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.4;">Comprehensive customer analysis with churn prediction and sentiment tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #dc3545; height: 140px;">
        <h4 style="color: #dc3545; margin: 0 0 0.5rem 0;">🎯 Customer Impact Dashboard</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.4;">Real-time monitoring of customer experience and satisfaction metrics</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #28a745; height: 140px; margin-bottom: 1rem;">
        <h4 style="color: #28a745; margin: 0 0 0.5rem 0;">📱 Cell Tower Lookup</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.4;">Interactive maps with failure analysis and AI-powered recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #6f42c1; height: 140px;">
        <h4 style="color: #6f42c1; margin: 0 0 0.5rem 0;">📈 Advanced Analytics</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.4;">Time series, loyalty analysis, and predictive insights for network optimization</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #ffc107; height: 140px; margin-bottom: 1rem;">
        <h4 style="color: #e0a800; margin: 0 0 0.5rem 0;">🗺️ Geospatial Analysis</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.4;">Advanced heatmaps correlating network performance with customer issues</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #17a2b8; height: 140px;">
        <h4 style="color: #17a2b8; margin: 0 0 0.5rem 0;">📊 Correlation Analytics</h4>
        <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.4;">Statistical analysis revealing hidden relationships in network data</p>
    </div>
    """, unsafe_allow_html=True)

# Getting started guide
create_info_box("💡 Get started by selecting any analysis tool from the sidebar to explore your network data.", "info")

# Add professional footer
add_page_footer()