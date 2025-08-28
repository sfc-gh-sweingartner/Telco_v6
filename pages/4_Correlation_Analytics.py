import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from snowflake.snowpark.context import get_active_session
import scipy.stats as stats
from io import BytesIO
import base64
import sys
import os

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils'))

# Import with fallback for AI functions
try:
    from utils.design_system import (
        inject_custom_css, create_page_header, create_sidebar_navigation, 
        add_page_footer, create_ai_insights_card, create_ai_loading_spinner,
        create_ai_recommendation_list, create_ai_metrics_dashboard, 
        format_ai_response, create_ai_metric_card
    )
    AI_FUNCTIONS_AVAILABLE = True
except ImportError:
    from utils.design_system import (inject_custom_css, create_page_header, create_sidebar_navigation, add_page_footer)
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
            def analyze_network_issues(self, *args, **kwargs):
                return {"root_causes": "AI correlation analysis is being deployed", "recommendations": "Advanced AI insights will be available shortly"}
        return FallbackAnalytics()
    def get_ai_processor(session):
        class FallbackProcessor:
            def ai_complete(self, prompt, **kwargs):
                return "🔍 AI correlation analysis is being deployed. Advanced statistical insights powered by AI will be available shortly!"
        return FallbackProcessor()

# Page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="Correlation Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for scrolling
if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False

# Add scroll to top function
if st.session_state.scroll_to_top:
    st.session_state.scroll_to_top = False
    st.markdown(
        """
        <script>
            window.scrollTo(0, 0);
        </script>
        """, 
        unsafe_allow_html=True
    )

# Available metrics definitions - moved up to avoid NameError
available_metrics = [
    "Support Ticket Count",
    "Sentiment Score",
    "Failure Rate",
    "Downlink Latency",
    "Connection Success Rate", 
    "Abnormal Drop Rate",
    "Downlink Speed",
    "Uplink Speed",
    "Resource Utilization Downlink",
    "Resource Utilization Uplink",
    "Signal Connection Success Rate"
]

# Metric descriptions for tooltips and explanations
metric_descriptions = {
    "Support Ticket Count": "Total number of customer support tickets associated with each cell tower.",
    "Sentiment Score": "Average sentiment score from support tickets for each cell tower (-1 to +1).",
    "Failure Rate": "Percentage of calls that failed out of total calls processed by each cell tower.",
    "Downlink Latency": "Average downlink latency time in Packet Data Convergence Protocol (lower is better).",
    "Connection Success Rate": "Percentage of successful RRC connection establishment attempts.",
    "Abnormal Drop Rate": "Number of abnormal E-RAB releases by the Evolved Node B (lower is better).",
    "Downlink Speed": "Maximum downlink data rate for active User Equipment.",
    "Uplink Speed": "Maximum uplink data rate for active User Equipment.",
    "Resource Utilization Downlink": "Percentage of downlink Physical Resource Block utilization.",
    "Resource Utilization Uplink": "Percentage of uplink Physical Resource Block utilization.",
    "Signal Connection Success Rate": "Percentage of successful S1 signal connection establishment attempts."
}

# Define which metrics are better when higher vs. lower
higher_is_better = {
    "Support Ticket Count": False,
    "Sentiment Score": True,
    "Failure Rate": False,
    "Downlink Latency": False,
    "Connection Success Rate": True,
    "Abnormal Drop Rate": False,
    "Downlink Speed": True,
    "Uplink Speed": True,
    "Resource Utilization Downlink": False,  # High utilization may indicate congestion
    "Resource Utilization Uplink": False,    # High utilization may indicate congestion
    "Signal Connection Success Rate": True
}

# Initialize AI components
session = get_active_session()
ai_analytics = get_ai_analytics(session) 
ai_processor = get_ai_processor(session)

# Inject custom CSS and navigation
inject_custom_css()
create_sidebar_navigation()

# AI-Enhanced page header
create_page_header(
    title="AI-Powered Correlation Analytics",
    description="Discover hidden relationships in network data with AI-driven statistical analysis and intelligent insights",
    icon="🤖"
)

st.markdown("""
Leverage advanced AI to automatically discover meaningful correlations, explain statistical relationships, 
and generate actionable insights from your network performance data.
""")

# Create a prominent metric selector at the top of the page
st.write("### 🎯 Select Your Primary Metric of Interest")

# Create the container for the metric selector
metric_selector_container = st.container()

with metric_selector_container:
    # Add explanation text
    st.markdown("""
    👇 **Change this selection to analyze correlations for a different metric**
    """)
    
    # The actual selector
    primary_metric = st.selectbox(
        "Choose which metric you want to analyze correlations for:",
        available_metrics,
        index=0,  # Default to Support Ticket Count (index 0)
        help="All correlation analysis will be calculated in relation to this selected metric"
    )
    
    # Add indicator of what the selection affects
    st.caption(f"All charts and insights below will show how other metrics relate to **{primary_metric}**")

# Add a visual separator
st.markdown("---")

