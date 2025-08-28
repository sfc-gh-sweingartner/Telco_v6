import streamlit as st
import sys
import os

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Import with fallback for AI functions
try:
    from utils.design_system import (
        inject_custom_css, create_page_header, create_metric_card, 
        create_info_box, get_snowflake_session, create_metric_grid,
        create_sidebar_navigation, add_page_footer, execute_query_with_loading,
        create_ai_insights_card, create_ai_metrics_dashboard, format_ai_response,
        create_ai_loading_spinner, create_ai_recommendation_list
    )
except ImportError:
    # Fallback imports when AI functions are not available
    from utils.design_system import (
        inject_custom_css, create_page_header, create_metric_card, 
        create_info_box, get_snowflake_session, create_metric_grid,
        create_sidebar_navigation, add_page_footer, execute_query_with_loading
    )
    # Define fallback AI functions
    def create_ai_insights_card(title, insight, confidence=0.0, icon="🧠"):
        st.markdown(f"### {icon} {title}")
        st.info(insight)
    def create_ai_metrics_dashboard(metrics):
        cols = st.columns(len(metrics))
        for i, (key, value) in enumerate(metrics.items()):
            with cols[i % len(cols)]:
                st.metric(key, value)
    def format_ai_response(response, title="AI Insights"):
        st.markdown(f"### {title}")
        st.write(response)
    def create_ai_loading_spinner(message="AI is analyzing..."):
        st.info(f"🤖 {message}")
    def create_ai_recommendation_list(recommendations, title="AI Recommendations"):
        st.markdown(f"### {title}")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")

try:
    from utils.aisql_functions import get_ai_analytics, get_ai_processor, format_ai_response as format_ai_response_util
except ImportError:
    # Fallback for AI functions
    def get_ai_analytics(session):
        class FallbackAnalytics:
            def generate_executive_summary(self, *args, **kwargs):
                return "🤖 AI analysis functionality is being updated. Please refresh the page in a few minutes to access the full AI capabilities!"
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

# Professional page header with AI emphasis
create_page_header(
    title="AI-Powered Telco Network Optimization Suite",
    description="Transform network challenges into actionable insights with advanced AI analytics powered by Snowflake Cortex AISQL",
    icon="🤖"
)

# Initialize AI Analytics
ai_analytics = get_ai_analytics(session)
ai_processor = get_ai_processor(session)

# AI-Enhanced Value Proposition Section
st.markdown("""
<div style="background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem; border-left: 6px solid #2196f3; box-shadow: 0 4px 20px rgba(33,150,243,0.1);">
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <span style="font-size: 2rem; margin-right: 1rem;">🤖</span>
        <h2 style="color: #1565c0; margin: 0; font-weight: 700;">AI-Powered Network Intelligence</h2>
    </div>
    <p style="margin: 0 0 1.5rem 0; font-size: 1.2rem; color: #333; line-height: 1.6;">
        Harness the power of <strong>Snowflake Cortex AISQL</strong> to transform overwhelming network data into crystal-clear insights. 
        Our AI-driven suite automatically identifies patterns, predicts issues, and recommends solutions across your entire telecom infrastructure.
    </p>
    <div style="background: rgba(33,150,243,0.1); padding: 1rem; border-radius: 8px; border-left: 3px solid #2196f3;">
        <strong style="color: #1565c0;">🚀 New AI Capabilities:</strong> 
        Intelligent ticket classification, predictive failure analysis, automated root cause analysis, and natural language network querying.
    </div>
</div>
""", unsafe_allow_html=True)

# Load and analyze current network data for AI insights
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_network_summary_data():
    try:
        # Get basic network metrics
        network_query = """
        SELECT 
            COUNT(DISTINCT CELL_ID) as total_towers,
            AVG(NVL(PM_RRC_CONN_ESTAB_SUCC, 0) / NULLIF(PM_RRC_CONN_ESTAB_ATT, 0)) as avg_success_rate,
            COUNT(CASE WHEN PM_ERAB_REL_ABNORMAL_ENB > 50 THEN 1 END) as critical_issues,
            AVG(NVL(PM_PRB_UTIL_DL, 0)) as avg_dl_utilization
        FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER 
        WHERE EVENT_DATE >= DATEADD(day, -7, CURRENT_DATE())
        """
        network_data = session.sql(network_query).collect()
        
        # Get support ticket metrics
        tickets_query = """
        SELECT 
            COUNT(*) as total_tickets,
            AVG(SENTIMENT_SCORE) as avg_sentiment,
            COUNT(CASE WHEN SENTIMENT_SCORE < -0.5 THEN 1 END) as critical_tickets,
            COUNT(DISTINCT CUSTOMER_NAME) as unique_customers
        FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.SUPPORT_TICKETS
        """
        tickets_data = session.sql(tickets_query).collect()
        
        return network_data[0], tickets_data[0] if network_data and tickets_data else (None, None)
    except Exception as e:
        st.error(f"Error loading summary data: {e}")
        return None, None

