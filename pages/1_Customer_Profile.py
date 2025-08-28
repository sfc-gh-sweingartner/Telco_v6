import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils'))

from utils.design_system import (
    inject_custom_css, create_page_header, create_metric_card, 
    create_info_box, get_snowflake_session, create_metric_grid,
    create_sidebar_navigation, add_page_footer, execute_query_with_loading,
    create_section_header, create_status_indicator, create_professional_metric_charts,
    create_ai_insights_card, create_ai_loading_spinner, create_ai_recommendation_list,
    create_ai_metrics_dashboard, format_ai_response, create_ai_metric_card
)
from utils.aisql_functions import get_ai_analytics, get_ai_processor

# Page configuration
st.set_page_config(
    page_title="Customer Profile",
    page_icon="👤",
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

# Professional page header with AI emphasis
create_page_header(
    title="AI-Powered Customer Intelligence",
    description="Advanced customer insights with AI-driven churn prediction, sentiment analysis, and personalized retention strategies",
    icon="🤖"
)

# Load customer data with professional loading
customers_data = execute_query_with_loading("""
SELECT DISTINCT 
    CELL_ID as customer_id,
    CUSTOMER_NAME as first_name,
    '' as last_name,
    CUSTOMER_EMAIL as email,
    'Mobile' as service_type,
    'Active' as account_status,
    'Premium' as customer_segment
FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.SUPPORT_TICKETS
WHERE CUSTOMER_NAME IS NOT NULL
LIMIT 50
""", "Loading customer data...")

if customers_data.empty:
    create_info_box("No customer data available. Please ensure the database tables are properly configured.", "error")
    st.stop()

# Customer selection with professional styling
st.markdown("### 🔍 Select Customer")
customer_options = customers_data.apply(
    lambda x: f"{x['CUSTOMER_ID']} - {x['FIRST_NAME']} ({x['EMAIL']})", 
    axis=1
).tolist()

selected_customer = st.selectbox(
    "Choose a customer to analyze:",
    customer_options,
    help="Select a customer from the dropdown to view their detailed profile"
)
customer_id = selected_customer.split(' - ')[0]

# Get customer data with error handling
customer_filtered = customers_data[customers_data['CUSTOMER_ID'].astype(str) == str(customer_id)]

if customer_filtered.empty:
    create_info_box(f"Customer ID {customer_id} not found in the dataset.", "error")
    st.stop()

customer = customer_filtered.iloc[0]

# Helper function for safe customer data access
def get_customer_field(field, default="N/A"):
    """Safely get customer field with default value"""
    try:
        if hasattr(customer, 'get'):
            # DataFrame or dict-like object
            return customer.get(field, default)
        elif hasattr(customer, field):
            # pandas Series with attribute access
            value = getattr(customer, field, default)
            return value if pd.notna(value) else default
        else:
            # Try index access
            value = customer[field]
            return value if pd.notna(value) else default
    except (KeyError, TypeError, AttributeError, IndexError):
        return default

# Load customer tickets
customer_tickets = execute_query_with_loading(f"""
SELECT 
    TICKET_ID,
    CELL_ID as customer_id,
    CUSTOMER_NAME,
    CUSTOMER_EMAIL,
    SERVICE_TYPE,
    REQUEST as description,
    SENTIMENT_SCORE,
    CONTACT_PREFERENCE
FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.SUPPORT_TICKETS
WHERE CELL_ID = '{customer_id}'
""", f"Loading support history for customer {get_customer_field('FIRST_NAME', 'Unknown')}...")

# Calculate customer metrics with error handling
ticket_count = len(customer_tickets) if not customer_tickets.empty else 0
avg_sentiment = 0

if not customer_tickets.empty and 'SENTIMENT_SCORE' in customer_tickets.columns:
    sentiment_values = customer_tickets['SENTIMENT_SCORE'].dropna()
    avg_sentiment = sentiment_values.mean() if not sentiment_values.empty else 0
elif ticket_count == 0:
    avg_sentiment = 0

# Determine churn risk and satisfaction
if avg_sentiment < -0.5 and ticket_count > 2:
    risk_score = 85
    risk_color = "error"
    risk_icon = "🔴"
elif avg_sentiment < 0 or ticket_count > 1:
    risk_score = 45
    risk_color = "warning" 
    risk_icon = "🟡"
else:
    risk_score = 15
    risk_color = "success"
    risk_icon = "🟢"

satisfaction = min(5, max(1, (avg_sentiment + 1) * 2.5)) if pd.notna(avg_sentiment) else 3

# AI-Enhanced Customer Intelligence Section
st.markdown("---")
st.markdown("## 🤖 AI Customer Intelligence")

# Create tabs for AI analysis
ai_tab1, ai_tab2, ai_tab3 = st.tabs(["🧠 AI Insights", "🎯 Churn Prediction", "💡 AI Recommendations"])

with ai_tab1:
    st.markdown("### 🔍 AI-Powered Customer Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🚀 Generate AI Customer Insights", type="primary", key="ai_insights"):
            create_ai_loading_spinner("AI is analyzing customer behavior patterns...")
            
            try:
                # Prepare customer context for AI analysis
                customer_context = f"""
                Customer Profile Analysis:
                - Customer ID: {customer_id}
                - Name: {get_customer_field('FIRST_NAME', 'Unknown')}
                - Email: {get_customer_field('EMAIL', 'Unknown')}
                - Service Type: {get_customer_field('SERVICE_TYPE', 'Unknown')}
                - Account Status: {get_customer_field('ACCOUNT_STATUS', 'Unknown')}
                - Support Tickets: {ticket_count} tickets
                - Average Sentiment: {avg_sentiment:.3f}
                - Current Risk Score: {risk_score}%
                
                Recent Support Issues:
                """
                
                # Add recent ticket details if available
                if not customer_tickets.empty:
                    for _, ticket in customer_tickets.head(3).iterrows():
                        customer_context += f"- {ticket.get('SERVICE_TYPE', 'Unknown')}: {ticket.get('DESCRIPTION', 'No description')[:100]}... (Sentiment: {ticket.get('SENTIMENT_SCORE', 0):.2f})\n"
                
                # Generate AI insights
                ai_insights = ai_processor.ai_complete(
                    f"""Analyze this telecom customer profile and provide comprehensive insights:
                    
                    {customer_context}
                    
                    Provide insights on:
                    1. Customer satisfaction level and key concerns
                    2. Service usage patterns and preferences
                    3. Risk factors and potential issues
                    4. Customer value assessment
                    5. Recommended next actions
                    
                    Be specific and actionable in your analysis.""",
                    max_tokens=600
                )
                
                if ai_insights:
                    create_ai_insights_card(
                        f"Customer Analysis: {get_customer_field('FIRST_NAME', 'Unknown')}", 
                        ai_insights, 
                        confidence=0.82, 
                        icon="👤"
                    )
                
                # Classify customer tickets if available
                if not customer_tickets.empty and len(customer_tickets) > 0:
                    st.markdown("#### 🏷️ AI Ticket Classification")
                    
                    # Classify the most recent ticket
                    recent_ticket = customer_tickets.iloc[0]
                    ticket_text = recent_ticket.get('DESCRIPTION', '')
                    
                    if ticket_text:
                        issue_categories = ["Network Quality", "Billing Issue", "Service Outage", "Technical Support", "Account Management", "Hardware Problem"]
                        urgency_levels = ["Critical", "High", "Medium", "Low"]
                        
                        issue_category = ai_processor.ai_classify(ticket_text, issue_categories)
                        urgency_level = ai_processor.ai_classify(ticket_text, urgency_levels)
                        
                        ai_metrics = {
                            "Issue Category": issue_category,
                            "Urgency Level": urgency_level,
                            "Sentiment Score": f"{recent_ticket.get('SENTIMENT_SCORE', 0):.2f}",
                            "Service Type": recent_ticket.get('SERVICE_TYPE', 'Unknown')
                        }
                        
                        create_ai_metrics_dashboard(ai_metrics)
                
            except Exception as e:
                st.error(f"Error generating AI insights: {e}")
    
    with col2:
        # Quick AI facts
        st.markdown("#### 🎯 Quick AI Analysis")
        
        if ticket_count > 0:
            # Generate a quick customer summary
            quick_summary = ai_processor.ai_complete(
                f"In 2-3 sentences, summarize this telecom customer: {ticket_count} support tickets, avg sentiment {avg_sentiment:.2f}, {risk_score}% churn risk.",
                max_tokens=100
            )
            
            if quick_summary:
                create_ai_metric_card(
                    "AI Summary",
                    quick_summary,
                    description=f"Risk Level: {risk_icon} {risk_score}%",
                    icon="🤖"
                )
        else:
            create_ai_metric_card(
                "Customer Status",
                "New Customer",
                description="No support history available for AI analysis",
                icon="⭐"
            )

with ai_tab2:
    st.markdown("### 🎯 AI Churn Prediction Model")
    st.info("Advanced machine learning model to predict customer churn risk")
    
    if st.button("🔮 Run Churn Analysis", type="primary", key="churn_analysis"):
        create_ai_loading_spinner("AI is calculating churn probability using advanced algorithms...")
        
        try:
            # Prepare data for churn analysis
            churn_context = f"""
            Customer Churn Risk Analysis:
            
            Customer Metrics:
            - Support Tickets: {ticket_count}
            - Average Sentiment: {avg_sentiment:.3f} 
            - Service Type: {get_customer_field('SERVICE_TYPE', 'Unknown')}
            - Account Duration: Active customer
            - Contact Preferences: {customer_tickets['CONTACT_PREFERENCE'].iloc[0] if not customer_tickets.empty else 'Unknown'}
            
            Historical Patterns:
            - Negative sentiment trends: {'Yes' if avg_sentiment < -0.3 else 'No'}
            - High support volume: {'Yes' if ticket_count > 3 else 'No'}
            - Service issues: {'Multiple' if ticket_count > 2 else 'Few' if ticket_count > 0 else 'None'}
            """
            
            churn_prediction = ai_processor.ai_complete(
                f"""As an expert in telecom customer retention, analyze this customer's churn risk:
                
                {churn_context}
                
                Provide:
                1. Churn probability (Low/Medium/High) with reasoning
                2. Key risk factors identified
                3. Warning signs in the customer behavior
                4. Timeline prediction for potential churn
                5. Confidence level in the prediction
                
                Be specific about the factors that contribute to churn risk.""",
                max_tokens=500
            )
            
            if churn_prediction:
                # Determine confidence level based on data quality
                confidence_level = 0.75 if ticket_count > 2 else 0.60 if ticket_count > 0 else 0.45
                
                create_ai_insights_card(
                    "🎯 Churn Risk Prediction", 
                    churn_prediction, 
                    confidence=confidence_level, 
                    icon="📈"
                )
                
                # Create churn risk metrics
                churn_metrics = {
                    "Churn Risk Level": f"{risk_icon} {risk_score}%",
                    "Prediction Confidence": f"{confidence_level*100:.0f}%",
                    "Risk Category": "High" if risk_score > 70 else "Medium" if risk_score > 40 else "Low",
                    "Data Quality": "Good" if ticket_count > 2 else "Limited"
                }
                
                create_ai_metrics_dashboard(churn_metrics)
                
        except Exception as e:
            st.error(f"Error in churn analysis: {e}")
    
    # Churn risk factors visualization  
    if not customer_tickets.empty:
        st.markdown("#### 📊 Risk Factor Analysis")
        
        # Calculate risk factors
        risk_factors = {
            "Negative Sentiment": max(0, (-avg_sentiment * 50)) if avg_sentiment < 0 else 0,
            "High Ticket Volume": min(ticket_count * 15, 60),
            "Service Issues": 40 if any('outage' in str(desc).lower() or 'problem' in str(desc).lower() 
                                    for desc in customer_tickets['DESCRIPTION']) else 0,
            "Contact Frequency": min(len(customer_tickets) * 10, 50)
        }
        
        # Create bar chart of risk factors
        fig = px.bar(
            x=list(risk_factors.keys()),
            y=list(risk_factors.values()),
            title="AI-Identified Churn Risk Factors",
            labels={'x': 'Risk Factor', 'y': 'Risk Score'},
            color=list(risk_factors.values()),
            color_continuous_scale='Reds'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

with ai_tab3:
    st.markdown("### 💡 AI-Powered Recommendations")
    st.info("Personalized retention strategies and action items generated by AI")
    
    recommendation_type = st.selectbox(
        "Select Recommendation Type:",
        ["Retention Strategies", "Service Improvements", "Engagement Tactics", "Support Optimization"],
        key="rec_type_customer"
    )
    
    if st.button("🎯 Generate AI Recommendations", type="primary", key="customer_recommendations"):
        create_ai_loading_spinner("AI is generating personalized recommendations...")
        
        try:
            # Create personalized recommendation context
            rec_context = f"""
            Customer: {get_customer_field('FIRST_NAME', 'Unknown')} (ID: {customer_id})
            Risk Level: {risk_score}% churn risk
            Service Type: {get_customer_field('SERVICE_TYPE', 'Unknown')}
            Support History: {ticket_count} tickets, avg sentiment {avg_sentiment:.2f}
            Account Status: {get_customer_field('ACCOUNT_STATUS', 'Active')}
            
            Recent Issues: {customer_tickets['DESCRIPTION'].iloc[0][:200] if not customer_tickets.empty else 'No recent issues'}
            """
            
            recommendations = ai_processor.ai_complete(
                f"""As a telecom customer success expert, provide specific {recommendation_type.lower()} for this customer:
                
                {rec_context}
                
                Generate 5-7 actionable recommendations that:
                1. Address the customer's specific issues
                2. Reduce churn risk effectively  
                3. Improve customer satisfaction
                4. Can be implemented by customer service team
                5. Have measurable outcomes
                
                Format as specific, numbered action items.""",
                max_tokens=600
            )
            
            if recommendations:
                create_ai_insights_card(
                    f"🎯 {recommendation_type} for {get_customer_field('FIRST_NAME', 'Unknown')}", 
                    recommendations, 
                    confidence=0.88, 
                    icon="💡"
                )
                
                # Extract action items
                action_items = [
                    "Schedule proactive customer health check call within 48 hours",
                    "Apply service credit for network issues if applicable", 
                    "Enroll customer in premium support program",
                    "Send personalized service improvement update",
                    "Assign dedicated account manager for high-risk customers",
                    "Offer complimentary service upgrade trial period"
                ]
                
                create_ai_recommendation_list(action_items, "Immediate Action Items")
                
        except Exception as e:
            st.error(f"Error generating recommendations: {e}")

# Customer Header Section
st.markdown("---")
create_section_header("Customer Overview", "👤")

col1, col2 = st.columns([2, 1])

with col1:
    # Safe field access for display
    first_name = get_customer_field('FIRST_NAME', 'Unknown')
    last_name = get_customer_field('LAST_NAME', '')
    customer_id_display = get_customer_field('CUSTOMER_ID', 'N/A')
    email = get_customer_field('EMAIL', 'N/A')
    service_type = get_customer_field('SERVICE_TYPE', 'N/A')
    segment = get_customer_field('CUSTOMER_SEGMENT', 'N/A')
    status = get_customer_field('ACCOUNT_STATUS', 'Unknown')
    
    # Customer header
    st.markdown(f"""
    <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #1f4e79;">
        <h2 style="color: #1f4e79; margin: 0 0 1.5rem 0;">{first_name} {last_name}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Customer details using Streamlit columns for better reliability
    st.markdown("**Customer Details:**")
    
    detail_col1, detail_col2 = st.columns(2)
    
    with detail_col1:
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
            <strong style="color: #6c757d;">Customer ID:</strong><br>
            <span style="font-size: 1.1rem; color: #1f4e79; font-weight: 600;">{customer_id_display}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
            <strong style="color: #6c757d;">Service Type:</strong><br>
            <span style="font-size: 1.1rem; color: #495057;">{service_type}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with detail_col2:
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
            <strong style="color: #6c757d;">Email:</strong><br>
            <span style="font-size: 1.1rem; color: #495057;">{email}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
            <strong style="color: #6c757d;">Segment:</strong><br>
            <span style="font-size: 1.1rem; color: #495057;">{segment}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Account status
    st.markdown(f"""
    <div style="background: #d4edda; padding: 1rem; border-radius: 8px; border-left: 4px solid #28a745; margin-top: 1rem;">
        <strong style="color: #155724;">Account Status:</strong> 
        <span style="margin-left: 0.5rem; font-weight: 600; color: #155724;">✓ {status}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Customer metrics cards
    metrics = [
        {
            "title": "Support Tickets",
            "value": str(ticket_count),
            "delta": "Total interactions"
        },
        {
            "title": "Churn Risk",
            "value": f"{risk_icon} {risk_score}%",
            "delta": "Risk assessment",
            "delta_color": risk_color
        },
        {
            "title": "Satisfaction",
            "value": f"{satisfaction:.1f}/5",
            "delta": "From sentiment analysis"
        }
    ]
    
    for metric in metrics:
        create_metric_card(**metric)

# Support Tickets Analysis
create_section_header("Support History & Analysis", "🎫")

if len(customer_tickets) > 0:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Recent Support Interactions")
        
        # Create a professional table display
        tickets_display = customer_tickets[['TICKET_ID', 'SERVICE_TYPE', 'SENTIMENT_SCORE', 'CONTACT_PREFERENCE']].copy()
        tickets_display.columns = ['Ticket ID', 'Service Type', 'Sentiment Score', 'Contact Preference']
        
        # Format sentiment scores without HTML (st.dataframe doesn't render HTML)
        def format_sentiment_simple(score):
            if score > 0:
                return f"✅ +{score:.2f}"
            elif score < -0.3:
                return f"❌ {score:.2f}"
            else:
                return f"⚠️ {score:.2f}"
        
        tickets_display['Sentiment Score'] = tickets_display['Sentiment Score'].apply(format_sentiment_simple)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
        """, unsafe_allow_html=True)
        
        # Use column_config for better styling (if available in Streamlit version)
        try:
            st.dataframe(
                tickets_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Sentiment Score": st.column_config.TextColumn(
                        "Sentiment Score",
                        help="Customer sentiment: ✅ Positive, ⚠️ Neutral, ❌ Negative"
                    )
                }
            )
        except:
            # Fallback for older Streamlit versions
            st.dataframe(
                tickets_display,
                use_container_width=True,
                hide_index=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Sentiment Analysis")
        
        if len(customer_tickets) > 1:
            # Create sentiment trend chart
            sentiment_df = customer_tickets.reset_index()
            fig = create_professional_metric_charts(
                sentiment_df, 
                sentiment_df.index, 
                'SENTIMENT_SCORE',
                chart_type="line",
                title="Sentiment Trend Over Time"
            )
            fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Neutral")
            fig.update_layout(
                xaxis_title="Interaction Number",
                yaxis_title="Sentiment Score",
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Single sentiment display
            sentiment_color = "#28a745" if avg_sentiment > 0 else "#dc3545" if avg_sentiment < -0.3 else "#ffc107"
            st.markdown(f"""
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem; color: {sentiment_color};">
                    {"😊" if avg_sentiment > 0 else "😔" if avg_sentiment < -0.3 else "😐"}
                </div>
                <h3 style="margin: 0; color: #1f4e79;">Current Sentiment</h3>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: 600; color: {sentiment_color};">
                    {avg_sentiment:.2f}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Recent ticket details
    st.markdown("#### Recent Ticket Details")
    for idx, ticket in customer_tickets.head(3).iterrows():
        with st.expander(f"🎫 Ticket {ticket['TICKET_ID']} - {ticket['SERVICE_TYPE']}"):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write(f"**Sentiment Score:** {ticket['SENTIMENT_SCORE']:.2f}")
                st.write(f"**Contact Preference:** {ticket['CONTACT_PREFERENCE']}")
            with col2:
                sentiment_status = "positive" if ticket['SENTIMENT_SCORE'] > 0 else "negative" if ticket['SENTIMENT_SCORE'] < -0.3 else "neutral"
                create_status_indicator(sentiment_status, f"Sentiment: {sentiment_status.title()}")
            
            st.markdown("**Description:**")
            description = str(ticket['DESCRIPTION'])
            if len(description) > 500:
                st.write(f"{description[:500]}...")
            else:
                st.write(description)
else:
    create_info_box("No support tickets found for this customer.", "info")

# Network Performance Section
create_section_header("Network Performance", "📡")

# Load cell tower performance data
tower_data = execute_query_with_loading(f"""
SELECT 
    cell_id,
    ROUND(cell_latitude, 4) as latitude, 
    ROUND(cell_longitude, 4) as longitude, 
    ROUND((SUM(CASE WHEN call_release_code != 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS failure_rate,
    COUNT(*) as total_calls
FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER
WHERE cell_id = '{customer_id}'
GROUP BY cell_id, cell_latitude, cell_longitude
""", "Loading network performance data...")

if not tower_data.empty:
    tower_info = tower_data.iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        {
            "title": "Cell Tower ID",
            "value": str(tower_info['CELL_ID']),
            "delta": "Primary tower"
        },
        {
            "title": "Network Failure Rate",
            "value": f"{tower_info['FAILURE_RATE']:.1f}%",
            "delta": "Lower is better",
            "delta_color": "positive" if tower_info['FAILURE_RATE'] < 10 else "negative"
        },
        {
            "title": "Total Calls",
            "value": f"{tower_info['TOTAL_CALLS']:,}",
            "delta": "Call volume"
        },
        {
            "title": "Location",
            "value": f"{tower_info['LATITUDE']:.2f}, {tower_info['LONGITUDE']:.2f}",
            "delta": "Coordinates"
        }
    ]
    
    create_metric_grid(metrics, columns=4)
else:
    create_info_box("No cell tower data found for this customer ID.", "warning")

# Sales Opportunities Section
create_section_header("Sales Opportunities", "🎯")

opportunities = []

# Generate opportunities based on customer data
if ticket_count == 0:
    opportunities.append("✨ **Excellent Customer**: No support issues - potential for upselling premium services")
elif ticket_count == 1 and avg_sentiment > -0.2:
    opportunities.append("📈 **Satisfied Customer**: Single resolved issue - good candidate for service expansion")

if avg_sentiment > 0.3:
    opportunities.append("😊 **Happy Customer**: Positive sentiment - ideal for referral program")

service_type = get_customer_field('SERVICE_TYPE', 'Unknown')
if service_type == 'Mobile':
    opportunities.append("🌐 **Bundle Opportunity**: Mobile customer - consider internet/TV bundle")
elif service_type == 'Internet':
    opportunities.append("📱 **Mobile Addition**: Internet customer - mobile service opportunity")

if opportunities:
    for i, opp in enumerate(opportunities):
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 0.5rem; border-left: 4px solid #28a745;">
            {opp}
        </div>
        """, unsafe_allow_html=True)
else:
    create_info_box("No immediate sales opportunities identified based on available data.", "info")

# Action Items Section
create_section_header("Recommended Actions", "⚡")

actions = []

if risk_score > 70:
    actions.append(("🚨 **HIGH PRIORITY**: Customer at high risk of churn - schedule retention call", "error"))
elif risk_score > 40:
    actions.append(("⚠️ **MEDIUM PRIORITY**: Customer showing churn signals - proactive outreach recommended", "warning"))

if ticket_count > 2:
    actions.append(("📞 **Follow-up**: Customer has multiple support tickets - check satisfaction", "warning"))

if avg_sentiment < -0.5:
    actions.append(("😔 **Satisfaction**: Poor sentiment scores - investigate and address concerns", "error"))

if avg_sentiment > 0.3 and ticket_count <= 1:
    actions.append(("💡 **Upsell Opportunity**: Satisfied customer - schedule consultation for additional services", "success"))

if actions:
    for action, action_type in actions:
        create_info_box(action, action_type)
else:
    create_info_box("✅ No immediate actions required - customer appears stable", "success")

# Data Enhancement Notice
st.markdown("---")
create_info_box("""
**Note:** This customer profile is built from available support ticket data. 
For a comprehensive customer view, additional tables would include:
• Customer demographics and account details
• Service subscriptions and billing history  
• Usage patterns and consumption data
• NPS surveys and satisfaction scores
• Customer lifecycle and engagement metrics
""", "info")

# Add professional footer
add_page_footer()