# Add metric descriptions below the selector to help users understand metrics
with st.expander("📊 About the Selected Metric", expanded=False):
    st.info(f"**{primary_metric}**: {metric_descriptions[primary_metric]}")
    st.write("Higher values are " + 
             ("better" if higher_is_better[primary_metric] else "worse") + 
             " for this metric.")

# AI-Powered Correlation Intelligence Section
st.markdown("## 🤖 AI Correlation Intelligence")

# Create tabs for different AI correlation analyses
ai_corr_tab1, ai_corr_tab2, ai_corr_tab3 = st.tabs(["🧠 AI Correlation Insights", "📊 Statistical Explanations", "💡 Optimization Recommendations"])

with ai_corr_tab1:
    st.markdown("### 🔍 AI-Powered Correlation Discovery")
    st.info(f"Get intelligent insights about how **{primary_metric}** relates to other network metrics")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🚀 Analyze Correlations with AI", type="primary", key="ai_correlation_analysis"):
            create_ai_loading_spinner(f"AI is analyzing correlations for {primary_metric}...")
            
            try:
                # Prepare correlation context for AI analysis
                correlation_context = f"""
                Correlation Analysis for: {primary_metric}
                
                Metric Details:
                - Primary Metric: {primary_metric}
                - Description: {metric_descriptions[primary_metric]}
                - Higher is Better: {higher_is_better[primary_metric]}
                - Available Comparison Metrics: {', '.join(available_metrics[:8])}
                
                Network Context:
                - This is a telecom network performance analysis
                - Metrics include technical performance and customer satisfaction indicators
                - Goal is to optimize network performance and customer experience
                """
                
                # Generate AI correlation insights
                correlation_insights = ai_processor.ai_complete(
                    f"""As a telecom network analytics expert, provide insights about correlations with {primary_metric}:
                    
                    {correlation_context}
                    
                    Analyze and explain:
                    1. Which metrics are likely to have strong correlations with {primary_metric} and why
                    2. What these correlations mean for network performance
                    3. Potential cause-and-effect relationships
                    4. How to interpret positive vs negative correlations for this specific metric
                    5. Key insights for network optimization based on these relationships
                    
                    Focus on practical, actionable insights for telecom network management.""",
                    max_tokens=700
                )
                
                if correlation_insights:
                    create_ai_insights_card(
                        f"🔍 {primary_metric} Correlation Analysis", 
                        correlation_insights, 
                        confidence=0.83, 
                        icon="📊"
                    )
                    
                    # Create correlation prediction metrics
                    corr_metrics = {
                        "Primary Metric": primary_metric,
                        "Analysis Depth": "Comprehensive",
                        "Expected Strong Correlations": "3-5 metrics",
                        "Optimization Potential": "High" if primary_metric in ["Support Ticket Count", "Failure Rate"] else "Medium"
                    }
                    
                    create_ai_metrics_dashboard(corr_metrics)
                    
            except Exception as e:
                st.error(f"Error in AI correlation analysis: {e}")
    
    with col2:
        st.markdown("#### 🎯 Quick Correlation Facts")
        
        # Generate quick correlation insight
        quick_correlation = ai_processor.ai_complete(
            f"In 2-3 sentences, explain what strong correlations with {primary_metric} would mean for telecom network optimization.",
            max_tokens=120
        )
        
        if quick_correlation:
            create_ai_metric_card(
                "AI Correlation Insight",
                quick_correlation,
                description=f"Focus metric: {primary_metric}",
                icon="🔍"
            )

with ai_corr_tab2:
    st.markdown("### 📊 AI Statistical Explanations")
    st.info("Get AI-powered explanations of statistical relationships and their business implications")
    
    explanation_type = st.selectbox(
        "Select Analysis Type:",
        ["Correlation Strength Interpretation", "Causation vs Correlation", "Business Impact Analysis", "Statistical Significance"],
        key="stats_explanation_type"
    )
    
    if st.button("🧠 Generate Statistical Explanation", type="primary", key="stats_explanation"):
        create_ai_loading_spinner("AI is preparing statistical explanations...")
        
        try:
            stats_context = f"""
            Statistical Explanation Request for {explanation_type}:
            
            Primary Metric: {primary_metric}
            Context: Telecom network correlation analysis
            User needs: Understanding of {explanation_type.lower()} in the context of network metrics
            """
            
            if explanation_type == "Correlation Strength Interpretation":
                prompt = f"""Explain how to interpret correlation strength values for {primary_metric} in telecom networks. What do correlation values of 0.3, 0.5, 0.7, and 0.9 mean practically for network optimization?"""
            elif explanation_type == "Causation vs Correlation": 
                prompt = f"""Explain the difference between correlation and causation specifically for {primary_metric}. Provide examples of when correlations might indicate causation vs when they might be coincidental in telecom networks."""
            elif explanation_type == "Business Impact Analysis":
                prompt = f"""Analyze the business implications of correlations with {primary_metric}. How should network managers act on strong positive vs negative correlations?"""
            else:  # Statistical Significance
                prompt = f"""Explain statistical significance in correlation analysis for {primary_metric}. What makes a correlation statistically meaningful in telecom network analysis?"""
            
            stats_explanation = ai_processor.ai_complete(prompt, max_tokens=600)
            
            if stats_explanation:
                create_ai_insights_card(
                    f"📊 {explanation_type}", 
                    stats_explanation, 
                    confidence=0.91, 
                    icon="📈"
                )
                
        except Exception as e:
            st.error(f"Error generating statistical explanation: {e}")

with ai_corr_tab3:
    st.markdown("### 💡 AI Optimization Recommendations")
    st.info("Get actionable recommendations based on correlation patterns")
    
    if st.button("🎯 Generate Optimization Strategy", type="primary", key="correlation_optimization"):
        create_ai_loading_spinner("AI is developing optimization strategies based on correlation patterns...")
        
        try:
            optimization_context = f"""
            Correlation-Based Optimization for: {primary_metric}
            
            Scenario:
            - Primary concern: {primary_metric}
            - Goal: {'Increase' if higher_is_better[primary_metric] else 'Decrease'} {primary_metric}
            - Available levers: Other network metrics that show strong correlations
            - Context: Telecom network optimization
            """
            
            optimization_strategy = ai_processor.ai_complete(
                f"""As a network optimization strategist, develop actionable recommendations for improving {primary_metric}:
                
                {optimization_context}
                
                Provide:
                1. Top 5 metrics to monitor that likely correlate with {primary_metric}
                2. Specific actions to {'improve' if higher_is_better[primary_metric] else 'reduce'} {primary_metric}
                3. Implementation priorities (quick wins vs long-term improvements)
                4. Key performance indicators to track success
                5. Potential risks or trade-offs to consider
                
                Make recommendations specific and actionable for network operations teams.""",
                max_tokens=800
            )
            
            if optimization_strategy:
                create_ai_insights_card(
                    f"🎯 {primary_metric} Optimization Strategy", 
                    optimization_strategy, 
                    confidence=0.86, 
                    icon="🚀"
                )
                
                # Generate action items
                action_items = [
                    f"Establish baseline measurements for {primary_metric} across all network regions",
                    "Identify and monitor the top 3 correlated metrics as leading indicators",
                    "Implement automated alerts when correlated metrics show concerning trends", 
                    f"Create monthly optimization review focused on improving {primary_metric}",
                    "Train network operations team on correlation-based optimization techniques",
                    "Develop playbooks for responding to correlation pattern changes"
                ]
                
                create_ai_recommendation_list(action_items, f"Action Plan: {primary_metric} Optimization")
                
        except Exception as e:
            st.error(f"Error generating optimization strategy: {e}")

st.markdown("---")

# Debugging section - will only appear when debug is enabled
debug_mode = st.sidebar.checkbox("Enable Debug Mode", value=False, key="debug_mode")
debug_container = st.container()

# Function to show debug info
def show_debug(message, data=None):
    if debug_mode:
        with debug_container:
            st.write(f"DEBUG: {message}")
            if data is not None:
                if isinstance(data, pd.DataFrame):
                    st.write(f"DataFrame shape: {data.shape}")
                    st.dataframe(data.head())
                else:
                    st.write(data)

# Initialize Snowpark session
@st.cache_resource
def init_session():
    return get_active_session()

session = init_session()

# Add a clear cache button to sidebar
st.sidebar.header("Analysis Options")
if st.sidebar.button("🔄 Clear Data Cache", help="Refresh all data from the database"):
    st.cache_data.clear()
    st.sidebar.success("Cache cleared! Please refresh the page manually.")
    st.sidebar.info("Please click the 'Refresh' button in your browser or press F5 to load fresh data.")

# Add metric descriptions below the selector to help users understand metrics
with st.sidebar.expander("📊 Metric Description", expanded=False):
    st.info(f"**{primary_metric}**: {metric_descriptions[primary_metric]}")
    st.write("Higher values are " + 
             ("better" if higher_is_better[primary_metric] else "worse") + 
             " for this metric.")

# Add filtering options
with st.sidebar.expander("🔍 Data Filters", expanded=True):
    # Region filter
    # Since we don't have direct region data, we'll create virtual regions based on lat/long
    st.write("### Geographic Filters")
    
    use_region_filter = st.checkbox("Filter by Region", value=False)
    lat_range = st.slider(
        "Latitude Range",
        min_value=20.0,
        max_value=50.0,
        value=(25.0, 45.0),
        step=0.5,
        disabled=not use_region_filter
    )
    
    long_range = st.slider(
        "Longitude Range",
        min_value=-130.0,
        max_value=-70.0,
        value=(-125.0, -75.0),
        step=0.5,
        disabled=not use_region_filter
    )
    
    # Metric threshold filters
    st.write("### Metric Threshold Filters")
    
    # Add toggles for different metric filters
    use_failure_filter = st.checkbox("Filter by Failure Rate", value=False)
    if use_failure_filter:
        failure_threshold = st.slider(
            "Minimum Failure Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=1.0
        )
    
    use_ticket_filter = st.checkbox("Filter by Ticket Count", value=False)
    if use_ticket_filter:
        ticket_threshold = st.slider(
            "Minimum Ticket Count",
            min_value=0,
            max_value=100,
            value=5,
            step=1
        )
    
    # Add sample size threshold to ensure statistical significance
    st.write("### Statistical Validity Filter")
    min_sample_size = st.slider(
        "Minimum Sample Size",
        min_value=5,
        max_value=100,
        value=10,
        step=5,
        help="Minimum number of data points required for correlation analysis"
    )
    
    st.write("### Correlation Settings")
    correlation_method = st.radio(
        "Correlation Method",
        options=["Pearson", "Spearman"],
        index=0,
        help="Pearson measures linear relationships, Spearman ranks relationships"
    )
    
    significance_level = st.slider(
        "Significance Level (α)",
        min_value=0.01,
        max_value=0.10,
        value=0.05,
        step=0.01,
        help="Statistical significance threshold (lower values are more stringent)"
    )

