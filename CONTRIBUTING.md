# Contributing to TQQQ Trading Strategies

First off, thank you for considering contributing to this project! It's people like you that make this tool better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. By participating, you are expected to uphold this standard.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, sample data)
- **Describe the behavior you observed** and what you expected
- **Include your environment details** (Python version, OS, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **Include examples** of how it would work

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the coding standards below
3. **Add tests** if applicable
4. **Update documentation** as needed
5. **Ensure tests pass**
6. **Submit your pull request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/tqqq-trading-strategies.git
cd tqqq-trading-strategies

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use type hints where appropriate

```python
# Good
def calculate_profit(entry_price: float, exit_price: float, quantity: int) -> float:
    """Calculate profit from a trade."""
    return (exit_price - entry_price) * quantity

# Avoid
def calc(e, x, q):
    return (x - e) * q
```

### Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Include examples in docstrings where helpful

```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of function.
    
    Longer description if needed, explaining what the function does,
    any important behavior, or edge cases.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
        
    Example:
        >>> example_function("test", 5)
        True
    """
    if param2 < 0:
        raise ValueError("param2 must be non-negative")
    return len(param1) > param2
```

### Testing

- Write tests for new features
- Maintain or improve code coverage
- Use descriptive test names

```python
def test_calculate_profit_with_positive_return():
    """Test profit calculation when exit price is higher than entry."""
    profit = calculate_profit(entry_price=100.0, exit_price=105.0, quantity=10)
    assert profit == 50.0
```

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be concise (50 chars or less)
- Add detailed description after blank line if needed

```
Add tiered selling strategy with custom targets

- Implement configurable profit tiers
- Add validation for tier percentages
- Update documentation with usage examples
```

## Project Structure Guidelines

### Adding New Strategies

1. Add the strategy method to `TradingStrategyAnalyzer` class
2. Follow the naming convention: `strategy_N_descriptive_name()`
3. Return a dictionary with standard keys
4. Add strategy to `run_all_strategies()` method
5. Update README.md with strategy description
6. Add tests

### Adding New Visualizations

1. Add method to `StrategyVisualizer` class
2. Use consistent styling with existing charts
3. Include save and display options
4. Update documentation

## Testing Guidelines

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_strategies.py

# Run specific test
pytest tests/test_strategies.py::test_strategy_1_basic
```

## Code Review Process

1. All submissions require review
2. Reviewers will check for:
   - Code quality and style
   - Test coverage
   - Documentation
   - Performance considerations
3. Address reviewer comments
4. Once approved, maintainer will merge

## Recognition

Contributors will be:
- Listed in the README.md acknowledgments
- Credited in release notes for significant contributions

## Questions?

Feel free to:
- Open an issue with the "question" label
- Reach out to the maintainer
- Start a discussion in the repository

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
