# Contributing to Fraud Detection System

Thank you for your interest in contributing to the Fraud Detection System! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use issue templates** when available
3. **Provide detailed information**:
   - Operating system and version
   - Python version
   - PostgreSQL version
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Error messages and stack traces

### Suggesting Enhancements

1. **Check existing feature requests** to avoid duplicates
2. **Describe the enhancement** in detail:
   - Use case and motivation
   - Proposed solution
   - Alternative solutions considered
   - Potential impact on existing functionality

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Git
- Docker (optional, for database setup)

### Setup Development Environment

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/fraud-detection-sql.git
   cd fraud-detection-sql
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

4. **Install development dependencies**:
   ```bash
   pip install pytest pytest-cov black flake8 mypy
   ```

5. **Setup database**:
   ```bash
   docker-compose up -d  # Or setup PostgreSQL manually
   python scripts/setup_environment.py
   ```

## 📝 Coding Standards

### Python Style Guide

We follow PEP 8 with these specific guidelines:

- **Line length**: 88 characters (Black default)
- **Imports**: Use absolute imports, group in this order:
  1. Standard library
  2. Third-party packages
  3. Local application imports
- **Docstrings**: Use Google-style docstrings
- **Type hints**: Required for all new code

### Code Formatting

Use Black for automatic code formatting:
```bash
black src/ tests/
```

### Linting

Use flake8 for code linting:
```bash
flake8 src/ tests/
```

### Type Checking

Use mypy for static type checking:
```bash
mypy src/
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_fraud_detection.py

# Run specific test function
pytest tests/test_fraud_detection.py::test_early_morning_detection
```

### Writing Tests

1. **Test file naming**: `test_*.py` in the `tests/` directory
2. **Test function naming**: `test_*`
3. **Test class naming**: `Test*`
4. **Use descriptive test names** that explain what is being tested
5. **Follow AAA pattern**: Arrange, Act, Assert

Example test:
```python
def test_early_morning_transaction_detection():
    """Test that early morning transactions are correctly identified."""
    # Arrange
    transactions = create_sample_transactions()
    analyzer = FraudAnalyzer(mock_engine)
    
    # Act
    early_morning_txs = analyzer.get_early_morning_transactions()
    
    # Assert
    assert len(early_morning_txs) == 5
    assert all(7 <= tx.hour <= 9 for tx in early_morning_txs['date'])
```

### Test Coverage

Aim for at least 80% test coverage for new code. Critical fraud detection logic should have higher coverage.

## 📊 SQL Guidelines

### Query Style

- Use uppercase for SQL keywords: `SELECT`, `FROM`, `WHERE`
- Use meaningful table aliases: `t` for transaction, `ch` for card_holder
- Indent nested queries and subqueries
- Comment complex queries

Example:
```sql
-- Find high-risk transactions with multiple fraud indicators
SELECT 
    t.id,
    t.date,
    t.amount,
    ch.name as cardholder_name,
    COUNT(small_tx.id) as small_transaction_count
FROM transaction t
JOIN credit_card cc ON t.card = cc.card
JOIN card_holder ch ON cc.id_card_holder = ch.id
LEFT JOIN (
    SELECT id, card 
    FROM transaction 
    WHERE amount < 2.00
) small_tx ON small_tx.card = t.card
WHERE EXTRACT(HOUR FROM t.date) BETWEEN 7 AND 9
  AND t.amount > 100
GROUP BY t.id, t.date, t.amount, ch.name
ORDER BY small_transaction_count DESC, t.amount DESC;
```

## 🔧 Adding New Features

### Fraud Detection Algorithms

When adding new fraud detection methods:

1. **Add to `FraudAnalyzer` class** in `src/fraud_analysis.py`
2. **Create corresponding SQL view** in `sql/schema.sql`
3. **Add visualization** in `src/fraud_visualization.py`
4. **Update configuration** in `config/fraud_rules.yaml`
5. **Write comprehensive tests**

### Database Schema Changes

1. **Create migration script** in `sql/migrations/`
2. **Update `schema.sql`** with new structure
3. **Update data models** in source code
4. **Add backward compatibility** if needed
5. **Update documentation**

### Configuration Options

1. **Add to appropriate YAML file** in `config/`
2. **Update validation logic**
3. **Add documentation**
4. **Provide sensible defaults**

## 📚 Documentation

### Code Documentation

- **Docstrings**: Required for all public functions and classes
- **Inline comments**: For complex logic
- **Type hints**: For all function parameters and return values

### Project Documentation

- **Update relevant markdown files** in `docs/`
- **Update API reference** for new public methods
- **Update README** if adding major features
- **Update execution guide** if changing workflows

### Documentation Style

Use clear, concise language and include examples where helpful.

## 🚀 Pull Request Process

### Before Submitting

1. **Run all tests**: `pytest`
2. **Check code formatting**: `black --check src/ tests/`
3. **Run linting**: `flake8 src/ tests/`
4. **Check type hints**: `mypy src/`
5. **Update documentation** as needed
6. **Test manually** with sample data

### Pull Request Guidelines

1. **Create feature branch**: `git checkout -b feature/your-feature-name`
2. **Write descriptive commit messages**
3. **Keep PRs focused**: One feature/fix per PR
4. **Update CHANGELOG.md** if applicable
5. **Reference related issues**: Use "Fixes #123" or "Relates to #456"

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or breaking changes documented)
```

## 🏷️ Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist

1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create release tag
4. Update documentation
5. Test release candidate
6. Publish release

## 🤔 Questions and Support

- **Documentation**: Check `docs/` directory first
- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub Discussions for questions
- **Security**: Email security@company.com for security issues

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the issue, not the person
- Help others learn and grow

## 🏆 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project README

Thank you for contributing to making fraud detection better for everyone! 🎉