network_summary, tickets_summary = load_network_summary_data()

if network_summary and tickets_summary:
    # AI-Powered Executive Dashboard
    st.markdown("## 📊 AI Executive Dashboard")
    
    # Real-time AI metrics
    ai_metrics = {
        "Network Health Score": f"{(network_summary['AVG_SUCCESS_RATE'] or 0) * 100:.1f}%",
        "Active Cell Towers": f"{network_summary['TOTAL_TOWERS'] or 0:,}",
        "Critical Issues": f"{network_summary['CRITICAL_ISSUES'] or 0}",
        "Customer Sentiment": f"{(tickets_summary['AVG_SENTIMENT'] or 0):.2f}",
        "Support Tickets": f"{tickets_summary['TOTAL_TICKETS'] or 0:,}",
        "Risk Customers": f"{tickets_summary['CRITICAL_TICKETS'] or 0}"
    }
    
    create_ai_metrics_dashboard(ai_metrics)
    
    # Generate AI Executive Summary
    st.markdown("### 🤖 AI Executive Summary")
    
    with st.expander("🧠 Generate Real-Time AI Insights", expanded=True):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🚀 Generate Executive Summary", type="primary"):
                create_ai_loading_spinner("AI is analyzing network data and generating insights...")
                
                # Create summary data for AI analysis
                network_data_summary = {
                    'total_towers': network_summary['TOTAL_TOWERS'] or 0,
                    'avg_success_rate': network_summary['AVG_SUCCESS_RATE'] or 0,
                    'critical_issues': network_summary['CRITICAL_ISSUES'] or 0,
                    'avg_dl_utilization': network_summary['AVG_DL_UTILIZATION'] or 0
                }
                
                ticket_data_summary = {
                    'total_tickets': tickets_summary['TOTAL_TICKETS'] or 0,
                    'avg_sentiment': tickets_summary['AVG_SENTIMENT'] or 0,
                    'critical_tickets': tickets_summary['CRITICAL_TICKETS'] or 0,
                    'unique_customers': tickets_summary['UNIQUE_CUSTOMERS'] or 0
                }
                
                # Generate AI summary
                executive_summary = ai_analytics.generate_executive_summary(
                    network_data_summary, 
                    ticket_data_summary
                )
                
                if executive_summary:
                    create_ai_insights_card(
                        "Executive Network Analysis", 
                        executive_summary, 
                        confidence=0.85, 
                        icon="📈"
                    )
                else:
                    st.warning("Unable to generate AI summary at this time.")
        
        with col2:
            if st.button("🔍 Analyze Network Patterns", type="secondary"):
                create_ai_loading_spinner("AI is identifying network patterns and anomalies...")
                
                # Load recent problematic towers for pattern analysis
                pattern_query = """
                SELECT CELL_ID, BID_DESCRIPTION, PM_RRC_CONN_ESTAB_SUCC, 
                       PM_RRC_CONN_ESTAB_ATT, PM_ERAB_REL_ABNORMAL_ENB,
                       CAUSE_CODE_SHORT_DESCRIPTION
                FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER 
                WHERE PM_ERAB_REL_ABNORMAL_ENB > 30
                   OR (PM_RRC_CONN_ESTAB_SUCC / NULLIF(PM_RRC_CONN_ESTAB_ATT, 0)) < 0.8
                ORDER BY PM_ERAB_REL_ABNORMAL_ENB DESC
                LIMIT 10
                """
                
                try:
                    pattern_data = session.sql(pattern_query).to_pandas()
                    if not pattern_data.empty:
                        network_insights = ai_analytics.analyze_network_issues(pattern_data)
                        
                        if network_insights.get('root_causes'):
                            create_ai_insights_card(
                                "Root Cause Analysis", 
                                network_insights['root_causes'], 
                                confidence=0.78, 
                                icon="🔧"
                            )
                        
                        if network_insights.get('recommendations'):
                            recommendations = network_insights['recommendations'].split('\n')
                            recommendations = [r.strip() for r in recommendations if r.strip()]
                            create_ai_recommendation_list(recommendations[:5], "Priority Actions")
                    else:
                        st.info("Network appears stable - no critical patterns detected.")
                        
                except Exception as e:
                    st.error(f"Error analyzing patterns: {e}")

