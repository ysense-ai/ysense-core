# Contributing to YSense™ Platform

First off, thank you for considering contributing to YSense™! 🎉

It's people like you that make YSense™ such a great tool for ethical AI collaboration.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Community](#community)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our commitment to:

- **Be respectful** - Treat all contributors with respect
- **Be collaborative** - Work together towards common goals
- **Be inclusive** - Welcome contributors from all backgrounds
- **Be ethical** - Follow Z Protocol v2.0 principles

Please report unacceptable behavior to conduct@ysenseai.org

---

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**Good Bug Report Includes:**
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)

**Template:**
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g., Windows 10]
- Python Version: [e.g., 3.11.5]
- YSense Version: [e.g., 4.1.0]
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**Good Enhancement Suggestion Includes:**
- Clear use case
- Why it would be useful
- Potential implementation approach
- Any drawbacks or considerations

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - Simple issues for beginners
- `help wanted` - Issues needing assistance
- `documentation` - Documentation improvements

---

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/YSense-Platform-v4.1.git
cd YSense-Platform-v4.1

# Add upstream remote
git remote add upstream https://github.com/ysenseiai/YSense-Platform-v4.1.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy
```

### 3. Create .env File

```bash
cp env_template.txt .env
# Add your API keys (optional for development)
```

### 4. Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_crypto_auth.py

# Run with coverage
pytest --cov=src tests/
```

---

## 🔄 Development Workflow

### 1. Create a Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/amazing-feature

# Or for bug fixes
git checkout -b fix/bug-description
```

### 2. Make Changes

- Write clean, readable code
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation

### 3. Test Your Changes

```bash
# Run tests
pytest tests/

# Check code style
black src/ tests/
flake8 src/ tests/

# Type checking
mypy src/
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add amazing feature"
```

See [Commit Guidelines](#commit-guidelines) below.

### 5. Push and Create PR

```bash
git push origin feature/amazing-feature
```

Then open a Pull Request on GitHub.

---

## 🎨 Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

- **Line Length**: 100 characters (not 79)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Organized (stdlib, third-party, local)

### Code Formatting

Use **Black** for automatic formatting:

```bash
# Format all code
black src/ tests/

# Check without modifying
black --check src/ tests/
```

### Type Hints

Use type hints for all functions:

```python
def process_wisdom(wisdom_id: int, user_id: int) -> Dict[str, Any]:
    """Process wisdom drop with attribution."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def create_user(username: str, password: str, tier: str = "Standard") -> Dict[str, Any]:
    """Create a new user with crypto authentication.
    
    Args:
        username: Unique username for the user
        password: Password to encrypt private key
        tier: Contributor tier (default: "Standard")
        
    Returns:
        Dictionary containing user info and keys
        
    Raises:
        ValueError: If username already exists
        
    Example:
        >>> result = create_user("alice", "secure123", "Founding Contributor")
        >>> print(result['public_key'])
    """
    pass
```

### Error Handling

Always handle errors gracefully:

```python
try:
    result = api_call()
except APIError as e:
    logger.error(f"API call failed: {e}")
    return fallback_response()
except Exception as e:
    logger.exception("Unexpected error")
    raise
```

---

## 📝 Commit Guidelines

We follow **Conventional Commits** specification:

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

### Examples

```bash
# Feature
git commit -m "feat(auth): add crypto key authentication"

# Bug fix
git commit -m "fix(database): resolve connection timeout issue"

# Documentation
git commit -m "docs(readme): update installation instructions"

# With body
git commit -m "feat(revenue): add performance multipliers

- Add view count multiplier
- Add recency factor
- Update dashboard display"
```

---

## 🔀 Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts with main
- [ ] Commit messages follow guidelines

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests pass
- [ ] No new warnings
```

### Review Process

1. **Automated Checks**: CI/CD runs tests automatically
2. **Code Review**: Maintainers review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, maintainers will merge

### After Merge

- Delete your branch
- Update your fork
- Celebrate! 🎉

---

## 🐛 Issue Guidelines

### Creating Issues

Use appropriate issue templates:
- Bug Report
- Feature Request
- Documentation Improvement
- Question

### Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `priority: high` - High priority
- `priority: low` - Low priority

### Issue Workflow

1. **Open**: Issue is created
2. **Triaged**: Maintainers review and label
3. **Assigned**: Someone is working on it
4. **In Progress**: Work has started
5. **Review**: PR is open
6. **Closed**: Issue is resolved

---

## 👥 Community

### Communication Channels

- **GitHub Discussions**: For questions and discussions
- **GitHub Issues**: For bugs and feature requests
- **Email**: contact@ysenseai.org for private matters

### Getting Help

- Check [documentation](docs/)
- Search existing issues
- Ask in GitHub Discussions
- Email for private questions

### Recognition

Contributors are recognized in:
- CHANGELOG.md
- GitHub contributors page
- Annual contributor highlights

---

## 🎯 Development Guidelines

### Project Structure

```
src/
├── main.py              # FastAPI backend
├── config.py            # Configuration
├── models.py            # Database models
├── agent_system_v41.py  # AI agents
└── ...

tests/
├── test_auth.py
├── test_database.py
└── ...
```

### Adding New Features

1. **Plan**: Discuss in issue first
2. **Design**: Consider architecture impact
3. **Implement**: Write clean, tested code
4. **Document**: Update relevant docs
5. **Test**: Ensure all tests pass
6. **PR**: Submit for review

### Testing Guidelines

- Write tests for all new features
- Aim for 80%+ code coverage
- Include unit and integration tests
- Mock external API calls

Example test:

```python
def test_create_user_success():
    """Test successful user creation."""
    auth = CryptoAuthManager()
    result = auth.create_user("testuser", "password123", "Standard")
    
    assert result['success'] is True
    assert 'public_key' in result
    assert 'private_key' in result
    assert result['tier'] == "Standard"
```

---

## 📚 Resources

### Documentation

- [Quick Start Guide](QUICK_START_GUIDE.md)
- [Platform Checkup](docs/PLATFORM_CHECKUP_REPORT.md)
- [API Configuration](docs/API_CONFIGURATION_GUIDE.md)

### Tools

- [Black](https://black.readthedocs.io/) - Code formatter
- [Flake8](https://flake8.pycqa.org/) - Linter
- [MyPy](http://mypy-lang.org/) - Type checker
- [Pytest](https://pytest.org/) - Testing framework

### Learning

- [PEP 8](https://pep8.org/) - Python style guide
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

## 🙏 Thank You!

Your contributions make YSense™ better for everyone. We appreciate your time and effort!

**Questions?** Contact us at contact@ysenseai.org

---

**Happy Contributing! 🚀**

*Last Updated: September 30, 2025*
