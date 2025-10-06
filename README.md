# 📡 Telco Network Intelligence Suite

> **AI-Powered Network Operations Command Center for Telecommunications**

[![Snowflake](https://img.shields.io/badge/Snowflake-Cortex_AI-29B5E8?style=flat&logo=snowflake)](https://www.snowflake.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat&logo=streamlit)](https://streamlit.io/)

A comprehensive multi-page Streamlit application built on Snowflake for real-time visualization, analysis, and AI-powered insights into cell tower performance and customer support data.

---

## 🚀 Features

### **Executive Dashboard**
- Real-time network health metrics
- Production-realistic KPIs (Network Health, Critical Issues, Premium Performance)
- AI-powered strategic insights
- Revenue protection analytics

### **Interactive Cell Tower Analysis**
- 3D visualization with PyDeck
- Color-coded failure rate mapping (Red/Yellow/Green)
- Click-to-select grid cells for detailed analysis
- AI-powered recommendations using Mistral-Large
- Customer loyalty correlation analysis
- Sentiment scoring from support tickets

### **Customer Intelligence**
- AI customer profiling with churn prediction
- Sentiment analysis on support tickets
- Customer journey analytics
- Retention strategy recommendations

### **Geospatial Analytics**
- Heatmap overlays for support ticket density
- Coverage gap identification
- Performance correlation by region
- Investment prioritization mapping

### **AI-Powered Features**
- Natural language querying with Snowflake Intelligence
- Cortex Search integration
- Automated root cause analysis
- Predictive maintenance recommendations
- Executive summary generation

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [Demo Mode](#demo-mode)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)
- [Contributing](#contributing)

---

## 🔧 Prerequisites

### Required
- **Snowflake Account** with Cortex AI enabled
- **ACCOUNTADMIN** privileges for initial setup
- **Warehouse** (Small or larger recommended)
- **Python 3.11+** (for local development)

### Recommended
- Snowflake Intelligence enabled
- Cross-region inference configured
- Git integration setup

---

## ⚡ Quick Start

### Option 1: Deploy from GitHub (Recommended)

1. **Create Git API Integration** in Snowflake:
```sql
CREATE OR REPLACE API INTEGRATION git_telco_v4
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com/Deepjyoti-ricky/')
  ENABLED = TRUE;
```

2. **Deploy Streamlit App**:
   - Navigate to **Projects > Streamlit** in Snowsight
   - Click **+ Streamlit App** → **Create from repository**
   - Repository URL: `https://github.com/Deepjyoti-ricky/Telco_v4`
   - Select API Integration: `git_telco_v4`
   - Deploy to: `TELCO_NETWORK_OPTIMIZATION_PROD.RAW`
   - Main file: `main.py`

3. **Install Required Packages**:
   - In Streamlit editor, add packages: `altair, branca, h3-py, matplotlib, numpy, pandas, plotly, pydeck, scipy`

4. **Run Setup Scripts** (in order):
   ```sql
   -- Execute in Snowflake worksheet
   USE DATABASE TELCO_NETWORK_OPTIMIZATION_PROD;
   USE SCHEMA RAW;
   
   -- 1. Create tables and load data
   @Setup/create_tables.sql
   
   -- 2. Setup Cortex Search services
   @CortexSearch/create_cortex_searches.sql
   
   -- 3. Configure Mapbox access
   @Setup/connectMapBoxNoKey.sql
   
   -- 4. Setup data generators (optional for live demo)
   @Setup/setup_data_generators.sql
   ```

---

## 🆕 SPCS Migration (Snowpark Container Services)

**NEW: Run Streamlit on containers for better performance and features!**

### Why Migrate to SPCS?

✅ **Full Streamlit Features** - Complete `st.cache_resource` and `st.cache_data` support  
✅ **Latest Streamlit** - Use newest versions (>=1.49) as soon as published  
✅ **Any PyPI Package** - No longer limited to Anaconda channel  
✅ **Better Performance** - Long-running service (3-day keep-alive)  
✅ **Experimental Features** - Access streamlit-nightly for cutting edge  

### Quick SPCS Migration (3 Steps)

```sql
-- 1. Create compute pool
@Setup/spcs_migration/01_create_compute_pool.sql

-- 2. Create external access integrations (PyPI + Mapbox)
@Setup/spcs_migration/02_create_external_access_integrations.sql

-- 3. Create SPCS Streamlit app
@Setup/spcs_migration/03_create_streamlit_app_spcs.sql
```

### External Access Integrations Explained

**Two integrations are required:**

1. **`pypi_access_integration`** - Downloads Python packages from PyPI during container build
   - Required for: streamlit, pandas, plotly, pydeck, all dependencies
   - Without it: Container build fails, app won't start

2. **`mapbox_access_integration`** - Loads map tiles for geospatial features
   - Required for: pydeck maps, st.map(), H3 hexagon visualizations
   - Without it: Maps show blank, no tiles load

### Migration Documentation

- **Full Guide**: `Setup/spcs_migration/README_SPCS_MIGRATION.md` - Complete migration walkthrough
- **Quick Reference**: `Setup/spcs_migration/QUICK_REFERENCE.md` - Commands and troubleshooting
- **Individual Scripts**: Run `01_*.sql`, `02_*.sql`, `03_*.sql` separately for control
- **Master Script**: `00_RUN_ALL_MIGRATION_STEPS.sql` - All steps in one (requires manual app creation)

---

## 📦 Detailed Setup

### Step 1: Database Setup

```sql
-- Create database and schema
CREATE DATABASE IF NOT EXISTS TELCO_NETWORK_OPTIMIZATION_PROD;
CREATE SCHEMA IF NOT EXISTS TELCO_NETWORK_OPTIMIZATION_PROD.RAW;

-- Create warehouse
CREATE WAREHOUSE IF NOT EXISTS TELCO_WH
  WITH WAREHOUSE_SIZE = 'SMALL'
  AUTO_SUSPEND = 300
  AUTO_RESUME = TRUE;

USE DATABASE TELCO_NETWORK_OPTIMIZATION_PROD;
USE SCHEMA RAW;
USE WAREHOUSE TELCO_WH;
```

### Step 2: Load Data

Execute `Setup/create_tables.sql` to create:
- `CELL_TOWER` table (~2.6M records)
- `SUPPORT_TICKETS` table (~180K records)
- `CUSTOMER_LOYALTY` table

### Step 3: Cortex Search Setup

```sql
-- Create Cortex Search services for semantic search
@CortexSearch/create_cortex_searches.sql

-- Verify services are ready
SHOW CORTEX SEARCH SERVICES;
```

### Step 4: Configure Network Access

```sql
-- Setup Mapbox integration (no API key required)
@Setup/connectMapBoxNoKey.sql

-- Update with your Streamlit app name
ALTER STREAMLIT TELCO_NETWORK_OPTIMIZATION_PROD.RAW.YOUR_APP_NAME
  SET EXTERNAL_ACCESS_INTEGRATIONS = (map_access_int);
```

### Step 5: Semantic Model (for Snowflake Intelligence)

Upload `telco_network_opt.yaml` to Snowflake as a semantic model to enable natural language querying.

---

## 📁 Project Structure

```
Telco_v6/
├── main.py                          # Main dashboard and landing page
├── requirements.txt                 # Python dependencies (SPCS: streamlit>=1.49)
├── pyproject.toml                   # NEW: Python 3.11 + dependency management for SPCS
├── telco_network_opt.yaml          # Semantic model for Snowflake Intelligence
├── .gitignore                      # Git ignore rules
│
├── pages/                          # Multi-page Streamlit app
│   ├── 0_AI_Insights_and_Recommendations.py
│   ├── 1_Customer_Profile.py
│   ├── 2_Cell_Tower_Lookup.py     # Interactive 3D map
│   ├── 3_Geospatial_Analysis.py
│   ├── 7_Executive_AI_Summary.py
│   ├── 8_Predictive_Analytics.py
│   ├── 9_AI_Network_Assistant.py
│   └── 12_Snowflake_Intelligence.py
│
├── utils/                          # Utility modules
│   ├── design_system.py            # UI components and styling
│   └── aisql_functions.py          # AI/SQL helper functions
│
├── Setup/                          # SQL setup scripts
│   ├── create_tables.sql           # Main data setup
│   ├── connectMapBoxNoKey.sql      # Mapbox configuration
│   ├── mapbox_access_setup.sql     # Alternative Mapbox setup
│   ├── setup_data_generators.sql   # Streaming data generators
│   ├── manage_data_generators.sql  # Generator management
│   ├── START_DEMO.sql              # Quick demo start
│   ├── STOP_DEMO.sql               # Quick demo stop
│   ├── regenerate_demo_data.sql    # Data refresh
│   └── spcs_migration/            # NEW: SPCS Container Runtime Migration
│       ├── README_SPCS_MIGRATION.md          # Complete migration guide
│       ├── QUICK_REFERENCE.md                # Quick commands and troubleshooting
│       ├── 00_RUN_ALL_MIGRATION_STEPS.sql    # Master migration script
│       ├── 01_create_compute_pool.sql        # Step 1: Compute pool
│       ├── 02_create_external_access_integrations.sql  # Step 2: PyPI + Mapbox
│       └── 03_create_streamlit_app_spcs.sql  # Step 3: Create SPCS app
│
├── CortexSearch/                   # Cortex Search configuration
│   ├── create_cortex_searches.sql  # Create search services
│   ├── resume_cortex_searches.sql  # Resume services
│   └── suspend_cortex_searches.sql # Suspend services
│
└── Documentation/                  # Additional documentation
    ├── ExampleQuestions.md         # 30 demo questions for Snowflake Intelligence
    └── enhancements.md             # Enhancement roadmap
```

---

## 🎯 Usage Guide

### Executive Dashboard
Access the main dashboard to see:
- Network health score (production-realistic metrics)
- Critical issues count
- Premium performance percentage
- Revenue protection metrics
- AI strategic recommendations

### Cell Tower Analysis
1. Navigate to **Cell Tower Lookup** page
2. View 3D grid visualization of California cell towers
3. Click on grid cells to analyze specific areas
4. Review AI-generated recommendations for prioritization

### Customer Intelligence
1. Go to **Customer Profile** page
2. Enter customer ID or browse profiles
3. View churn prediction and sentiment analysis
4. Access AI-powered retention strategies

### Snowflake Intelligence
1. Open **Snowflake Intelligence** page
2. Use natural language queries (see `Documentation/ExampleQuestions.md`)
3. Example: *"Which cell towers have the highest failure rates?"*

---

## 🎬 Demo Mode

### Starting Live Demo

```sql
-- Start streaming data generators
@Setup/START_DEMO.sql

-- Or manually
CALL MANAGE_DATA_GENERATORS('START');
```

### Stopping Demo

```sql
-- Stop streaming data generators
@Setup/STOP_DEMO.sql

-- Or manually
CALL MANAGE_DATA_GENERATORS('STOP');
```

### Regenerating Demo Data

```sql
-- Refresh data to reset demo state
@Setup/regenerate_demo_data.sql
```

---

## 🔍 Troubleshooting

### Maps Not Displaying

1. **Verify External Access Integration**:
```sql
SHOW EXTERNAL ACCESS INTEGRATIONS;
```

2. **Check Streamlit Configuration**:
```sql
SHOW STREAMLITS;
DESC STREAMLIT YOUR_APP_NAME;
```

3. **Update Integration**:
```sql
ALTER STREAMLIT TELCO_NETWORK_OPTIMIZATION_PROD.RAW.YOUR_APP_NAME
  SET EXTERNAL_ACCESS_INTEGRATIONS = (map_access_int);
```

### Import Errors

If you encounter `cannot import name 'DAY_IN_SECONDS'`:
- This has been fixed in the latest version
- Ensure you're pulling the latest code from GitHub
- The issue was caused by improper session caching

### Performance Issues

- Use **SMALL** warehouse minimum
- Enable query result caching
- Consider **MEDIUM** warehouse for large datasets

### Data Not Loading

```sql
-- Verify tables exist
SHOW TABLES IN TELCO_NETWORK_OPTIMIZATION_PROD.RAW;

-- Check row counts
SELECT 'CELL_TOWER' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM CELL_TOWER
UNION ALL
SELECT 'SUPPORT_TICKETS', COUNT(*) FROM SUPPORT_TICKETS;
```

---

## 🏗️ Architecture

### Technology Stack
- **Platform**: Snowflake (Data Cloud)
- **AI/ML**: Snowflake Cortex (Claude, GPT-4, Mistral, Llama)
- **Frontend**: Streamlit in Snowflake
- **Visualization**: PyDeck, Plotly, Matplotlib
- **Geospatial**: H3, Branca

### Data Flow
1. **Source Data** → Cell Tower metrics (2.6M records) + Support Tickets (180K records)
2. **Cortex AI** → Sentiment analysis, classification, embeddings
3. **Semantic Layer** → Natural language querying
4. **Streamlit** → Interactive visualization and dashboards
5. **Real-time Updates** → Optional streaming data generators

### Key Design Decisions
- **No API Keys Required**: Leverages Snowflake's built-in Mapbox integration
- **Session Management**: Direct `get_active_session()` without caching
- **Production Metrics**: Realistic thresholds (95%+ health, <5% critical issues)
- **AI Integration**: Multiple Cortex models for different use cases

---

## 🤝 Contributing

This is a demonstration project for Snowflake Cortex AI capabilities in telecommunications. For questions or collaboration:

**Contact**: deepjyoti.dev@snowflake.com

---

## 📄 License

This project is provided as-is for demonstration purposes.

---

## 🙏 Acknowledgments

- Built on [Snowflake's network optimization quickstart](https://github.com/sfc-gh-sweingartner/network_optmise)
- Powered by Snowflake Cortex AI
- Uses Ericsson-inspired telco branding guidelines

---

## 📊 Dataset Information

- **Cell Towers**: ~2.6M performance records
  - Ericsson LTE towers in California
  - Metrics: RRC connections, E-RAB releases, PRB utilization
  - Location data with lat/long coordinates

- **Support Tickets**: ~180K customer records
  - Sentiment scores (-1 to +1)
  - Service types: Cellular, Business Internet, Home Internet
  - Correlated with cell tower performance

- **Customer Loyalty**: Tiered status tracking
  - Bronze, Silver, Gold tiers
  - Linked to cell tower usage patterns

---

**Built with ❄️ Snowflake Cortex AI • Demonstrating the Future of Network Operations**