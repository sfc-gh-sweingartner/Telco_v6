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

### Prerequisites Setup (5 minutes)

1. **Run Database Setup Scripts** (in order):
   ```sql
   -- Execute in Snowflake worksheet
   USE ROLE ACCOUNTADMIN;
   
   -- 1. Create tables and load data
   @Setup/create_tables.sql
   
   -- 2. Setup Cortex Search services
   @CortexSearch/create_cortex_searches.sql
   
   -- 3. Create SPCS infrastructure (compute pool + external access)
   @Setup/spcs_migration/01_create_compute_pool.sql
   @Setup/spcs_migration/02_create_external_access_integrations.sql
   @Setup/spcs_migration/05_fix_mapbox_access.sql
   
   -- 4. Optional: Setup data generators for live demo
   @Setup/setup_data_generators.sql
   ```

### Deploy Streamlit App in Snowsight (2 minutes)

2. **Create App via Snowsight UI** (required for SPCS):
   - Navigate to **Projects > Streamlit** in Snowsight
   - Click **+ Streamlit App**
   - **App title**: `Telco Network Intelligence Suite`
   - **Database**: `TELCO_NETWORK_OPTIMIZATION_PROD`
   - **Schema**: `RAW`
   - **Python environment**: **⭐ Run on container** (critical!)
   - **Compute pool**: `TELCO_STREAMLIT_POOL`
   - **Warehouse**: `TELCO_WH` (or your warehouse name)
   - Connect to your Git repository or upload files
   - **Main file**: `main.py`

3. **Enable External Access** (critical!):
   - Click app menu (⋮) → **App settings**
   - Go to **External networks** tab
   - ✅ Enable `PYPI_ACCESS_INTEGRATION`
   - ✅ Enable `MAPBOX_ACCESS_INTEGRATION`
   - Click **Save**

4. **First Launch** (2-5 minutes for container build):
   - App will build container and install dependencies
   - Subsequent launches are much faster (10-30 seconds)

📖 **Detailed Guide**: See `CREATE_APP_IN_SNOWSIGHT.md` for step-by-step instructions with screenshots

---

## 🚀 SPCS Deployment (Snowpark Container Services)

**This app runs on SPCS for best performance and features!**

### Why SPCS?

✅ **Full Streamlit Features** - Complete `st.cache_resource` and `st.cache_data` support  
✅ **Latest Streamlit** - Use newest versions (>=1.49) as soon as published  
✅ **Any PyPI Package** - No longer limited to Anaconda channel  
✅ **Better Performance** - Long-running service (3-day keep-alive)  
✅ **Professional Grade** - Container-based runtime for production workloads

### Key Components

#### 1. Compute Pool
- **Name**: `TELCO_STREAMLIT_POOL`
- **Purpose**: Runs Python container (not SQL queries)
- **Instance**: CPU_X64_XS (cost-effective)
- **Nodes**: 2-5 (auto-scaling)

#### 2. External Access Integrations

**Two integrations are required:**

**`pypi_access_integration`** - Package installation
- Downloads Python packages from PyPI during container build
- Required for: streamlit, pandas, plotly, pydeck, h3, all dependencies
- Without it: ❌ Container build fails, app won't start

**`mapbox_access_integration`** - Map tiles
- Loads Carto basemap tiles for geospatial visualizations
- Required for: PyDeck maps, H3 hexagon overlays, geospatial analysis
- Without it: ❌ Maps show blank, no background

#### 3. Carto Basemaps
- **Public** - No API key required
- **Fast** - Reliable global CDN
- **Free** - No usage limits
- **Clean** - Professional styling perfect for data overlays

### Deployment Method

**⚠️ IMPORTANT**: Must create app via **Snowsight UI**, not SQL!

The UI properly configures:
- Git integration and stages
- External access integrations
- Compute pool assignment
- Runtime environment

📖 **Detailed Instructions**: See `CREATE_APP_IN_SNOWSIGHT.md` or `QUICK_CREATE_GUIDE.md`

### Troubleshooting

If you encounter issues:
- **Maps blank?** Check `MAPBOX_ACCESS_INTEGRATION` is enabled in App Settings → External networks
- **Build fails?** Check `PYPI_ACCESS_INTEGRATION` is enabled
- **App won't start?** Verify compute pool has available nodes
- See `MAPBOX_FIX_SUMMARY.md` for map troubleshooting

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

### Step 4: SPCS Infrastructure Setup

```sql
-- Create compute pool for containerized Streamlit
@Setup/spcs_migration/01_create_compute_pool.sql

-- Create external access integrations (PyPI + Carto)
@Setup/spcs_migration/02_create_external_access_integrations.sql
@Setup/spcs_migration/05_fix_mapbox_access.sql
```

### Step 5: Create Streamlit App in Snowsight UI

**You must use Snowsight UI to create the app** (SQL creation doesn't work well for SPCS)

See detailed instructions in:
- `CREATE_APP_IN_SNOWSIGHT.md` - Complete guide
- `QUICK_CREATE_GUIDE.md` - Quick reference

### Step 6: Semantic Model (for Snowflake Intelligence)

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
│   ├── setup_data_generators.sql   # Streaming data generators
│   ├── manage_data_generators.sql  # Generator management
│   ├── START_DEMO.sql              # Quick demo start
│   ├── STOP_DEMO.sql               # Quick demo stop
│   ├── regenerate_demo_data.sql    # Data refresh
│   └── spcs_migration/            # SPCS Container Runtime Setup
│       ├── README_SPCS_MIGRATION.md          # Complete deployment guide
│       ├── QUICK_REFERENCE.md                # Quick commands and troubleshooting
│       ├── EXTERNAL_ACCESS_DIAGRAM.md        # Visual guide to integrations
│       ├── 01_create_compute_pool.sql        # Step 1: Compute pool
│       ├── 02_create_external_access_integrations.sql  # Step 2: PyPI + Carto
│       └── 05_fix_mapbox_access.sql          # Final: Expanded network access
│
├── CortexSearch/                   # Cortex Search configuration
│   ├── create_cortex_searches.sql  # Create search services
│   ├── resume_cortex_searches.sql  # Resume services
│   └── suspend_cortex_searches.sql # Suspend services
│
├── Documentation/                  # Additional documentation
│   ├── ExampleQuestions.md         # 30 demo questions for Snowflake Intelligence
│   └── enhancements.md             # Enhancement roadmap
│
├── CREATE_APP_IN_SNOWSIGHT.md     # ⭐ Detailed UI deployment guide
├── QUICK_CREATE_GUIDE.md           # ⭐ Quick deployment reference
├── MAPBOX_FIX_SUMMARY.md           # Map troubleshooting guide
├── SPCS_MIGRATION_SUMMARY.md       # SPCS overview and benefits
│
└── Trash/                          # Obsolete files (kept for reference)
    ├── mapbox_access_setup.sql     # Old warehouse Mapbox setup
    └── connectMapBoxNoKey.sql      # Old warehouse map config
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
- **No API Keys Required**: Uses public Carto basemaps via external access integration
- **Session Management**: Direct `get_active_session()` without caching
- **Production Metrics**: Realistic thresholds (95%+ health, <5% critical issues)
- **AI Integration**: Multiple Cortex models for different use cases
- **Container Runtime**: SPCS provides full Streamlit features and any PyPI package

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