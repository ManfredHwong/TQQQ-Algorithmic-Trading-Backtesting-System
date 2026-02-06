# Quick Start Installation Guide

## Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)
- pip (Python package manager)

## Installation Steps

### 1. Clone or Download the Repository

**Option A: Clone with Git**
```bash
git clone https://github.com/yourusername/tqqq-trading-strategies.git
cd tqqq-trading-strategies
```

**Option B: Download ZIP**
1. Download all files from GitHub
2. Extract to a folder
3. Open terminal/command prompt in that folder

### 2. Create Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- pandas (data manipulation)
- numpy (numerical computing)
- matplotlib (visualization)
- seaborn (advanced plotting)

### 4. Verify Installation

```bash
python -c "import pandas, numpy, matplotlib; print('All dependencies installed successfully!')"
```

## Running the Code

### Option 1: Run Main Script

```bash
python trading_strategies.py
```

You'll be prompted to select or provide a TQQQ CSV data file.

### Option 2: Run Example Script

```bash
python examples.py
```

This will create sample data and demonstrate all features.

### Option 3: Use Jupyter Notebook

```bash
jupyter notebook tutorial.ipynb
```

This opens an interactive tutorial in your web browser.

## Data Format

Your TQQQ CSV file should have these columns:
- Date (as index)
- Open
- High
- Low
- Close
- Volume (optional)

Example:
```
Date,Open,High,Low,Close,Volume
2023-01-01,25.50,26.00,25.20,25.80,5000000
2023-01-02,25.85,26.50,25.70,26.30,4500000
...
```

## Running Tests

```bash
pytest test_strategies.py -v
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
- Make sure you activated the virtual environment
- Run: `pip install -r requirements.txt`

### "FileNotFoundError: TQQQ data file not found"
- Place your CSV file in the project directory
- Or use the example script to generate sample data

### Matplotlib display issues
- On macOS: May need to install: `pip install pyobjc-framework-Cocoa`
- On Linux: May need: `sudo apt-get install python3-tk`

## Project Structure

```
tqqq-trading-strategies/
│
├── trading_strategies.py      # Main backtesting engine
├── visualization.py            # Charting module
├── examples.py                 # Example usage scripts
├── test_strategies.py          # Unit tests
├── tutorial.ipynb             # Jupyter tutorial
│
├── README.md                   # Project overview
├── API_DOCUMENTATION.md        # Detailed API docs
├── CONTRIBUTING.md             # Contribution guide
├── PROJECT_SUMMARY.md          # Resume-focused summary
│
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
├── LICENSE                     # MIT License
└── .gitignore                 # Git ignore rules
```

## Next Steps

1. **Read the Documentation**
   - Start with `README.md`
   - Check `API_DOCUMENTATION.md` for detailed API info
   - Review `PROJECT_SUMMARY.md` for project highlights

2. **Try the Examples**
   - Run `examples.py` to see all features
   - Open `tutorial.ipynb` for interactive learning

3. **Customize**
   - Add your own strategies
   - Modify parameters
   - Analyze your own data

4. **Contribute**
   - Read `CONTRIBUTING.md`
   - Submit issues or pull requests
   - Share improvements

## Getting Help

- Check documentation in `API_DOCUMENTATION.md`
- Review examples in `examples.py` and `tutorial.ipynb`
- Open an issue on GitHub
- Contact: [your.email@example.com]

## Quick Command Reference

```bash
# Activate environment
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Run main script
python trading_strategies.py

# Run examples
python examples.py

# Run tests
pytest test_strategies.py -v

# Launch Jupyter
jupyter notebook tutorial.ipynb

# Deactivate environment
deactivate
```

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Ready to start? Run this:**
```bash
python examples.py
```

This will generate sample data and demonstrate all features!
