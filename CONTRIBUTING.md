# Contributing to Telco Network Intelligence Suite

Thank you for your interest in contributing to the Telco Network Intelligence Suite! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Issues

If you encounter bugs or have feature requests:

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear, descriptive title
   - Detailed description of the problem/feature
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (Snowflake region, warehouse size, etc.)

### Suggesting Enhancements

We welcome enhancement suggestions! Please:

1. **Check** `Documentation/enhancements.md` for planned features
2. **Open an issue** with the "enhancement" label
3. **Describe** the use case and benefits
4. **Provide examples** of how it would work

### Code Contributions

#### Before You Start

1. **Fork the repository**
2. **Clone your fork locally**
3. **Create a feature branch**: `git checkout -b feature/your-feature-name`
4. **Set up your environment** (see README.md)

#### Development Guidelines

##### Code Style

- Follow **PEP 8** for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

```python
def calculate_network_health(success_rate: float, critical_issues: int) -> float:
    """
    Calculate network health score based on performance metrics.
    
    Args:
        success_rate: Connection success rate (0-100)
        critical_issues: Number of critical issues
        
    Returns:
        Network health score (0-100)
    """
    pass
```

##### SQL Scripts

- Use **uppercase** for SQL keywords
- Include comments for complex queries
- Test with sample data before committing
- Follow Snowflake best practices

```sql
-- Good example
SELECT 
    CELL_ID,
    COUNT(*) AS total_calls,
    AVG(PM_RRC_CONN_ESTAB_SUCC) AS avg_success_rate
FROM TELCO_NETWORK_OPTIMIZATION_PROD.RAW.CELL_TOWER
WHERE EVENT_DATE >= DATEADD(day, -7, CURRENT_DATE())
GROUP BY CELL_ID
ORDER BY avg_success_rate ASC;
```

##### Streamlit Pages

- Use the design system from `utils/design_system.py`
- Follow existing page structure and patterns
- Add page configuration at the top
- Include loading states for queries

```python
import streamlit as st
from utils.design_system import create_page_header, create_metric_card

st.set_page_config(
    page_title="Your Page",
    page_icon="📊",
    layout="wide"
)

create_page_header(
    title="Your Page Title",
    description="Description of what this page does",
    icon="📊"
)
```

#### Testing

Before submitting:

1. **Test in Snowflake Streamlit** environment
2. **Verify** all pages load without errors
3. **Check** that queries execute successfully
4. **Test** with different data scenarios
5. **Ensure** responsive design on different screen sizes

#### Commit Guidelines

Use clear, descriptive commit messages:

```
feat: Add customer churn prediction model
fix: Correct cell tower aggregation in main dashboard
docs: Update setup instructions for Cortex Search
style: Format SQL queries in create_tables.sql
refactor: Simplify AI classification logic
```

Commit message format:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no logic changes)
- `refactor`: Code restructuring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

#### Pull Request Process

1. **Update** your branch with latest main: `git pull origin main`
2. **Ensure** all tests pass
3. **Update** documentation if needed
4. **Create** a pull request with:
   - Clear title describing the change
   - Detailed description of what and why
   - Reference to related issues
   - Screenshots (if UI changes)

5. **Wait** for review and address feedback

### Project Structure Guidelines

When adding new files:

- **Python modules** → `utils/`
- **Streamlit pages** → `pages/` (numbered for order)
- **SQL scripts** → `Setup/` or `CortexSearch/`
- **Documentation** → `Documentation/`
- **Tests** → `tests/` (if adding tests)

### Documentation

Update documentation when:

- Adding new features
- Changing existing functionality
- Adding new SQL scripts
- Modifying setup process

Keep in sync:
- `README.md` - Main documentation
- `CHANGELOG.md` - Version history
- `Documentation/enhancements.md` - Enhancement roadmap
- Inline code comments

## 🎯 Areas for Contribution

We're particularly interested in contributions for:

### High Priority
- [ ] Additional visualization types
- [ ] Enhanced AI models integration
- [ ] Performance optimization
- [ ] Unit and integration tests
- [ ] Automated deployment scripts

### Medium Priority
- [ ] Additional demo scenarios
- [ ] More Snowflake Intelligence questions
- [ ] Export functionality (PDF reports)
- [ ] Email alert integration
- [ ] Advanced filtering options

### Documentation
- [ ] Video tutorials
- [ ] Architecture diagrams
- [ ] API documentation
- [ ] Troubleshooting guides
- [ ] Best practices guide

## 🐛 Bug Reports

Include in bug reports:

- **Snowflake Account** region and edition
- **Warehouse** size being used
- **Browser** and version
- **Error messages** (full text)
- **Screenshots** (if applicable)
- **Steps to reproduce**
- **Data volume** (approximate row counts)

## 💡 Feature Requests

Good feature requests include:

- **Use case** description
- **Problem** it solves
- **Proposed solution**
- **Alternatives** considered
- **Example** workflow
- **Priority** (nice-to-have vs critical)

## 📞 Questions?

- **Email**: deepjyoti.dev@snowflake.com
- **Issues**: Use GitHub Issues for questions
- **Discussions**: Consider opening a GitHub Discussion for broader topics

## 🙏 Thank You!

Your contributions help make this project better for everyone in the telecommunications community!

---

**Note**: By contributing, you agree that your contributions will be licensed under the MIT License.