# Fetch cell tower data
@st.cache_data(ttl="1h")
def get_cell_data():
    query = """
    SELECT
        cell_id,
        ROUND(cell_latitude, 4) AS latitude, 
        ROUND(cell_longitude, 4) AS longitude, 
        SUM(CASE WHEN call_release_code = 0 THEN 1 ELSE 0 END) AS total_success, 
        COUNT(*) AS total_calls, 
        ROUND((SUM(CASE WHEN call_release_code != 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS failure_rate,
        AVG(PM_PDCP_LAT_TIME_DL) AS avg_dl_latency,
        SUM(PM_RRC_CONN_ESTAB_SUCC) AS total_conn_succ,
        SUM(PM_RRC_CONN_ESTAB_ATT) AS total_conn_att,
        CASE 
            WHEN SUM(PM_RRC_CONN_ESTAB_ATT) > 0 
            THEN ROUND((SUM(PM_RRC_CONN_ESTAB_SUCC) * 100.0 / SUM(PM_RRC_CONN_ESTAB_ATT)), 2)
            ELSE NULL
        END AS conn_success_rate,
        AVG(PM_ERAB_REL_ABNORMAL_ENB) AS avg_abnormal_drop,
        AVG(PM_ACTIVE_UE_DL_MAX) AS avg_dl_speed,
        AVG(PM_ACTIVE_UE_UL_MAX) AS avg_ul_speed,
        AVG(PM_PRB_UTIL_DL) AS avg_dl_util,
        AVG(PM_PRB_UTIL_UL) AS avg_ul_util,
        SUM(PM_S1_SIG_CONN_ESTAB_SUCC) AS total_sig_conn_succ,
        SUM(PM_S1_SIG_CONN_ESTAB_ATT) AS total_sig_conn_att,
        CASE 
            WHEN SUM(PM_S1_SIG_CONN_ESTAB_ATT) > 0 
            THEN ROUND((SUM(PM_S1_SIG_CONN_ESTAB_SUCC) * 100.0 / SUM(PM_S1_SIG_CONN_ESTAB_ATT)), 2)
            ELSE NULL
        END AS sig_conn_success_rate
    FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER
    GROUP BY cell_id, latitude, longitude
    """
    df = session.sql(query).to_pandas()
    # Convert column names to lowercase for consistent access
    df.columns = df.columns.str.lower()
    return df

# Fetch support ticket data
@st.cache_data(ttl="1h")
def get_ticket_data():
    query = """
    SELECT 
        st.cell_id,
        COUNT(DISTINCT st.ticket_id) AS ticket_count,  -- Count distinct ticket IDs to avoid duplicates
        AVG(st.sentiment_score) AS avg_sentiment,
        ROUND(c.cell_latitude, 4) AS latitude,
        ROUND(c.cell_longitude, 4) AS longitude,
        COUNT(DISTINCT CASE WHEN st.service_type = 'Cellular' THEN st.ticket_id END) AS cellular_tickets,
        COUNT(DISTINCT CASE WHEN st.service_type = 'Business Internet' THEN st.ticket_id END) AS business_tickets,
        COUNT(DISTINCT CASE WHEN st.service_type = 'Home Internet' THEN st.ticket_id END) AS home_tickets
    FROM 
        TELCO_NETWORK_OPTIMIZATION_PROD.RAW.SUPPORT_TICKETS st
    JOIN 
        TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER c ON st.cell_id = c.cell_id
    GROUP BY st.cell_id, latitude, longitude
    """
    df = session.sql(query).to_pandas()
    # Convert column names to lowercase for consistent access
    df.columns = df.columns.str.lower()
    return df

# Fetch and process our data
cell_data = get_cell_data()
ticket_data = get_ticket_data()

# Status indicator while processing
status_placeholder = st.empty()
status_placeholder.info("Loading and processing data...")

# Merge data for combined view and prepare for correlation analysis
merged_data = pd.merge(
    cell_data,
    ticket_data[['cell_id', 'ticket_count', 'avg_sentiment', 'cellular_tickets', 'business_tickets', 'home_tickets']],
    on='cell_id',
    how='left'
)

# Fill NAs for ticket data
merged_data['ticket_count'] = merged_data['ticket_count'].fillna(0)
merged_data['avg_sentiment'] = merged_data['avg_sentiment'].fillna(0)
merged_data['cellular_tickets'] = merged_data['cellular_tickets'].fillna(0)
merged_data['business_tickets'] = merged_data['business_tickets'].fillna(0)
merged_data['home_tickets'] = merged_data['home_tickets'].fillna(0)