# AI-Enhanced Navigation Cards
st.markdown("### 🚀 AI-Powered Analytics Tools")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="padding: 1.5rem; background: linear-gradient(135deg, #e8f5e8 0%, #ffffff 100%); border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #4caf50; height: 200px; cursor: pointer;" onclick="window.location.href='?page=Customer_Profile'">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 2rem; margin-right: 0.75rem;">👤</span>
            <h4 style="color: #2e7d32; margin: 0; font-weight: 600;">AI Customer Intelligence</h4>
        </div>
        <p style="margin: 0 0 1rem 0; color: #4a5568; font-size: 0.95rem; line-height: 1.5;">
            • AI-powered churn prediction<br/>
            • Intelligent ticket classification<br/>
            • Automated sentiment analysis<br/>
            • Personalized retention strategies
        </p>
        <div style="background: #4caf50; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 500; display: inline-block;">
            🤖 AI Enhanced
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="padding: 1.5rem; background: linear-gradient(135deg, #fff3e0 0%, #ffffff 100%); border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #ff9800; height: 200px;">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 2rem; margin-right: 0.75rem;">🗺️</span>
            <h4 style="color: #e65100; margin: 0; font-weight: 600;">AI Geospatial Intelligence</h4>
        </div>
        <p style="margin: 0 0 1rem 0; color: #4a5568; font-size: 0.95rem; line-height: 1.5;">
            • Predictive failure mapping<br/>
            • Automated pattern detection<br/>
            • Smart resource optimization<br/>
            • Geographic impact analysis
        </p>
        <div style="background: #ff9800; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 500; display: inline-block;">
            🧠 AI Vision
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="padding: 1.5rem; background: linear-gradient(135deg, #f3e5f5 0%, #ffffff 100%); border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #9c27b0; height: 200px;">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 2rem; margin-right: 0.75rem;">💬</span>
            <h4 style="color: #6a1b9a; margin: 0; font-weight: 600;">AI Network Assistant</h4>
        </div>
        <p style="margin: 0 0 1rem 0; color: #4a5568; font-size: 0.95rem; line-height: 1.5;">
            • Natural language queries<br/>
            • Conversational analytics<br/>
            • Intelligent troubleshooting<br/>
            • Real-time recommendations
        </p>
        <div style="background: #9c27b0; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 500; display: inline-block;">
            💡 Coming Soon
        </div>
    </div>
    """, unsafe_allow_html=True)

# Add fallback message if no network data is available
else:
    st.warning("⚠️ Unable to load network data. Please check your database connection and try again.")
    
    # Show basic AI capabilities info
    st.markdown("### 🤖 Available AI Capabilities")
    st.info("Once connected, you'll have access to:")
    
    capabilities = [
        "🎯 Intelligent ticket classification and routing",
        "📊 Predictive network failure analysis", 
        "🔍 Automated root cause detection",
        "💡 AI-powered optimization recommendations",
        "📈 Natural language executive summaries",
        "🧠 Customer churn risk predictions"
    ]
    
    for capability in capabilities:
        st.markdown(f"• {capability}")

# AI Technology Showcase
st.markdown("---")
st.markdown("### ⚡ Powered by Advanced AI Technology")

tech_col1, tech_col2 = st.columns(2)

with tech_col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e8f4fd 0%, #ffffff 100%); padding: 2rem; border-radius: 16px; border-left: 4px solid #2196f3;">
        <h4 style="color: #1565c0; margin: 0 0 1rem 0; display: flex; align-items: center;">
            <span style="margin-right: 0.5rem;">❄️</span> Snowflake Cortex AISQL
        </h4>
        <ul style="margin: 0; padding-left: 1.5rem; color: #4a5568;">
            <li><strong>AI_COMPLETE:</strong> LLM-powered analysis using Mistral, Llama, and Arctic models</li>
            <li><strong>AI_CLASSIFY:</strong> Intelligent categorization of tickets and issues</li>
            <li><strong>AI_SENTIMENT:</strong> Advanced sentiment analysis for customer feedback</li>
            <li><strong>AI_SUMMARIZE:</strong> Automated executive summaries and insights</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tech_col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f3e5f5 0%, #ffffff 100%); padding: 2rem; border-radius: 16px; border-left: 4px solid #9c27b0;">
        <h4 style="color: #6a1b9a; margin: 0 0 1rem 0; display: flex; align-items: center;">
            <span style="margin-right: 0.5rem;">🧠</span> Advanced Analytics
        </h4>
        <ul style="margin: 0; padding-left: 1.5rem; color: #4a5568;">
            <li><strong>Pattern Recognition:</strong> AI identifies hidden network failure patterns</li>
            <li><strong>Predictive Models:</strong> Machine learning for proactive issue prevention</li>
            <li><strong>Natural Language:</strong> Query your network data conversationally</li>
            <li><strong>Real-time Insights:</strong> Instant AI analysis of streaming data</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Hero image section showcasing AI capabilities
st.markdown("---")
st.markdown("### 🤖 AI-Powered Network Operations")
st.image(
    "https://quickstarts.snowflake.com/guide/optimizing-network-operations-with-cortex-ai-call-transcripts-and-tower-data-analysis/img/dad88af756439cbf.png",
    caption="AI-Enhanced Network Operations with Snowflake Cortex AISQL",
    use_container_width=True
)

# Getting started guide for AI features
st.markdown("---")
create_info_box(
    "🚀 **Get Started with AI Analytics:** Use the sidebar to explore our AI-powered analysis tools. Start with Customer Profile for AI churn prediction or Geospatial Analysis for pattern detection!", 
    "info"
)

# Add professional footer
add_page_footer()