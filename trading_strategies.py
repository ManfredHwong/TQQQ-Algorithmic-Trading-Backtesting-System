"""
TQQQ Trading Strategies Backtesting System

A comprehensive backtesting framework for analyzing multiple trading strategies
on TQQQ (ProShares UltraPro QQQ) leveraged ETF data.

Author: [Your Name]
License: MIT
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import warnings
import logging

# Suppress pandas warnings for cleaner output
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class Position:
    """Represents an open trading position.
    
    Attributes:
        entry_price (float): Price at which position was entered
        entry_time (pd.Timestamp): Timestamp of position entry
        quantity (int): Number of shares in position
        sell_target (float): Target price for exit
        strategy_name (str): Name of strategy that created position
        position_id (int): Unique identifier for position
        lot_number (int): Lot number for tiered strategies (default: 1)
    """
    
    def __init__(
        self,
        entry_price: float,
        entry_time: pd.Timestamp,
        quantity: int,
        sell_target: float,
        strategy_name: str,
        position_id: int,
        lot_number: int = 1
    ):
        self.entry_price = entry_price
        self.entry_time = entry_time
        self.quantity = quantity
        self.sell_target = sell_target
        self.strategy_name = strategy_name
        self.position_id = position_id
        self.lot_number = lot_number
    
    def __repr__(self) -> str:
        return (f"Position(id={self.position_id}, entry=${self.entry_price:.2f}, "
                f"target=${self.sell_target:.2f}, qty={self.quantity})")


class Trade:
    """Represents a completed trade with all relevant metrics.
    
    Attributes:
        entry_price (float): Entry price of trade
        exit_price (float): Exit price of trade
        entry_time (pd.Timestamp): Entry timestamp
        exit_time (pd.Timestamp): Exit timestamp
        quantity (int): Number of shares traded
        profit_loss (float): Absolute profit/loss in dollars
        return_pct (float): Return percentage
        strategy_name (str): Strategy that executed trade
        position_id (int): Associated position identifier
    """
    
    def __init__(
        self,
        entry_price: float,
        exit_price: float,
        entry_time: pd.Timestamp,
        exit_time: pd.Timestamp,
        quantity: int,
        profit_loss: float,
        return_pct: float,
        strategy_name: str,
        position_id: int
    ):
        self.entry_price = entry_price
        self.exit_price = exit_price
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.quantity = quantity
        self.profit_loss = profit_loss
        self.return_pct = return_pct
        self.strategy_name = strategy_name
        self.position_id = position_id
    
    def __repr__(self) -> str:
        return (f"Trade(id={self.position_id}, P/L=${self.profit_loss:.2f}, "
                f"return={self.return_pct:.2f}%)")


class TradingStrategyAnalyzer:
    """Main analyzer class for backtesting trading strategies on TQQQ.
    
    This class provides a framework for backtesting multiple trading strategies
    on historical OHLCV data, calculating performance metrics, and comparing results.
    
    Attributes:
        data (pd.DataFrame): Prepared OHLCV data with datetime index
        initial_cash (float): Starting capital for backtesting
        strategies (dict): Dictionary of available strategy functions
        results (dict): Results from executed strategies
    
    Example:
        >>> data = pd.read_csv('TQQQ_data.csv', index_col=0, parse_dates=True)
        >>> analyzer = TradingStrategyAnalyzer(data, initial_cash=25000)
        >>> results = analyzer.run_all_strategies()
        >>> analyzer.generate_summary_report()
    """
    
    def __init__(self, data: pd.DataFrame, initial_cash: float = 23000):
        """Initialize the strategy analyzer.
        
        Args:
            data: DataFrame with OHLCV columns and datetime index
            initial_cash: Starting cash amount for backtesting (default: $23,000)
        
        Raises:
            ValueError: If required columns are missing from data
        """
        self.data = self._prepare_data(data)
        self.initial_cash = initial_cash
        self.strategies = {}
        self.results = {}
        logger.info(f"Analyzer initialized with ${initial_cash:,.2f} starting capital")
        
    def _prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare OHLCV data for analysis.
        
        Handles multi-level columns, standardizes column names, and validates
        required columns are present.
        
        Args:
            data: Raw DataFrame with OHLCV data
            
        Returns:
            Cleaned DataFrame ready for backtesting
            
        Raises:
            ValueError: If required columns (Open, High, Low, Close) are missing
        """
        df = data.copy()
        
        # Handle multi-level columns from some data sources
        if hasattr(df.columns, 'levels') or any(isinstance(col, tuple) for col in df.columns):
            if hasattr(df.columns, 'droplevel'):
                df.columns = df.columns.droplevel(1)
            else:
                new_cols = []
                for col in df.columns:
                    if isinstance(col, tuple):
                        new_cols.append(col[0])
                    else:
                        new_cols.append(str(col))
                df.columns = new_cols
        
        # Standardize column names to Title Case
        df.columns = [str(col).strip().title() for col in df.columns]
        
        # Validate required columns
        required_cols = ['Open', 'High', 'Low', 'Close']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Remove NaN values
        original_len = len(df)
        df = df.dropna()
        dropped = original_len - len(df)
        
        if dropped > 0:
            logger.warning(f"Dropped {dropped} rows with NaN values")
        
        logger.info(f"Data prepared: {len(df)} records from {df.index[0]} to {df.index[-1]}")
        return df
    
    def strategy_1_buy_on_drop_sell_at_target(self) -> Dict:
        """Strategy 1: Buy on price drops or when no holdings, sell at fixed target.
        
        Rules:
        - Buy immediately if no active positions (stay invested)
        - Buy 1 share when price drops $0.50 from last purchase
        - Sell when price reaches 1.5% gain
        
        Returns:
            Dictionary with strategy results including trades, positions, and metrics
        """
        logger.info("Running Strategy 1: Buy on $0.50 drop OR immediate buy when no holdings")
        
        positions: List[Position] = []
        completed_trades: List[Trade] = []
        cash = self.initial_cash
        position_id = 0
        last_buy_price: Optional[float] = None
        
        for i, (timestamp, row) in enumerate(self.data.iterrows()):
            current_price = row['Close']
            
            # Execute sells first
            positions_to_remove = []
            for pos in positions:
                if current_price >= pos.sell_target:
                    # Sell position at target
                    profit = (current_price - pos.entry_price) * pos.quantity
                    return_pct = ((current_price - pos.entry_price) / pos.entry_price) * 100
                    
                    trade = Trade(
                        entry_price=pos.entry_price,
                        exit_price=current_price,
                        entry_time=pos.entry_time,
                        exit_time=timestamp,
                        quantity=pos.quantity,
                        profit_loss=profit,
                        return_pct=return_pct,
                        strategy_name=pos.strategy_name,
                        position_id=pos.position_id
                    )
                    completed_trades.append(trade)
                    positions_to_remove.append(pos)
                    cash += current_price * pos.quantity
            
            # Remove sold positions
            for pos in positions_to_remove:
                positions.remove(pos)
            
            # Determine if should buy
            should_buy = False
            buy_reason = ""
            
            # Rule 1: No active holdings - buy immediately to stay invested
            if len(positions) == 0 and cash >= current_price:
                should_buy = True
                buy_reason = "No holdings - immediate buy"
                last_buy_price = current_price
            # Rule 2: Price dropped $0.50 from last buy
            elif (len(positions) > 0 and last_buy_price is not None and 
                  current_price <= last_buy_price - 0.50 and cash >= current_price):
                should_buy = True
                buy_reason = f"Price drop ${last_buy_price - current_price:.2f}"
                last_buy_price = current_price
            
            # Execute buy
            if should_buy:
                position_id += 1
                sell_target = current_price * 1.015  # 1.5% gain target
                
                position = Position(
                    entry_price=current_price,
                    entry_time=timestamp,
                    quantity=1,
                    sell_target=sell_target,
                    strategy_name="Strategy_1",
                    position_id=position_id
                )
                positions.append(position)
                cash -= current_price
                
                # Log progress periodically
                if position_id % 100 == 0:
                    logger.debug(f"Buy #{position_id}: ${current_price:.2f} at "
                               f"{timestamp.strftime('%Y-%m-%d %H:%M')} ({buy_reason})")
        
        # Calculate final portfolio value
        final_position_value = sum(self.data['Close'].iloc[-1] * pos.quantity 
                                   for pos in positions)
        total_final_value = cash + final_position_value
        
        return {
            'strategy_name': 'Strategy 1 (Always Invested)',
            'completed_trades': completed_trades,
            'open_positions': positions,
            'final_cash': cash,
            'final_position_value': final_position_value,
            'total_final_value': total_final_value,
            'total_return': total_final_value - self.initial_cash,
            'return_percentage': ((total_final_value - self.initial_cash) / 
                                self.initial_cash * 100)
        }
    
    def strategy_2_tiered_selling(self) -> Dict:
        """Strategy 2: Buy on price drops, sell in tiers at multiple targets.
        
        Rules:
        - Buy 1 share when price drops $0.50 from last purchase
        - Create 10 lots from each purchase
        - Sell lots at tiered profit targets: 1.5%, 4%, 8%, 10%, 12%, 15%, 20%, 25%, 30%, 35%
        
        Returns:
            Dictionary with strategy results including trades, positions, and metrics
        """
        logger.info("Running Strategy 2: Buy on $0.50 drop with tiered selling")
        
        positions: List[Position] = []
        completed_trades: List[Trade] = []
        cash = self.initial_cash
        position_id = 0
        last_buy_price: Optional[float] = None
        
        # Tiered profit targets (percentages)
        tier_targets = [1.5, 4, 8, 10, 12, 15, 20, 25, 30, 35]
        lots_per_purchase = 10
        
        for i, (timestamp, row) in enumerate(self.data.iterrows()):
            current_price = row['Close']
            
            # Check for sells at tiered targets
            positions_to_remove = []
            for pos in positions:
                if current_price >= pos.sell_target:
                    # Sell the lot
                    profit = (current_price - pos.entry_price) * pos.quantity
                    return_pct = ((current_price - pos.entry_price) / pos.entry_price) * 100
                    
                    trade = Trade(
                        entry_price=pos.entry_price,
                        exit_price=current_price,
                        entry_time=pos.entry_time,
                        exit_time=timestamp,
                        quantity=pos.quantity,
                        profit_loss=profit,
                        return_pct=return_pct,
                        strategy_name=pos.strategy_name,
                        position_id=pos.position_id
                    )
                    completed_trades.append(trade)
                    positions_to_remove.append(pos)
                    cash += current_price * pos.quantity
            
            # Remove sold positions
            for pos in positions_to_remove:
                positions.remove(pos)
            
            # Determine if should buy
            should_buy = False
            if last_buy_price is None:
                should_buy = True
                last_buy_price = current_price
            elif current_price <= last_buy_price - 0.50:
                should_buy = True
                last_buy_price = current_price
            
            # Execute buy with tiered lots
            if should_buy and cash >= current_price:
                position_id += 1
                
                # Create tiered positions (lots)
                for lot_num, target_pct in enumerate(tier_targets, 1):
                    sell_target = current_price * (1 + target_pct / 100)
                    
                    position = Position(
                        entry_price=current_price,
                        entry_time=timestamp,
                        quantity=1,  # Each lot is 1 share
                        sell_target=sell_target,
                        strategy_name="Strategy_2",
                        position_id=position_id,
                        lot_number=lot_num
                    )
                    positions.append(position)
                
                # Deduct cost of all lots
                cash -= current_price * lots_per_purchase
                
                # Log progress
                if position_id % 50 == 0:
                    logger.debug(f"Buy #{position_id}: ${current_price:.2f} at "
                               f"{timestamp.strftime('%Y-%m-%d %H:%M')} (10 tiered lots)")
        
        # Calculate final portfolio value
        final_position_value = sum(self.data['Close'].iloc[-1] * pos.quantity 
                                   for pos in positions)
        total_final_value = cash + final_position_value
        
        return {
            'strategy_name': 'Strategy 2 (Tiered Selling)',
            'completed_trades': completed_trades,
            'open_positions': positions,
            'final_cash': cash,
            'final_position_value': final_position_value,
            'total_final_value': total_final_value,
            'total_return': total_final_value - self.initial_cash,
            'return_percentage': ((total_final_value - self.initial_cash) / 
                                self.initial_cash * 100)
        }
    
    def strategy_3_moderate_tiered(self) -> Dict:
        """Strategy 3: Moderate tiered approach with balanced targets.
        
        Rules:
        - Buy on $0.50 drop or when no holdings
        - Create 5 lots per purchase  
        - Sell lots at targets: 2%, 5%, 10%, 15%, 20%
        
        Returns:
            Dictionary with strategy results including trades, positions, and metrics
        """
        logger.info("Running Strategy 3: Moderate tiered selling (5 lots)")
        
        positions: List[Position] = []
        completed_trades: List[Trade] = []
        cash = self.initial_cash
        position_id = 0
        last_buy_price: Optional[float] = None
        
        # Moderate tier targets
        tier_targets = [2, 5, 10, 15, 20]
        lots_per_purchase = 5
        
        for i, (timestamp, row) in enumerate(self.data.iterrows()):
            current_price = row['Close']
            
            # Execute sells
            positions_to_remove = []
            for pos in positions:
                if current_price >= pos.sell_target:
                    profit = (current_price - pos.entry_price) * pos.quantity
                    return_pct = ((current_price - pos.entry_price) / pos.entry_price) * 100
                    
                    trade = Trade(
                        entry_price=pos.entry_price,
                        exit_price=current_price,
                        entry_time=pos.entry_time,
                        exit_time=timestamp,
                        quantity=pos.quantity,
                        profit_loss=profit,
                        return_pct=return_pct,
                        strategy_name=pos.strategy_name,
                        position_id=pos.position_id
                    )
                    completed_trades.append(trade)
                    positions_to_remove.append(pos)
                    cash += current_price * pos.quantity
            
            for pos in positions_to_remove:
                positions.remove(pos)
            
            # Buy logic: no holdings or price drop
            should_buy = False
            if len(positions) == 0 and cash >= current_price * lots_per_purchase:
                should_buy = True
                last_buy_price = current_price
            elif (last_buy_price is not None and 
                  current_price <= last_buy_price - 0.50 and 
                  cash >= current_price * lots_per_purchase):
                should_buy = True
                last_buy_price = current_price
            
            # Execute buy with tiered lots
            if should_buy:
                position_id += 1
                
                for lot_num, target_pct in enumerate(tier_targets, 1):
                    sell_target = current_price * (1 + target_pct / 100)
                    
                    position = Position(
                        entry_price=current_price,
                        entry_time=timestamp,
                        quantity=1,
                        sell_target=sell_target,
                        strategy_name="Strategy_3",
                        position_id=position_id,
                        lot_number=lot_num
                    )
                    positions.append(position)
                
                cash -= current_price * lots_per_purchase
        
        # Calculate final value
        final_position_value = sum(self.data['Close'].iloc[-1] * pos.quantity 
                                   for pos in positions)
        total_final_value = cash + final_position_value
        
        return {
            'strategy_name': 'Strategy 3 (Moderate Tiers)',
            'completed_trades': completed_trades,
            'open_positions': positions,
            'final_cash': cash,
            'final_position_value': final_position_value,
            'total_final_value': total_final_value,
            'total_return': total_final_value - self.initial_cash,
            'return_percentage': ((total_final_value - self.initial_cash) / 
                                self.initial_cash * 100)
        }
    
    def buy_and_hold_baseline(self) -> Dict:
        """Baseline strategy: Buy and hold for comparison.
        
        Buys maximum shares at start and holds until end.
        
        Returns:
            Dictionary with strategy results
        """
        logger.info("Running Buy & Hold baseline strategy")
        
        initial_price = self.data['Close'].iloc[0]
        final_price = self.data['Close'].iloc[-1]
        shares_bought = int(self.initial_cash / initial_price)
        cash_remaining = self.initial_cash - (shares_bought * initial_price)
        
        final_value = (shares_bought * final_price) + cash_remaining
        total_return = final_value - self.initial_cash
        return_pct = (total_return / self.initial_cash) * 100
        
        return {
            'strategy_name': 'Buy & Hold (Baseline)',
            'shares_bought': shares_bought,
            'initial_price': initial_price,
            'final_price': final_price,
            'final_value': final_value,
            'total_return': total_return,
            'return_percentage': return_pct
        }
    
    def run_all_strategies(self) -> Dict:
        """Execute all trading strategies and store results.
        
        Returns:
            Dictionary containing results from all strategies
        """
        logger.info("=" * 60)
        logger.info("Starting backtest for all strategies")
        logger.info("=" * 60)
        
        self.results = {
            'strategy_1': self.strategy_1_buy_on_drop_sell_at_target(),
            'strategy_2': self.strategy_2_tiered_selling(),
            'strategy_3': self.strategy_3_moderate_tiered(),
            'buy_hold': self.buy_and_hold_baseline()
        }
        
        logger.info("All strategies completed successfully")
        return self.results
    
    def generate_summary_report(self) -> None:
        """Generate and print comprehensive summary report of all strategies."""
        if not self.results:
            logger.warning("No results available. Run strategies first.")
            return
        
        print("\n" + "=" * 80)
        print(" " * 25 + "STRATEGY PERFORMANCE SUMMARY")
        print("=" * 80)
        
        # Summary table
        summary_data = []
        for key, result in self.results.items():
            final_val = result.get('total_final_value', result.get('final_value', 0))
            summary_data.append({
                'Strategy': result['strategy_name'],
                'Final Value': f"${final_val:,.2f}",
                'Total Return': f"${result['total_return']:,.2f}",
                'Return %': f"{result['return_percentage']:.2f}%",
                'Trades': len(result.get('completed_trades', [])) if 'completed_trades' in result else 'N/A',
                'Open Positions': len(result.get('open_positions', [])) if 'open_positions' in result else 'N/A'
            })
        
        df_summary = pd.DataFrame(summary_data)
        print(f"\nInitial Capital: ${self.initial_cash:,.2f}")
        print(f"Data Period: {self.data.index[0].strftime('%Y-%m-%d')} to "
              f"{self.data.index[-1].strftime('%Y-%m-%d')}")
        print(f"Total Trading Days: {len(self.data)}\n")
        print(df_summary.to_string(index=False))
        
        # Detailed analysis for each active strategy
        for strategy_key, result in self.results.items():
            if strategy_key == 'buy_hold':
                continue
            
            print(f"\n{'-' * 80}")
            print(f"📈 {result['strategy_name']} - Detailed Analysis")
            print(f"{'-' * 80}")
            
            trades = result.get('completed_trades', [])
            if trades:
                profits = [t.profit_loss for t in trades]
                returns = [t.return_pct for t in trades]
                
                winning_trades = [p for p in profits if p > 0]
                losing_trades = [p for p in profits if p < 0]
                
                print(f"Total Completed Trades: {len(trades)}")
                print(f"Open Positions: {len(result.get('open_positions', []))}")
                print(f"\nTrade Statistics:")
                print(f"  Winning Trades: {len(winning_trades)} ({len(winning_trades)/len(trades)*100:.1f}%)")
                print(f"  Losing Trades: {len(losing_trades)} ({len(losing_trades)/len(trades)*100:.1f}%)")
                print(f"  Average Profit per Trade: ${np.mean(profits):.2f}")
                print(f"  Average Return per Trade: {np.mean(returns):.2f}%")
                print(f"  Best Trade: ${max(profits):.2f} ({max(returns):.2f}%)")
                print(f"  Worst Trade: ${min(profits):.2f} ({min(returns):.2f}%)")
                print(f"  Total Profit from Trades: ${sum(profits):.2f}")
                
                # Trading frequency
                total_days = (self.data.index[-1] - self.data.index[0]).days
                trades_per_day = len(trades) / total_days if total_days > 0 else 0
                print(f"  Trading Frequency: {trades_per_day:.3f} trades/day")
                
                # Risk metrics
                if len(returns) > 1:
                    sharpe_approx = np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
                    print(f"  Return Std Dev: {np.std(returns):.2f}%")
                    print(f"  Sharpe-like Ratio: {sharpe_approx:.2f}")
            else:
                print("No completed trades for this strategy")
    
    def export_results_to_csv(self, output_dir: str = ".") -> List[str]:
        """Export detailed trade results to CSV files.
        
        Args:
            output_dir: Directory to save CSV files (default: current directory)
            
        Returns:
            List of filenames that were created
        """
        if not self.results:
            logger.warning("No results to export. Run strategies first.")
            return []
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        created_files = []
        
        for strategy_key, result in self.results.items():
            if 'completed_trades' in result and result['completed_trades']:
                trades_data = []
                for trade in result['completed_trades']:
                    trades_data.append({
                        'Entry_Time': trade.entry_time,
                        'Exit_Time': trade.exit_time,
                        'Entry_Price': trade.entry_price,
                        'Exit_Price': trade.exit_price,
                        'Quantity': trade.quantity,
                        'Profit_Loss': trade.profit_loss,
                        'Return_Pct': trade.return_pct,
                        'Position_ID': trade.position_id,
                        'Hold_Duration': (trade.exit_time - trade.entry_time).total_seconds() / 3600  # hours
                    })
                
                trades_df = pd.DataFrame(trades_data)
                filename = output_path / f"TQQQ_{strategy_key}_trades_{timestamp}.csv"
                trades_df.to_csv(filename, index=False)
                created_files.append(str(filename))
                logger.info(f"Exported {result['strategy_name']} trades to: {filename}")
        
        return created_files


