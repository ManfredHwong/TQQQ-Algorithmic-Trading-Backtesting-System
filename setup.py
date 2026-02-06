"""
Setup script for TQQQ Trading Strategies Backtesting System.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="tqqq-trading-strategies",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive backtesting framework for TQQQ trading strategies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tqqq-trading-strategies",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "matplotlib>=3.6.0",
        "seaborn>=0.12.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.2.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "notebook>=6.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tqqq-backtest=trading_strategies:main",
        ],
    },
    include_package_data=True,
    keywords="trading backtesting TQQQ quantitative-finance algorithmic-trading",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/tqqq-trading-strategies/issues",
        "Source": "https://github.com/yourusername/tqqq-trading-strategies",
        "Documentation": "https://github.com/yourusername/tqqq-trading-strategies#readme",
    },
)
