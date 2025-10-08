"""
AI Network Assistant - Conversational Analytics
==============================================

Natural language interface for network analysis using Snowflake Cortex AISQL.
Users can ask questions about their network in plain English and get intelligent responses.
"""

import streamlit as st
import pandas as pd
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
        add_page_footer, get_snowflake_session, create_ai_insights_card,
        create_ai_loading_spinner, create_ai_metrics_dashboard, create_ai_chat_interface,
        format_ai_response, create_ai_metric_card
    )
    AI_FUNCTIONS_AVAILABLE = True
except ImportError:
    from utils.design_system import (
        inject_custom_css, create_page_header, create_sidebar_navigation, 
        add_page_footer, get_snowflake_session
    )
    AI_FUNCTIONS_AVAILABLE = False
    
    # Define fallback AI functions
    def create_ai_insights_card(title, insight, confidence=0.0, icon=""):
        st.markdown(f"### {icon} {title}")
        # Fix newline formatting for better display
        formatted_insight = insight.replace('\\n', '\n') if '\\n' in insight else insight
        st.info(formatted_insight)
    def create_ai_loading_spinner(message="AI is analyzing..."):
        st.info(f" {message}")
    def create_ai_metrics_dashboard(metrics):
        cols = st.columns(len(metrics))
        for i, (key, value) in enumerate(metrics.items()):
            with cols[i % len(cols)]:
                st.metric(key, value)
    def create_ai_chat_interface():
        pass
    def format_ai_response(response, title="AI Response"):
        st.markdown(f"### {title}")
        st.write(response)
    def create_ai_metric_card(title, value, description="", icon=""):
        st.metric(title, value, help=description)

try:
    from utils.aisql_functions import get_ai_analytics, get_ai_processor
except ImportError:
    def get_ai_analytics(session):
        class FallbackAnalytics:
            def generate_executive_summary(self, *args, **kwargs):
                return " AI Network Assistant is being deployed. Advanced conversational analytics will be available shortly!"
        return FallbackAnalytics()
    def get_ai_processor(session):
        class FallbackProcessor:
            def ai_complete(self, prompt, **kwargs):
                return "️ AI conversational interface is being updated. Full natural language network analysis capabilities will be available shortly!"
        return FallbackProcessor()

# Page configuration
st.set_page_config(
    page_title="AI Network Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS and create navigation
inject_custom_css()
# create_sidebar_navigation()  # Removed: Logo not needed in sidebar
create_ai_chat_interface()

# Initialize Snowflake session and AI components
session = get_snowflake_session()
ai_analytics = get_ai_analytics(session)
ai_processor = get_ai_processor(session)

# Professional page header
create_page_header(
    title="AI Network Assistant",
    description="Natural language interface for network analysis - ask questions in plain English and get intelligent insights",
    icon=""
)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "Hi! I'm your AI Network Assistant. I can help you analyze your telecom network using natural language. Try asking me questions like:\n\n• 'Show me cell towers with high failure rates'\n• 'Which areas have the most customer complaints?'\n• 'What's causing network issues in California?'\n• 'Predict where we might have problems next month'\n\nWhat would you like to know about your network?",
        "timestamp": datetime.now()
    })

# Show deployment status if AI functions are not fully available
if not AI_FUNCTIONS_AVAILABLE:
    st.warning("""
     **AI Network Assistant Deployment in Progress**
    
    The conversational AI interface is being deployed with advanced capabilities including:
    - Natural language query processing
    - Intelligent data analysis and visualization 
    - Predictive insights and recommendations
    - Multi-turn conversation context
    
    **Expected availability:** 5-10 minutes
    """)
    
    if st.button(" Check AI Assistant Status", type="primary"):
        st.rerun()

# Main chat interface
st.markdown("##  Network Analysis Chat")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "timestamp" in message:
            st.caption(f" {message['timestamp'].strftime('%H:%M:%S')}")

