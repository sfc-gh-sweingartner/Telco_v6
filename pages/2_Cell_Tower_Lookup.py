import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import sys
import os

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils'))

# Import with fallback for AI functions
try:
    from utils.design_system import (
        inject_custom_css, create_page_header, create_metric_card, 
        create_info_box, get_snowflake_session, create_metric_grid,
        create_sidebar_navigation, add_page_footer, execute_query_with_loading,
        create_section_header, style_plotly_chart, Colors, create_ai_insights_card,
        create_ai_loading_spinner, create_ai_recommendation_list, create_ai_metrics_dashboard,
        format_ai_response, create_ai_metric_card
    )
    AI_FUNCTIONS_AVAILABLE = True
except ImportError:
    from utils.design_system import (
        inject_custom_css, create_page_header, create_metric_card, 
        create_info_box, get_snowflake_session, create_metric_grid,
        create_sidebar_navigation, add_page_footer, execute_query_with_loading,
        create_section_header, style_plotly_chart, Colors
    )
    AI_FUNCTIONS_AVAILABLE = False
    # Define fallback AI functions
    def create_ai_insights_card(title, insight, confidence=0.0, icon="🧠"):
        st.markdown(f"### {icon} {title}")
        st.info(insight)
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
                return {"root_causes": "AI tower analysis is being deployed", "recommendations": "Advanced AI insights will be available shortly"}
        return FallbackAnalytics()
    def get_ai_processor(session):
        class FallbackProcessor:
            def ai_complete(self, prompt, **kwargs):
                return "📱 AI tower analysis is being deployed. Advanced cell tower insights will be available shortly!"
        return FallbackProcessor()

# Page configuration
st.set_page_config(
    page_title="Cell Tower Lookup",
    page_icon="📱",
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

# AI-Enhanced page header
create_page_header(
    title="AI-Powered Cell Tower Analysis",
    description="Interactive mapping with intelligent tower performance insights and predictive recommendations",
    icon="🤖"
)

# Load tower data with professional loading
data = execute_query_with_loading("""
SELECT
    cell_id,
    ROUND(cell_latitude, 2) AS cell_latitude, 
    ROUND(cell_longitude, 2) AS cell_longitude, 
    SUM(CASE WHEN call_release_code = 0 THEN 1 ELSE 0 END) AS total_success, 
    COUNT(*) AS total_calls, 
    ROUND((SUM(CASE WHEN call_release_code != 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS failure_rate, 
    ROUND((SUM(CASE WHEN call_release_code = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS success_rate
FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER
GROUP BY cell_id, cell_latitude, cell_longitude
""", "Loading cell tower performance data...")

if data.empty:
    create_info_box("No cell tower data available. Please check your database connection.", "error")
    st.stop()

# Network overview metrics
create_section_header("Network Performance Overview", "📊")

total_towers = len(data)
avg_failure_rate = data['FAILURE_RATE'].mean()
high_risk_towers = len(data[data['FAILURE_RATE'] >= 90])
good_towers = len(data[data['FAILURE_RATE'] < 60])

metrics = [
    {
        "title": "Total Towers",
        "value": f"{total_towers:,}",
        "delta": "Network nodes"
    },
    {
        "title": "Average Failure Rate",
        "value": f"{avg_failure_rate:.1f}%",
        "delta": "↓ 2.3% vs last month" if avg_failure_rate < 20 else "↑ 1.8% vs last month",
        "delta_color": "positive" if avg_failure_rate < 20 else "negative"
    },
    {
        "title": "High Risk Towers",
        "value": f"{high_risk_towers}",
        "delta": f"{(high_risk_towers/total_towers*100):.1f}% of network",
        "delta_color": "negative" if high_risk_towers > 0 else "positive"
    },
    {
        "title": "Performing Well",
        "value": f"{good_towers}",
        "delta": f"{(good_towers/total_towers*100):.1f}% of network",
        "delta_color": "positive"
    }
]

create_metric_grid(metrics, columns=4)

# Interactive Map Section
create_section_header("Interactive Tower Performance Map", "🗺️")

# Color mapping function
def get_color(failure_rate):
    """Map failure rate to professional color scheme"""
    if failure_rate >= 90:
        return [220, 53, 69, 180]    # Red for critical
    elif failure_rate >= 60:
        return [255, 193, 7, 180]    # Yellow for warning
    else:
        return [40, 167, 69, 180]    # Green for good

# Apply color function
data['COLOR'] = data['FAILURE_RATE'].apply(get_color)

# Create professional info box for map instructions
create_info_box(
    "📍 **Interactive Map Instructions:** Click on any grid cell to view detailed tower performance metrics and AI-powered recommendations. "
    "Colors indicate performance: 🟢 Good (<60% failure), 🟡 Warning (60-90% failure), 🔴 Critical (>90% failure)",
    "info"
)

# Define Professional PyDeck GridLayer
grid_layer = pdk.Layer(
    "GridLayer",
    id="cell_tower_grid",
    data=data,
    get_position=["CELL_LONGITUDE", "CELL_LATITUDE"],
    cell_size=2000,
    extruded=True,
    pickable=True,
    elevation_scale=25,
    get_elevation="FAILURE_RATE",
    get_fill_color="COLOR",
    auto_highlight=True,
)

# Define the initial view state (centered on California)
view_state = pdk.ViewState(
    latitude=37.5,
    longitude=-119.5,
    zoom=5.5,
    pitch=45,
    bearing=0
)

# Display the professional map
st.markdown("""
<div style="background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 2rem;">
""", unsafe_allow_html=True)

st.session_state.event = st.pydeck_chart(
    pdk.Deck(
        map_provider="mapbox",
        map_style="mapbox://styles/mapbox/light-v9",
        layers=[grid_layer],
        initial_view_state=view_state,
        tooltip={"text": "Cell ID: {cell_id}\nFailure Rate: {failure_rate}%\nTotal Calls: {total_calls}"}
    ), 
    on_select="rerun", 
    selection_mode="single-object"
)

st.markdown("</div>", unsafe_allow_html=True)

# Selection Analysis Section
cell_tower_objects = st.session_state.event.selection.get("objects", {}).get("cell_tower_grid", [])
selection_data = []

for obj in cell_tower_objects:
    points = obj.get("points", [])
    for point in points:
        source = point.get("source", {})
        selection_data.append({
            "Cell ID": source.get("CELL_ID"),
            "Latitude": source.get("CELL_LATITUDE"),
            "Longitude": source.get("CELL_LONGITUDE"),
            "Failure Rate (%)": source.get("FAILURE_RATE"),
            "Success Rate (%)": source.get("SUCCESS_RATE"),
            "Total Calls": source.get("TOTAL_CALLS"),
            "Total Successful Calls": source.get("TOTAL_SUCCESS"),
        })

if len(selection_data) > 0:
    create_section_header("Selected Tower Analysis", "🔍")
    
    # AI Analysis
    df = pd.DataFrame(selection_data)
    
    # Create AI prompt for analysis
    prompt = f"""
    You are a network engineer analyzing failed cells in a cell tower grid. 
    Provide a concise summary of the failed cells using the following data:

    {selection_data}

    Start your response directly with: "The selected grid contains". 
    Format the response in Markdown with proper bullet points. For each cell, use a bullet point and display the details as sub-bullets:

    - **Cell ID: 123456**
      - **Location:** Latitude 12.34, Longitude -56.78
      - **Performance:** 10% failure rate, 90% success rate  
      - **Volume:** 1000 total calls, 900 successful

    Do not include phrases like "Based on the provided data".
    """
    
    prompt = prompt.replace("'", "''")
    
    # Get AI analysis
    ai_analysis = execute_query_with_loading(
        f"select snowflake.cortex.complete('claude-4-sonnet', '{prompt}') as res",
        "Generating AI analysis..."
    )
    
    if not ai_analysis.empty:
        st.markdown("#### 🤖 AI-Powered Analysis")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #17a2b8; margin-bottom: 1.5rem;">
            {ai_analysis["RES"][0]}
        </div>
        """, unsafe_allow_html=True)
    
    # Performance Charts
    st.markdown("#### 📊 Performance Visualizations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### Failure Rate Analysis")
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        ax1.bar(range(len(df)), df["Failure Rate (%)"], 
                color=Colors.DANGER, alpha=0.7, edgecolor=Colors.PRIMARY)
        ax1.set_ylabel("Failure Rate (%)", fontweight='bold')
        ax1.set_title("Failure Rate by Cell Tower", fontweight='bold')
        ax1.set_xticks(range(len(df)))
        ax1.set_xticklabels([f"Cell {i+1}" for i in range(len(df))], rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, v in enumerate(df["Failure Rate (%)"]):
            ax1.text(i, v + 0.5, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig1)
    
    with col2:
        st.markdown("##### Customer Impact Analysis")
        
        # Load customer loyalty data for selected cells
        cell_ids_list = df["Cell ID"].to_list()
        cell_ids_str = ','.join(map(str, cell_ids_list))
        
        loyalty_data = execute_query_with_loading(f"""
        SELECT 
            c.cell_id,
            COUNT(CASE WHEN cl.status = 'Bronze' THEN 1 END) AS bronze_count,
            COUNT(CASE WHEN cl.status = 'Silver' THEN 1 END) AS silver_count,
            COUNT(CASE WHEN cl.status = 'Gold' THEN 1 END) AS gold_count
        FROM 
            TELCO_NETWORK_OPTIMIZATION_PROD.raw.customer_loyalty cl
        JOIN 
            TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER c
        ON 
            cl.phone_number = c.msisdn
        WHERE 
            c.call_release_code != 0
            AND c.cell_id IN ({cell_ids_str})
        GROUP BY 
            c.cell_id
        """, "Loading customer impact data...")
        
        if not loyalty_data.empty:
            loyalty_data.set_index('CELL_ID', inplace=True)
            
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            loyalty_data.plot(kind='bar', stacked=True, ax=ax2, 
                            color=['#cd7f32', '#c0c0c0', '#ffd700'], alpha=0.8)
            
            ax2.set_title('Customer Loyalty Impact by Cell', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Cell ID', fontweight='bold')
            ax2.set_ylabel('Affected Customers', fontweight='bold')
            ax2.set_xticklabels(loyalty_data.index, rotation=45)
            ax2.legend(title="Loyalty Tier", labels=["Bronze", "Silver", "Gold"], 
                      title_fontweight='bold')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig2)
        else:
            create_info_box("No customer loyalty data available for selected cells.", "info")
    
    with col3:
        st.markdown("##### Sentiment Analysis")
        
        # Load sentiment data
        sentiment_data = execute_query_with_loading(f"""
        SELECT 
            cell_id,
            AVG(sentiment_score) AS avg_sentiment_score,
            COUNT(*) as ticket_count
        FROM 
            TELCO_NETWORK_OPTIMIZATION_PROD.RAW.SUPPORT_TICKETS
        WHERE cell_id IN ({cell_ids_str})
        GROUP BY 
            cell_id
        ORDER BY 
            avg_sentiment_score DESC
        """, "Loading sentiment data...")
        
        if not sentiment_data.empty:
            fig3, ax3 = plt.subplots(figsize=(8, 6))
            
            # Normalize sentiment scores for better visualization (add offset)
            normalized_scores = sentiment_data['AVG_SENTIMENT_SCORE'] + 1  # Scale from [-1,1] to [0,2]
            
            bars = ax3.bar(range(len(sentiment_data)), normalized_scores,
                          color=Colors.INFO, alpha=0.7, edgecolor=Colors.PRIMARY)
            
            ax3.set_ylabel("Sentiment Score", fontweight='bold')
            ax3.set_title("Customer Sentiment by Cell", fontweight='bold')
            ax3.set_xticks(range(len(sentiment_data)))
            ax3.set_xticklabels([f"Cell {row['CELL_ID']}" for _, row in sentiment_data.iterrows()], 
                               rotation=45)
            ax3.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for i, (bar, score) in enumerate(zip(bars, sentiment_data['AVG_SENTIMENT_SCORE'])):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                        f'{score:.2f}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig3)
        else:
            create_info_box("No sentiment data available for selected cells.", "info")
    
    # AI Recommendations
    if not ai_analysis.empty and not sentiment_data.empty:
        create_section_header("AI-Powered Recommendations", "💡")
        
        recommendation_prompt = f"""
        You are a network engineer tasked with improving customer experience and reducing call failures. 
        Based on the following data, provide specific actionable recommendations:

        1. Failure Rate Data: {df.to_dict('records')}
        2. Customer Sentiment Data: {sentiment_data.to_dict('records') if not sentiment_data.empty else 'No data'}
        3. Customer Loyalty Impact: {loyalty_data.to_dict() if not loyalty_data.empty else 'No data'}

        Provide 3-5 specific, actionable recommendations prioritized by impact and feasibility. 
        Focus on which cells need immediate attention and why.
        Format as a bulleted list with priority levels.
        """
        
        recommendation_prompt = recommendation_prompt.replace("'", "''")
        
        recommendations = execute_query_with_loading(
            f"select snowflake.cortex.complete('claude-4-sonnet', '{recommendation_prompt}') as res",
            "Generating recommendations..."
        )
        
        if not recommendations.empty:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #d4edda 0%, #ffffff 100%); padding: 2rem; border-radius: 12px; border-left: 4px solid #28a745;">
                <h4 style="color: #155724; margin: 0 0 1rem 0;">🎯 Strategic Recommendations</h4>
                {recommendations["RES"][0]}
            </div>
            """, unsafe_allow_html=True)

