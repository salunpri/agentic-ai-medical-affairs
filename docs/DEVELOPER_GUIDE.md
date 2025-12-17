# Developer Guide

## Getting Started

This guide will help you understand the codebase and contribute to the project.

## Project Structure

```
agentic-ai-medical-affairs/
├── src/policy_drafting/      # Main source code
│   ├── evidence/              # Evidence extraction modules
│   ├── models/                # AI model integration
│   ├── compliance/            # Validation modules
│   ├── explainability/        # Audit and logging
│   ├── integration/           # Export and integration
│   ├── workflow.py            # Main orchestrator
│   └── cli.py                 # Command-line interface
├── tests/                     # Test suite
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
├── config/                    # Configuration files
├── data/                      # Data storage
│   ├── templates/             # Policy templates
│   ├── sample_data/           # Sample datasets
│   ├── exports/               # Generated exports
│   └── audit_logs/            # Audit trail logs
└── docs/                      # Documentation

```

## Development Setup

1. **Clone and Install**:
```bash
git clone https://github.com/salunpri/agentic-ai-medical-affairs.git
cd agentic-ai-medical-affairs
pip install -e ".[dev]"
```

2. **Set Up Pre-commit Hooks** (optional):
```bash
pre-commit install
```

3. **Configure Environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Code Style

We follow PEP 8 guidelines with these tools:
- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking

Run formatting:
```bash
black src/ tests/
flake8 src/ tests/
mypy src/
```

## Testing Guidelines

### Writing Tests

1. **Unit Tests**: Test individual functions/classes
   - Place in `tests/unit/`
   - Mock external dependencies
   - Test edge cases

2. **Integration Tests**: Test module interactions
   - Place in `tests/integration/`
   - Use minimal mocking
   - Test complete workflows

### Test Structure

```python
import pytest
from module import ClassName

class TestClassName:
    """Test ClassName functionality."""
    
    def test_method_name(self):
        """Test specific behavior."""
        # Arrange
        instance = ClassName()
        
        # Act
        result = instance.method()
        
        # Assert
        assert result == expected
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/unit/test_pubmed_client.py -v

# With coverage
pytest tests/ --cov=src/policy_drafting --cov-report=html

# Mark slow tests
pytest tests/ -m "not slow"
```

## Module Deep Dive

### Evidence Module

**PubMedClient** fetches articles from PubMed:
- Uses NCBI E-utilities API
- Handles rate limiting
- Parses XML responses

**EvidenceProcessor** analyzes articles:
- Extracts key findings
- Assesses evidence quality
- Synthesizes multiple sources

### Models Module

**PolicyGenerator** creates policy drafts:
- Uses AI models (GPT-4, etc.)
- Applies policy templates
- Generates structured documents

### Compliance Module

**ComplianceValidator** validates policies:
- Checks required sections
- Validates against frameworks
- Calculates compliance scores

### Explainability Module

**AuditLogger** maintains audit trails:
- Logs all activities
- Generates audit reports
- Ensures traceability

### Integration Module

**DashboardExporter** exports policies:
- Multiple format support
- API payload generation
- Package creation

## Adding New Features

### Adding a New Evidence Source

1. Create new client class in `evidence/`:
```python
class NewSourceClient:
    def __init__(self):
        pass
    
    def search_articles(self, query):
        pass
    
    def fetch_details(self, ids):
        pass
```

2. Add tests in `tests/unit/`

3. Update workflow to use new source

### Adding a New Compliance Framework

1. Update `ComplianceValidator._load_validation_rules()`:
```python
"new_framework": {
    "required_sections": [...],
    "keywords": [...]
}
```

2. Add tests for new framework

3. Update documentation

### Adding a New Export Format

1. Add method to `DashboardExporter`:
```python
def _export_new_format(self, policy_draft, policy_id):
    # Implementation
    pass
```

2. Update `export_policy_draft()` to handle new format

3. Add tests

## API Design Principles

1. **Modularity**: Each module has a single responsibility
2. **Extensibility**: Easy to add new features
3. **Type Safety**: Use type hints
4. **Error Handling**: Graceful error recovery
5. **Logging**: Comprehensive logging for debugging

## Debugging Tips

### Enable Verbose Logging

```python
from loguru import logger
logger.add("debug.log", level="DEBUG")
```

### Mock External APIs

```python
from unittest.mock import patch

@patch('requests.Session.get')
def test_api_call(mock_get):
    mock_get.return_value = mock_response
    # Test code
```

### Inspect Audit Logs

```python
from policy_drafting.explainability import AuditLogger

logger = AuditLogger()
trail = logger.get_session_audit_trail()
for entry in trail:
    print(entry)
```

## Performance Optimization

1. **Caching**: Cache frequently accessed data
2. **Batch Processing**: Process multiple items together
3. **Async Operations**: Use async for I/O operations
4. **Lazy Loading**: Load data only when needed

## Common Issues

### PubMed API Rate Limiting

**Problem**: Too many requests
**Solution**: Use API key, add delays between requests

### Memory Issues with Large Evidence Sets

**Problem**: Processing too many articles
**Solution**: Implement pagination, stream processing

### Compliance Validation False Positives

**Problem**: Keywords not found
**Solution**: Adjust validation rules, improve text matching

## Documentation

### Docstring Format

```python
def function_name(param1: str, param2: int) -> Dict:
    """
    Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When invalid input
    """
```

### Updating Documentation

1. Update docstrings in code
2. Update README.md for user-facing changes
3. Update this guide for developer changes
4. Generate API docs: `mkdocs build`

## Release Process

1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Run full test suite
4. Create git tag
5. Push to repository
6. Create GitHub release

## Getting Help

- Check existing issues on GitHub
- Review test cases for examples
- Read module docstrings
- Ask in discussions

## Contributing

See CONTRIBUTING.md for contribution guidelines.
