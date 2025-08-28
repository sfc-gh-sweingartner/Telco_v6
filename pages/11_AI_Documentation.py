"""
AI Documentation & User Guide
==============================

Comprehensive documentation for all AI features and capabilities.
User guides, technical documentation, and best practices for AI-powered telco analytics.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils'))

from utils.design_system import (
    inject_custom_css, create_page_header, create_sidebar_navigation, 
    add_page_footer, create_ai_insights_card, create_ai_metrics_dashboard
)

# Page configuration
st.set_page_config(
    page_title="AI Documentation",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS and create navigation
inject_custom_css()
create_sidebar_navigation()

# Professional page header
create_page_header(
    title="AI Documentation & User Guide",
    description="Comprehensive guide to AI-powered telco network optimization capabilities and best practices",
    icon="📚"
)

# Documentation sidebar navigation
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📖 Documentation Sections")
    
    doc_section = st.radio(
        "Select Documentation Topic:",
        [
            "🚀 Getting Started",
            "🤖 AI Features Overview", 
            "🔧 Technical Reference",
            "📊 Use Cases & Examples",
            "⚡ Best Practices",
            "🔧 Troubleshooting",
            "❓ FAQ"
        ],
        key="doc_section"
    )
    
    st.markdown("---")
    st.markdown("### 📋 Quick Links")
    
    quick_links = [
        ("🏠 Main Dashboard", "Main page with executive insights"),
        ("🧠 AI Insights", "Central AI analysis hub"),
        ("👤 Customer Profile", "AI customer analytics"),
        ("🗺️ Geospatial Analysis", "Geographic AI insights"),
        ("🔮 Predictive Analytics", "AI forecasting tools"),
        ("💬 AI Assistant", "Natural language interface"),
        ("🧪 Testing & Monitoring", "AI system health")
    ]
    
    for link, desc in quick_links[:5]:
        st.markdown(f"**{link}**")
        st.caption(desc)

# Main documentation content
if doc_section == "🚀 Getting Started":
    st.markdown("## 🚀 Getting Started with AI-Powered Telco Analytics")
    
    st.markdown("### Welcome to the AI-Enhanced Telco Network Optimization Suite")
    
    st.info("""
    This platform combines advanced telecommunications network analytics with cutting-edge AI capabilities 
    powered by **Snowflake Cortex AISQL**. Get intelligent insights, predictive analytics, and automated 
    recommendations to optimize your network performance and customer experience.
    """)
    
    # Quick start guide
    st.markdown("### 📋 Quick Start Guide")
    
    start_col1, start_col2 = st.columns(2)
    
    with start_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%); padding: 2rem; border-radius: 16px; border-left: 4px solid #2196f3;">
            <h4 style="color: #1565c0; margin: 0 0 1rem 0;">🎯 Step 1: Explore AI Insights</h4>
            <p style="margin: 0; color: #4a5568;">Navigate to the <strong>AI Insights & Recommendations</strong> page to get started with intelligent network analysis. Select your preferred AI model and generate comprehensive insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #ffffff 100%); padding: 2rem; border-radius: 16px; border-left: 4px solid #28a745; margin-top: 1rem;">
            <h4 style="color: #155724; margin: 0 0 1rem 0;">🔮 Step 2: Try Predictive Analytics</h4>
            <p style="margin: 0; color: #4a5568;">Use the <strong>Predictive Analytics</strong> page to forecast network issues, predict customer churn, and schedule proactive maintenance using AI models.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with start_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f3e5f5 0%, #ffffff 100%); padding: 2rem; border-radius: 16px; border-left: 4px solid #9c27b0;">
            <h4 style="color: #6a1b9a; margin: 0 0 1rem 0;">💬 Step 3: Use AI Assistant</h4>
            <p style="margin: 0; color: #4a5568;">Try the <strong>AI Network Assistant</strong> to ask questions in plain English like "Which towers need immediate attention?" or "What's causing high churn in California?"</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffffff 100%); padding: 2rem; border-radius: 16px; border-left: 4px solid #f57c00; margin-top: 1rem;">
            <h4 style="color: #e65100; margin: 0 0 1rem 0;">📊 Step 4: Monitor Performance</h4>
            <p style="margin: 0; color: #4a5568;">Check the <strong>AI Testing & Monitoring</strong> page to track AI performance, costs, and system health for optimal operation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key capabilities overview
    st.markdown("### 🌟 Key AI Capabilities")
    
    capabilities = [
        ("🧠 **Intelligent Analysis**", "AI-powered insights across all network data with confidence scoring"),
        ("🔮 **Predictive Forecasting**", "Network failure prediction, churn analysis, and capacity planning"),
        ("💬 **Natural Language Interface**", "Ask questions in plain English and get intelligent responses"),
        ("🎯 **Automated Recommendations**", "Strategic action items and optimization suggestions"),
        ("📊 **Executive Reporting**", "Automated executive summaries and business intelligence"),
        ("🗺️ **Geographic Intelligence**", "AI-powered geospatial analysis and pattern detection")
    ]
    
    cap_col1, cap_col2 = st.columns(2)
    
    for i, (title, desc) in enumerate(capabilities):
        with cap_col1 if i % 2 == 0 else cap_col2:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 1rem; border-left: 3px solid #4caf50;">
                <h5 style="color: #2e7d32; margin: 0 0 0.5rem 0;">{title}</h5>
                <p style="margin: 0; color: #555; line-height: 1.5;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

elif doc_section == "🤖 AI Features Overview":
    st.markdown("## 🤖 AI Features & Capabilities Overview")
    
    st.markdown("### Powered by Snowflake Cortex AISQL")
    
    st.success("""
    Our platform leverages **Snowflake Cortex AISQL** - a comprehensive suite of LLM-powered functions 
    that bring AI capabilities directly to your data. This includes advanced language models like 
    Claude 4 Sonnet, GPT-5, Mistral Large, Llama 4, and Snowflake Arctic for diverse analytical needs.
    """)
    
    # Feature breakdown by page
    features_data = [
        {
            "Page": "🏠 Main Dashboard",
            "AI Features": [
                "AI-powered executive summary generation",
                "Network pattern analysis with insights",
                "Real-time AI metrics dashboard",
                "Automated network health scoring"
            ]
        },
        {
            "Page": "🧠 AI Insights & Recommendations",
            "AI Features": [
                "Multi-model AI selection (Claude, GPT, Mistral, Llama, Arctic)",
                "Executive report generation",
                "Pattern detection and analysis",
                "Intelligent recommendation engine"
            ]
        },
        {
            "Page": "👤 Customer Profile",
            "AI Features": [
                "AI-powered churn prediction",
                "Intelligent ticket classification",
                "Sentiment analysis and insights",
                "Personalized retention strategies"
            ]
        },
        {
            "Page": "📡 Cell Tower Analysis", 
            "AI Features": [
                "Network infrastructure analysis",
                "AI-powered risk assessment",
                "Optimization strategy generation",
                "Predictive maintenance recommendations"
            ]
        },
        {
            "Page": "🗺️ Geospatial Analysis",
            "AI Features": [
                "Geographic pattern detection",
                "Predictive mapping and forecasting",
                "Coverage optimization recommendations",
                "Regional performance analysis"
            ]
        },
        {
            "Page": "📊 Correlation Analytics",
            "AI Features": [
                "AI-powered correlation discovery",
                "Statistical explanation generation",
                "Business impact analysis",
                "Optimization strategy recommendations"
            ]
        },
        {
            "Page": "🔮 Predictive Analytics",
            "AI Features": [
                "Network failure forecasting",
                "Anomaly detection with configurable sensitivity",
                "Predictive maintenance scheduling",
                "Customer behavior forecasting"
            ]
        },
        {
            "Page": "💬 AI Network Assistant",
            "AI Features": [
                "Natural language query processing",
                "Conversational AI interface",
                "Context-aware responses",
                "Interactive analysis suggestions"
            ]
        }
    ]
    
    for feature_group in features_data:
        with st.expander(f"{feature_group['Page']} - AI Capabilities", expanded=False):
            for feature in feature_group['AI Features']:
                st.markdown(f"✅ {feature}")

    # Technical AI capabilities
    st.markdown("### 🔧 Technical AI Capabilities")
    
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown("""
        #### 🧠 Core AI Functions
        - **AI_COMPLETE**: Text generation and completion
        - **AI_CLASSIFY**: Intelligent categorization
        - **AI_SENTIMENT**: Sentiment analysis
        - **AI_SUMMARIZE**: Content summarization
        - **AI_EXTRACT**: Information extraction
        - **AI_EMBED**: Semantic embeddings
        """)
    
    with tech_col2:
        st.markdown("""
        #### 🎯 Business Applications
        - **Executive Reporting**: Automated insights
        - **Predictive Maintenance**: Proactive scheduling
        - **Customer Analytics**: Churn and satisfaction
        - **Network Optimization**: Performance tuning
        - **Risk Assessment**: Vulnerability analysis
        - **Strategic Planning**: Data-driven decisions
        """)

elif doc_section == "🔧 Technical Reference":
    st.markdown("## 🔧 Technical Reference")
    
    st.markdown("### AI Model Configuration")
    
    model_data = pd.DataFrame([
        {
            "Model": "claude-4-sonnet",
            "Use Case": "DEFAULT: Balanced analysis, executive reporting",
            "Strengths": "Excellent reasoning, balanced speed & quality",
            "Typical Response Time": "1.5-2.5 seconds"
        },
        {
            "Model": "claude-4-opus",
            "Use Case": "Complex analysis, deep reasoning",
            "Strengths": "Maximum intelligence, highest accuracy",
            "Typical Response Time": "2-4 seconds"
        },
        {
            "Model": "openai-gpt-5",
            "Use Case": "Next-generation AI capabilities",
            "Strengths": "Cutting-edge performance",
            "Typical Response Time": "2-3 seconds"
        },
        {
            "Model": "mistral-large",
            "Use Case": "Open-source alternative, complex analysis",
            "Strengths": "High accuracy, detailed responses",
            "Typical Response Time": "2-3 seconds"
        },
        {
            "Model": "llama3.1-8b", 
            "Use Case": "Quick insights, classification",
            "Strengths": "Fast responses, efficient",
            "Typical Response Time": "1-2 seconds"
        },
        {
            "Model": "snowflake-arctic",
            "Use Case": "Data-specific analysis",
            "Strengths": "Optimized for Snowflake data",
            "Typical Response Time": "2-4 seconds"
        }
    ])
    
    st.dataframe(model_data, use_container_width=True)
    
    st.markdown("### API Functions Reference")
    
    api_functions = [
        {
            "Function": "ai_complete(prompt, max_tokens, temperature)",
            "Description": "Generate AI completions for analysis and insights",
            "Parameters": "prompt: str, max_tokens: int (default 500), temperature: float (default 0.7)",
            "Returns": "Generated text response"
        },
        {
            "Function": "ai_classify(text, categories)",
            "Description": "Classify text into predefined categories", 
            "Parameters": "text: str, categories: List[str]",
            "Returns": "Selected category"
        },
        {
            "Function": "ai_sentiment(text)",
            "Description": "Analyze sentiment of text content",
            "Parameters": "text: str",
            "Returns": "Float between -1 (negative) and 1 (positive)"
        }
    ]
    
    for func in api_functions:
        with st.expander(f"📋 {func['Function']}", expanded=False):
            st.markdown(f"**Description:** {func['Description']}")
            st.markdown(f"**Parameters:** `{func['Parameters']}`")
            st.markdown(f"**Returns:** {func['Returns']}")
    
    st.markdown("### Performance Optimization")
    
    st.markdown("""
    #### 🚀 Caching Strategy
    - **TTL Configuration**: 1 hour default cache time
    - **Cache Keys**: Based on prompt content and parameters
    - **Cache Hit Rate**: Target >80% for optimal performance
    
    #### ⚡ Response Time Optimization
    - **Model Selection**: Choose appropriate model for task complexity
    - **Token Limits**: Balance between detail and speed
    - **Batch Processing**: Group similar requests when possible
    
    #### 💰 Cost Optimization
    - **Smart Prompting**: Minimize unnecessary tokens
    - **Cache Utilization**: Leverage cached responses
    - **Model Routing**: Use efficient models for simple tasks
    """)

elif doc_section == "📊 Use Cases & Examples":
    st.markdown("## 📊 Use Cases & Examples")
    
    st.markdown("### Common Business Scenarios")
    
    use_cases = [
        {
            "scenario": "🚨 Network Performance Crisis",
            "description": "Multiple towers showing high failure rates",
            "ai_solution": "Use AI Network Assistant to ask 'What's causing high failure rates?' and get root cause analysis with specific recommendations.",
            "example_query": "Which towers have failure rates above 80% and what are the common factors?"
        },
        {
            "scenario": "📈 Executive Board Meeting",
            "description": "Need comprehensive network performance summary",
            "ai_solution": "Generate automated executive summary with key metrics, trends, and strategic recommendations.",
            "example_query": "Generate an executive summary of network performance for Q4 board presentation"
        },
        {
            "scenario": "👥 Customer Churn Investigation",
            "description": "Increased customer complaints in specific region",
            "ai_solution": "Use Customer Profile AI to identify churn patterns and generate retention strategies.",
            "example_query": "Analyze churn risk factors for customers in high-complaint regions"
        },
        {
            "scenario": "🔮 Budget Planning",
            "description": "Planning network investments for next year",
            "ai_solution": "Use Predictive Analytics to forecast capacity needs and maintenance requirements.",
            "example_query": "Predict network capacity requirements and maintenance costs for 2025"
        }
    ]
    
    for use_case in use_cases:
        with st.expander(f"{use_case['scenario']}: {use_case['description']}", expanded=False):
            st.markdown(f"**AI Solution:** {use_case['ai_solution']}")
            st.code(use_case['example_query'], language='text')
    
    st.markdown("### Sample AI Prompts")
    
    prompt_categories = {
        "Network Analysis": [
            "Analyze the correlation between cell tower failure rates and customer satisfaction",
            "Identify geographic patterns in network performance issues",
            "What are the top 5 optimization opportunities for our network?"
        ],
        "Customer Intelligence": [
            "Which customer segments have the highest churn risk and why?",
            "Generate personalized retention strategies for high-value at-risk customers",
            "Analyze customer sentiment trends by service type"
        ],
        "Predictive Insights": [
            "Predict which towers are likely to fail in the next 30 days",
            "Forecast customer support ticket volume for next quarter",
            "Identify early warning signs of network congestion"
        ],
        "Executive Reporting": [
            "Create a strategic overview of network performance and investment priorities",
            "Generate ROI analysis for proposed network upgrades",
            "Summarize key business risks and mitigation strategies"
        ]
    }
    
    for category, prompts in prompt_categories.items():
        st.markdown(f"#### {category}")
        for prompt in prompts:
            st.markdown(f"💡 _{prompt}_")

elif doc_section == "⚡ Best Practices":
    st.markdown("## ⚡ Best Practices for AI-Powered Analytics")
    
    best_practices = [
        {
            "category": "🎯 Effective Prompting",
            "practices": [
                "Be specific about what you want to analyze",
                "Include relevant context and constraints",
                "Ask follow-up questions to dive deeper",
                "Use business terminology familiar to your organization"
            ]
        },
        {
            "category": "🔄 Model Selection",
            "practices": [
                "Use claude-4-sonnet as default for balanced performance",
                "Use claude-4-opus for complex strategic analysis",
                "Choose llama3.1-8b for quick operational insights",  
                "Try different models to compare results",
                "Consider response time vs accuracy trade-offs"
            ]
        },
        {
            "category": "📊 Data Interpretation",
            "practices": [
                "Always consider confidence levels in AI responses",
                "Validate AI insights with domain expertise",
                "Use AI as a starting point for deeper investigation",
                "Combine AI insights with human judgment"
            ]
        },
        {
            "category": "💰 Cost Management",
            "practices": [
                "Leverage caching for repeated queries",
                "Monitor token usage and optimize prompts",
                "Use appropriate models for task complexity",
                "Set up cost alerts and budgets"
            ]
        }
    ]
    
    for practice_group in best_practices:
        st.markdown(f"### {practice_group['category']}")
        for practice in practice_group['practices']:
            st.markdown(f"✅ {practice}")
        st.markdown("---")
    
    st.markdown("### 🎓 Pro Tips")
    
    pro_tips = [
        "Start with broad questions, then narrow down based on initial insights",
        "Use the AI Assistant for exploratory analysis before diving into specific pages", 
        "Combine multiple AI features for comprehensive analysis",
        "Export and share AI insights with stakeholders for decision-making",
        "Regularly review AI performance metrics to optimize usage",
        "Keep prompts focused but provide sufficient context"
    ]
    
    for tip in pro_tips:
        st.info(f"💡 **Pro Tip:** {tip}")

elif doc_section == "🔧 Troubleshooting":
    st.markdown("## 🔧 Troubleshooting Guide")
    
    troubleshooting_items = [
        {
            "issue": "🚨 AI functions not responding",
            "cause": "Services may be initializing or experiencing temporary issues",
            "solution": "Wait 2-3 minutes and try again. Check AI Testing & Monitoring page for system status."
        },
        {
            "issue": "⏰ Slow response times", 
            "cause": "High load or complex queries",
            "solution": "Try using a faster model like llama3.1-8b or claude-3-5-sonnet, reduce max_tokens, or simplify your prompt."
        },
        {
            "issue": "📊 Incomplete or unclear responses",
            "cause": "Insufficient context or vague prompts",
            "solution": "Provide more specific context, business constraints, and clear questions in your prompts."
        },
        {
            "issue": "💰 Higher than expected costs",
            "cause": "High token usage or inefficient prompting",
            "solution": "Monitor usage in AI Testing page, optimize prompts, and leverage caching more effectively."
        },
        {
            "issue": "🔄 Cache not working effectively",
            "cause": "Prompt variations or cache configuration issues",
            "solution": "Use consistent prompt formats and check cache configuration in system optimization."
        }
    ]
    
    for item in troubleshooting_items:
        with st.expander(f"{item['issue']}", expanded=False):
            st.markdown(f"**Likely Cause:** {item['cause']}")
            st.markdown(f"**Solution:** {item['solution']}")
    
    st.markdown("### 📞 Getting Help")
    
    st.info("""
    **Need Additional Support?**
    
    1. **System Health**: Check the AI Testing & Monitoring page for real-time status
    2. **Performance Issues**: Review the cost and performance dashboard
    3. **Feature Questions**: Consult this documentation or try the AI Assistant
    4. **Technical Issues**: Contact your system administrator or AI platform support
    """)

elif doc_section == "❓ FAQ":
    st.markdown("## ❓ Frequently Asked Questions")
    
    faqs = [
        {
            "question": "What AI models are available and which should I use?",
            "answer": "We support Mistral Large, Llama 3.1 (8B, 70B, 405B), Snowflake Arctic, and others. Use Mistral Large for complex analysis, Llama 3.1-8b for quick insights, and Arctic for Snowflake-optimized tasks."
        },
        {
            "question": "How accurate are the AI predictions and insights?",
            "answer": "AI insights include confidence scores. Generally, predictions have 80-90% accuracy for well-defined scenarios. Always validate critical insights with domain expertise and historical data."
        },
        {
            "question": "Can I customize AI models for my specific network?",
            "answer": "The models adapt to your data context automatically. You can optimize performance through prompt engineering, model selection, and parameter tuning in the system optimization page."
        },
        {
            "question": "What data does the AI have access to?",
            "answer": "AI functions access cell tower performance data, customer support tickets, and network metrics from your Snowflake database. No external data is used without explicit configuration."
        },
        {
            "question": "How much do AI features cost to operate?",
            "answer": "Costs vary based on usage and model selection. Monitor costs in the AI Testing & Monitoring page. Typical enterprise usage ranges from $50-500/month depending on volume."
        },
        {
            "question": "Can I integrate AI insights with other business systems?",
            "answer": "Yes, you can export AI-generated reports and insights in various formats (JSON, CSV) for integration with BI tools, executive dashboards, and other business systems."
        },
        {
            "question": "Is my data secure when using AI features?",
            "answer": "Yes, all AI processing happens within your Snowflake environment. Data never leaves your security boundary, and all communications are encrypted."
        },
        {
            "question": "How do I optimize AI performance and reduce costs?",
            "answer": "Use caching effectively, choose appropriate models for task complexity, optimize prompt length, and monitor usage patterns. The optimization page provides specific recommendations."
        }
    ]
    
    for faq in faqs:
        with st.expander(f"❓ {faq['question']}", expanded=False):
            st.markdown(faq['answer'])

# Documentation metrics
st.markdown("---")
st.markdown("### 📊 Documentation Metrics")

doc_col1, doc_col2, doc_col3, doc_col4 = st.columns(4)

with doc_col1:
    st.metric("Documentation Sections", "7")

with doc_col2:
    st.metric("AI Features Documented", "50+")

with doc_col3:
    st.metric("Use Cases & Examples", "20+")

with doc_col4:
    st.metric("Last Updated", datetime.now().strftime("%Y-%m-%d"))

# Documentation feedback
st.markdown("### 💬 Documentation Feedback")

feedback_col1, feedback_col2 = st.columns(2)

with feedback_col1:
    if st.button("👍 This documentation was helpful", type="secondary"):
        st.success("Thank you for your feedback! We're glad the documentation was useful.")

with feedback_col2:
    if st.button("📝 Suggest improvements", type="secondary"):
        st.info("Thank you! Your feedback helps us improve the documentation for everyone.")

# Add professional footer
add_page_footer()
