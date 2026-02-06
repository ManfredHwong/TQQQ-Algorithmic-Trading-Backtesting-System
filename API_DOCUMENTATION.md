# API Documentation

## Table of Contents

1. [Core Classes](#core-classes)
2. [Trading Strategies](#trading-strategies)
3. [Visualization](#visualization)
4. [Utility Functions](#utility-functions)

---

## Core Classes

### `Position`

Represents an open trading position.

**Attributes:**
- `entry_price` (float): Price at which position was entered
- `entry_time` (pd.Timestamp): Timestamp of position entry
- `quantity` (int): Number of shares in position
- `sell_target` (float): Target price for exit
- `strategy_name` (str): Name of strategy that created position
- `position_id` (int): Unique identifier for position
- `lot_number` (int): Lot number for tiered strategies (default: 1)

**Example:**
```python
position = Position(
    entry_price=100.50,
    entry_time=pd.Timestamp('2023-01-15'),
    quantity=10,
    sell_target=102.00,
    strategy_name='Strategy_1',
    position_id=1
)
```

---

### `Trade`

Represents a completed trade with all relevant metrics.

**Attributes:**
- `entry_price` (float): Entry price of trade
- `exit_price` (float): Exit price of trade
- `entry_time` (pd.Timestamp): Entry timestamp
- `exit_time` (pd.Timestamp): Exit timestamp
- `quantity` (int): Number of shares traded
- `profit_loss` (float): Absolute profit/loss in dollars
- `return_pct` (float): Return percentage
- `strategy_name` (str): Strategy that executed trade
- `position_id` (int): Associated position identifier

**Example:**
```python
trade = Trade(
    entry_price=100.50,
    exit_price=102.00,
    entry_time=pd.Timestamp('2023-01-15'),
    exit_time=pd.Timestamp('2023-01-20'),
    quantity=10,
    profit_loss=15.00,
    return_pct=1.49,
    strategy_name='Strategy_1',
    position_id=1
)
```

---

### `TradingStrategyAnalyzer`

Main analyzer class for backtesting trading strategies.

#### Initialization

```python
TradingStrategyAnalyzer(data: pd.DataFrame, initial_cash: float = 23000)
```

**Parameters:**
- `data`: DataFrame with OHLCV columns and datetime index
  - Required columns: Open, High, Low, Close
  - Optional: Volume
- `initial_cash`: Starting cash amount (default: $23,000)

**Raises:**
- `ValueError`: If required columns are missing

**Example:**
```python
data = pd.read_csv('TQQQ_data.csv', index_col=0, parse_dates=True)
analyzer = TradingStrategyAnalyzer(data, initial_cash=25000)
```

#### Methods

##### `run_all_strategies()`

Execute all trading strategies and store results.

**Returns:**
- Dictionary containing results from all strategies

**Example:**
```python
results = analyzer.run_all_strategies()
```

##### `strategy_1_buy_on_drop_sell_at_target()`

Execute Strategy 1: Buy on drops or when no holdings, sell at fixed target.

**Rules:**
- Buy immediately if no active positions
- Buy 1 share when price drops $0.50 from last purchase
- Sell when price reaches 1.5% gain

**Returns:**
- Dictionary with strategy results

##### `strategy_2_tiered_selling()`

Execute Strategy 2: Buy on drops, sell in tiers at multiple targets.

**Rules:**
- Buy on $0.50 price drops
- Split into 10 lots per purchase
- Progressive targets: 1.5%, 4%, 8%, 10%, 12%, 15%, 20%, 25%, 30%, 35%

**Returns:**
- Dictionary with strategy results

##### `strategy_3_moderate_tiered()`

Execute Strategy 3: Moderate tiered approach.

**Rules:**
- Buy on drops or when no holdings
- Create 5 lots per purchase
- Targets: 2%, 5%, 10%, 15%, 20%

**Returns:**
- Dictionary with strategy results

##### `buy_and_hold_baseline()`

Execute baseline buy-and-hold strategy.

**Returns:**
- Dictionary with strategy results

##### `generate_summary_report()`

Generate and print comprehensive summary report.

**Example:**
```python
analyzer.generate_summary_report()
```

##### `export_results_to_csv(output_dir: str = ".")`

Export detailed trade results to CSV files.

**Parameters:**
- `output_dir`: Directory to save CSV files (default: current directory)

**Returns:**
- List of filenames that were created

**Example:**
```python
files = analyzer.export_results_to_csv(output_dir='./results')
```

---

## Trading Strategies

### Strategy Result Dictionary Structure

All strategies return a dictionary with the following structure:

```python
{
    'strategy_name': str,           # Display name of strategy
    'completed_trades': List[Trade], # List of completed Trade objects
    'open_positions': List[Position], # List of open Position objects
    'final_cash': float,             # Remaining cash
    'final_position_value': float,   # Value of open positions
    'total_final_value': float,      # Total portfolio value
    'total_return': float,           # Absolute return ($)
    'return_percentage': float       # Percentage return
}
```

### Adding Custom Strategies

To add a custom strategy:

1. Define a method in `TradingStrategyAnalyzer` class
2. Follow the naming convention: `strategy_N_description()`
3. Return a dictionary with the standard structure
4. Add to `run_all_strategies()` method

**Example:**
```python
def strategy_custom_example(self) -> Dict:
    """My custom trading strategy."""
    positions = []
    completed_trades = []
    cash = self.initial_cash
    position_id = 0
    
    for timestamp, row in self.data.iterrows():
        current_price = row['Close']
        
        # Your custom logic here
        # ...
    
    # Calculate final value
    final_position_value = sum(
        self.data['Close'].iloc[-1] * pos.quantity 
        for pos in positions
    )
    total_final_value = cash + final_position_value
    
    return {
        'strategy_name': 'My Custom Strategy',
        'completed_trades': completed_trades,
        'open_positions': positions,
        'final_cash': cash,
        'final_position_value': final_position_value,
        'total_final_value': total_final_value,
        'total_return': total_final_value - self.initial_cash,
        'return_percentage': (
            (total_final_value - self.initial_cash) / self.initial_cash * 100
        )
    }
```

---

## Visualization

### `StrategyVisualizer`

Creates comprehensive visualizations for backtesting results.

#### Initialization

```python
StrategyVisualizer(results: Dict, data: pd.DataFrame)
```

**Parameters:**
- `results`: Dictionary of strategy results from analyzer
- `data`: OHLCV DataFrame with datetime index

**Example:**
```python
viz = StrategyVisualizer(results, data)
```

#### Methods

##### `create_performance_dashboard(save_path=None, show_plot=True)`

Create comprehensive performance dashboard.

**Parameters:**
- `save_path`: Optional path to save figure
- `show_plot`: Whether to display plot (default: True)

**Returns:**
- Path to saved figure file

**Example:**
```python
path = viz.create_performance_dashboard(
    save_path='dashboard.png',
    show_plot=False
)
```

##### `create_equity_curve(save_path=None, show_plot=True)`

Create equity curve showing portfolio value over time.

**Parameters:**
- `save_path`: Optional path to save figure
- `show_plot`: Whether to display plot

**Returns:**
- Path to saved figure

**Example:**
```python
path = viz.create_equity_curve(save_path='equity.png')
```

##### `create_profit_distribution(save_path=None, show_plot=True)`

Create histogram of profit/loss distribution.

**Parameters:**
- `save_path`: Optional path to save figure
- `show_plot`: Whether to display plot

**Returns:**
- Path to saved figure

**Example:**
```python
path = viz.create_profit_distribution(save_path='distribution.png')
```

---

## Utility Functions

### `load_data_from_csv(filename=None)`

Load TQQQ data from CSV file.

**Parameters:**
- `filename`: Path to CSV file. If None, will search for TQQQ*.csv files

**Returns:**
- DataFrame with OHLCV data, or None if loading fails

**Example:**
```python
# Load specific file
data = load_data_from_csv('TQQQ_2023_data.csv')

# Auto-search for TQQQ files
data = load_data_from_csv()
```

---

## Performance Metrics

### Calculated Metrics

The system automatically calculates the following metrics:

**Return Metrics:**
- Total Return ($)
- Return Percentage (%)
- Average Return per Trade (%)

**Trade Metrics:**
- Number of Completed Trades
- Number of Open Positions
- Win Rate (%)
- Average Profit per Trade ($)
- Best Trade ($ and %)
- Worst Trade ($ and %)

**Risk Metrics:**
- Return Standard Deviation
- Sharpe-like Ratio (simplified)
- Trading Frequency (trades/day)

**Portfolio Metrics:**
- Final Cash
- Final Position Value
- Total Final Value

---

## Error Handling

### Common Errors

**ValueError: Missing required columns**
```python
# Ensure your data has: Open, High, Low, Close
df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
```

**FileNotFoundError**
```python
# Check file path is correct
data = load_data_from_csv('path/to/TQQQ_data.csv')
```

**Empty Results**
```python
# Run strategies before generating reports
results = analyzer.run_all_strategies()
analyzer.generate_summary_report()  # Now works
```

---

## Best Practices

1. **Data Preparation:**
   - Ensure datetime index is properly formatted
   - Check for missing values (NaN)
   - Verify OHLC relationships (High >= Open/Close, Low <= Open/Close)

2. **Strategy Development:**
   - Start with simple logic
   - Test on small datasets first
   - Validate results make sense
   - Add logging for debugging

3. **Performance:**
   - Use vectorized operations where possible
   - Limit number of positions for complex strategies
   - Consider data timeframe (daily vs intraday)

4. **Analysis:**
   - Compare against buy-and-hold baseline
   - Check win rate and average returns
   - Review trade distribution
   - Examine equity curve for consistency

---

## Examples

See `examples.py` for comprehensive usage examples including:
- Basic backtesting workflow
- Custom strategy implementation
- Visualization generation
- Comparative analysis
- Result export

---

## Support

For issues, questions, or contributions:
- GitHub Issues: [Report a bug](https://github.com/yourusername/tqqq-trading-strategies/issues)
- Documentation: [Full docs](https://github.com/yourusername/tqqq-trading-strategies#readme)
