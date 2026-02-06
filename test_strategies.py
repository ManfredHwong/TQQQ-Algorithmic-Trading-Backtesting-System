"""
Unit tests for the TQQQ Trading Strategies Backtesting System.

Run with: pytest tests/test_strategies.py
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from trading_strategies import (
    Position, Trade, TradingStrategyAnalyzer, load_data_from_csv
)


@pytest.fixture
def sample_data():
    """Create sample OHLCV data for testing."""
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    
    np.random.seed(42)
    initial_price = 25.0
    returns = np.random.normal(0.001, 0.02, len(dates))
    prices = initial_price * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'Open': prices * (1 + np.random.uniform(-0.01, 0.01, len(dates))),
        'High': prices * (1 + np.random.uniform(0, 0.02, len(dates))),
        'Low': prices * (1 - np.random.uniform(0, 0.02, len(dates))),
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, len(dates))
    }, index=dates)
    
    return df


@pytest.fixture
def analyzer(sample_data):
    """Create analyzer instance with sample data."""
    return TradingStrategyAnalyzer(sample_data, initial_cash=25000)


class TestPosition:
    """Test the Position class."""
    
    def test_position_creation(self):
        """Test creating a Position object."""
        pos = Position(
            entry_price=100.0,
            entry_time=pd.Timestamp('2023-01-01'),
            quantity=10,
            sell_target=105.0,
            strategy_name='Test',
            position_id=1
        )
        
        assert pos.entry_price == 100.0
        assert pos.quantity == 10
        assert pos.sell_target == 105.0
        assert pos.position_id == 1
        assert pos.lot_number == 1  # Default value
    
    def test_position_repr(self):
        """Test Position string representation."""
        pos = Position(
            entry_price=100.0,
            entry_time=pd.Timestamp('2023-01-01'),
            quantity=10,
            sell_target=105.0,
            strategy_name='Test',
            position_id=1
        )
        
        repr_str = repr(pos)
        assert 'Position' in repr_str
        assert 'id=1' in repr_str
        assert 'entry=$100.00' in repr_str


class TestTrade:
    """Test the Trade class."""
    
    def test_trade_creation(self):
        """Test creating a Trade object."""
        trade = Trade(
            entry_price=100.0,
            exit_price=105.0,
            entry_time=pd.Timestamp('2023-01-01'),
            exit_time=pd.Timestamp('2023-01-05'),
            quantity=10,
            profit_loss=50.0,
            return_pct=5.0,
            strategy_name='Test',
            position_id=1
        )
        
        assert trade.entry_price == 100.0
        assert trade.exit_price == 105.0
        assert trade.profit_loss == 50.0
        assert trade.return_pct == 5.0
    
    def test_trade_repr(self):
        """Test Trade string representation."""
        trade = Trade(
            entry_price=100.0,
            exit_price=105.0,
            entry_time=pd.Timestamp('2023-01-01'),
            exit_time=pd.Timestamp('2023-01-05'),
            quantity=10,
            profit_loss=50.0,
            return_pct=5.0,
            strategy_name='Test',
            position_id=1
        )
        
        repr_str = repr(trade)
        assert 'Trade' in repr_str
        assert 'P/L=$50.00' in repr_str
        assert 'return=5.00%' in repr_str


class TestTradingStrategyAnalyzer:
    """Test the TradingStrategyAnalyzer class."""
    
    def test_analyzer_initialization(self, sample_data):
        """Test analyzer initialization."""
        analyzer = TradingStrategyAnalyzer(sample_data, initial_cash=25000)
        
        assert analyzer.initial_cash == 25000
        assert len(analyzer.data) > 0
        assert 'Close' in analyzer.data.columns
        assert analyzer.results == {}
    
    def test_data_preparation(self, sample_data):
        """Test data preparation logic."""
        analyzer = TradingStrategyAnalyzer(sample_data)
        
        # Check required columns exist
        assert 'Open' in analyzer.data.columns
        assert 'High' in analyzer.data.columns
        assert 'Low' in analyzer.data.columns
        assert 'Close' in analyzer.data.columns
        
        # Check no NaN values
        assert not analyzer.data.isnull().any().any()
    
    def test_missing_columns_raises_error(self):
        """Test that missing required columns raises ValueError."""
        bad_data = pd.DataFrame({
            'Date': pd.date_range('2023-01-01', periods=10),
            'Price': np.random.rand(10)
        })
        bad_data.set_index('Date', inplace=True)
        
        with pytest.raises(ValueError, match="Missing required columns"):
            TradingStrategyAnalyzer(bad_data)
    
    def test_strategy_1_returns_valid_results(self, analyzer):
        """Test Strategy 1 returns expected result structure."""
        result = analyzer.strategy_1_buy_on_drop_sell_at_target()
        
        assert 'strategy_name' in result
        assert 'completed_trades' in result
        assert 'open_positions' in result
        assert 'final_cash' in result
        assert 'total_final_value' in result
        assert 'return_percentage' in result
        
        # Check types
        assert isinstance(result['completed_trades'], list)
        assert isinstance(result['open_positions'], list)
        assert isinstance(result['final_cash'], (int, float))
    
    def test_strategy_2_returns_valid_results(self, analyzer):
        """Test Strategy 2 returns expected result structure."""
        result = analyzer.strategy_2_tiered_selling()
        
        assert 'strategy_name' in result
        assert 'completed_trades' in result
        assert 'open_positions' in result
        assert result['strategy_name'] == 'Strategy 2 (Tiered Selling)'
    
    def test_strategy_3_returns_valid_results(self, analyzer):
        """Test Strategy 3 returns expected result structure."""
        result = analyzer.strategy_3_moderate_tiered()
        
        assert 'strategy_name' in result
        assert 'completed_trades' in result
        assert result['strategy_name'] == 'Strategy 3 (Moderate Tiers)'
    
    def test_buy_hold_baseline(self, analyzer):
        """Test buy and hold baseline strategy."""
        result = analyzer.buy_and_hold_baseline()
        
        assert 'strategy_name' in result
        assert 'shares_bought' in result
        assert 'initial_price' in result
        assert 'final_price' in result
        assert 'final_value' in result
        assert 'return_percentage' in result
        
        # Basic sanity check
        assert result['shares_bought'] > 0
        assert result['final_value'] > 0
    
    def test_run_all_strategies(self, analyzer):
        """Test running all strategies at once."""
        results = analyzer.run_all_strategies()
        
        assert 'strategy_1' in results
        assert 'strategy_2' in results
        assert 'strategy_3' in results
        assert 'buy_hold' in results
        
        # Check each has required fields
        for key, result in results.items():
            assert 'strategy_name' in result
            assert 'return_percentage' in result
    
    def test_final_value_greater_than_zero(self, analyzer):
        """Test that all strategies end with positive portfolio value."""
        results = analyzer.run_all_strategies()
        
        for key, result in results.items():
            final_val = result.get('total_final_value', result.get('final_value', 0))
            assert final_val > 0, f"{result['strategy_name']} has invalid final value"
    
    def test_export_results_to_csv(self, analyzer, tmp_path):
        """Test exporting results to CSV."""
        # Run strategies first
        analyzer.run_all_strategies()
        
        # Export to temp directory
        files = analyzer.export_results_to_csv(output_dir=str(tmp_path))
        
        # Should create CSV files for strategies with trades
        assert len(files) > 0
        
        # Check files exist
        for filepath in files:
            assert Path(filepath).exists()
            
            # Check CSV can be read
            df = pd.read_csv(filepath)
            assert len(df) > 0
            assert 'Entry_Price' in df.columns
            assert 'Exit_Price' in df.columns
            assert 'Profit_Loss' in df.columns


class TestDataLoading:
    """Test data loading functionality."""
    
    def test_load_data_from_existing_file(self, tmp_path, sample_data):
        """Test loading data from CSV file."""
        # Save sample data
        csv_path = tmp_path / "test_data.csv"
        sample_data.to_csv(csv_path)
        
        # Load it back
        loaded_data = load_data_from_csv(str(csv_path))
        
        assert loaded_data is not None
        assert len(loaded_data) == len(sample_data)
        assert 'Close' in loaded_data.columns
    
    def test_load_nonexistent_file_returns_none(self):
        """Test that loading non-existent file returns None."""
        result = load_data_from_csv('nonexistent_file_12345.csv')
        assert result is None


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_analyzer_with_small_dataset(self):
        """Test analyzer with very small dataset."""
        # Create minimal dataset
        small_data = pd.DataFrame({
            'Open': [25.0, 25.5],
            'High': [25.5, 26.0],
            'Low': [24.8, 25.3],
            'Close': [25.2, 25.8],
            'Volume': [1000000, 1000000]
        }, index=pd.date_range('2023-01-01', periods=2))
        
        analyzer = TradingStrategyAnalyzer(small_data, initial_cash=1000)
        result = analyzer.strategy_1_buy_on_drop_sell_at_target()
        
        # Should still return valid result structure
        assert 'strategy_name' in result
        assert 'total_final_value' in result
    
    def test_analyzer_with_insufficient_funds(self):
        """Test analyzer with very low initial cash."""
        dates = pd.date_range('2023-01-01', periods=10)
        data = pd.DataFrame({
            'Open': [1000] * 10,
            'High': [1010] * 10,
            'Low': [990] * 10,
            'Close': [1000] * 10,
            'Volume': [1000000] * 10
        }, index=dates)
        
        # Very low cash - can't afford any shares
        analyzer = TradingStrategyAnalyzer(data, initial_cash=100)
        result = analyzer.strategy_1_buy_on_drop_sell_at_target()
        
        # Should complete without errors
        assert result['completed_trades'] == []
        assert result['final_cash'] == 100


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