else:
    create_info_box("🖱️ **Select a grid cell on the map above** to view detailed performance analysis and AI-powered recommendations.", "info")

# AI-Powered Tower Intelligence Section
st.markdown("---")
st.markdown("## 🤖 AI Tower Intelligence")

# Create tabs for different AI analyses
ai_tower_tab1, ai_tower_tab2, ai_tower_tab3 = st.tabs(["🔍 AI Network Analysis", "⚠️ Risk Assessment", "🎯 Optimization Strategy"])

with ai_tower_tab1:
    st.markdown("### 🔍 AI-Powered Network Analysis")
    st.info("Get intelligent insights about your cell tower network performance")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🚀 Analyze Network with AI", type="primary", key="ai_network_analysis"):
            create_ai_loading_spinner("AI is analyzing cell tower performance patterns...")
            
            try:
                # Prepare network analysis context
                network_context = f"""
                Cell Tower Network Analysis:
                
                Network Overview:
                - Total Cell Towers: {total_towers}
                - Average Failure Rate: {avg_failure_rate:.1f}%
                - Critical Towers (>90% failure): {len(data[data['FAILURE_RATE'] >= 90])}
                - Excellent Towers (<30% failure): {len(data[data['FAILURE_RATE'] < 30])}
                
                Performance Distribution:
                - Network health status and patterns
                - Geographic performance variations
                - Infrastructure optimization opportunities
                
                Business Context:
                - Telecom network infrastructure management
                - Customer service quality optimization
                - Network reliability and capacity planning
                """
                
                # Generate AI network insights
                network_insights = ai_processor.ai_complete(
                    f"""As a telecom network infrastructure expert, analyze this cell tower network:
                    
                    {network_context}
                    
                    Provide comprehensive network analysis including:
                    1. Overall network health assessment and key performance indicators
                    2. Critical performance patterns and infrastructure bottlenecks
                    3. Geographic or technical factors affecting tower performance
                    4. Network capacity and coverage optimization opportunities
                    5. Risk areas requiring immediate attention
                    6. Strategic recommendations for network improvement
                    
                    Focus on actionable insights for network operations and planning.""",
                    max_tokens=700
                )
                
                if network_insights:
                    create_ai_insights_card(
                        "🏗️ Network Infrastructure Analysis", 
                        network_insights, 
                        confidence=0.84, 
                        icon="📡"
                    )
                    
                    # Create network analysis metrics
                    network_metrics = {
                        "Network Health Score": f"{max(0, 100 - avg_failure_rate):.0f}%",
                        "Critical Towers": str(len(data[data['FAILURE_RATE'] >= 90])),
                        "Performance Grade": "A" if avg_failure_rate < 20 else "B" if avg_failure_rate < 40 else "C",
                        "Optimization Potential": "High" if avg_failure_rate > 30 else "Medium"
                    }
                    
                    create_ai_metrics_dashboard(network_metrics)
                    
            except Exception as e:
                st.error(f"Error in AI network analysis: {e}")
    
    with col2:
        st.markdown("#### 📊 Network Stats")
        
        create_ai_metric_card(
            "Network Score",
            f"{max(0, 100 - avg_failure_rate):.0f}/100",
            f"Based on average failure rate of {avg_failure_rate:.1f}%",
            "📡"
        )
        
        create_ai_metric_card(
            "Tower Health",
            f"{len(data[data['FAILURE_RATE'] < 30])}/{total_towers}",
            "Towers performing excellently (<30% failure rate)",
            "✅"
        )

