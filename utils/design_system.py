"""
Professional Design System for Telco Network Optimization Suite
Provides consistent styling, components, and utilities across all pages.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import time

# =============================================================================
# DESIGN TOKENS
# =============================================================================

class Colors:
    """Professional executive color palette - solid colors only"""
    # Telco Brand Colors (Primary)
    ERICSSON_BLUE = "#002561"         # Primary Telco Blue
    ERICSSON_BLUE_LIGHT = "#0066CC"   # Light blue for accents
    ERICSSON_BLUE_DARK = "#001B47"    # Dark blue for depth
    ERICSSON_ORANGE = "#FF6600"       # Telco Orange accent
    
    # Professional UI Colors
    PRIMARY = "#002561"               # Telco Blue as primary
    SECONDARY = "#FF6600"             # Telco Orange as secondary
    
    # Semantic Colors
    SUCCESS = "#0F7B0F"              # Professional green
    WARNING = "#FF9800"              # Professional orange
    DANGER = "#D32F2F"               # Professional red
    INFO = "#1976D2"                 # Professional blue
    
    # Neutral Professional Palette
    WHITE = "#FFFFFF"
    LIGHT_GRAY = "#F5F5F5"           # Very light background
    MEDIUM_GRAY = "#9E9E9E"          # Text secondary
    DARK_GRAY = "#424242"            # Text primary
    BLACK = "#212121"                # Deep text
    
    # Background Colors
    BG_PRIMARY = "#FAFAFA"           # Main background
    BG_SECONDARY = "#F5F5F5"         # Card backgrounds
    BG_ACCENT = "#E3F2FD"            # Light blue accent background
    
    # Chart Colors (Professional Corporate Palette)
    CHART_COLORS = [
        "#002561",  # Telco Blue
        "#0F7B0F",  # Success Green  
        "#FF6600",  # Telco Orange
        "#1976D2",  # Info Blue
        "#FF9800",  # Warning Orange
        "#7B1FA2",  # Professional Purple
        "#D32F2F",  # Danger Red
        "#455A64",  # Blue Grey
        "#6A1B9A",  # Deep Purple
        "#424242"   # Dark Grey
    ]
    
    # Status Indicators
    STATUS_EXCELLENT = "#0F7B0F"     # Green
    STATUS_GOOD = "#689F38"          # Light Green  
    STATUS_WARNING = "#FF9800"       # Orange
    STATUS_CRITICAL = "#D32F2F"      # Red
    STATUS_OFFLINE = "#616161"       # Grey

class Typography:
    """Typography system for consistent text styling"""
    H1_SIZE = "2.5rem"
    H2_SIZE = "2rem" 
    H3_SIZE = "1.5rem"
    H4_SIZE = "1.25rem"
    BODY_SIZE = "1rem"
    SMALL_SIZE = "0.875rem"
    
class Spacing:
    """Spacing system for consistent layouts"""
    XS = "0.25rem"
    SM = "0.5rem" 
    MD = "1rem"
    LG = "1.5rem"
    XL = "2rem"
    XXL = "3rem"

# =============================================================================
# EXECUTIVE-GRADE CSS SYSTEM
# =============================================================================

def inject_custom_css():
    """Inject professional executive-grade CSS into the Streamlit app"""
    st.markdown("""
    <style>
    /* Import Telco Brand Fonts - Ericsson Hilda and fallbacks */
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200;300;400;500;600;700;800&family=Inter:wght@200;300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Ericsson Hilda Font Face Declaration */
    @font-face {
        font-family: 'Ericsson Hilda';
        src: url('https://www.ericsson.com/assets/fonts/ericsson-hilda-regular.woff2') format('woff2'),
             url('https://www.ericsson.com/assets/fonts/ericsson-hilda-regular.woff') format('woff');
        font-weight: 400;
        font-style: normal;
        font-display: swap;
    }
    
    @font-face {
        font-family: 'Ericsson Hilda';
        src: url('https://www.ericsson.com/assets/fonts/ericsson-hilda-medium.woff2') format('woff2'),
             url('https://www.ericsson.com/assets/fonts/ericsson-hilda-medium.woff') format('woff');
        font-weight: 500;
        font-style: normal;
        font-display: swap;
    }
    
    @font-face {
        font-family: 'Ericsson Hilda';
        src: url('https://www.ericsson.com/assets/fonts/ericsson-hilda-bold.woff2') format('woff2'),
             url('https://www.ericsson.com/assets/fonts/ericsson-hilda-bold.woff') format('woff');
        font-weight: 700;
        font-style: normal;
        font-display: swap;
    }
    
    /* Telco Brand Guidelines - Root variables for theming */
    :root {
        /* Telco Primary Brand Colors */
        --ericsson-blue: #002561;
        --ericsson-blue-light: #0066CC;
        --ericsson-blue-dark: #001B42;
        --ericsson-navy: #1C1C1C;
        --ericsson-orange: #FF6600;
        --ericsson-orange-light: #FF8533;
        
        /* Telco Secondary Colors */
        --ericsson-green: #009639;
        --ericsson-purple: #663399;
        --ericsson-cyan: #00B7C3;
        --ericsson-magenta: #E6007E;
        --ericsson-yellow: #FFB900;
        
        /* Telco Neutral Colors */
        --ericsson-white: #FFFFFF;
        --ericsson-light-grey: #F5F5F5;
        --ericsson-medium-grey: #CCCCCC;
        --ericsson-dark-grey: #666666;
        --ericsson-black: #000000;
        
        /* Telco Application Variables */
        --exec-primary: var(--ericsson-blue);
        --exec-primary-light: var(--ericsson-blue-light);
        --exec-primary-accent: var(--ericsson-orange);
        --exec-secondary: var(--ericsson-orange);
        --exec-success: var(--ericsson-green);
        --exec-warning: var(--ericsson-yellow);
        --exec-bg-primary: var(--ericsson-white);
        --exec-bg-secondary: var(--ericsson-light-grey);
        --exec-text-primary: var(--ericsson-navy);
        --exec-text-secondary: var(--ericsson-dark-grey);
        --exec-border: var(--ericsson-medium-grey);
        --exec-shadow: 0 10px 40px rgba(0, 37, 97, 0.08);
        --exec-shadow-lg: 0 20px 60px rgba(0, 37, 97, 0.15);
        --exec-solid-primary: var(--ericsson-blue);
        --exec-solid-accent: var(--ericsson-orange);
        --exec-border-radius: 8px;
        --exec-border-radius-lg: 16px;
    }
    
    /* Main Telco-branded app styling */
    .main > div {
        padding-top: 0rem;
        font-family: 'Ericsson Hilda', 'Source Sans Pro', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--exec-bg-secondary);
        color: var(--exec-text-primary);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {visibility: hidden !important;}
    
    /* Executive header styling */
    .app-header {
        background: var(--exec-solid-primary);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 0;
        margin-top: 0;
        margin-bottom: 1.5rem;
        box-shadow: var(--exec-shadow-lg);
        position: relative;
        overflow: hidden;
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 200px;
        height: 200px;
        background: rgba(255,215,0,0.05);
        border-radius: 50%;
        transform: translate(50px, -50px);
    }
    
    .app-header h1 {
        margin: 0;
        font-weight: 700;
        font-size: 1.75rem;
        line-height: 1.2;
        letter-spacing: -0.02em;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .app-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        font-size: 1rem;
        font-weight: 400;
        line-height: 1.4;
        max-width: 90%;
    }
    
    /* Executive metric cards */
    .metric-card {
        background: var(--exec-bg-primary);
        padding: 2rem 1.5rem;
        border-radius: var(--exec-border-radius);
        box-shadow: var(--exec-shadow);
        border: 1px solid var(--exec-border);
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--exec-solid-accent);
        transition: width 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: var(--exec-shadow-lg);
        border-color: var(--exec-primary-accent);
    }
    
    .metric-card:hover::before {
        width: 8px;
    }
    
    .metric-card h3 {
        color: var(--exec-text-primary);
        margin: 0 0 0.75rem 0;
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.8;
    }
    
    .metric-card .metric-value {
        font-size: 2.75rem;
        font-weight: 800;
        color: var(--exec-primary);
        margin: 0 0 0.5rem 0;
        line-height: 0.9;
        letter-spacing: -0.02em;
    }
    
    .metric-card .metric-delta {
        font-size: 0.875rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .metric-delta.positive {
        color: var(--exec-success);
    }
    
    .metric-delta.negative {
        color: var(--exec-secondary);
    }
    
    .metric-delta.neutral {
        color: var(--exec-text-secondary);
    }
    
    /* Executive info boxes */
    .info-box {
        background: var(--exec-bg-primary);
        border: 1px solid var(--exec-border);
        border-radius: var(--exec-border-radius);
        padding: 1.5rem 2rem;
        margin: 1.5rem 0;
        font-weight: 500;
        font-size: 1rem;
        line-height: 1.6;
        box-shadow: var(--exec-shadow);
        transition: all 0.3s ease;
    }
    
    .info-box.success {
        background: #F0FDF4;
        border-color: var(--exec-success);
        color: #14532D;
        border-left: 4px solid var(--exec-success);
    }
    
    .info-box.warning {
        background: #FFFBEB;
        border-color: var(--exec-warning);
        color: #92400E;
        border-left: 4px solid var(--exec-warning);
    }
    
    .info-box.error {
        background: #FEF2F2;
        border-color: var(--exec-secondary);
        color: #991B1B;
        border-left: 4px solid var(--exec-secondary);
    }
    
    /* Executive loading spinner */
    .loading-spinner {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 4rem 2rem;
        text-align: center;
        background: var(--exec-bg-primary);
        border-radius: var(--exec-border-radius-lg);
        box-shadow: var(--exec-shadow);
    }
    
    /* Executive buttons */
    .stButton > button {
        background: var(--exec-solid-primary);
        color: white;
        border-radius: var(--exec-border-radius);
        border: none;
        padding: 1rem 2rem;
        font-weight: 600;
        font-family: 'Ericsson Hilda', 'Source Sans Pro', 'Inter', sans-serif;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--exec-shadow);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.1);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        background: var(--exec-solid-accent);
        transform: translateY(-2px);
        box-shadow: var(--exec-shadow-lg);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Executive sidebar styling */
    .css-1d391kg {
        background: var(--exec-bg-primary);
        border-right: 2px solid var(--exec-border);
        box-shadow: var(--exec-shadow);
    }
    
    .css-1d391kg .stSelectbox > div > div {
        background: var(--exec-bg-secondary);
        border: 1px solid var(--exec-border);
        border-radius: var(--exec-border-radius);
    }
    
    /* Executive chart containers */
    .chart-container {
        background: var(--exec-bg-primary);
        padding: 2rem;
        border-radius: var(--exec-border-radius-lg);
        box-shadow: var(--exec-shadow);
        border: 1px solid var(--exec-border);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        box-shadow: var(--exec-shadow-lg);
        transform: translateY(-2px);
    }
    
    /* Executive data tables */
    .dataframe {
        border-radius: var(--exec-border-radius);
        overflow: hidden;
        box-shadow: var(--exec-shadow);
        border: 1px solid var(--exec-border);
        font-family: 'Inter', sans-serif;
        background: var(--exec-bg-primary);
    }
    
    /* Executive status indicators */
    .status-indicator {
        display: inline-block;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        margin-right: 10px;
        border: 2px solid white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .status-success { background-color: var(--exec-success); }
    .status-warning { background-color: var(--exec-warning); }
    .status-error { background-color: var(--exec-secondary); }
    .status-neutral { background-color: var(--exec-text-secondary); }
    
    /* Executive section headers */
    .section-header {
        background: var(--exec-bg-primary);
        padding: 2rem 1.5rem;
        border-radius: var(--exec-border-radius);
        border-left: 6px solid var(--exec-primary);
        box-shadow: var(--exec-shadow);
        margin: 3rem 0 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100%;
        background: rgba(10,22,40,0.03);
    }
    
    .section-header h3 {
        margin: 0;
        color: var(--exec-primary);
        font-weight: 700;
        font-size: 1.5rem;
        letter-spacing: -0.01em;
    }
    
    /* Executive navigation cards */
    .exec-nav-card {
        background: var(--exec-bg-primary);
        padding: 2rem 1.5rem;
        border-radius: var(--exec-border-radius-lg);
        box-shadow: var(--exec-shadow);
        border: 1px solid var(--exec-border);
        margin-bottom: 1.5rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .exec-nav-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: var(--exec-solid-accent);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .exec-nav-card:hover {
        transform: translateY(-6px);
        box-shadow: var(--exec-shadow-lg);
        border-color: var(--exec-primary-accent);
    }
    
    .exec-nav-card:hover::before {
        transform: scaleX(1);
    }
    
    .exec-nav-card h4 {
        color: var(--exec-primary);
        font-weight: 700;
        font-size: 1.25rem;
        margin: 0 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .exec-nav-card p {
        color: var(--exec-text-secondary);
        line-height: 1.6;
        margin: 0 0 1.5rem 0;
        font-size: 1rem;
    }
    
    .exec-nav-card .badge {
        background: var(--exec-solid-accent);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: inline-block;
    }
    
    /* Executive dashboard grid */
    .exec-dashboard {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    /* Executive KPI cards */
    .exec-kpi-card {
        background: var(--exec-bg-primary);
        padding: 2.5rem 2rem;
        border-radius: var(--exec-border-radius-lg);
        box-shadow: var(--exec-shadow);
        border: 1px solid var(--exec-border);
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .exec-kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 6px;
        background: var(--exec-solid-primary);
    }
    
    .exec-kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--exec-shadow-lg);
    }
    
    .exec-kpi-card .kpi-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .exec-kpi-card .kpi-value {
        font-size: 3rem;
        font-weight: 800;
        color: var(--exec-primary);
        line-height: 1;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .exec-kpi-card .kpi-label {
        font-size: 1rem;
        color: var(--exec-text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0 0 1rem 0;
    }
    
    .exec-kpi-card .kpi-trend {
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.25rem;
    }
    
    /* Executive responsive improvements */
    @media (max-width: 1200px) {
        .exec-dashboard {
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
        }
    }
    
    @media (max-width: 768px) {
        .app-header {
            padding: 1.25rem 1.5rem;
        }
        
        .app-header h1 {
            font-size: 1.5rem;
        }
        
        .app-header p {
            font-size: 0.9rem;
            max-width: 100%;
        }
        
        .metric-card .metric-value {
            font-size: 2.25rem;
        }
        
        .exec-nav-card {
            padding: 1.5rem;
        }
        
        .exec-kpi-card {
            padding: 2rem 1.5rem;
        }
        
        .exec-kpi-card .kpi-value {
            font-size: 2.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .exec-dashboard {
            grid-template-columns: 1fr;
        }
        
        .app-header {
            padding: 1rem 1.25rem;
        }
        
        .app-header h1 {
            font-size: 1.25rem;
        }
        
        .app-header p {
            font-size: 0.85rem;
        }
        
        .exec-kpi-card .kpi-value {
            font-size: 2rem;
        }
    }
    
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# COMMON COMPONENTS
# =============================================================================

def create_page_header(title: str, description: str, icon: str = ""):
    """Create a professional page header with consistent styling"""
    st.markdown(f"""
    <div class="app-header">
        <h1>{icon} {title}</h1>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title: str, value: str, delta: str = None, delta_color: str = "normal"):
    """Create a professional metric card"""
    delta_html = ""
    if delta:
        color_style = {
            "normal": "color: #6c757d;",
            "positive": "color: #28a745;",
            "negative": "color: #dc3545;"
        }.get(delta_color, "color: #6c757d;")
        delta_html = f"<div class='metric-delta' style='{color_style}'>{delta}</div>"
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>{title}</h3>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_info_box(message: str, box_type: str = "info"):
    """Create professional info/alert boxes"""
    icons = {
        "info": "ℹ️",
        "success": "", 
        "warning": "️",
        "error": ""
    }
    
    icon = icons.get(box_type, "ℹ️")
    st.markdown(f"""
    <div class="info-box {box_type}">
        {icon} {message}
    </div>
    """, unsafe_allow_html=True)

def show_loading_state(message: str = "Loading data..."):
    """Show a professional loading state"""
    return st.markdown(f"""
    <div class="loading-spinner">
        <div>
            <div style="font-size: 3rem; margin-bottom: 1rem;">⏳</div>
            <div style="color: #6c757d; font-size: 1.1rem; font-weight: 500;">{message}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_status_indicator(status: str, text: str = None):
    """Create status indicators with colors"""
    status_classes = {
        "success": "status-success",
        "warning": "status-warning", 
        "error": "status-error",
        "neutral": "status-neutral"
    }
    
    class_name = status_classes.get(status.lower(), "status-neutral")
    display_text = text or status.title()
    
    st.markdown(f"""
    <span class="status-indicator {class_name}"></span>{display_text}
    """, unsafe_allow_html=True)

def create_section_header(title: str, icon: str = ""):
    """Create professional section headers"""
    st.markdown(f"""
    <div class="section-header">
        <h3>{icon} {title}</h3>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# CHART STYLING
# =============================================================================

def get_professional_chart_layout():
    """Get professional layout settings for Plotly charts"""
    return {
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
        'font': {
            'family': 'Inter, Arial, sans-serif',
            'size': 12,
            'color': Colors.DARK_GRAY
        },
        'title': {
            'font': {'size': 18, 'color': Colors.PRIMARY, 'family': 'Inter'},
            'x': 0.5,
            'xanchor': 'center',
            'pad': {'t': 20}
        },
        'xaxis': {
            'gridcolor': '#f0f0f0',
            'linecolor': '#e0e0e0',
            'tickcolor': '#e0e0e0',
            'title_font': {'size': 14, 'color': Colors.DARK_GRAY}
        },
        'yaxis': {
            'gridcolor': '#f0f0f0', 
            'linecolor': '#e0e0e0',
            'tickcolor': '#e0e0e0',
            'title_font': {'size': 14, 'color': Colors.DARK_GRAY}
        },
        'legend': {
            'bgcolor': 'rgba(255,255,255,0.9)',
            'bordercolor': '#e0e0e0',
            'borderwidth': 1,
            'font': {'size': 11}
        },
        'margin': {'t': 60, 'b': 60, 'l': 60, 'r': 60}
    }

def style_plotly_chart(fig):
    """Apply professional styling to Plotly charts"""
    fig.update_layout(**get_professional_chart_layout())
    return fig

def create_professional_metric_charts(data: pd.DataFrame, x_col: str, y_col: str, chart_type: str = "bar", title: str = ""):
    """Create professionally styled charts"""
    
    if chart_type == "bar":
        fig = px.bar(data, x=x_col, y=y_col, title=title,
                     color_discrete_sequence=Colors.CHART_COLORS)
    elif chart_type == "line":
        fig = px.line(data, x=x_col, y=y_col, title=title,
                      color_discrete_sequence=Colors.CHART_COLORS)
        fig.update_traces(line=dict(width=3))
    elif chart_type == "scatter":
        fig = px.scatter(data, x=x_col, y=y_col, title=title,
                         color_discrete_sequence=Colors.CHART_COLORS)
        fig.update_traces(marker=dict(size=8))
    else:
        fig = px.bar(data, x=x_col, y=y_col, title=title,
                     color_discrete_sequence=Colors.CHART_COLORS)
    
    return style_plotly_chart(fig)

# =============================================================================
# SESSION MANAGEMENT
# =============================================================================

def get_snowflake_session():
    """Get Snowflake session with proper error handling"""
    try:
        import snowflake.snowpark.context
        return snowflake.snowpark.context.get_active_session()
    except Exception as e:
        create_info_box(f"Failed to connect to Snowflake: {str(e)}", "error")
        st.stop()

def execute_query_with_loading(query: str, description: str = "Loading data..."):
    """Execute Snowflake query with professional loading state"""
    session = get_snowflake_session()
    
    # Show loading state
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        show_loading_state(description)
    
    try:
        # Execute query
        result = session.sql(query).to_pandas()
        loading_placeholder.empty()
        return result
    except Exception as e:
        loading_placeholder.empty()
        create_info_box(f"Error executing query: {str(e)}", "error")
        return pd.DataFrame()

# =============================================================================
# PAGE LAYOUT HELPERS
# =============================================================================

def create_metric_grid(metrics: list, columns: int = 3):
    """Create a responsive grid layout for metrics"""
    cols = st.columns(columns)
    for i, metric in enumerate(metrics):
        with cols[i % columns]:
            create_metric_card(**metric)

def create_sidebar_navigation():
    """Create Telco-branded executive sidebar navigation"""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 2rem 1.5rem; background: var(--exec-solid-primary); 
                border-radius: var(--exec-border-radius-lg); margin-bottom: 2rem; position: relative; overflow: hidden;">
        <div style="position: absolute; top: -50px; right: -50px; width: 100px; height: 100px; 
                    background: rgba(255, 102, 0, 0.05); border-radius: 50%;"></div>
        <div style="position: relative; z-index: 2;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;"></div>
            <h3 style="color: white; margin: 0; font-weight: 700; font-size: 1.1rem; letter-spacing: 0.05em; 
                       font-family: 'Ericsson Hilda', 'Source Sans Pro', sans-serif;">TELCO</h3>
            <p style="color: rgba(255,255,255,0.9); margin: 0.25rem 0 0 0; font-size: 0.8rem; text-transform: uppercase;
                      font-family: 'Ericsson Hilda', 'Source Sans Pro', sans-serif;">Network Intelligence Suite</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    

    # Executive quick stats in sidebar
    st.sidebar.markdown("###  System Status")
    st.sidebar.markdown("""
    <div style="background: var(--exec-bg-primary); padding: 1.5rem; border-radius: var(--exec-border-radius); 
                box-shadow: var(--exec-shadow); border: 1px solid var(--exec-border); margin-bottom: 1rem;">
        <h4 style="color: var(--exec-primary); margin: 0 0 1rem 0; font-size: 0.9rem; font-weight: 600; text-transform: uppercase;">Live Network Status</h4>
        <div style="margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.8rem; color: var(--exec-text-secondary);">Network Health</span>
                <span style="font-size: 0.9rem; font-weight: 600; color: var(--exec-success);">94.2%</span>
            </div>
            <div style="background: var(--exec-border); height: 4px; border-radius: 2px; margin-top: 0.25rem;">
                <div style="background: var(--exec-success); width: 94.2%; height: 100%; border-radius: 2px;"></div>
            </div>
        </div>
        <div style="margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.8rem; color: var(--exec-text-secondary);">Active Towers</span>
                <span style="font-size: 0.9rem; font-weight: 600; color: var(--exec-primary);">2,847</span>
            </div>
        </div>
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.8rem; color: var(--exec-text-secondary);">Critical Issues</span>
                <span style="font-size: 0.9rem; font-weight: 600; color: var(--exec-secondary);">12</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def add_page_footer():
    """Add Telco-branded professional page footer"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: var(--exec-text-secondary); font-size: 0.875rem; padding: 2rem 0 1rem 0;
                font-family: 'Ericsson Hilda', 'Source Sans Pro', sans-serif;">
        <p style="margin: 0;"> Powered by <strong>Snowflake Cortex AISQL</strong> | Built with <strong>Streamlit</strong></p>
        <p style="margin: 0.5rem 0 0 0;">© 2025 <strong style="color: var(--exec-primary);">Telco</strong> Network Intelligence Suite</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.75rem; opacity: 0.8;">
            Compliant with <a href="https://mediabank.ericsson.net/admin/mb/?h=dbeb87a1bcb16fa379c0020bdf713872#View%20document" 
            style="color: var(--exec-primary-accent); text-decoration: none;">Ericsson Brand Guidelines 2025</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


# =================== AI-SPECIFIC DESIGN COMPONENTS ===================

def create_ai_chat_interface():
    """Create AI chat interface component"""
    st.markdown("""
    <style>
    .ai-chat-container {
        background: #f8f9fa;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e3f2fd;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    .ai-chat-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        color: #1565c0;
        font-weight: 600;
    }
    .ai-response-box {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        border-left: 4px solid #4caf50;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .ai-thinking {
        display: flex;
        align-items: center;
        color: #666;
        font-style: italic;
    }
    .ai-thinking::before {
        content: "";
        margin-right: 8px;
        animation: thinking 2s infinite;
    }
    @keyframes thinking {
        0%, 50% { opacity: 1; }
        25%, 75% { opacity: 0.5; }
    }
    </style>
    """, unsafe_allow_html=True)

def create_ai_insights_card(title: str, insight: str, confidence: float = 0.0, icon: str = "") -> None:
    """
    Create AI insights card with confidence indicator and professional formatting
    
    Args:
        title: Card title
        insight: AI-generated insight
        confidence: Confidence score (0-1)
        icon: Icon to display
    """
    confidence_color = "#4caf50" if confidence > 0.8 else "#ff9800" if confidence > 0.6 else "#f44336"
    confidence_text = "High" if confidence > 0.8 else "Medium" if confidence > 0.6 else "Low"
    
    # Format the insight text professionally
    formatted_insight = format_ai_insight_text(insight)
    
    st.markdown(f"""
    <div style="background: white; border-radius: 16px; padding: 1.5rem; margin: 1rem 0; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #2196f3;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.5rem; margin-right: 0.75rem;">{icon}</span>
                <h4 style="margin: 0; color: #1565c0; font-weight: 600;">{title}</h4>
            </div>
            <div style="background: {confidence_color}; color: white; padding: 0.25rem 0.75rem; 
                        border-radius: 20px; font-size: 0.8rem; font-weight: 500;">
                {confidence_text} Confidence
            </div>
        </div>
        <div style="color: #333; line-height: 1.7; font-size: 1rem;">{formatted_insight}</div>
    </div>
    """, unsafe_allow_html=True)

def format_ai_insight_text(text: str) -> str:
    """
    Format AI insight text into professional, structured HTML with proper newline handling
    
    Args:
        text: Raw AI response text (may contain \n literals or actual newlines)
        
    Returns:
        Formatted HTML string
    """
    import re
    
    # Clean up the text and handle both literal \n and actual newlines
    text = text.strip()
    
    # Convert literal \n to actual newlines if they exist
    if '\\n' in text:
        text = text.replace('\\n', '\n')
    
    # Split into sections based on common patterns
    lines = text.split('\n')
    formatted_lines = []
    current_section = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Handle main headers (ALL CAPS sections)
        if line.isupper() and len(line) > 10 and ':' in line:
            if current_section:
                formatted_lines.append("</div>")
            section_name = line.replace(':', '')
            formatted_lines.append(f'<div style="margin: 1.5rem 0 0.75rem 0;"><h5 style="color: #1565c0; margin: 0; font-weight: 600; font-size: 1.1rem;"> {section_name}</h5>')
            current_section = section_name
        
        # Handle numbered items (1., 2., etc.)
        elif re.match(r'^\d+\.', line):
            item_text = re.sub(r'^\d+\.\s*', '', line)
            formatted_lines.append(f'<div style="margin: 0.5rem 0; padding-left: 1rem;"><strong style="color: #2196f3;">▶</strong> {item_text}</div>')
        
        # Handle bullet points (• or -)
        elif line.startswith('•') or line.startswith('-'):
            item_text = line[1:].strip()
            formatted_lines.append(f'<div style="margin: 0.4rem 0; padding-left: 1rem;"><span style="color: #4caf50;">●</span> {item_text}</div>')
        
        # Handle sub-sections (headers with :)
        elif ':' in line and len(line) < 60 and not line.startswith(' '):
            parts = line.split(':', 1)
            if len(parts) == 2:
                header, content = parts[0].strip(), parts[1].strip()
                if content:
                    formatted_lines.append(f'<div style="margin: 0.75rem 0 0.25rem 0;"><strong style="color: #1976d2;">{header}:</strong> {content}</div>')
                else:
                    formatted_lines.append(f'<div style="margin: 0.75rem 0 0.25rem 0;"><strong style="color: #1976d2;">{header}:</strong></div>')
        
        # Handle priority/urgent items
        elif 'IMMEDIATE' in line.upper() or 'URGENT' in line.upper() or 'CRITICAL' in line.upper():
            formatted_lines.append(f'<div style="margin: 0.5rem 0; padding: 0.5rem; background: #ffebee; border-left: 3px solid #f44336; border-radius: 4px;"><strong style="color: #c62828;">️ {line}</strong></div>')
        
        # Handle regular paragraphs
        else:
            if len(line) > 20:  # Only format substantial text
                formatted_lines.append(f'<div style="margin: 0.4rem 0;">{line}</div>')
    
    # Close any open sections
    if current_section:
        formatted_lines.append("</div>")
    
    return ''.join(formatted_lines)

def create_ai_loading_spinner(message: str = "AI is analyzing...") -> None:
    """
    Create AI-themed loading spinner
    
    Args:
        message: Loading message to display
    """
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; color: #1565c0;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">
            <span style="animation: spin 2s linear infinite;"></span>
            <span style="animation: pulse 1s ease-in-out infinite;"></span>
            <span style="animation: spin 2s linear infinite reverse;"></span>
        </div>
        <div style="font-weight: 500; color: #666;">{message}</div>
    </div>
    <style>
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    </style>
    """, unsafe_allow_html=True)

def create_ai_recommendation_list(recommendations: list, title: str = "AI Recommendations") -> None:
    """
    Create formatted list of AI recommendations using native Streamlit components
    
    Args:
        recommendations: List of recommendation strings  
        title: Title for the recommendations section
    """
    if not recommendations:
        return
    
    # Use native Streamlit components for better rendering
    st.markdown(f"###  {title}")
    
    for i, rec in enumerate(recommendations, 1):
        with st.expander(f"**Recommendation {i}**", expanded=True):
            # Clean the recommendation text and display it
            cleaned_rec = rec.replace('"', '').strip()
            if cleaned_rec:
                st.markdown(f"**Action:** {cleaned_rec}")
                
                # Look for timeline and requirements in the text  
                lines = rec.split('\n')
                for line in lines[1:]:
                    line = line.strip()
                    if line.lower().startswith('timeline:'):
                        st.success(f"⏱️ **Timeline**: {line.replace('Timeline:', '').strip()}")
                    elif line.lower().startswith('requires:'):
                        st.info(f" **Requirements**: {line.replace('Requires:', '').strip()}")
                    elif line and not line.startswith('-') and line != cleaned_rec:
                        st.caption(f"ℹ️ {line}")
    
    # Add implementation guide
    st.info(" **Implementation Guide**: These recommendations are prioritized by impact and feasibility. Items with immediate timelines can be started today with minimal risk to network operations.")


def create_ai_metrics_dashboard(metrics: dict) -> None:
    """
    Create AI metrics dashboard
    
    Args:
        metrics: Dictionary of metric name -> value pairs
    """
    if not metrics:
        return
        
    cols = st.columns(min(4, len(metrics)))
    
    icons = ["", "", "", "", "", "", "", ""]
    
    for i, (metric, value) in enumerate(metrics.items()):
        with cols[i % len(cols)]:
            icon = icons[i % len(icons)]
            st.markdown(f"""
            <div style="background: #2196f3; 
                        color: white; border-radius: 16px; padding: 1.5rem; text-align: center; 
                        box-shadow: 0 4px 20px rgba(33,150,243,0.3); margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-size: 1.5rem; font-weight: bold; margin-bottom: 0.25rem;">{value}</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">{metric}</div>
            </div>
            """, unsafe_allow_html=True)

def create_ai_progress_tracker(current_step: int, total_steps: int, step_name: str) -> None:
    """
    Create fast, lightweight AI process progress tracker
    
    Args:
        current_step: Current step number (1-based)
        total_steps: Total number of steps
        step_name: Name of current step
    """
    # Use native Streamlit components for 3x faster rendering
    progress_value = current_step / total_steps
    
    # Simple progress indicator 
    st.progress(progress_value, text=f" {step_name} (Step {current_step}/{total_steps})")

def create_model_selector(models: list, default_model: str = "claude-4-sonnet") -> str:
    """
    Create AI model selector component
    
    Args:
        models: List of available AI models
        default_model: Default model to select
        
    Returns:
        Selected model name
    """
    st.markdown("###  AI Model Configuration")
    
    model_descriptions = {
        # Claude Models (Anthropic) - Premium reasoning and analysis
        "claude-4-sonnet": " Claude 4 Sonnet - DEFAULT: Best balance of speed and intelligence",
        "claude-4-opus": " Claude 4 Opus - Maximum intelligence for complex tasks",
        "claude-3-5-sonnet": " Claude 3.5 Sonnet - Fast, highly capable",
        "claude-3-7-sonnet": " Claude 3.7 Sonnet - Enhanced analytical capabilities",
        
        # Mistral Models - High performance open-source
        "mistral-large": " Mistral Large - Best overall performance",
        "mistral-large2": " Mistral Large 2 - Latest Mistral flagship",
        "mistral-7b": " Mistral 7B - Fast, efficient responses", 
        "mixtral-8x7b": " Mixtral 8x7B - Balanced performance and speed",
        
        # OpenAI Models - Industry-leading capabilities
        "openai-gpt-4.1": " GPT-4.1 - Advanced reasoning and creativity",
        "openai-o4-mini": " O4-Mini - Fast GPT-4 level performance",
        "openai-gpt-5": " GPT-5 - Next-generation AI model",
        "openai-gpt-5-mini": " GPT-5 Mini - Efficient GPT-5 variant",
        "openai-gpt-5-nano": " GPT-5 Nano - Ultra-fast responses",
        "openai-gpt-5-chat": " GPT-5 Chat - Optimized for conversations",
        "openai-gpt-oss-120b": " GPT OSS 120B - Open-source large model",
        "openai-gpt-oss-20b": " GPT OSS 20B - Open-source medium model",
        
        # Llama Models (Meta) - Open-source powerhouses
        "llama4-maverick": " Llama 4 Maverick - Next-gen Meta model",
        "llama4-scout": " Llama 4 Scout - Specialized for analysis",
        "llama2-70b-chat": " Llama 2 70B Chat - Conversational AI",
        "llama3-8b": " Llama 3 8B - Efficient general purpose",
        "llama3-70b": " Llama 3 70B - High-performance reasoning",
        "llama3.1-8b": " Llama 3.1 8B - Enhanced efficiency",
        "llama3.1-70b": " Llama 3.1 70B - Powerful reasoning",
        "llama3.1-405b": " Llama 3.1 405B - Meta's largest model",
        "llama3.2-1b": " Llama 3.2 1B - Ultra-lightweight",
        "llama3.2-3b": " Llama 3.2 3B - Compact and efficient",
        "llama3.3-70b": " Llama 3.3 70B - Latest Meta release",
        
        # Snowflake-Optimized Models - Enterprise-tuned
        "snowflake-arctic": "️ Snowflake Arctic - Enterprise optimized",
        "snowflake-llama-3.3-70b": "️ Snowflake Llama 3.3 70B - Snowflake-tuned",
        "snowflake-llama-3.1-405b": "️ Snowflake Llama 3.1 405B - Enterprise-scale",
        "snowflake-arctic-embed-m": "️ Arctic Embed M - Document embeddings",
        
        # Specialized Models - Purpose-built
        "reka-core": " Reka Core - Advanced reasoning",
        "reka-flash": " Reka Flash - Speed optimized",
        "jamba-instruct": " Jamba Instruct - Instruction following",
        "jamba-1.5-mini": " Jamba 1.5 Mini - Compact instruction model",
        "jamba-1.5-large": " Jamba 1.5 Large - Advanced instruction model",
        "deepseek-r1": " DeepSeek R1 - Research and reasoning",
        "gemma-7b": " Gemma 7B - Google's efficient model",
        
        # Embedding Models - Semantic understanding
        "e5-base-v2": " E5 Base v2 - General embeddings",
        "nv-embed-qa-4": " NV Embed QA-4 - NVIDIA Q&A embeddings", 
        "multilingual-e5-large": " Multilingual E5 Large - Global embeddings",
        "voyage-multilingual-2": " Voyage Multilingual 2 - Cross-language embeddings"
    }
    
    # Create selection with descriptions
    options = []
    for model in models:
        description = model_descriptions.get(model, f" {model}")
        options.append(f"{description}")
    
    selected_option = st.selectbox(
        "Choose AI Model:",
        options,
        index=models.index(default_model) if default_model in models else 0,
        help="Different models have different strengths. Larger models are more capable but slower."
    )
    
    # Extract model name from selection
    selected_model = models[options.index(selected_option)]
    
    # Show model info
    if selected_model in model_descriptions:
        st.info(f"Selected: {model_descriptions[selected_model]}")
    
    return selected_model

def format_ai_response(response: str, title: str = "AI Insights") -> None:
    """
    Format and display AI response in Streamlit
    
    Args:
        response: AI generated response
        title: Title for the response section
    """
    if response:
        st.markdown(f"###  {title}")
        st.markdown(f"""
        <div style="background: #f8f9fa; 
                    padding: 1.5rem; border-radius: 12px; margin: 1rem 0; 
                    border-left: 4px solid #2196f3; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
            <div style="color: #1565c0; line-height: 1.6;">{response}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(f"No {title.lower()} available at this time.")

# =============================================================================
# EXECUTIVE COMPONENTS
# =============================================================================

def create_executive_dashboard(kpis: dict, trends: dict = None) -> None:
    """
    Create executive-grade dashboard with synchronized KPIs and trends
    
    Args:
        kpis: Dictionary of KPI name -> {value, trend, icon} 
        trends: Optional trending data for visualization
    """
    st.markdown('<div class="exec-dashboard">', unsafe_allow_html=True)
    
    # Create KPI grid
    cols = st.columns(min(4, len(kpis)))
    
    for i, (kpi_name, kpi_data) in enumerate(kpis.items()):
        with cols[i % len(cols)]:
            value = kpi_data.get('value', 'N/A')
            trend = kpi_data.get('trend', 0)
            icon = kpi_data.get('icon', '')
            trend_icon = "" if trend > 0 else "" if trend < 0 else ""
            trend_class = "positive" if trend > 0 else "negative" if trend < 0 else "neutral"
            trend_color = "var(--exec-success)" if trend > 0 else "var(--exec-secondary)" if trend < 0 else "var(--exec-text-secondary)"
            
            st.markdown(f"""
            <div class="exec-kpi-card">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-label">{kpi_name}</div>
                <div class="kpi-trend" style="color: {trend_color};">
                    {trend_icon} {abs(trend):.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_executive_navigation_grid(nav_items: list) -> None:
    """
    Create executive navigation cards grid
    
    Args:
        nav_items: List of navigation items with title, description, icon, badge
    """
    cols = st.columns(3)
    
    for i, item in enumerate(nav_items):
        with cols[i % 3]:
            title = item.get('title', 'Navigation Item')
            description = item.get('description', '')
            icon = item.get('icon', '')
            badge = item.get('badge', 'AVAILABLE')
            page_key = item.get('page_key', '')
            
            st.markdown(f"""
            <div class="exec-nav-card" onclick="document.querySelector('[data-testid=\\"stSelectbox\\"] input').value='{page_key}'; document.querySelector('[data-testid=\\"stSelectbox\\"] input').dispatchEvent(new Event('change'));">
                <h4>{icon} {title}</h4>
                <p>{description}</p>
                <div class="badge">{badge}</div>
            </div>
            """, unsafe_allow_html=True)

def create_executive_summary_card(title: str, content: str, metrics: dict = None, icon: str = "") -> None:
    """
    Create executive summary card with key insights
    
    Args:
        title: Summary title
        content: Main summary content
        metrics: Optional key metrics to display
        icon: Card icon
    """
    # Create the card with proper HTML structure
    card_html = f"""
    <div style="background: var(--exec-bg-primary); border-radius: var(--exec-border-radius-lg); 
                padding: 2.5rem; box-shadow: var(--exec-shadow-lg); border: 1px solid var(--exec-border);
                margin: 2rem 0; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: var(--exec-solid-primary);"></div>
        <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
            <span style="font-size: 2rem; margin-right: 1rem;">{icon}</span>
            <h2 style="margin: 0; color: var(--exec-primary); font-weight: 700; font-size: 1.5rem;">{title}</h2>
        </div>
        <div style="color: var(--exec-text-primary); line-height: 1.7; font-size: 1.1rem; margin-bottom: 1rem;">
    """
    
    # Add content
    card_html += content
    
    # Add metrics if provided
    if metrics:
        card_html += """
        </div>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 2px solid var(--exec-border);'>
        """
        
        for metric_name, metric_value in metrics.items():
            card_html += f"""
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 700; color: var(--exec-primary); margin-bottom: 0.25rem;">{metric_value}</div>
                <div style="font-size: 0.8rem; color: var(--exec-text-secondary); text-transform: uppercase; font-weight: 600;">{metric_name}</div>
            </div>
            """
        
        card_html += "</div>"
    else:
        card_html += "</div>"
    
    # Close the main card div
    card_html += "</div>"
    
    st.markdown(card_html, unsafe_allow_html=True)

def create_executive_alert_banner(message: str, alert_type: str = "info", dismissible: bool = True) -> None:
    """
    Create executive alert banner for important notifications
    
    Args:
        message: Alert message
        alert_type: Type of alert (success, warning, error, info)
        dismissible: Whether alert can be dismissed
    """
    color_map = {
        "success": "var(--exec-success)",
        "warning": "var(--exec-warning)", 
        "error": "var(--exec-secondary)",
        "info": "var(--exec-primary)"
    }
    
    icon_map = {
        "success": "",
        "warning": "️",
        "error": "", 
        "info": "ℹ️"
    }
    
    color = color_map.get(alert_type, color_map["info"])
    icon = icon_map.get(alert_type, icon_map["info"])
    
    dismiss_button = """
    <button style="background: none; border: none; color: white; font-size: 1.2rem; cursor: pointer; 
                    padding: 0; margin-left: 1rem;" onclick="this.parentElement.style.display='none'">×</button>
    """ if dismissible else ""
    
    st.markdown(f"""
    <div style="background: {color}; color: white; padding: 1rem 2rem; border-radius: var(--exec-border-radius);
                margin: 1rem 0; display: flex; align-items: center; justify-content: space-between;
                box-shadow: var(--exec-shadow); font-weight: 500;">
        <div style="display: flex; align-items: center;">
            <span style="font-size: 1.2rem; margin-right: 0.75rem;">{icon}</span>
            <span>{message}</span>
        </div>
        {dismiss_button}
    </div>
    """, unsafe_allow_html=True)

def create_executive_demo_controller() -> dict:
    """
    Create executive demo controller with synchronized state management
    
    Returns:
        Dictionary with demo state and controls
    """
    if 'exec_demo_state' not in st.session_state:
        st.session_state.exec_demo_state = {
            'current_scenario': 'baseline',
            'demo_speed': 'normal',
            'auto_advance': False,
            'demo_active': False
        }
    
    # Demo controls removed for cleaner sidebar interface
    
    return st.session_state.exec_demo_state

def create_immediate_action_items(action_items: str, title: str = " Immediate Action Items") -> None:
    """
    Create formatted immediate action items using native Streamlit components
    
    Args:
        action_items: AI-generated action items text with numbered list
        title: Title for the action items section
    """
    if not action_items:
        return
    
    # Use native Streamlit components for clean rendering
    st.markdown(f"### {title}")
    
    # Parse and display action items
    cleaned_text = action_items.replace('"', '').strip()
    
    # Split into individual numbered items
    lines = cleaned_text.split('\n')
    current_item = ""
    item_number = 1
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a numbered item (starts with digit followed by period)
        if line and line[0].isdigit() and '. ' in line[:5]:
            # Display previous item if exists
            if current_item:
                with st.container():
                    col1, col2 = st.columns([0.1, 0.9])
                    with col1:
                        st.markdown(f"**{item_number-1}.**")
                    with col2:
                        st.markdown(f"**{current_item}**")
                        st.markdown("---")
            
            # Start new item
            current_item = line.split('. ', 1)[1] if '. ' in line else line
            item_number += 1
        elif line.lower().startswith('- timeline:'):
            timeline = line.replace('- Timeline:', '').replace('- timeline:', '').strip()
            if current_item:
                with st.container():
                    col1, col2 = st.columns([0.1, 0.9])
                    with col1:
                        st.markdown(f"**{item_number-1}.**")
                    with col2:
                        st.markdown(f"**{current_item}**")
                        if timeline:
                            st.success(f"⏱️ **Timeline**: {timeline}")
        elif line.lower().startswith('- requires:'):
            requirements = line.replace('- Requires:', '').replace('- requires:', '').strip()
            if requirements:
                st.info(f" **Requirements**: {requirements}")
                st.markdown("---")
                current_item = ""  # Reset after displaying
        elif not line.startswith('These items') and line:
            # Additional details
            st.caption(f"ℹ️ {line}")
    
    # Display final item if exists
    if current_item:
        with st.container():
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.markdown(f"**{item_number-1}.**")
            with col2:
                st.markdown(f"**{current_item}**")
    
    # Add implementation guide
    st.info(" **Implementation Guide**: These action items are prioritized by urgency. Items marked IMMEDIATE can be started today with minimal risk to network operations.")

def create_ai_metric_card(title: str, value: str, description: str = "", icon: str = "") -> None:
    """
    Create AI-specific metric card
    
    Args:
        title: Card title
        value: Main value to display
        description: Additional description
        icon: Icon to display
    """
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 4px solid #4caf50; margin-bottom: 1rem;">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
            <h4 style="margin: 0; color: #2e7d32; font-weight: 600;">{title}</h4>
        </div>
        <div style="font-size: 1.25rem; font-weight: 500; color: #1565c0; margin-bottom: 0.5rem;">{value}</div>
        {f'<div style="color: #6c757d; font-size: 0.9rem;">{description}</div>' if description else ''}
    </div>
    """, unsafe_allow_html=True)