def load_data_from_csv(filename: Optional[str] = None) -> Optional[pd.DataFrame]:
    """Load TQQQ data from CSV file.
    
    Args:
        filename: Path to CSV file. If None, will search for TQQQ*.csv files
        
    Returns:
        DataFrame with OHLCV data, or None if loading fails
    """
    if filename is None:
        import glob
        logger.info("Looking for TQQQ data files...")
        csv_files = glob.glob("TQQQ*.csv")
        
        if csv_files:
            logger.info(f"Found {len(csv_files)} CSV file(s)")
            for i, file in enumerate(csv_files, 1):
                print(f"  {i}. {file}")
            
            try:
                choice = int(input("Select file number: ")) - 1
                filename = csv_files[choice]
            except (ValueError, IndexError):
                filename = csv_files[0]
                logger.info(f"Using first file: {filename}")
        else:
            filename = input("Enter TQQQ CSV filename: ")
    
    try:
        # Attempt to read with datetime index
        try:
            df = pd.read_csv(filename, index_col=0, parse_dates=True)
        except Exception:
            df = pd.read_csv(filename, index_col=0)
            df.index = pd.to_datetime(df.index)
        
        logger.info(f"Successfully loaded {len(df)} records from {filename}")
        return df
    
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        return None
    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
        return None


def main():
    """Main execution function for running the backtesting system."""
    print("\n" + "=" * 80)
    print(" " * 20 + "🎯 TQQQ TRADING STRATEGIES ANALYZER")
    print("=" * 80 + "\n")
    
    # Load data
    data = load_data_from_csv()
    if data is None:
        logger.error("Could not load data. Exiting.")
        return
    
    # Initialize analyzer
    try:
        analyzer = TradingStrategyAnalyzer(data, initial_cash=23000)
    except ValueError as e:
        logger.error(f"Error initializing analyzer: {e}")
        return
    
    # Run all strategies
    try:
        results = analyzer.run_all_strategies()
    except Exception as e:
        logger.error(f"Error running strategies: {e}", exc_info=True)
        return
    
    # Generate report
    analyzer.generate_summary_report()
    
    # Export detailed results
    try:
        exported_files = analyzer.export_results_to_csv()
        if exported_files:
            print(f"\n✅ Exported {len(exported_files)} detailed trade report(s)")
    except Exception as e:
        logger.warning(f"Could not export results: {e}")
    
    print(f"\n{'=' * 80}")
    print("✅ Analysis complete!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