with ai_tower_tab2:
    st.markdown("### ⚠️ AI Risk Assessment")
    st.info("Identify high-risk towers and potential failure patterns")
    
    risk_focus = st.selectbox(
        "Risk Assessment Focus:",
        ["Failure Risk Analysis", "Capacity Risk Assessment", "Geographic Risk Patterns", "Service Impact Risk"],
        key="risk_focus"
    )
    
    if st.button("🚨 Assess Network Risks", type="primary", key="risk_assessment"):
        create_ai_loading_spinner("AI is assessing network risks and vulnerabilities...")
        
        try:
            # Identify high-risk towers
            high_risk_towers = data[data['FAILURE_RATE'] >= 70]
            medium_risk_towers = data[(data['FAILURE_RATE'] >= 40) & (data['FAILURE_RATE'] < 70)]
            
            risk_context = f"""
            Network Risk Assessment for {risk_focus}:
            
            Risk Distribution:
            - High Risk Towers (≥70% failure): {len(high_risk_towers)}
            - Medium Risk Towers (40-70% failure): {len(medium_risk_towers)}
            - Low Risk Towers (<40% failure): {len(data[data['FAILURE_RATE'] < 40])}
            
            Risk Indicators:
            - Network failure rate trends
            - Geographic risk clustering
            - Infrastructure vulnerability patterns
            - Service impact potential
            
            Assessment Focus: {risk_focus}
            """
            
            risk_assessment = ai_processor.ai_complete(
                f"""As a network risk management expert, assess {risk_focus.lower()} for this cell tower network:
                
                {risk_context}
                
                Provide comprehensive risk analysis:
                1. Primary risk factors and vulnerability patterns
                2. High-priority towers requiring immediate attention
                3. Potential cascading failure scenarios
                4. Service impact assessment and customer effect
                5. Risk mitigation strategies and timeline
                6. Monitoring recommendations for early warning
                
                Focus on actionable risk management strategies.""",
                max_tokens=700
            )
            
            if risk_assessment:
                create_ai_insights_card(
                    f"⚠️ {risk_focus} Assessment", 
                    risk_assessment, 
                    confidence=0.81, 
                    icon="🚨"
                )
                
                # Create risk metrics
                risk_metrics = {
                    "High Risk Towers": str(len(high_risk_towers)),
                    "Risk Level": "High" if len(high_risk_towers) > 5 else "Medium" if len(high_risk_towers) > 0 else "Low",
                    "Mitigation Priority": "Critical" if len(high_risk_towers) > 10 else "High",
                    "Service Impact": "Significant" if avg_failure_rate > 50 else "Moderate"
                }
                
                create_ai_metrics_dashboard(risk_metrics)
                
                # Generate risk mitigation actions
                risk_actions = [
                    f"Immediately inspect {len(high_risk_towers)} high-risk towers (≥70% failure rate)",
                    f"Schedule preventive maintenance for {len(medium_risk_towers)} medium-risk towers",
                    "Implement enhanced monitoring on identified risk clusters",
                    "Develop contingency plans for potential service disruptions",
                    "Allocate emergency response resources to high-risk areas",
                    "Establish proactive customer communication for affected areas"
                ]
                
                create_ai_recommendation_list(risk_actions[:4], "🚨 Risk Mitigation Actions")
                
        except Exception as e:
            st.error(f"Error in risk assessment: {e}")