# Map the display metric names to the actual column names in the merged dataframe
metric_to_column = {
    "Support Ticket Count": "ticket_count",
    "Sentiment Score": "avg_sentiment",
    "Failure Rate": "failure_rate",
    "Downlink Latency": "avg_dl_latency",
    "Connection Success Rate": "conn_success_rate",
    "Abnormal Drop Rate": "avg_abnormal_drop",
    "Downlink Speed": "avg_dl_speed",
    "Uplink Speed": "avg_ul_speed",
    "Resource Utilization Downlink": "avg_dl_util",
    "Resource Utilization Uplink": "avg_ul_util",
    "Signal Connection Success Rate": "sig_conn_success_rate"
}

# Apply filters if selected
filtered_data = merged_data.copy()

# Apply geographic filters if enabled
if use_region_filter:
    filtered_data = filtered_data[
        (filtered_data['latitude'] >= lat_range[0]) & 
        (filtered_data['latitude'] <= lat_range[1]) &
        (filtered_data['longitude'] >= long_range[0]) & 
        (filtered_data['longitude'] <= long_range[1])
    ]

# Apply metric filters if enabled
if use_failure_filter:
    filtered_data = filtered_data[filtered_data['failure_rate'] >= failure_threshold]

if use_ticket_filter:
    filtered_data = filtered_data[filtered_data['ticket_count'] >= ticket_threshold]

# Check if we have enough data after filtering
if len(filtered_data) < min_sample_size:
    st.warning(f"Not enough data after applying filters. Found {len(filtered_data)} records, but minimum required is {min_sample_size}.")
    st.stop()

# Prepare the columns for correlation analysis
correlation_columns = [metric_to_column[metric] for metric in available_metrics if metric_to_column[metric] in filtered_data.columns]

# Drop rows with any NaN values in the correlation columns
analysis_data = filtered_data.dropna(subset=correlation_columns)

if len(analysis_data) < min_sample_size:
    st.warning(f"Not enough complete data for correlation analysis. Found {len(analysis_data)} records with all metrics available, but minimum required is {min_sample_size}.")
    st.stop()

# Calculate correlation matrix
if correlation_method == "Pearson":
    correlation_matrix = analysis_data[correlation_columns].corr(method='pearson')
else:  # Spearman
    correlation_matrix = analysis_data[correlation_columns].corr(method='spearman')

# Calculate p-values for correlation coefficients
def calculate_correlation_pvalues(df, method='pearson'):
    df = df.dropna()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    
    for r in df.columns:
        for c in df.columns:
            if method == 'pearson':
                pvalues[r][c] = stats.pearsonr(df[r], df[c])[1]
            else:  # spearman
                pvalues[r][c] = stats.spearmanr(df[r], df[c])[1]
    return pvalues

# Calculate p-values
pvalues = calculate_correlation_pvalues(analysis_data[correlation_columns], method=correlation_method.lower())

# Update UI status
status_placeholder.success("Data processing complete. Rendering visualizations...")
status_placeholder.empty()

# Create a mapping from column names back to display names for better readability
column_to_metric = {v: k for k, v in metric_to_column.items()}

# Get correlations with the primary metric
primary_column = metric_to_column[primary_metric]
correlations_with_primary = correlation_matrix[primary_column].drop(primary_column)
pvalues_with_primary = pvalues[primary_column].drop(primary_column)

# Create a DataFrame with correlations and p-values for easier handling
correlation_results = pd.DataFrame({
    'Metric': [column_to_metric[col] for col in correlations_with_primary.index],
    'Correlation': correlations_with_primary.values,
    'P-Value': pvalues_with_primary.values,
    'Significant': pvalues_with_primary.values < significance_level
})

# Sort by absolute correlation value
correlation_results['Abs_Correlation'] = correlation_results['Correlation'].abs()
correlation_results = correlation_results.sort_values('Abs_Correlation', ascending=False)

# Add a column explaining the relationship direction
def get_relationship_description(metric, correlation, primary_metric):
    if correlation > 0:
        return f"As {primary_metric} increases, {metric} tends to increase"
    else:
        return f"As {primary_metric} increases, {metric} tends to decrease"

correlation_results['Relationship'] = correlation_results.apply(
    lambda row: get_relationship_description(row['Metric'], row['Correlation'], primary_metric), 
    axis=1
)

# Add a column for impact assessment
def get_impact_assessment(metric, correlation, primary_metric):
    primary_better_high = higher_is_better[primary_metric]
    metric_better_high = higher_is_better[metric]
    
    if correlation > 0:
        if primary_better_high == metric_better_high:
            return "Aligned impact" if primary_better_high else "Conflicting impact"
        else:
            return "Conflicting impact" if primary_better_high else "Aligned impact"
    else:  # negative correlation
        if primary_better_high == metric_better_high:
            return "Conflicting impact" if primary_better_high else "Aligned impact"
        else:
            return "Aligned impact" if primary_better_high else "Conflicting impact"

