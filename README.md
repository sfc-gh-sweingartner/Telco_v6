# network_optmise

##This is a demo of Snowflake's geospatial, advanced analytics and text2chat capability against telco network data

Note this demo builds on top of two projects you should be familar with:

Optimising Network Operations Quickstart: A hands on lab to generate some data and deliver some analytics against it
https://quickstarts.snowflake.com/guide/optimizing-network-operations-with-cortex-ai-call-transcripts-and-tower-data-analysis/index.html?index=..%2F..index#0

Cortex Analyst Charting: A Streamlit in Snowflake app that produces nice charts on top of Cortex Analyst
https://github.com/sfc-gh-sweingartner/CortexCharts/tree/main


### How to Deploy the geospatial and advanced analytics SIS demo 
1) In Snowsight, open a SQL worksheet and run this with ACCOUNTADMIN to allow your env to see this GIT project:
    CREATE OR REPLACE API INTEGRATION git_sweingartner
    API_PROVIDER = git_https_api
    API_ALLOWED_PREFIXES = ('https://github.com/sfc-gh-sweingartner')
    ENABLED = TRUE;
2) click Projects > Streamlit
3) Tick the drop downbox next to the blue "+ Streamlit App" and select "create from repository"
4) Click "Create Git Repository"
5) In the Repository URL field, enter: https://github.com/sfc-gh-sweingartner/network_optmise
6) In the API Integration drop down box, choose GIT_SWEINGARTNER
7) Deploy it into any DB, Schema and use any WH
8) Click Home.py then "Select File"
9) Click create
10) Optional - In a SQL worksheet, run the statements in modify_support_tickets.sql against the table created in the quickstart.  (This increases the support ticket count for cell's where the sentiment is low)  
11) Go to mapbox.com and create a free account.  This is a mapping service.  Log in and you will be provided an API key.   In a Snowflake SQL worksheet open mapbox_access_setup.sql and enter in your key in line 7
12) Run the App.


### How to Deploy the text2sql demo 
1. Save the telco_network_opt.yaml file into an internal stage.  If you deployed the geospatial app above, you can save it here:  TELCO_NETWORK_OPTIMIZATION_PROD.RAW.DATA/telco_network_opt.yaml
2. Create a Cortex Analyst charting app per the instructions in the Gitlab above.  
