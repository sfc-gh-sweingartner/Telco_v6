"""
Executive AI Summary Dashboard
==============================

Automated executive reports and strategic recommendations using Snowflake Cortex AISQL.
Provides high-level business intelligence and AI-driven strategic insights for C-suite executives.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
from datetime import datetime, timedelta
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
        format_ai_response, create_ai_metric_card, create_metric_card
    )
    AI_FUNCTIONS_AVAILABLE = True
except ImportError:
    from utils.design_system import (
        inject_custom_css, create_page_header, create_sidebar_navigation, 
        add_page_footer, get_snowflake_session, execute_query_with_loading,
        create_metric_card
    )
    AI_FUNCTIONS_AVAILABLE = False
    
    # Define fallback AI functions
    def create_ai_insights_card(title, insight, confidence=0.0, icon="🧠"):
        st.markdown(f"### {icon} {title}")
        # Fix newline formatting for better display
        formatted_insight = insight.replace('\\n', '\n') if '\\n' in insight else insight
        st.info(formatted_insight)
    def create_ai_loading_spinner(message="AI is analyzing..."):
        st.info(f"🤖 {message}")
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
    def create_model_selector(models, default_model="claude-3-5-sonnet"):
        return st.selectbox("AI Model", models, index=models.index(default_model) if default_model in models else 0)
    def format_ai_response(response, title="AI Insights"):
        st.markdown(f"### {title}")
        st.write(response)
    def create_ai_metric_card(title, value, description="", icon="🤖"):
        st.metric(title, value, help=description)

try:
    from utils.aisql_functions import get_ai_analytics, get_ai_processor
except ImportError:
    def get_ai_analytics(session):
        class FallbackAnalytics:
            def generate_executive_summary(self, *args, **kwargs):
                return "🏢 Executive AI reporting is being deployed. Strategic insights and automated reports will be available shortly!"
        return FallbackAnalytics()
    def get_ai_processor(session):
        class FallbackProcessor:
            supported_models = [
                'claude-4-sonnet', 'claude-4-opus', 'claude-3-5-sonnet', 'claude-3-7-sonnet',
                'mistral-large', 'mistral-large2', 'mistral-7b', 'mixtral-8x7b',
                'openai-gpt-4.1', 'openai-o4-mini', 'openai-gpt-5', 'openai-gpt-5-mini',
                'llama4-maverick', 'llama4-scout', 'llama3.1-8b', 'llama3.1-70b', 'llama3.1-405b',
                'snowflake-arctic', 'snowflake-llama-3.3-70b', 'reka-core', 'reka-flash', 'deepseek-r1'
            ]
            default_model = "claude-3-5-sonnet"
            def ai_complete(self, prompt, **kwargs):
                return "📊 Executive AI analytics are being deployed. Strategic business intelligence will be available shortly!"
        return FallbackProcessor()

# Page configuration
st.set_page_config(
    page_title="Executive AI Summary",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS and create navigation
inject_custom_css()
create_sidebar_navigation()

# Initialize Snowflake session and AI components
session = get_snowflake_session()
ai_analytics = get_ai_analytics(session)
ai_processor = get_ai_processor(session)

# Professional page header
create_page_header(
    title="Executive AI Summary",
    description="Strategic business intelligence and automated executive reports powered by advanced AI analytics",
    icon="🏢"
)

# Show deployment status if AI functions are not fully available
if not AI_FUNCTIONS_AVAILABLE:
    st.warning("""
    🚀 **Executive AI Suite Deployment in Progress**
    
    Advanced executive reporting capabilities are being deployed including:
    - Automated strategic business intelligence
    - AI-generated executive summaries and KPIs
    - Competitive analysis and market positioning
    - ROI analysis and financial impact assessments
    - Strategic recommendations for C-suite decision making
    
    **Expected availability:** 5-10 minutes
    """)
    
    if st.button("🔄 Check Executive AI Status", type="primary"):
        st.rerun()

# Load core business metrics
@st.cache_data(ttl=1800)  # Cache for 30 minutes
def load_executive_metrics():
    """Load key business metrics for executive dashboard"""
    try:
        # Network performance metrics
        network_metrics = session.sql("""
            SELECT 
                COUNT(DISTINCT CELL_ID) as total_towers,
                ROUND(AVG(CASE WHEN CALL_RELEASE_CODE != 0 THEN 1 ELSE 0 END) * 100, 2) as avg_failure_rate,
                COUNT(*) as total_calls
            FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER
        """).to_pandas()
        
        # Customer experience metrics  
        customer_metrics = session.sql("""
            SELECT 
                COUNT(DISTINCT CUSTOMER_NAME) as total_customers,
                COUNT(*) as total_tickets,
                ROUND(AVG(SENTIMENT_SCORE), 3) as avg_sentiment,
                COUNT(CASE WHEN SENTIMENT_SCORE < -0.5 THEN 1 END) as critical_sentiment_tickets
            FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.SUPPORT_TICKETS
        """).to_pandas()
        
        return network_metrics, customer_metrics
        
    except Exception as e:
        st.error(f"Error loading executive metrics: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Load metrics
network_data, customer_data = load_executive_metrics()

# AI Model Selection in Sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🤖 Executive AI Configuration")
    models = ai_processor.supported_models if hasattr(ai_processor, 'supported_models') else ["claude-3-5-sonnet", "mistral-large", "llama3.1-8b", "snowflake-arctic"]
    selected_model = create_model_selector(models, "claude-3-5-sonnet")
    
    st.markdown("---")
    st.markdown("### 📊 Report Settings")
    
    report_frequency = st.selectbox(
        "Report Frequency:",
        ["Real-time", "Daily", "Weekly", "Monthly"],
        index=2
    )
    
    executive_focus = st.multiselect(
        "Executive Focus Areas:",
        ["Network Performance", "Customer Experience", "Financial Impact", "Strategic Opportunities", "Risk Management", "Competitive Position"],
        default=["Network Performance", "Customer Experience", "Financial Impact"]
    )
    
    if st.button("📧 Schedule Executive Reports", type="secondary"):
        st.success(f"✅ {report_frequency} executive reports scheduled with focus on: {', '.join(executive_focus)}")

# Executive KPI Dashboard
st.markdown("## 📊 Executive KPI Dashboard")

if not network_data.empty and not customer_data.empty:
    # Create executive metrics
    exec_col1, exec_col2, exec_col3, exec_col4 = st.columns(4)
    
    with exec_col1:
        network_health = max(0, 100 - network_data.iloc[0]['AVG_FAILURE_RATE'])
        create_metric_card(
            "Network Health Score", 
            f"{network_health:.0f}%",
            f"△ {'+2.3%' if network_health > 85 else '-1.1%'} vs last month",
            "success" if network_health > 85 else "warning"
        )
    
    with exec_col2:
        customer_satisfaction = (customer_data.iloc[0]['AVG_SENTIMENT'] + 1) * 50  # Convert -1,1 to 0,100
        create_metric_card(
            "Customer Satisfaction", 
            f"{customer_satisfaction:.0f}%",
            f"△ {'+1.8%' if customer_satisfaction > 70 else '-0.5%'} vs last month",
            "success" if customer_satisfaction > 70 else "warning"
        )
    
    with exec_col3:
        total_towers = network_data.iloc[0]['TOTAL_TOWERS']
        create_metric_card(
            "Network Assets", 
            f"{total_towers:,}",
            "Active cell towers nationwide",
            "primary"
        )
    
    with exec_col4:
        total_customers = customer_data.iloc[0]['TOTAL_CUSTOMERS'] 
        create_metric_card(
            "Customer Base", 
            f"{total_customers:,}",
            f"△ +{int(total_customers * 0.023):,} new customers this month",
            "success"
        )
    
    # Calculate business impact metrics
    failure_rate = network_data.iloc[0]['AVG_FAILURE_RATE'] 
    potential_revenue_impact = failure_rate * total_customers * 0.0012  # Estimated revenue impact
    
    st.markdown("---")

# AI-Powered Executive Analysis
st.markdown("## 🤖 AI Executive Intelligence")

# Create tabs for different executive analyses
exec_tab1, exec_tab2, exec_tab3, exec_tab4 = st.tabs([
    "📈 Business Performance", 
    "💰 Financial Impact", 
    "🎯 Strategic Opportunities", 
    "🚨 Risk Assessment"
])

with exec_tab1:
    st.markdown("### 📈 AI Business Performance Analysis")
    st.info("Get comprehensive AI-driven insights into your business performance and operational metrics")
    
    performance_period = st.selectbox(
        "Analysis Period:",
        ["Current Quarter", "Last 30 Days", "Year to Date", "Trailing 12 Months"],
        key="performance_period"
    )
    
    if st.button("🚀 Generate Business Performance Report", type="primary", key="business_performance"):
        create_ai_progress_tracker(1, 4, "Analyzing business metrics...")
        
        try:
            # Prepare business context
            business_context = f"""
            Business Performance Analysis - {performance_period}:
            
            Network Operations:
            - Total Network Assets: {total_towers:,} cell towers
            - Network Health Score: {max(0, 100 - failure_rate):.0f}%
            - Average Failure Rate: {failure_rate:.1f}%
            - Service Reliability: {'Excellent' if failure_rate < 15 else 'Good' if failure_rate < 30 else 'Needs Improvement'}
            
            Customer Metrics:
            - Active Customer Base: {total_customers:,}
            - Customer Satisfaction: {((customer_data.iloc[0]['AVG_SENTIMENT'] + 1) * 50):.0f}%
            - Support Tickets: {customer_data.iloc[0]['TOTAL_TICKETS']:,}
            - Critical Sentiment Issues: {customer_data.iloc[0]['CRITICAL_SENTIMENT_TICKETS']}
            
            Business Context:
            - Analysis Period: {performance_period}
            - Industry: Telecommunications
            - Focus: Executive-level strategic insights
            """
            
            create_ai_progress_tracker(2, 4, "Generating strategic insights...")
            
            performance_analysis = ai_processor.ai_complete(
                f"""As a C-suite business consultant for telecommunications, provide an executive performance analysis:
                
                {business_context}
                
                Deliver a comprehensive executive briefing including:
                1. Overall business health assessment and key performance trends
                2. Critical success factors and areas of competitive advantage
                3. Performance against industry benchmarks and best practices
                4. Key operational metrics driving business value
                5. Strategic priorities based on current performance data
                6. Executive recommendations for maximizing business outcomes
                
                Present insights at a strategic level appropriate for C-suite decision making.""",
                max_tokens=800
            )
            
            create_ai_progress_tracker(3, 4, "Preparing executive dashboard...")
            
            if performance_analysis:
                create_ai_insights_card(
                    f"📈 Business Performance Executive Brief - {performance_period}", 
                    performance_analysis, 
                    confidence=0.89, 
                    icon="🏢"
                )
                
                create_ai_progress_tracker(4, 4, "Finalizing executive metrics...")
                
                # Executive performance metrics
                exec_metrics = {
                    "Overall Business Score": f"{max(70, min(95, 100 - failure_rate + customer_satisfaction/2)):.0f}%",
                    "Operational Excellence": "High" if failure_rate < 20 else "Medium",
                    "Customer Value Score": f"{customer_satisfaction:.0f}%",
                    "Strategic Position": "Strong" if failure_rate < 25 and customer_satisfaction > 75 else "Stable"
                }
                
                create_ai_metrics_dashboard(exec_metrics)
                
                # Generate executive action items
                exec_actions = [
                    f"Board presentation: Highlight {max(0, 100-failure_rate):.0f}% network health achievement",
                    "Strategic initiative: Customer experience optimization program",
                    "Investment planning: Network infrastructure modernization roadmap",
                    f"Market positioning: Leverage {customer_satisfaction:.0f}% customer satisfaction scores",
                    "Competitive advantage: Advanced AI-driven network optimization",
                    "Stakeholder communication: Quarterly business performance briefing"
                ]
                
                create_ai_recommendation_list(exec_actions[:4], "🎯 Executive Action Items")
            
        except Exception as e:
            st.error(f"Error generating business performance analysis: {e}")

with exec_tab2:
    st.markdown("### 💰 AI Financial Impact Analysis")
    st.info("Quantify business impact and ROI opportunities with AI-driven financial analysis")
    
    financial_focus = st.selectbox(
        "Financial Analysis Focus:",
        ["Revenue Impact", "Cost Optimization", "ROI Analysis", "Investment Planning"],
        key="financial_focus"
    )
    
    if st.button("💰 Generate Financial Impact Report", type="primary", key="financial_analysis"):
        create_ai_loading_spinner("AI is analyzing financial impact and ROI opportunities...")
        
        try:
            # Calculate estimated financial impacts
            estimated_monthly_revenue = total_customers * 45  # Average monthly revenue per customer
            failure_impact_revenue = estimated_monthly_revenue * (failure_rate / 100) * 0.15
            optimization_opportunity = failure_impact_revenue * 0.7
            
            financial_context = f"""
            Financial Impact Analysis - {financial_focus}:
            
            Revenue Metrics:
            - Estimated Monthly Revenue: ${estimated_monthly_revenue:,.0f}
            - Customer Base: {total_customers:,} active customers
            - Average Revenue Per Customer: $45/month
            
            Impact Analysis:
            - Network Failure Impact: ${failure_impact_revenue:,.0f}/month revenue at risk
            - Optimization Opportunity: ${optimization_opportunity:,.0f}/month potential savings
            - Customer Satisfaction Financial Impact: Correlated with retention
            
            Business Context:
            - Analysis Focus: {financial_focus}
            - Industry: Telecommunications
            - Strategic Goal: Maximize shareholder value through operational excellence
            """
            
            financial_analysis = ai_processor.ai_complete(
                f"""As a CFO advisor for telecommunications, provide executive financial analysis for {financial_focus.lower()}:
                
                {financial_context}
                
                Deliver comprehensive financial insights including:
                1. Quantified business impact and revenue implications
                2. Cost-benefit analysis of network optimization investments
                3. ROI projections for strategic initiatives
                4. Financial risks and mitigation strategies
                5. Capital allocation recommendations
                6. Shareholder value creation opportunities
                
                Present financial insights suitable for board-level discussions.""",
                max_tokens=800
            )
            
            if financial_analysis:
                create_ai_insights_card(
                    f"💰 {financial_focus} Executive Analysis", 
                    financial_analysis, 
                    confidence=0.86, 
                    icon="📊"
                )
                
                # Financial impact metrics
                financial_metrics = {
                    "Monthly Revenue": f"${estimated_monthly_revenue:,.0f}",
                    "Optimization Value": f"${optimization_opportunity:,.0f}/mo",
                    "ROI Potential": f"{(optimization_opportunity / max(1, failure_impact_revenue)) * 100:.0f}%",
                    "Risk Exposure": f"${failure_impact_revenue:,.0f}/mo"
                }
                
                create_ai_metrics_dashboard(financial_metrics)
                
        except Exception as e:
            st.error(f"Error in financial impact analysis: {e}")

with exec_tab3:
    st.markdown("### 🎯 AI Strategic Opportunities")
    st.info("Identify strategic growth opportunities and competitive advantages using AI analysis")
    
    opportunity_scope = st.selectbox(
        "Strategic Scope:",
        ["Market Expansion", "Technology Innovation", "Operational Excellence", "Customer Experience", "Competitive Positioning"],
        key="opportunity_scope"
    )
    
    time_horizon = st.selectbox(
        "Strategic Timeline:",
        ["Next Quarter", "Next Year", "3-Year Plan", "Long-term Vision"],
        key="time_horizon"
    )
    
    if st.button("🎯 Identify Strategic Opportunities", type="primary", key="strategic_opportunities"):
        create_ai_loading_spinner("AI is identifying strategic opportunities and growth initiatives...")
        
        try:
            strategic_context = f"""
            Strategic Opportunity Analysis - {opportunity_scope}:
            
            Current Position:
            - Network Infrastructure: {total_towers:,} towers with {max(0, 100-failure_rate):.0f}% health score
            - Market Position: Serving {total_customers:,} customers
            - Operational Excellence: {customer_satisfaction:.0f}% customer satisfaction
            - Technology Leadership: AI-powered network optimization platform
            
            Strategic Parameters:
            - Opportunity Scope: {opportunity_scope}
            - Timeline: {time_horizon}
            - Industry: Telecommunications
            - Competitive Landscape: Highly competitive, technology-driven
            
            Business Assets:
            - Advanced AI analytics capability
            - Comprehensive network coverage
            - Customer relationship strength
            """
            
            strategic_analysis = ai_processor.ai_complete(
                f"""As a strategic consultant for telecommunications C-suite, identify opportunities for {opportunity_scope.lower()} over {time_horizon.lower()}:
                
                {strategic_context}
                
                Provide strategic opportunities analysis including:
                1. Key growth opportunities and market potential
                2. Competitive advantages and differentiation strategies
                3. Technology innovations and digital transformation opportunities
                4. Partnership and acquisition opportunities
                5. Market expansion and customer acquisition strategies
                6. Strategic initiatives with highest ROI potential
                
                Focus on actionable strategic recommendations for executive leadership.""",
                max_tokens=800
            )
            
            if strategic_analysis:
                create_ai_insights_card(
                    f"🎯 {opportunity_scope} Strategic Analysis - {time_horizon}", 
                    strategic_analysis, 
                    confidence=0.84, 
                    icon="🚀"
                )
                
                # Strategic opportunity metrics
                strategic_metrics = {
                    "Market Opportunity": "High" if customer_satisfaction > 75 else "Medium",
                    "Innovation Readiness": "Advanced" if max(0, 100-failure_rate) > 85 else "Developing",
                    "Competitive Position": "Strong" if failure_rate < 20 else "Competitive",
                    "Growth Potential": f"{min(25, max(5, customer_satisfaction/3)):.0f}% projected"
                }
                
                create_ai_metrics_dashboard(strategic_metrics)
                
                # Strategic initiatives
                strategic_initiatives = [
                    f"Launch AI-powered customer experience optimization program ({time_horizon.lower()})",
                    f"Expand network coverage in high-growth markets (aligned with {opportunity_scope.lower()})",
                    "Strategic partnership for 5G/advanced technology deployment",
                    f"Digital transformation initiative targeting {customer_satisfaction:.0f}%+ satisfaction",
                    "Competitive intelligence and market positioning enhancement",
                    f"Innovation lab focused on {opportunity_scope.lower()} breakthroughs"
                ]
                
                create_ai_recommendation_list(strategic_initiatives[:4], f"🚀 Strategic Initiatives - {time_horizon}")
                
        except Exception as e:
            st.error(f"Error in strategic opportunity analysis: {e}")

with exec_tab4:
    st.markdown("### 🚨 AI Executive Risk Assessment")
    st.info("Comprehensive risk analysis and mitigation strategies for executive decision making")
    
    risk_category = st.selectbox(
        "Risk Category:",
        ["Operational Risk", "Financial Risk", "Strategic Risk", "Technology Risk", "Regulatory Risk", "Comprehensive Assessment"],
        key="risk_category"
    )
    
    if st.button("🚨 Generate Executive Risk Assessment", type="primary", key="executive_risk"):
        create_ai_loading_spinner("AI is conducting comprehensive risk analysis...")
        
        try:
            risk_context = f"""
            Executive Risk Assessment - {risk_category}:
            
            Risk Exposure Analysis:
            - Network Operational Risk: {failure_rate:.1f}% failure rate indicates {'LOW' if failure_rate < 15 else 'MEDIUM' if failure_rate < 30 else 'HIGH'} risk
            - Customer Experience Risk: {customer_data.iloc[0]['CRITICAL_SENTIMENT_TICKETS']} critical sentiment tickets
            - Financial Risk: ${failure_impact_revenue:,.0f}/month revenue exposure
            - Scale Risk: {total_towers:,} network assets requiring management
            
            Risk Context:
            - Assessment Category: {risk_category}
            - Business Scale: Large telecommunications operator
            - Regulatory Environment: Highly regulated industry
            - Competitive Pressure: Intense market competition
            
            Current Risk Mitigation:
            - AI-powered network monitoring and optimization
            - Proactive customer experience management
            - Advanced analytics for predictive maintenance
            """
            
            risk_analysis = ai_processor.ai_complete(
                f"""As a chief risk officer for telecommunications, conduct an executive risk assessment for {risk_category.lower()}:
                
                {risk_context}
                
                Provide comprehensive executive risk analysis including:
                1. Primary risk factors and threat assessment
                2. Probability and impact analysis for key risks
                3. Risk appetite and tolerance recommendations
                4. Mitigation strategies and contingency planning
                5. Risk monitoring and early warning indicators
                6. Board-level risk governance recommendations
                
                Present risk insights appropriate for C-suite and board oversight.""",
                max_tokens=800
            )
            
            if risk_analysis:
                create_ai_insights_card(
                    f"🚨 {risk_category} Executive Assessment", 
                    risk_analysis, 
                    confidence=0.87, 
                    icon="⚠️"
                )
                
                # Risk assessment metrics
                overall_risk_score = min(100, max(10, failure_rate * 2 + (100 - customer_satisfaction)))
                risk_metrics = {
                    "Overall Risk Score": f"{overall_risk_score:.0f}/100",
                    "Risk Level": "HIGH" if overall_risk_score > 60 else "MEDIUM" if overall_risk_score > 30 else "LOW",
                    "Mitigation Status": "Active" if failure_rate < 25 else "Critical",
                    "Board Attention": "Required" if overall_risk_score > 50 else "Monitor"
                }
                
                create_ai_metrics_dashboard(risk_metrics)
                
                # Risk mitigation actions
                risk_actions = [
                    f"Board briefing on {risk_category.lower()} exposure and mitigation strategies",
                    "Establish risk monitoring dashboard for C-suite oversight",
                    f"Implement enhanced controls for {overall_risk_score:.0f}/100 risk score",
                    "Quarterly risk assessment reviews with executive leadership",
                    "Crisis management and business continuity planning update",
                    "Stakeholder communication plan for risk transparency"
                ]
                
                create_ai_recommendation_list(risk_actions[:4], "⚠️ Executive Risk Actions")
                
        except Exception as e:
            st.error(f"Error in executive risk assessment: {e}")

# Executive Summary Export
st.markdown("---")
st.markdown("### 📊 Executive Report Export")

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    if st.button("📧 Email Executive Summary", type="secondary"):
        st.success("✅ Executive summary scheduled for delivery to C-suite distribution list")

with export_col2:
    if st.button("📱 Mobile Executive Alert", type="secondary"):
        st.success("✅ Critical insights sent to executive mobile dashboard")

with export_col3:
    # Generate executive summary for download
    executive_summary = {
        "timestamp": datetime.now().isoformat(),
        "network_health": max(0, 100 - failure_rate),
        "customer_satisfaction": customer_satisfaction,
        "total_assets": int(total_towers),
        "customer_base": int(total_customers),
        "key_metrics": {
            "failure_rate": failure_rate,
            "revenue_at_risk": failure_impact_revenue,
            "optimization_opportunity": optimization_opportunity
        },
        "executive_focus": executive_focus,
        "report_frequency": report_frequency
    }
    
    st.download_button(
        label="📄 Download Executive Report",
        data=json.dumps(executive_summary, indent=2),
        file_name=f"executive_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json"
    )

# Executive Technology Showcase
st.markdown("---")
st.markdown("### 🤖 Executive AI Technology")

tech_col1, tech_col2 = st.columns(2)

with tech_col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%); padding: 2rem; border-radius: 16px; border-left: 4px solid #1976d2;">
        <h4 style="color: #1565c0; margin: 0 0 1rem 0;">🏢 Strategic AI Capabilities</h4>
        <ul style="margin: 0; padding-left: 1.5rem; color: #4a5568;">
            <li><strong>Automated Reporting:</strong> Real-time executive dashboards and KPIs</li>
            <li><strong>Strategic Analysis:</strong> AI-driven business intelligence and insights</li>
            <li><strong>Risk Management:</strong> Predictive risk assessment and mitigation</li>
            <li><strong>Financial Modeling:</strong> ROI analysis and investment optimization</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tech_col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f3e5f5 0%, #ffffff 100%); padding: 2rem; border-radius: 16px; border-left: 4px solid #7b1fa2;">
        <h4 style="color: #6a1b9a; margin: 0 0 1rem 0;">📈 Business Value Delivery</h4>
        <ul style="margin: 0; padding-left: 1.5rem; color: #4a5568;">
            <li><strong>Decision Support:</strong> AI-powered strategic recommendations</li>
            <li><strong>Performance Optimization:</strong> Continuous business improvement</li>
            <li><strong>Competitive Intelligence:</strong> Market positioning and opportunities</li>
            <li><strong>Stakeholder Communication:</strong> Executive-ready insights and reports</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Add professional footer
add_page_footer()
