# Telco Network Optimization Suite

A multi-page Streamlit application for visualizing and analyzing cell tower performance and customer support data.

## Features

- **Home Dashboard**: Overview of network statistics and navigation
- **Cell Tower Lookup**: Interactive map for examining individual cell tower performance metrics
- **Heatmap Overlay**: Visualize support ticket density and sentiment data
- **Additional Analysis Pages**: Coming soon!

## Setup Instructions

### 1. File Structure

The application follows Snowflake's multi-page Streamlit app structure:

```
/
├── main.py                       # Main landing page
├── pages/                        # Subdirectory for individual pages
│   ├── 1_Cell_Tower_Lookup.py    # Cell tower lookup page
│   ├── 2_Heatmap_Overlay.py      # Interactive heatmap page
│   ├── 3_Customer_Impact.py      # Customer impact dashboard (placeholder)
│   └── 4_Loyalty_Impact.py       # Loyalty status impact view (placeholder)
└── README.md                     # Documentation
```

### 2. Mapbox Configuration

The application uses Mapbox API key configured through Snowflake's secret management. The following has already been done:

```sql
-- Create secret for Mapbox API key
CREATE OR REPLACE SECRET mapbox_key
  TYPE = GENERIC_STRING
  SECRET_STRING = $MAPBOX_API_KEY;

-- Create external access integration
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION map_access_int
  ALLOWED_NETWORK_RULES = (map_tile_rule)
  ALLOWED_AUTHENTICATION_SECRETS = (mapbox_key)
  ENABLED = TRUE;

-- Grant necessary privileges
GRANT READ ON SECRET mapbox_key TO ROLE IDENTIFIER($APP_CREATOR_ROLE);
GRANT USAGE ON INTEGRATION map_access_int TO ROLE IDENTIFIER($APP_CREATOR_ROLE);

-- Enable the Streamlit app to use the integration and secret
ALTER STREAMLIT TELCO_NETWORK_OPTIMIZATION_PROD.RAW.FQYVZ89K8QDAWHRK
  SET EXTERNAL_ACCESS_INTEGRATIONS = (map_access_int)
  SECRETS = ('mapbox_key' = TELCO_NETWORK_OPTIMIZATION_PROD.RAW.mapbox_key);
```

If you create a new Streamlit app or need to reconfigure the existing one, make sure to update the ALTER STREAMLIT statement with your app's identifier.

## Multi-Page Navigation

The application uses Streamlit's built-in multi-page support, which automatically adds navigation in the sidebar. According to Snowflake's documentation:

* The main.py file serves as the landing page
* Files in the pages/ directory are displayed as navigation options
* File naming with numbers (e.g., 1_Cell_Tower_Lookup.py) controls the order
* Each page can be accessed directly via URL paths

## Key Features of the Heatmap Overlay

The Heatmap Overlay page provides several powerful visualizations:

1. **Interactive Heatmap** with options to view:
   - Cell Tower Failure Rate
   - Support Ticket Density
   - Customer Sentiment Distribution
   - Combined Issue Severity

2. **Correlation Analysis** showing the relationship between:
   - Failure Rate vs. Support Ticket Count
   - Failure Rate vs. Sentiment Score

3. **Key Statistics** tables displaying:
   - Top 5 worst performing cell towers
   - Areas with the most support tickets

4. **Priority Areas** highlighting the most problematic locations based on a combination of technical and customer impact metrics

## Troubleshooting

- If pages aren't loading correctly, ensure each page has `st.set_page_config()` as the first Streamlit command
- If maps aren't displaying properly, verify that the Mapbox secret is properly configured
- For data issues, check the SQL queries in each file to ensure they match your database schema 