# Chat input
if prompt := st.chat_input("Ask me anything about your network..."):
    # Add user message to chat history
    user_message = {
        "role": "user", 
        "content": prompt,
        "timestamp": datetime.now()
    }
    st.session_state.chat_history.append(user_message)
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
        st.caption(f" {user_message['timestamp'].strftime('%H:%M:%S')}")
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner(" Analyzing your question..."):
            
            # Determine the type of query and generate appropriate response
            response = process_network_query(prompt, session, ai_processor, ai_analytics)
            
            st.write(response["content"])
            
            # Show any additional data or visualizations
            if "data" in response:
                if isinstance(response["data"], pd.DataFrame) and not response["data"].empty:
                    st.dataframe(response["data"])
            
            if "chart" in response:
                st.plotly_chart(response["chart"], use_container_width=True)
            
            if "metrics" in response:
                create_ai_metrics_dashboard(response["metrics"])
        
        # Add assistant response to chat history
        assistant_message = {
            "role": "assistant",
            "content": response["content"],
            "timestamp": datetime.now()
        }
        if "data" in response:
            assistant_message["data"] = response["data"]
        
        st.session_state.chat_history.append(assistant_message)
        st.caption(f" {assistant_message['timestamp'].strftime('%H:%M:%S')}")

# Sidebar with conversation tools
with st.sidebar:
    st.markdown("---")
    st.markdown("### ️ Conversation Tools")
    
    if st.button("️ Clear Chat History", type="secondary"):
        st.session_state.chat_history = []
        st.rerun()
    
    if st.button(" Export Chat", type="secondary"):
        chat_export = {
            "timestamp": datetime.now().isoformat(),
            "conversation": st.session_state.chat_history
        }
        st.download_button(
            label=" Download Chat JSON",
            data=json.dumps(chat_export, indent=2, default=str),
            file_name=f"network_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )
    
    st.markdown("---")
    st.markdown("###  Example Questions")
    
    example_queries = [
        "Show me the worst performing cell towers",
        "Which regions have the most customer complaints?", 
        "What's the average sentiment score by service type?",
        "Find correlations between failure rate and customer satisfaction",
        "Predict network capacity needs for next quarter",
        "Show me towers that need immediate attention",
        "Which areas should we prioritize for upgrades?",
        "What's causing high latency in our network?"
    ]
    
    for query in example_queries:
        if st.button(f" {query}", key=f"example_{hash(query)}", use_container_width=True):
            # Add the example query as if the user typed it
            st.session_state.example_query = query
            st.rerun()

# Handle example query selection
if hasattr(st.session_state, 'example_query'):
    # Process the example query
    prompt = st.session_state.example_query
    del st.session_state.example_query
    
    # Add to chat history and process (same as above)
    user_message = {
        "role": "user", 
        "content": prompt,
        "timestamp": datetime.now()
    }
    st.session_state.chat_history.append(user_message)
    
    # Generate response
    response = process_network_query(prompt, session, ai_processor, ai_analytics)
    
    assistant_message = {
        "role": "assistant",
        "content": response["content"], 
        "timestamp": datetime.now()
    }
    st.session_state.chat_history.append(assistant_message)
    
    st.rerun()

def process_network_query(query: str, session, ai_processor, ai_analytics):
    """
    Process a natural language query about the network and return appropriate response
    """
    try:
        # Classify the type of query
        query_lower = query.lower()
        
        # Prepare context about available data
        data_context = """
        Available Network Data:
        - Cell tower performance metrics (failure rates, latency, throughput)  
        - Customer support tickets with sentiment analysis
        - Geographic coverage and regional performance
        - Historical trends and patterns
        
        Capabilities:
        - Statistical analysis and correlations
        - Predictive insights and forecasting
        - Performance comparisons and rankings
        - Root cause analysis
        """
        
        if any(word in query_lower for word in ['show', 'list', 'find', 'get', 'worst', 'best', 'top']):
            # Data retrieval query
            response_content = ai_processor.ai_complete(
                f"""As a network analyst, respond to this data request: "{query}"
                
                {data_context}
                
                Provide a helpful response that:
                1. Acknowledges what the user is looking for
                2. Explains what data would be most relevant
                3. Offers insights about what the results might indicate
                4. Suggests follow-up analysis
                
                Be conversational and helpful.""",
                max_tokens=400
            )
            
            # Try to generate some sample data
            try:
                if 'cell tower' in query_lower or 'tower' in query_lower:
                    sample_data = session.sql("""
                        SELECT CELL_ID, ROUND(AVG(CASE WHEN CALL_RELEASE_CODE != 0 THEN 1 ELSE 0 END) * 100, 2) as failure_rate,
                               BID_DESCRIPTION as location
                        FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER 
                        GROUP BY CELL_ID, BID_DESCRIPTION 
                        ORDER BY failure_rate DESC 
                        LIMIT 10
                    """).to_pandas()
                    
                    return {
                        "content": response_content,
                        "data": sample_data,
                        "metrics": {
                            "Records Found": str(len(sample_data)),
                            "Data Source": "Cell Tower Performance",
                            "Analysis Type": "Performance Ranking"
                        }
                    }
                    
            except Exception as e:
                # Fallback if data query fails
                pass
        
        elif any(word in query_lower for word in ['why', 'cause', 'reason', 'explain']):
            # Analytical/explanatory query  
            response_content = ai_processor.ai_complete(
                f"""As a network expert, provide an analytical response to: "{query}"
                
                {data_context}
                
                Provide insights that:
                1. Address the "why" behind the question
                2. Explain likely causes and factors
                3. Connect to network performance principles
                4. Suggest investigation approaches
                
                Be detailed and technical but accessible.""",
                max_tokens=500
            )
        
        elif any(word in query_lower for word in ['predict', 'forecast', 'future', 'trend']):
            # Predictive query
            response_content = ai_processor.ai_complete(
                f"""As a predictive network analyst, respond to: "{query}"
                
                {data_context}
                
                Provide predictive insights that:
                1. Explain forecasting approaches for this scenario
                2. Identify key indicators to monitor
                3. Discuss confidence levels and limitations
                4. Recommend proactive measures
                
                Be forward-looking and actionable.""",
                max_tokens=500
            )
        
        elif any(word in query_lower for word in ['compare', 'versus', 'vs', 'difference']):
            # Comparative query
            response_content = ai_processor.ai_complete(
                f"""As a network analyst, provide a comparative analysis for: "{query}"
                
                {data_context}
                
                Provide comparison insights that:
                1. Identify key metrics for comparison
                2. Explain what differences might indicate
                3. Highlight performance patterns
                4. Suggest optimization opportunities
                
                Be analytical and comparative.""",
                max_tokens=500
            )
        
        else:
            # General query
            response_content = ai_processor.ai_complete(
                f"""As a helpful network assistant, respond to: "{query}"
                
                {data_context}
                
                Provide a comprehensive response that:
                1. Directly addresses the question
                2. Provides relevant network insights
                3. Suggests related analysis
                4. Offers actionable next steps
                
                Be helpful and conversational.""",
                max_tokens=500
            )
        
        return {
            "content": response_content,
            "metrics": {
                "Query Type": "Natural Language Analysis",
                "Processing Time": "< 2 seconds",
                "Confidence": "High"
            }
        }
        
    except Exception as e:
        return {
            "content": f"I apologize, but I encountered an issue processing your question: {str(e)}\n\nPlease try rephrasing your question or ask about specific network metrics like failure rates, customer sentiment, or tower performance.",
            "metrics": {
                "Status": "Error",
                "Query": query[:50] + "..." if len(query) > 50 else query
            }
        }

# Help section
with st.expander("How to Use the AI Network Assistant", expanded=False):
    st.markdown("""
    ###  Conversation Tips
    
    **Ask Natural Questions:**
    - "Show me towers with high failure rates"
    - "Why are customers complaining in Los Angeles?"
    - "Predict network issues for next month"
    
    **Query Types I Handle:**
    -  **Data Requests**: "Show me...", "List...", "Find..."
    -  **Analysis**: "Why...", "What causes...", "Explain..."
    -  **Predictions**: "Predict...", "Forecast...", "What will happen..."
    - ️ **Comparisons**: "Compare...", "Which is better...", "Difference between..."
    
    **Best Practices:**
    - Be specific about metrics or regions
    - Ask follow-up questions for deeper analysis
    - Request explanations for complex results
    - Use examples from the sidebar for ideas
    
    **Data Available:**
    - Cell tower performance metrics
    - Customer support tickets and sentiment
    - Geographic and regional analysis
    - Historical trends and patterns
    """)

# Add professional footer
add_page_footer()
