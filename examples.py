"""
Example usage script demonstrating the TQQQ Trading Strategies Backtesting System.

This script shows how to:
1. Load historical data
2. Run backtesting analysis
3. Generate reports and visualizations
4. Export results
"""

import pandas as pd
from pathlib import Path
from trading_strategies import TradingStrategyAnalyzer, load_data_from_csv
from visualization import StrategyVisualizer


def example_basic_usage():
    """Demonstrate basic usage of the backtesting system."""
    print("=" * 80)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 80)
    
    # Load data (replace with your actual data file)
    data = load_data_from_csv('TQQQ_sample_data.csv')
    
    if data is None:
        print("Error: Could not load data. Please ensure TQQQ_sample_data.csv exists.")
        return
    
    # Initialize analyzer with $25,000 starting capital
    analyzer = TradingStrategyAnalyzer(data, initial_cash=25000)
    
    # Run all strategies
    results = analyzer.run_all_strategies()
    
    # Display summary report
    analyzer.generate_summary_report()
    
    # Export results to CSV
    exported_files = analyzer.export_results_to_csv(output_dir='./results')
    print(f"\n✅ Exported {len(exported_files)} result files")


def example_custom_analysis():
    """Demonstrate custom analysis and visualization."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Custom Analysis with Visualizations")
    print("=" * 80)
    
    # Load data
    data = load_data_from_csv('TQQQ_sample_data.csv')
    
    if data is None:
        print("Error: Could not load data.")
        return
    
    # Run analysis
    analyzer = TradingStrategyAnalyzer(data, initial_cash=25000)
    results = analyzer.run_all_strategies()
    
    # Create visualizer
    viz = StrategyVisualizer(results, data)
    
    # Generate comprehensive dashboard
    dashboard_path = viz.create_performance_dashboard(
        save_path='./results/performance_dashboard.png',
        show_plot=False  # Set to True to display
    )
    print(f"📊 Dashboard saved to: {dashboard_path}")
    
    # Generate equity curve
    equity_path = viz.create_equity_curve(
        save_path='./results/equity_curve.png',
        show_plot=False
    )
    print(f"📈 Equity curve saved to: {equity_path}")
    
    # Generate profit distribution
    profit_path = viz.create_profit_distribution(
        save_path='./results/profit_distribution.png',
        show_plot=False
    )
    print(f"📊 Profit distribution saved to: {profit_path}")


def example_single_strategy():
    """Demonstrate running a single strategy."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Running Single Strategy")
    print("=" * 80)
    
    # Load data
    data = load_data_from_csv('TQQQ_sample_data.csv')
    
    if data is None:
        print("Error: Could not load data.")
        return
    
    # Initialize analyzer
    analyzer = TradingStrategyAnalyzer(data, initial_cash=25000)
    
    # Run only Strategy 1
    print("\nRunning Strategy 1 only...")
    result = analyzer.strategy_1_buy_on_drop_sell_at_target()
    
    # Display results
    print(f"\nStrategy: {result['strategy_name']}")
    print(f"Final Value: ${result['total_final_value']:,.2f}")
    print(f"Total Return: ${result['total_return']:,.2f} ({result['return_percentage']:.2f}%)")
    print(f"Completed Trades: {len(result['completed_trades'])}")
    print(f"Open Positions: {len(result['open_positions'])}")
    
    # Show some trade details
    if result['completed_trades']:
        print("\nSample Trades:")
        for i, trade in enumerate(result['completed_trades'][:5], 1):
            print(f"  Trade {i}: ${trade.profit_loss:.2f} "
                  f"({trade.return_pct:.2f}%) - "
                  f"Entry: ${trade.entry_price:.2f}, Exit: ${trade.exit_price:.2f}")


def example_comparative_analysis():
    """Demonstrate comparative analysis between strategies."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Comparative Strategy Analysis")
    print("=" * 80)
    
    # Load data
    data = load_data_from_csv('TQQQ_sample_data.csv')
    
    if data is None:
        print("Error: Could not load data.")
        return
    
    # Run analysis
    analyzer = TradingStrategyAnalyzer(data, initial_cash=25000)
    results = analyzer.run_all_strategies()
    
    # Compare strategies
    print("\n📊 Strategy Comparison:")
    print("-" * 80)
    
    # Sort by return percentage
    sorted_strategies = sorted(
        results.items(),
        key=lambda x: x[1]['return_percentage'],
        reverse=True
    )
    
    print(f"{'Rank':<6} {'Strategy':<30} {'Return %':<12} {'Final Value':<15}")
    print("-" * 80)
    
    for rank, (key, result) in enumerate(sorted_strategies, 1):
        final_val = result.get('total_final_value', result.get('final_value', 0))
        print(f"{rank:<6} {result['strategy_name']:<30} "
              f"{result['return_percentage']:>10.2f}% "
              f"${final_val:>13,.2f}")
    
    # Find best strategy
    best_strategy_key, best_result = sorted_strategies[0]
    print(f"\n🏆 Best Performing Strategy: {best_result['strategy_name']}")
    print(f"   Return: {best_result['return_percentage']:.2f}%")
    
    # Calculate outperformance vs buy & hold
    buy_hold_return = results['buy_hold']['return_percentage']
    outperformance = best_result['return_percentage'] - buy_hold_return
    print(f"   Outperformance vs Buy & Hold: {outperformance:.2f}%")


def create_sample_data():
    """Create sample TQQQ data for testing (if no real data available)."""
    print("\nCreating sample TQQQ data for demonstration...")
    
    # Generate sample data (simplified)
    import numpy as np
    
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    
    # Simulate TQQQ-like price movement (simplified random walk)
    np.random.seed(42)
    initial_price = 25.0
    returns = np.random.normal(0.001, 0.03, len(dates))  # Daily returns
    prices = initial_price * np.exp(np.cumsum(returns))
    
    # Create OHLCV data
    df = pd.DataFrame({
        'Open': prices * (1 + np.random.uniform(-0.01, 0.01, len(dates))),
        'High': prices * (1 + np.random.uniform(0, 0.02, len(dates))),
        'Low': prices * (1 - np.random.uniform(0, 0.02, len(dates))),
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, len(dates))
    }, index=dates)
    
    # Save to CSV
    df.to_csv('TQQQ_sample_data.csv')
    print(f"✅ Sample data created: TQQQ_sample_data.csv ({len(df)} records)")
    
    return df


def main():
    """Run all examples."""
    # Create sample data if needed
    if not Path('TQQQ_sample_data.csv').exists():
        print("No data file found. Creating sample data...")
        create_sample_data()
    
    # Create results directory
    Path('./results').mkdir(exist_ok=True)
    
    # Run examples
    try:
        example_basic_usage()
        example_single_strategy()
        example_comparative_analysis()
        example_custom_analysis()
        
        print("\n" + "=" * 80)
        print("✅ All examples completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