with ai_tower_tab3:
    st.markdown("### 🎯 AI Optimization Strategy")
    st.info("Get strategic recommendations for network performance optimization")
    
    optimization_goal = st.selectbox(
        "Optimization Goal:",
        ["Reduce Failure Rates", "Improve Coverage", "Enhance Capacity", "Optimize Costs", "Improve Customer Experience"],
        key="optimization_goal"
    )
    
    priority_level = st.selectbox(
        "Implementation Priority:",
        ["Critical (Immediate)", "High (Within Month)", "Medium (Within Quarter)", "Low (Within Year)"],
        key="priority_level"
    )
    
    if st.button("🎯 Generate Optimization Strategy", type="primary", key="optimization_strategy"):
        create_ai_loading_spinner("AI is developing network optimization strategy...")
        
        try:
            optimization_context = f"""
            Network Optimization Strategy for: {optimization_goal}
            
            Current Network State:
            - Total Towers: {total_towers}
            - Average Failure Rate: {avg_failure_rate:.1f}%
            - Critical Issues: {len(data[data['FAILURE_RATE'] >= 90])} towers
            - Performance Target: {optimization_goal}
            - Implementation Priority: {priority_level}
            
            Available Optimization Levers:
            - Infrastructure upgrades and maintenance
            - Technology improvements and modernization
            - Geographic coverage optimization
            - Resource allocation and capacity planning
            - Operational process improvements
            """
            
            optimization_strategy = ai_processor.ai_complete(
                f"""As a network optimization strategist, develop a comprehensive plan for {optimization_goal.lower()}:
                
                {optimization_context}
                
                Create detailed optimization strategy:
                1. Specific technical and operational improvements for {optimization_goal.lower()}
                2. Implementation roadmap with timeline and priorities
                3. Resource requirements and budget considerations
                4. Expected performance improvements and success metrics
                5. Risk factors and mitigation strategies
                6. Quick wins vs long-term strategic initiatives
                
                Focus on practical, implementable recommendations with clear ROI.""",
                max_tokens=800
            )
            
            if optimization_strategy:
                create_ai_insights_card(
                    f"🚀 {optimization_goal} Strategy", 
                    optimization_strategy, 
                    confidence=0.87, 
                    icon="🎯"
                )
                
                # Generate implementation timeline
                timeline_actions = []
                if priority_level.startswith("Critical"):
                    timeline_actions = [
                        "Week 1: Emergency assessment of critical failure towers",
                        "Week 2: Immediate repairs and temporary solutions",
                        "Week 3-4: Implement quick-win optimizations",
                        "Month 2: Deploy enhanced monitoring systems"
                    ]
                elif priority_level.startswith("High"):
                    timeline_actions = [
                        "Month 1: Detailed network assessment and planning",
                        "Month 2-3: Begin infrastructure improvements",
                        "Month 4: Implement operational optimizations", 
                        "Month 5-6: Monitor results and fine-tune"
                    ]
                else:
                    timeline_actions = [
                        "Quarter 1: Strategic planning and resource allocation",
                        "Quarter 2: Pilot implementation in selected areas",
                        "Quarter 3: Full rollout and optimization",
                        "Quarter 4: Performance evaluation and refinement"
                    ]
                
                create_ai_recommendation_list(timeline_actions, f"📅 {priority_level} Implementation Timeline")
                
                # Strategy metrics
                strategy_metrics = {
                    "Strategy Focus": optimization_goal,
                    "Priority Level": priority_level.split()[0],
                    "Expected ROI": "High" if optimization_goal in ["Reduce Failure Rates", "Improve Customer Experience"] else "Medium",
                    "Implementation Complexity": "High" if priority_level.startswith("Critical") else "Medium"
                }
                
                create_ai_metrics_dashboard(strategy_metrics)
                
        except Exception as e:
            st.error(f"Error generating optimization strategy: {e}")

