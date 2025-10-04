# Changelog

All notable changes to the Telco Network Intelligence Suite will be documented in this file.

## [2.0.0] - 2025-01-04

### Added
- Professional repository structure with organized directories
- Comprehensive README with setup instructions and architecture details
- `.gitignore` file for Python projects
- Cortex Search integration for semantic search capabilities
- Data generator scripts for live demo mode
- START_DEMO.sql and STOP_DEMO.sql for easy demo control
- ExampleQuestions.md with 30 compelling demo questions
- Enhanced semantic model (TELCO_NETWORK_OPT2) with comprehensive synonyms

### Changed
- Reorganized SQL files into `Setup/` directory
- Moved documentation to `Documentation/` directory
- Updated SQL scripts from source repository
- Improved production-realistic metrics calculations
- Fixed SQL aggregation for accurate cell tower metrics
- Enhanced Cell Tower Lookup with 3D interactive visualization

### Fixed
- AttributeError: Replaced Row.get() with getattr() for Snowpark compatibility
- AI classify JSON parsing to extract labels properly
- Indentation errors in Cell Tower Lookup page
- Streamlit import error: Removed @st.cache_resource from session initialization
- Production data metrics showing unrealistic values
- Relationship direction in semantic model (Support_Tickets → Cell_Tower)

### Removed
- Deprecated enable_cross_region_inference.sql
- Old modify_support_tickets.sql (replaced with source version)
- __pycache__ directories from git tracking

## [1.0.0] - 2024-12-XX

### Initial Release
- Multi-page Streamlit application
- Cell tower performance visualization
- Customer support ticket analysis
- Basic AI insights and recommendations
- Mapbox integration for geospatial visualization
- Snowflake Cortex AI integration

---

## Version History Notes

### Semantic Versioning
- **Major**: Breaking changes or significant new features
- **Minor**: New features, non-breaking
- **Patch**: Bug fixes and minor improvements

### Categories
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes
