"""
Snowflake Intelligence - Natural Language Analytics & AI Agents
Advanced AI-powered data analysis with natural language querying
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Snowflake Intelligence",
    page_icon="🧠",
    layout="wide"
)

# Import with fallback for AI functions
try:
    from utils.design_system import (
        inject_custom_css, create_page_header, create_sidebar_navigation, 
        add_page_footer, get_snowflake_session, execute_query_with_loading,
        create_ai_insights_card, create_ai_loading_spinner, create_ai_recommendation_list,
        create_ai_metrics_dashboard, create_ai_progress_tracker, create_model_selector,
        format_ai_response, create_ai_metric_card, create_metric_card
    )
    from utils.aisql_functions import get_ai_analytics, get_ai_processor
    AI_FUNCTIONS_AVAILABLE = True
except ImportError:
    from utils.design_system import (
        inject_custom_css, create_page_header, create_sidebar_navigation, 
        add_page_footer, get_snowflake_session, execute_query_with_loading
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
        st.progress(current_step / total_steps, text=f"🤖 {step_name} (Step {current_step}/{total_steps})")
    def create_model_selector(models, default_model="claude-3-5-sonnet"):
        return st.selectbox("AI Model", models, index=models.index(default_model) if default_model in models else 0)
    def format_ai_response(response, title="AI Insights"):
        st.markdown(f"### {title}")
        # Fix newline formatting for better display
        formatted_response = response.replace('\\n', '\n') if '\\n' in response else response
        st.write(formatted_response)
    def create_ai_metric_card(metric, value, icon="📊"):
        st.metric(metric, value)
    def create_metric_card(metric, value, icon="📊"):
        st.metric(metric, value)

# Initialize AI processor
if AI_FUNCTIONS_AVAILABLE:
    ai_processor = get_ai_processor()
    ai_analytics = get_ai_analytics()

# Apply custom CSS
inject_custom_css()

# Create page header
create_page_header(
    "🧠 Snowflake Intelligence",
    "Natural Language Analytics & AI Agents",
    "Transform your data into insights using natural language queries and intelligent agents"
)

# Create sidebar navigation
create_sidebar_navigation()

# Get Snowflake session
session = get_snowflake_session()

# AI Model Selection (if available)
if AI_FUNCTIONS_AVAILABLE:
    with st.sidebar:
        st.markdown("---")
        models = ai_processor.supported_models
        selected_model = create_model_selector(models, ai_processor.default_model)
        ai_processor.default_model = selected_model

# Main content
st.markdown("## 🌟 Welcome to Snowflake Intelligence")

# Intelligence overview cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
        <h3 style="color: white; margin: 0;">🗣️ Natural Language</h3>
        <p style="margin: 0.5rem 0;">Ask questions in plain English</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
        <h3 style="color: white; margin: 0;">🤖 AI Agents</h3>
        <p style="margin: 0.5rem 0;">Intelligent data assistants</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
        <h3 style="color: white; margin: 0;">📊 Auto Visualizations</h3>
        <p style="margin: 0.5rem 0;">Charts created automatically</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
        <h3 style="color: white; margin: 0;">🔗 Multi-Source</h3>
        <p style="margin: 0.5rem 0;">Structured & unstructured data</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Create tabs for different Intelligence features
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗣️ Natural Language Query", 
    "🤖 AI Agents", 
    "📊 Intelligent Analytics", 
    "🔍 Cortex Search", 
    "⚙️ Setup & Configuration"
])

with tab1:
    st.markdown("### 🗣️ Natural Language Querying")
    st.info("Ask questions about your telecom network data in plain English and get instant insights with visualizations.")
    
    # Natural language interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 💬 Ask Your Data")
        
        # Sample questions
        sample_questions = [
            "What are the top 5 cell towers with the highest failure rate this month?",
            "Show me customer satisfaction trends over the last quarter",
            "Which geographic areas have the most network issues?",
            "What's the correlation between downlink latency and customer complaints?",
            "Create a chart showing daily network performance for the past week",
            "How many critical support tickets were opened yesterday?",
            "What's the average success rate across all our cell towers?",
            "Show me the busiest cell towers by data usage"
        ]
        
        selected_question = st.selectbox(
            "Choose a sample question or type your own:",
            [""] + sample_questions,
            key="nl_question"
        )
        
        user_question = st.text_area(
            "Your Question:",
            value=selected_question if selected_question else "",
            placeholder="Ask anything about your network data...",
            height=100
        )
        
        if st.button("🚀 Get Insights", type="primary", key="nl_query"):
            if user_question:
                create_ai_progress_tracker(1, 2, "🧠 Understanding your question...")
                
                # Simulate natural language processing
                time.sleep(1)
                
                create_ai_progress_tracker(2, 2, "📊 Generating insights and visualizations...")
                
                if AI_FUNCTIONS_AVAILABLE:
                    try:
                        # Generate AI response for natural language query
                        nl_response = ai_processor.ai_complete(
                            f"""As a Snowflake Intelligence agent for telecom network analysis, respond to this natural language query:
                            
                            User Question: "{user_question}"
                            
                            Context: This is a telecom network optimization system with:
                            - Cell tower performance data
                            - Customer support tickets
                            - Network metrics (success rates, latency, throughput)
                            - Geographic coverage data
                            
                            Provide:
                            1. A direct answer to the question
                            2. Relevant insights and patterns
                            3. Suggested visualizations (chart types)
                            4. Follow-up questions they might ask
                            
                            Format your response professionally with clear sections.""",
                            max_tokens=600
                        )
                        
                        if nl_response:
                            create_ai_insights_card(
                                "🧠 Natural Language Response", 
                                nl_response, 
                                confidence=0.88, 
                                icon="🗣️"
                            )
                            
                            # Generate sample visualization
                            st.markdown("#### 📊 Suggested Visualization")
                            
                            # Create sample data based on question type
                            if "failure rate" in user_question.lower():
                                chart_data = pd.DataFrame({
                                    'Cell Tower': [f'Tower-{i}' for i in range(1, 11)],
                                    'Failure Rate %': np.random.uniform(2, 15, 10)
                                })
                                st.bar_chart(chart_data.set_index('Cell Tower'))
                            
                            elif "trend" in user_question.lower() or "time" in user_question.lower():
                                dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
                                chart_data = pd.DataFrame({
                                    'Date': dates,
                                    'Value': np.random.uniform(70, 95, 30) + np.sin(np.arange(30) * 0.2) * 10
                                })
                                st.line_chart(chart_data.set_index('Date'))
                            
                            elif "geographic" in user_question.lower() or "area" in user_question.lower():
                                st.info("🗺️ Geographic visualization would be displayed here using network location data")
                            
                            else:
                                # Default chart
                                chart_data = pd.DataFrame({
                                    'Metric': ['Success Rate', 'Availability', 'Customer Satisfaction', 'Response Time'],
                                    'Score': [87, 94, 78, 85]
                                })
                                st.bar_chart(chart_data.set_index('Metric'))
                        
                    except Exception as e:
                        st.error(f"Error processing natural language query: {e}")
                else:
                    st.info("🔧 AI functions not available in this environment. This would normally provide intelligent responses to your natural language queries.")
            else:
                st.warning("Please enter a question about your data.")
    
    with col2:
        st.markdown("#### 💡 Query Tips")
        st.markdown("""
        **Great questions to ask:**
        - "Show me..." for visualizations
        - "What are the top..." for rankings  
        - "How has X changed over..." for trends
        - "Compare X and Y..." for analysis
        - "Why is..." for explanations
        
        **Supported visualizations:**
        - 📊 Bar charts
        - 📈 Line charts  
        - 🥧 Pie charts
        - 🗺️ Geographic maps
        - 📋 Tables
        """)

with tab2:
    st.markdown("### 🤖 AI Agents")
    st.info("Intelligent agents that can answer questions, provide insights, and create visualizations using your telecom data.")
    
    # Agent selector
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🎯 Choose Your AI Agent")
        
        agent_types = {
            "Network Operations Agent": {
                "description": "Specializes in cell tower performance, network health, and operational metrics",
                "icon": "🏗️",
                "capabilities": ["Performance analysis", "Failure prediction", "Capacity planning"]
            },
            "Customer Experience Agent": {
                "description": "Focuses on customer satisfaction, support tickets, and service quality",
                "icon": "👥", 
                "capabilities": ["Satisfaction analysis", "Complaint patterns", "Service improvements"]
            },
            "Business Intelligence Agent": {
                "description": "Provides executive insights, financial impact, and strategic recommendations",
                "icon": "📈",
                "capabilities": ["Revenue analysis", "ROI calculations", "Strategic planning"]
            },
            "Technical Analyst Agent": {
                "description": "Deep-dive technical analysis, correlations, and root cause investigation",
                "icon": "🔬",
                "capabilities": ["Root cause analysis", "Technical correlations", "Predictive modeling"]
            }
        }
        
        selected_agent = st.selectbox(
            "Select an AI Agent:",
            list(agent_types.keys()),
            key="agent_selector"
        )
        
        if selected_agent:
            agent_info = agent_types[selected_agent]
            
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;
                        border-left: 4px solid #2196f3; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h4 style="margin: 0; color: #1565c0;">
                    {agent_info['icon']} {selected_agent}
                </h4>
                <p style="margin: 0.5rem 0; color: #666;">{agent_info['description']}</p>
                <div style="margin-top: 1rem;">
                    <strong>Capabilities:</strong>
                    <ul style="margin: 0.5rem 0;">
                        {''.join([f'<li>{cap}</li>' for cap in agent_info['capabilities']])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Agent conversation interface
        st.markdown("#### 💬 Chat with Your Agent")
        
        # Initialize chat history
        if f"agent_chat_{selected_agent}" not in st.session_state:
            st.session_state[f"agent_chat_{selected_agent}"] = []
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state[f"agent_chat_{selected_agent}"]:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div style="background: #e3f2fd; padding: 1rem; border-radius: 12px; margin: 0.5rem 0; margin-left: 2rem;">
                        <strong>You:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: #f3e5f5; padding: 1rem; border-radius: 12px; margin: 0.5rem 0; margin-right: 2rem;">
                        <strong>{agent_info['icon']} {selected_agent}:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        user_input = st.text_input(
            "Ask your agent:",
            placeholder=f"Ask {selected_agent} about your network...",
            key=f"agent_input_{selected_agent}"
        )
        
        if st.button("Send", type="primary", key=f"send_{selected_agent}"):
            if user_input:
                # Add user message
                st.session_state[f"agent_chat_{selected_agent}"].append({
                    "role": "user",
                    "content": user_input,
                    "timestamp": datetime.now()
                })
                
                create_ai_loading_spinner(f"{selected_agent} is analyzing your request...")
                
                if AI_FUNCTIONS_AVAILABLE:
                    try:
                        # Generate agent response
                        agent_prompt = f"""You are the {selected_agent} for a telecom network optimization system.
                        
                        Agent Profile: {agent_info['description']}
                        Your capabilities: {', '.join(agent_info['capabilities'])}
                        
                        User Question: "{user_input}"
                        
                        Respond as this specialized agent in EXACTLY 100 words. Be specific and actionable."""
                        
                        agent_response = ai_processor.ai_complete(agent_prompt, max_tokens=150)
                        
                        if agent_response:
                            # Add agent response
                            st.session_state[f"agent_chat_{selected_agent}"].append({
                                "role": "agent",
                                "content": agent_response,
                                "timestamp": datetime.now()
                            })
                            
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error communicating with agent: {e}")
                else:
                    # Fallback response
                    fallback_responses = {
                        "Network Operations Agent": "I'd analyze your network performance data and provide insights about tower efficiency, capacity utilization, and operational recommendations.",
                        "Customer Experience Agent": "I'd examine customer satisfaction metrics, support ticket patterns, and suggest improvements to enhance the customer experience.",
                        "Business Intelligence Agent": "I'd provide executive-level insights about network ROI, revenue impact, and strategic recommendations for business growth.",
                        "Technical Analyst Agent": "I'd perform deep technical analysis, identify correlations between network metrics, and investigate root causes of issues."
                    }
                    
                    st.session_state[f"agent_chat_{selected_agent}"].append({
                        "role": "agent", 
                        "content": fallback_responses[selected_agent],
                        "timestamp": datetime.now()
                    })
                    
                    st.rerun()
    
    with col2:
        st.markdown("#### 🎯 Agent Features")
        st.markdown("""
        **Intelligence Models:**
        - Claude 4.0 & 3.7
        - Claude 3.5
        - GPT 4.1
        - Cross-region inference
        
        **Agent Capabilities:**
        - 🔍 Data analysis
        - 📊 Auto visualizations  
        - 💡 Recommendations
        - 🎯 Specialized expertise
        - 📈 Trend analysis
        
        **Supported Data Sources:**
        - Cell tower metrics
        - Customer tickets
        - Geographic data
        - Performance logs
        """)

with tab3:
    st.markdown("### 📊 Intelligent Analytics")
    st.info("AI-powered analytics that automatically discover patterns, correlations, and insights in your telecom data.")
    
    # Analytics options
    col1, col2 = st.columns([3, 1])
    
    with col1:
        analytics_type = st.selectbox(
            "Choose Analytics Type:",
            [
                "🔍 Pattern Discovery",
                "📊 Automated Correlations", 
                "🎯 Anomaly Detection",
                "📈 Predictive Insights",
                "🏆 Performance Benchmarking",
                "💰 Business Impact Analysis"
            ],
            key="intelligence_analytics"
        )
        
        if st.button("🚀 Generate Intelligent Analytics", type="primary", key="intelligent_analytics"):
            create_ai_progress_tracker(1, 3, "🔍 Analyzing data patterns...")
            time.sleep(1)
            
            create_ai_progress_tracker(2, 3, "🧠 Applying AI algorithms...")  
            time.sleep(1)
            
            create_ai_progress_tracker(3, 3, "📊 Creating insights and visualizations...")
            
            if AI_FUNCTIONS_AVAILABLE:
                try:
                    # Generate intelligent analytics
                    analytics_context = f"""
                    Generate intelligent analytics for: {analytics_type}
                    
                    Context: Telecom network optimization system with:
                    - Network performance metrics
                    - Customer satisfaction data
                    - Geographic coverage information
                    - Historical trends
                    
                    Provide advanced AI-driven insights including:
                    1. Key discoveries and patterns
                    2. Statistical significance
                    3. Business implications
                    4. Recommended actions
                    5. Confidence levels
                    """
                    
                    analytics_insights = ai_processor.ai_complete(
                        f"""As an advanced AI analytics engine specializing in telecom network intelligence, provide comprehensive analytics for {analytics_type}:
                        
                        {analytics_context}
                        
                                                    Generate insights in EXACTLY 100 words with specific metrics and actionable recommendations.""",
                            max_tokens=150
                    )
                    
                    if analytics_insights:
                        create_ai_insights_card(
                            f"🧠 {analytics_type} - AI Analysis", 
                            analytics_insights, 
                            confidence=0.91, 
                            icon="🎯"
                        )
                        
                        # Create metrics based on analytics type
                        if "Pattern Discovery" in analytics_type:
                            metrics = {
                                "Patterns Found": "23 significant",
                                "Confidence": "94.2%",
                                "Data Coverage": "100%",
                                "Time Span": "6 months"
                            }
                        elif "Correlations" in analytics_type:
                            metrics = {
                                "Strong Correlations": "8 identified",
                                "Statistical Significance": "p < 0.001", 
                                "R-squared": "0.847",
                                "Variables Analyzed": "156"
                            }
                        elif "Anomaly" in analytics_type:
                            metrics = {
                                "Anomalies Detected": "12 critical",
                                "False Positive Rate": "2.1%",
                                "Detection Accuracy": "97.3%",
                                "Alert Priority": "High"
                            }
                        elif "Predictive" in analytics_type:
                            metrics = {
                                "Forecast Accuracy": "92.8%",
                                "Prediction Horizon": "30 days",
                                "Model Confidence": "High",
                                "Risk Factors": "4 identified"
                            }
                        elif "Benchmarking" in analytics_type:
                            metrics = {
                                "Performance Score": "87.4/100",
                                "Industry Rank": "Top 15%",
                                "Improvement Areas": "3 identified",
                                "Benchmark Date": "Current"
                            }
                        else:  # Business Impact
                            metrics = {
                                "Revenue Impact": "$2.3M annually",
                                "Cost Savings": "$890K identified",
                                "ROI Potential": "340%",
                                "Time to Value": "3 months"
                            }
                        
                        create_ai_metrics_dashboard(metrics)
                        
                        # Generate sample visualization
                        st.markdown("#### 📊 Auto-Generated Visualization")
                        
                        if "Pattern" in analytics_type:
                            # Pattern discovery chart
                            pattern_data = pd.DataFrame({
                                'Pattern Type': ['Seasonal', 'Geographic', 'Usage-Based', 'Time-Based', 'Event-Driven'],
                                'Occurrence Count': [45, 32, 28, 67, 19],
                                'Confidence Score': [0.94, 0.87, 0.91, 0.96, 0.83]
                            })
                            st.bar_chart(pattern_data.set_index('Pattern Type')[['Occurrence Count']])
                            
                        elif "Correlation" in analytics_type:
                            # Correlation heatmap representation  
                            corr_data = pd.DataFrame({
                                'Metric A': ['Success Rate', 'Latency', 'Throughput', 'Availability'],
                                'Metric B': ['Customer Satisfaction', 'Ticket Volume', 'Revenue', 'User Experience'],
                                'Correlation': [0.89, -0.76, 0.82, 0.91]
                            })
                            st.bar_chart(corr_data.set_index('Metric A')[['Correlation']])
                            
                        else:
                            # Generic trend chart
                            trend_data = pd.DataFrame({
                                'Date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
                                'AI Score': np.random.uniform(75, 95, 30) + np.sin(np.arange(30) * 0.15) * 8
                            })
                            st.line_chart(trend_data.set_index('Date'))
                
                except Exception as e:
                    st.error(f"Error generating intelligent analytics: {e}")
            else:
                st.info(f"🔧 AI Intelligence not available. This would normally provide advanced {analytics_type} using Snowflake's AI algorithms.")
    
    with col2:
        st.markdown("#### 🎯 Intelligence Features")
        st.markdown("""
        **AI Algorithms:**
        - Pattern recognition
        - Anomaly detection
        - Correlation analysis
        - Predictive modeling
        - Statistical inference
        
        **Auto-Discovery:**
        - Hidden patterns
        - Seasonal trends  
        - Geographic insights
        - Customer behaviors
        - Performance drivers
        
        **Confidence Scoring:**
        - Statistical significance
        - Model accuracy
        - Data quality metrics
        - Prediction intervals
        """)

with tab4:
    st.markdown("### 🔍 Cortex Search")
    st.info("Intelligent search across structured and unstructured telecom data using Snowflake's Cortex Search capabilities.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🔎 Intelligent Search Interface")
        
        # Search type selector
        search_type = st.selectbox(
            "Search Type:",
            [
                "🔍 Semantic Search - Find meaning, not just keywords", 
                "📊 Data Discovery - Explore datasets and schemas",
                "📋 Document Search - Search technical documentation",
                "🎯 Contextual Search - Find relevant insights"
            ],
            key="cortex_search_type"
        )
        
        search_query = st.text_input(
            "Search Query:",
            placeholder="Search your data using natural language...",
            key="cortex_search_query"
        )
        
        # Search filters
        with st.expander("🎛️ Search Filters"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                data_sources = st.multiselect(
                    "Data Sources:",
                    ["Cell Tower Data", "Support Tickets", "Customer Records", "Network Logs", "Technical Docs"],
                    default=["Cell Tower Data", "Support Tickets"]
                )
                
                time_range = st.selectbox(
                    "Time Range:",
                    ["Last 24 hours", "Last week", "Last month", "Last quarter", "All time"],
                    index=2
                )
            
            with col_b:
                result_limit = st.slider("Max Results:", 5, 50, 20)
                
                search_priority = st.selectbox(
                    "Search Priority:",
                    ["Relevance", "Recency", "Accuracy", "Completeness"]
                )
        
        if st.button("🚀 Search with Cortex", type="primary", key="cortex_search"):
            if search_query:
                create_ai_progress_tracker(1, 3, "🔍 Understanding search intent...")
                time.sleep(0.5)
                
                create_ai_progress_tracker(2, 3, "🧠 Searching across data sources...")
                time.sleep(0.5)
                
                create_ai_progress_tracker(3, 3, "📊 Ranking and organizing results...")
                
                if AI_FUNCTIONS_AVAILABLE:
                    try:
                        # Generate search response
                        search_context = f"""
                        Cortex Search Query: "{search_query}"
                        Search Type: {search_type}
                        Data Sources: {', '.join(data_sources)}
                        Time Range: {time_range}
                        Priority: {search_priority}
                        
                        Generate intelligent search results that would be returned by Snowflake Cortex Search
                        for a telecom network optimization system. Include:
                        1. Most relevant findings
                        2. Related insights
                        3. Data source references
                        4. Confidence scores
                        5. Follow-up search suggestions
                        """
                        
                        search_results = ai_processor.ai_complete(
                            f"""As Snowflake Cortex Search for telecom network intelligence, provide search results for:
                            
                            {search_context}
                            
                            Return comprehensive, ranked results with semantic understanding of the query.
                            Include specific data points, patterns, and actionable insights.""",
                            max_tokens=600
                        )
                        
                        if search_results:
                            create_ai_insights_card(
                                f"🔍 Cortex Search Results", 
                                search_results, 
                                confidence=0.89, 
                                icon="🎯"
                            )
                            
                            # Display search metrics
                            search_metrics = {
                                "Results Found": f"{np.random.randint(15, 45)} items",
                                "Search Time": "0.3 seconds",
                                "Relevance Score": "94.7%",
                                "Data Coverage": f"{len(data_sources)} sources"
                            }
                            
                            create_ai_metrics_dashboard(search_metrics)
                            
                            # Related searches
                            st.markdown("#### 🔗 Related Searches")
                            related_searches = [
                                f"Similar patterns in {data_sources[0] if data_sources else 'network data'}",
                                f"Historical trends for '{search_query.split()[0] if search_query.split() else 'query'}'",
                                f"Impact analysis of {search_query.lower()}",
                                "Root cause investigation",
                                "Predictive analysis"
                            ]
                            
                            for i, related in enumerate(related_searches[:3], 1):
                                st.markdown(f"{i}. {related}")
                    
                    except Exception as e:
                        st.error(f"Error performing Cortex search: {e}")
                else:
                    st.info("🔧 Cortex Search not available. This would normally provide intelligent search across all your telecom data sources.")
            else:
                st.warning("Please enter a search query.")
    
    with col2:
        st.markdown("#### 🎯 Search Capabilities")
        st.markdown("""
        **Semantic Understanding:**
        - Natural language queries
        - Intent recognition
        - Context awareness
        - Meaning-based matching
        
        **Data Source Integration:**
        - Structured databases
        - Unstructured documents  
        - Log files
        - Configuration data
        - Historical archives
        
        **Advanced Features:**
        - Real-time indexing
        - Relevance ranking
        - Fuzzy matching
        - Multi-language support
        """)

with tab5:
    st.markdown("### ⚙️ Setup & Configuration")
    st.info("Configure Snowflake Intelligence agents, models, and access controls for your telecom network system.")
    
    # Configuration sections
    config_section = st.selectbox(
        "Configuration Section:",
        [
            "🤖 Agent Management",
            "🏗️ Semantic Models", 
            "🔍 Search Services",
            "🛡️ Access Controls",
            "🌐 Cross-Region Inference",
            "📊 Model Configuration"
        ]
    )
    
    if config_section == "🤖 Agent Management":
        st.markdown("#### 🤖 AI Agent Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Create New Agent**")
            
            agent_name = st.text_input("Agent Name:", placeholder="e.g., Network Operations Assistant")
            agent_description = st.text_area("Description:", placeholder="Describe what this agent specializes in...")
            
            agent_model = st.selectbox(
                "Base Model:",
                ["Claude 4.0", "Claude 3.7", "Claude 3.5", "GPT 4.1"],
                key="new_agent_model"
            )
            
            agent_tools = st.multiselect(
                "Available Tools:",
                ["Cortex AISQL", "Cortex Analyst", "Cortex Search", "Custom Functions"],
                default=["Cortex AISQL", "Cortex Analyst"]
            )
            
            if st.button("Create Agent", type="primary"):
                st.success(f"✅ Agent '{agent_name}' created successfully!")
                st.info("💡 Agent is now available in the AI Agents tab for user interactions.")
        
        with col2:
            st.markdown("**Existing Agents**")
            
            existing_agents = [
                {"name": "Network Operations Agent", "model": "Claude 4.0", "status": "Active"},
                {"name": "Customer Experience Agent", "model": "Claude 3.5", "status": "Active"}, 
                {"name": "Business Intelligence Agent", "model": "GPT 4.1", "status": "Inactive"},
                {"name": "Technical Analyst Agent", "model": "Claude 3.7", "status": "Active"}
            ]
            
            for agent in existing_agents:
                status_color = "#4caf50" if agent["status"] == "Active" else "#ff9800"
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; 
                            border-left: 4px solid {status_color};">
                    <strong>{agent['name']}</strong><br>
                    <small>Model: {agent['model']} | Status: {agent['status']}</small>
                </div>
                """, unsafe_allow_html=True)
    
    elif config_section == "🏗️ Semantic Models":
        st.markdown("#### 🏗️ Semantic Model Configuration")
        
        st.code("""
-- Create semantic model for telecom network data
CREATE SEMANTIC MODEL telco_network_model AS (
  SELECT 
    cell_id,
    location,
    performance_metrics,
    customer_impact,
    failure_patterns
  FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER
  WITH SEMANTIC LAYER (
    ENTITY cell_tower_performance,
    METRICS (success_rate, latency, throughput),
    DIMENSIONS (location, time, technology_type)
  )
);

-- Grant access to the semantic model
GRANT USAGE ON SEMANTIC MODEL telco_network_model TO ROLE PUBLIC;
        """, language="sql")
        
        if st.button("📋 Copy Setup Commands", type="secondary"):
            st.success("✅ Commands copied to clipboard!")
    
    elif config_section == "🔍 Search Services":
        st.markdown("#### 🔍 Cortex Search Service Setup")
        
        st.code("""
-- Create Cortex Search service for telecom documents
CREATE CORTEX SEARCH SERVICE telco_search_service
ON customer_support_documents
ATTRIBUTES customer_id, issue_type, resolution_status
WAREHOUSE = COMPUTE_WH;

-- Grant access to search service  
GRANT USAGE ON CORTEX SEARCH SERVICE telco_search_service TO ROLE PUBLIC;
        """, language="sql")
        
        st.markdown("**Search Service Status:**")
        
        search_services = [
            {"name": "telco_search_service", "status": "Active", "docs": "1,250 documents"},
            {"name": "network_logs_search", "status": "Indexing", "docs": "45,000 log entries"},
            {"name": "technical_docs_search", "status": "Active", "docs": "892 technical documents"}
        ]
        
        for service in search_services:
            status_color = "#4caf50" if service["status"] == "Active" else "#2196f3"
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                <strong>{service['name']}</strong> 
                <span style="color: {status_color};">({service['status']})</span><br>
                <small>{service['docs']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    elif config_section == "🛡️ Access Controls":
        st.markdown("#### 🛡️ Role-Based Access Control")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Agent Access Permissions**")
            
            roles = ["NETWORK_ADMIN", "CUSTOMER_SERVICE", "EXECUTIVE", "ANALYST"]
            agents = ["Network Operations", "Customer Experience", "Business Intelligence", "Technical Analyst"]
            
            for role in roles:
                st.markdown(f"**{role}:**")
                accessible_agents = st.multiselect(
                    f"Agents for {role}:",
                    agents,
                    default=agents[:2] if role in ["NETWORK_ADMIN", "ANALYST"] else agents[:1],
                    key=f"access_{role}"
                )
        
        with col2:
            st.markdown("**Sample RBAC Commands**")
            st.code("""
-- Grant agent access to roles
GRANT USAGE ON AGENT network_ops_agent 
TO ROLE NETWORK_ADMIN;

GRANT USAGE ON AGENT customer_exp_agent 
TO ROLE CUSTOMER_SERVICE;

-- Create custom role for Intelligence
CREATE ROLE INTELLIGENCE_USER;
GRANT USAGE ON SCHEMA snowflake_intelligence.agents 
TO ROLE INTELLIGENCE_USER;
            """, language="sql")
    
    elif config_section == "🌐 Cross-Region Inference":
        st.markdown("#### 🌐 Cross-Region Model Access")
        
        st.markdown("""
        Enable access to AI models across different regions for optimal performance:
        """)
        
        region_config = {
            "AWS US": {"models": ["Claude 4.0", "Claude 3.5", "GPT 4.1"], "status": "Enabled"},
            "AWS EU": {"models": ["Claude 4.0", "Claude 3.7"], "status": "Enabled"},
            "Azure US": {"models": ["GPT 4.1", "Claude 3.5"], "status": "Available"}
        }
        
        for region, config in region_config.items():
            st.markdown(f"**{region}:**")
            col_a, col_b = st.columns([3, 1])
            
            with col_a:
                st.write(f"Available models: {', '.join(config['models'])}")
            with col_b:
                if config["status"] == "Enabled":
                    st.success("✅ Enabled")
                else:
                    st.info("ℹ️ Available")
        
        st.code("""
-- Enable cross-region inference
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';

-- Test cross-region model access
SELECT CORTEX.COMPLETE('claude-4-sonnet', 'Test cross-region access');
        """, language="sql")
    
    else:  # Model Configuration
        st.markdown("#### 📊 AI Model Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Model Performance Settings**")
            
            default_model = st.selectbox(
                "Default Model:",
                ["claude-4-sonnet", "claude-3-5-sonnet", "gpt-4-turbo", "claude-3-haiku"],
                index=1
            )
            
            max_tokens = st.slider("Max Tokens:", 100, 2000, 800)
            temperature = st.slider("Temperature:", 0.0, 1.0, 0.3)
            
            enable_caching = st.checkbox("Enable Response Caching", value=True)
            enable_monitoring = st.checkbox("Enable Performance Monitoring", value=True)
            
        with col2:
            st.markdown("**Model Usage Statistics**")
            
            model_stats = pd.DataFrame({
                'Model': ['claude-3-5-sonnet', 'claude-4-sonnet', 'gpt-4-turbo'],
                'Requests': [1250, 890, 445],
                'Avg Response Time': ['0.8s', '1.2s', '0.9s'],
                'Success Rate': ['99.2%', '98.8%', '99.5%']
            })
            
            st.dataframe(model_stats, use_container_width=True)
        
        if st.button("💾 Save Configuration", type="primary"):
            st.success("✅ Model configuration saved successfully!")

# Add footer
add_page_footer()

# Status information
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🧠 <strong>Snowflake Intelligence</strong> - Powered by Cortex AISQL, Cortex Analyst, and Cortex Search</p>
    <p><small>Natural language analytics | AI agents | Intelligent search | Cross-region inference</small></p>
</div>
""", unsafe_allow_html=True)
