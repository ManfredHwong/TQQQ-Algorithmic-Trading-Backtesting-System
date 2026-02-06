# TQQQ Trading Strategies Backtesting System

A comprehensive Python-based backtesting framework for analyzing and comparing multiple trading strategies on TQQQ (ProShares UltraPro QQQ) leveraged ETF data.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

## 📋 Overview

This project implements a robust backtesting system to evaluate different trading strategies on historical TQQQ data. It features:

- **Multiple Strategy Support**: Test and compare various trading approaches
- **Comprehensive Analytics**: Detailed performance metrics and trade analysis
- **Professional Visualizations**: Generate charts and performance dashboards
- **Modular Architecture**: Easy to extend with new strategies
- **Export Capabilities**: Save results to CSV for further analysis

## 🎯 Features

### Implemented Strategies

1. **Strategy 1: Always Invested**
   - Buy immediately when no holdings
   - Buy on $0.50 price drops
   - Sell at 1.5% profit target
   - Ensures continuous market exposure

2. **Strategy 2: Tiered Selling (10 Lots)**
   - Buy on $0.50 price drops
   - Split each purchase into 10 lots
   - Progressive profit targets: 1.5%, 4%, 8%, 10%, 12%, 15%, 20%, 25%, 30%, 35%
   - Maximize upside capture

3. **Strategy 3: Moderate Tiers (5 Lots)**
   - Balanced approach with 5 lots per purchase
   - Profit targets: 2%, 5%, 10%, 15%, 20%
   - Good risk/reward balance

4. **Buy & Hold Baseline**
   - Simple buy-and-hold for performance comparison
   - Benchmark for active strategies

### Key Metrics

- Total Return ($ and %)
- Win Rate
- Average Profit per Trade
- Trading Frequency
- Risk Metrics (Standard Deviation, Sharpe-like Ratio)
- Drawdown Analysis
- Open vs. Closed Positions

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8 or higher
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/tqqq-trading-strategies.git
cd tqqq-trading-strategies
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Quick Start

1. **Prepare your data**: Place your TQQQ CSV file in the project directory
   - Required columns: Date (index), Open, High, Low, Close
   - Optional: Volume

2. **Run the analyzer**
```bash
python trading_strategies.py
```

3. **View results**: The program will:
   - Display a comprehensive summary report
   - Export detailed trade logs to CSV
   - (Optional) Generate visualization charts

## 📊 Usage Examples

### Basic Usage

```python
from trading_strategies import TradingStrategyAnalyzer, load_data_from_csv

# Load data
data = load_data_from_csv('TQQQ_historical_data.csv')

# Initialize analyzer
analyzer = TradingStrategyAnalyzer(data, initial_cash=25000)

# Run all strategies
results = analyzer.run_all_strategies()

# Generate report
analyzer.generate_summary_report()

# Export to CSV
analyzer.export_results_to_csv(output_dir='./results')
```

### Custom Strategy Implementation

```python
def custom_strategy(self) -> Dict:
    """Your custom trading strategy."""
    positions = []
    completed_trades = []
    cash = self.initial_cash
    
    for timestamp, row in self.data.iterrows():
        current_price = row['Close']
        
        # Your trading logic here
        # ...
        
    return {
        'strategy_name': 'My Custom Strategy',
        'completed_trades': completed_trades,
        'open_positions': positions,
        # ... other metrics
    }

# Add to analyzer
analyzer.custom_strategy = custom_strategy
```

### Generating Visualizations

```python
from visualization import StrategyVisualizer

# Create visualizer
viz = StrategyVisualizer(results, data)

# Generate dashboard
viz.create_performance_dashboard(save_path='dashboard.png')

# Create equity curve
viz.create_equity_curve(save_path='equity_curve.png')

# Profit distribution
viz.create_profit_distribution(save_path='profit_dist.png')
```

## 📁 Project Structure

```
tqqq-trading-strategies/
│
├── trading_strategies.py      # Main backtesting engine
├── visualization.py            # Charting and visualization module
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contribution guidelines
│
├── examples/                   # Example scripts and notebooks
│   ├── basic_usage.py
│   └── advanced_analysis.ipynb
│
├── tests/                      # Unit tests
│   ├── test_strategies.py
│   └── test_data_loading.py
│
└── docs/                       # Additional documentation
    ├── strategy_details.md
    └── performance_metrics.md
```

## 📈 Sample Output

```
================================================================================
                     STRATEGY PERFORMANCE SUMMARY
================================================================================

Initial Capital: $23,000.00
Data Period: 2023-01-01 to 2024-12-31
Total Trading Days: 504

Strategy                        Final Value    Total Return    Return %    Trades  Open Positions
-------------------------------------------------------------------------------------------
Strategy 1 (Always Invested)    $28,450.00     $5,450.00      23.70%      342     5
Strategy 2 (Tiered Selling)     $31,200.00     $8,200.00      35.65%      1,245   23
Strategy 3 (Moderate Tiers)     $29,800.00     $6,800.00      29.57%      628     12
Buy & Hold (Baseline)           $26,100.00     $3,100.00      13.48%      N/A     N/A
```

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 To-Do / Future Enhancements

- [ ] Add support for additional indicators (RSI, MACD, Bollinger Bands)
- [ ] Implement stop-loss mechanisms
- [ ] Add Monte Carlo simulation for risk analysis
- [ ] Support for multiple assets/comparison
- [ ] Real-time data integration
- [ ] Web-based dashboard
- [ ] Machine learning strategy optimization
- [ ] Position sizing algorithms

## ⚠️ Disclaimer

This software is for educational and research purposes only. It is not financial advice. Trading leveraged ETFs like TQQQ involves substantial risk of loss. Past performance does not guarantee future results. Always do your own research and consult with financial professionals before making investment decisions.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**[Your Name]**
- GitHub: https://github.com/ManfredHwong

## 🙏 Acknowledgments

- Inspired by quantitative trading research and algorithmic trading communities
- Built with Python data science stack (pandas, numpy, matplotlib)
- Special thanks to the open-source community

## 📚 References

- [ProShares TQQQ Official Page](https://www.proshares.com/our-etfs/leveraged-and-inverse/tqqq)
- [Quantitative Trading Resources](https://www.quantstart.com/)
- [Backtesting Best Practices](https://www.investopedia.com/articles/trading/05/030205.asp)

---

⭐ **Star this repository if you found it helpful!**