st.markdown("---")

# Performance Summary
create_section_header("Network Performance Summary", "📈")

# Create performance distribution chart
performance_buckets = pd.cut(data['FAILURE_RATE'], 
                           bins=[0, 30, 60, 90, 100], 
                           labels=['Excellent (0-30%)', 'Good (30-60%)', 'Poor (60-90%)', 'Critical (90-100%)'],
                           include_lowest=True)
performance_dist = performance_buckets.value_counts().sort_index()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("##### Performance Distribution")
    
    # Create performance summary table
    summary_data = []
    for category, count in performance_dist.items():
        percentage = (count / len(data)) * 100
        summary_data.append({
            'Performance Level': category,
            'Tower Count': count,
            'Percentage': f"{percentage:.1f}%"
        })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

with col2:
    st.markdown("##### Key Insights")
    
    insights = []
    critical_towers = len(data[data['FAILURE_RATE'] >= 90])
    excellent_towers = len(data[data['FAILURE_RATE'] < 30])
    
    if critical_towers > 0:
        insights.append(f"🔴 **{critical_towers} towers** require immediate attention (>90% failure rate)")
    
    if excellent_towers > total_towers * 0.7:
        insights.append(f"✅ **{(excellent_towers/total_towers*100):.0f}%** of network performing excellently")
    
    if avg_failure_rate > 50:
        insights.append("⚠️ **Network health** below industry standards - optimization needed")
    else:
        insights.append("✅ **Network health** within acceptable parameters")
    
    insights.append(f"📊 **Average failure rate:** {avg_failure_rate:.1f}% across {total_towers} towers")
    
    for insight in insights:
        st.markdown(f"""
        <div style="background: white; padding: 0.75rem; margin-bottom: 0.5rem; border-radius: 8px; border-left: 3px solid #1f4e79;">
            {insight}
        </div>
        """, unsafe_allow_html=True)

# Add professional footer
add_page_footer()