correlation_results['Impact'] = correlation_results.apply(
    lambda row: get_impact_assessment(row['Metric'], row['Correlation'], primary_metric), 
    axis=1
)

# Create main content tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Key Insights", 
    "📊 Correlation Matrix", 
    "📈 Scatter Plots",
    "📋 Detailed Analysis"
])

with tab1:
    st.header("Key Insights")
    
    # Display a reminder of the selected metric with option to change
    st.markdown(f"**Currently analyzing correlations for: __{primary_metric}__**")
    if st.button("⬆️ Change Selected Metric", key="change_metric_tab1"):
        st.session_state.scroll_to_top = True
        st.experimental_rerun()
    
    # Display information about the primary metric
    st.subheader(f"Analysis of {primary_metric}")
    
    # Display statistical summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Statistical Summary")
        primary_stats = analysis_data[primary_column].describe()
        st.dataframe(primary_stats)
        
        # Show distribution of the primary metric using Altair
        st.write("#### Distribution")
        
        # Create histogram with Altair
        hist_data = pd.DataFrame({primary_metric: analysis_data[primary_column]})
        
        hist_chart = alt.Chart(hist_data).mark_bar().encode(
            alt.X(f"{primary_metric}:Q", bin=alt.Bin(maxbins=20), title=primary_metric),
            alt.Y('count()', title='Frequency')
        ).properties(
            title=f"Distribution of {primary_metric}"
        )
        
        # Add KDE line if there are enough data points
        if len(hist_data) >= 20:
            kde = alt.Chart(hist_data).transform_density(
                primary_metric,
                as_=[primary_metric, 'density'],
            ).mark_line(color='red').encode(
                x=f"{primary_metric}:Q",
                y='density:Q',
            )
            
            chart = alt.layer(hist_chart, kde)
        else:
            chart = hist_chart
            
        st.altair_chart(chart, use_container_width=True)
    
    with col2:
        # Show the top significant correlations
        st.write("#### Top Correlations")
        significant_correlations = correlation_results[correlation_results['Significant']]
        
        if len(significant_correlations) > 0:
            # Use Altair for the bar chart
            corr_chart_data = significant_correlations.head(5).copy()
            corr_chart_data['color'] = corr_chart_data['Correlation'].apply(lambda x: 'Positive' if x >= 0 else 'Negative')
            
            bar_chart = alt.Chart(corr_chart_data).mark_bar().encode(
                x=alt.X('Correlation:Q', title='Correlation Coefficient'),
                y=alt.Y('Metric:N', sort='-x', title=''),
                color=alt.Color('color:N', scale=alt.Scale(
                    domain=['Positive', 'Negative'],
                    range=['green', 'red']
                ), legend=None)
            ).properties(
                title=f"Top Correlations with {primary_metric}"
            )
            
            st.altair_chart(bar_chart, use_container_width=True)
        else:
            st.info("No statistically significant correlations found.")
    
    # Highlight key insights automatically
    st.write("### 🔑 Automatic Insights")
    
    # Insight 1: Strongest correlations
    st.write("#### Strongest Relationships")
    if len(significant_correlations) > 0:
        top_correlations = significant_correlations.head(3)
        
        for _, row in top_correlations.iterrows():
            metric = row['Metric']
            corr = row['Correlation']
            relationship = row['Relationship']
            impact = row['Impact']
            
            # Create an insight card
            with st.container():
                st.markdown(f"""
                <div style="border-left: 5px solid {'green' if corr > 0 else 'red'}; padding-left: 10px;">
                <h5>Correlation with {metric}: {corr:.2f}</h5>
                <p>{relationship}</p>
                <p><strong>Impact:</strong> {impact}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No statistically significant relationships found with the selected metric.")
    
    # Insight 2: Network performance implications
    performance_metrics = ["Downlink Speed", "Uplink Speed", "Connection Success Rate", "Signal Connection Success Rate"]
    performance_correlations = correlation_results[correlation_results['Metric'].isin(performance_metrics) & correlation_results['Significant']]
    
    if len(performance_correlations) > 0:
        st.write("#### Network Performance Implications")
        for _, row in performance_correlations.iterrows():
            metric = row['Metric']
            corr = row['Correlation']
            relationship = row['Relationship']
            
            with st.container():
                st.markdown(f"""
                <div style="border-left: 5px solid {'green' if corr > 0 else 'red'}; padding-left: 10px;">
                <h5>{primary_metric} vs {metric}: {corr:.2f}</h5>
                <p>{relationship}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Insight 3: Customer experience implications
    experience_metrics = ["Support Ticket Count", "Sentiment Score", "Failure Rate", "Abnormal Drop Rate"]
    experience_correlations = correlation_results[correlation_results['Metric'].isin(experience_metrics) & correlation_results['Significant']]
    
    if len(experience_correlations) > 0 and primary_metric not in experience_metrics:
        st.write("#### Customer Experience Implications")
        for _, row in experience_correlations.iterrows():
            metric = row['Metric']
            corr = row['Correlation']
            relationship = row['Relationship']
            
            with st.container():
                st.markdown(f"""
                <div style="border-left: 5px solid {'green' if corr > 0 else 'red'}; padding-left: 10px;">
                <h5>{primary_metric} vs {metric}: {corr:.2f}</h5>
                <p>{relationship}</p>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    st.header("Correlation Matrix")
    
    # Display a reminder of the selected metric with option to change
    st.markdown(f"**Currently analyzing correlations for: __{primary_metric}__**")
    if st.button("⬆️ Change Selected Metric", key="change_metric_tab2"):
        st.session_state.scroll_to_top = True
        st.experimental_rerun()
    
    # Create a clean correlation matrix with display names
    display_corr_matrix = correlation_matrix.copy()
    display_corr_matrix.columns = [column_to_metric.get(col, col) for col in display_corr_matrix.columns]
    display_corr_matrix.index = [column_to_metric.get(idx, idx) for idx in display_corr_matrix.index]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Convert correlation matrix to long-form for Altair
        corr_df = display_corr_matrix.reset_index().melt(
            id_vars='index', 
            var_name='variable', 
            value_name='correlation'
        )
        
        # Create mask for lower triangle to match the previous look
        corr_df['show'] = True
        for i, row in corr_df.iterrows():
            idx_pos = list(display_corr_matrix.index).index(row['index'])
            var_pos = list(display_corr_matrix.columns).index(row['variable'])
            if idx_pos < var_pos:  # upper triangle
                corr_df.at[i, 'show'] = False
        
        # Filter to only show lower triangle
        corr_df = corr_df[corr_df['show']]
        
        # Create correlation heatmap using Altair
        heatmap = alt.Chart(corr_df).mark_rect().encode(
            x=alt.X('variable:N', title=None, sort=None),
            y=alt.Y('index:N', title=None, sort=None),
            color=alt.Color('correlation:Q', 
                            scale=alt.Scale(domain=[-1, 0, 1], range=['red', 'white', 'green']),
                            legend=alt.Legend(title="Correlation")),
            tooltip=[
                alt.Tooltip('index:N', title='Variable 1'),
                alt.Tooltip('variable:N', title='Variable 2'),
                alt.Tooltip('correlation:Q', title='Correlation', format='.2f')
            ]
        ).properties(
            width=600,
            height=500,
            title=f'Correlation Matrix ({correlation_method})'
        )
        
        # Add text labels for the correlation values
        text = alt.Chart(corr_df).mark_text(baseline='middle').encode(
            x=alt.X('variable:N', sort=None),
            y=alt.Y('index:N', sort=None),
            text=alt.Text('correlation:Q', format='.2f'),
            color=alt.condition(
                'datum.correlation > 0.5 || datum.correlation < -0.5',
                alt.value('white'),
                alt.value('black')
            )
        )
        
        # Combine heatmap and text
        chart = (heatmap + text).configure_axis(
            labelAngle=45,
            labelFontSize=12
        ).configure_title(
            fontSize=16,
            font='Arial',
            anchor='middle'
        )
        
        st.altair_chart(chart, use_container_width=True)
    
    with col2:
        st.write("#### Significance Indicators")
        
        # Create a significance mask
        significant_mask = pvalues < significance_level
        significant_mask.columns = [column_to_metric.get(col, col) for col in significant_mask.columns]
        significant_mask.index = [column_to_metric.get(idx, idx) for idx in significant_mask.index]
        
        # Create a styled dataframe showing only significant correlations
        def highlight_significant(val):
            if val:
                return 'background-color: rgba(76, 175, 80, 0.2)'
            return ''
        
        styled_significance = significant_mask.style.applymap(highlight_significant)
        st.dataframe(styled_significance, height=400)
        
        st.info(f"""
        **How to read the matrix:**
        - Values range from -1 (perfect negative correlation) to +1 (perfect positive correlation)
        - 0 indicates no correlation
        - Highlighted cells in the significance indicator show statistically significant correlations (p < {significance_level})
        """)

with tab3:
    st.header("Scatter Plots")
    
    # Display a reminder of the selected metric with option to change
    st.markdown(f"**Currently analyzing correlations for: __{primary_metric}__**")
    if st.button("⬆️ Change Selected Metric", key="change_metric_tab3"):
        st.session_state.scroll_to_top = True
        st.experimental_rerun()
    
    # Find the top correlations to show scatter plots for
    metrics_to_plot = correlation_results.head(6)['Metric'].tolist()
    
    # Create a grid of scatter plots
    col1, col2 = st.columns(2)
    
    plot_index = 0
    for metric in metrics_to_plot:
        col = col1 if plot_index % 2 == 0 else col2
        plot_index += 1
        
        with col:
            secondary_column = metric_to_column[metric]
            
            # Clean data for plotting (no NaNs)
            plot_data = analysis_data[[primary_column, secondary_column]].dropna()
            
            # Get correlation info
            corr_value = correlation_results[correlation_results['Metric'] == metric]['Correlation'].values[0]
            p_value = correlation_results[correlation_results['Metric'] == metric]['P-Value'].values[0]
            significant = p_value < significance_level
            
            # Determine color based on correlation direction
            color = 'green' if corr_value > 0 else 'red'
            
            # Create a pandas DataFrame for Altair
            plot_df = pd.DataFrame({
                primary_metric: plot_data[primary_column],
                metric: plot_data[secondary_column]
            })
            
            # Create scatter plot with Altair
            scatter = alt.Chart(plot_df).mark_circle(size=60, opacity=0.5).encode(
                x=alt.X(f'{primary_metric}:Q', title=primary_metric),
                y=alt.Y(f'{metric}:Q', title=metric),
                tooltip=[
                    alt.Tooltip(f'{primary_metric}:Q', title=primary_metric),
                    alt.Tooltip(f'{metric}:Q', title=metric)
                ]
            )
            
            # Add regression line
            regression = scatter.transform_regression(
                primary_metric, 
                metric
            ).mark_line(
                color=color, 
                size=3
            )
            
            # Combine scatter and regression
            chart = (scatter + regression).properties(
                title={
                    "text": f"{primary_metric} vs {metric} (r = {corr_value:.2f}, p = {p_value:.4f})",
                    "color": 'green' if significant and corr_value > 0 else 'red' if significant else 'black'
                },
                height=300
            ).configure_title(
                fontSize=16,
                font='Arial',
                anchor='start',
                color='black' if not significant else ('green' if corr_value > 0 else 'red')
            )
            
            # Add "SIGNIFICANT" text for significant correlations
            if significant:
                chart = chart.properties(
                    title={
                        "text": f"{primary_metric} vs {metric} (r = {corr_value:.2f}, p = {p_value:.4f}) - SIGNIFICANT",
                        "color": 'green' if corr_value > 0 else 'red'
                    }
                )
            
            st.altair_chart(chart, use_container_width=True)
            
            # Add description of the relationship
            relationship = correlation_results[correlation_results['Metric'] == metric]['Relationship'].values[0]
            impact = correlation_results[correlation_results['Metric'] == metric]['Impact'].values[0]
            
            st.info(f"""
            **Relationship:** {relationship}
            
            **Business Impact:** {impact}
            """)

with tab4:
    st.header("Detailed Analysis")
    
    # Display a reminder of the selected metric with option to change
    st.markdown(f"**Currently analyzing correlations for: __{primary_metric}__**")
    if st.button("⬆️ Change Selected Metric", key="change_metric_tab4"):
        st.session_state.scroll_to_top = True
        st.experimental_rerun()
    
    # Complete correlation table with all metrics
    st.subheader("Complete Correlation Results")
    
    # Style using pandas styler instead of Plotly table
    styled_corr_df = correlation_results.drop('Abs_Correlation', axis=1).copy()
    
    # Define style functions
    def color_correlation(val):
        try:
            val_float = float(val)
            if val_float < 0:
                return f'color: red; background-color: rgba(255,0,0,{abs(val_float) * 0.2})'
            elif val_float > 0.3:
                return f'color: green; background-color: rgba(0,255,0,{val_float * 0.2})'
            return ''
        except:
            return ''
    
    def highlight_significant(val):
        if val == True:
            return 'background-color: rgba(76, 175, 80, 0.2)'
        return ''
    
    # Apply styling
    styled_table = styled_corr_df.style.format({
        'Correlation': '{:.2f}',
        'P-Value': '{:.4f}'
    })
    styled_table = styled_table.applymap(color_correlation, subset=['Correlation'])
    styled_table = styled_table.applymap(highlight_significant, subset=['Significant'])
    
    # Display the styled table
    st.dataframe(styled_table, height=400, use_container_width=True)
    
    # Statistical significance explanation
    st.subheader("About Statistical Significance")
    st.write(f"""
    Statistical significance (p < {significance_level}) indicates that the observed correlation is unlikely 
    to have occurred by random chance. A smaller p-value provides stronger evidence against the null 
    hypothesis of no correlation.
    
    **Correlation Strength Guide:**
    - 0.0 to 0.3: Weak correlation
    - 0.3 to 0.5: Moderate correlation
    - 0.5 to 0.7: Strong correlation
    - 0.7 to 1.0: Very strong correlation
    """)
    
    # Data sample information
    st.subheader("Data Sample Information")
    st.write(f"""
    - Total cell towers in dataset: {len(merged_data)}
    - Cell towers after filtering: {len(filtered_data)}
    - Sample used for analysis: {len(analysis_data)} (after removing incomplete data)
    """)
    
    if use_region_filter:
        st.write(f"- Geographic filter: Latitude {lat_range}, Longitude {long_range}")
    
    if use_failure_filter:
        st.write(f"- Failure rate threshold: ≥ {failure_threshold}%")
    
    if use_ticket_filter:
        st.write(f"- Ticket count threshold: ≥ {ticket_threshold}")

# Footer with tips
st.markdown("""
---
### 📝 Tips for Interpretation

1. **Correlation ≠ Causation**: A strong correlation doesn't necessarily mean one metric causes changes in another.
2. **Look for Patterns**: Similar correlations across related metrics may indicate underlying factors.
3. **Consider Business Context**: Use your domain knowledge to interpret the results.
4. **Sample Size Matters**: Larger samples typically provide more reliable correlation results.
""")

# Update status at the end
st.success("Analysis complete! Use the tabs to explore correlations from different perspectives.") 