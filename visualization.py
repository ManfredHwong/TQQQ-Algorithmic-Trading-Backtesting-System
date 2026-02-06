"""
Visualization module for trading strategy analysis.

Provides comprehensive charting and visualization capabilities for
backtesting results and performance metrics.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Set visualization style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class StrategyVisualizer:
    """Creates comprehensive visualizations for strategy backtesting results.
    
    Attributes:
        results: Dictionary of strategy results from TradingStrategyAnalyzer
        data: OHLCV DataFrame used in backtesting
    """
    
    def __init__(self, results: Dict, data: pd.DataFrame):
        """Initialize the visualizer.
        
        Args:
            results: Dictionary of strategy results
            data: OHLCV DataFrame with datetime index
        """
        self.results = results
        self.data = data
        
    def create_performance_dashboard(
        self, 
        save_path: Optional[str] = None,
        show_plot: bool = True
    ) -> str:
        """Create comprehensive performance dashboard with multiple charts.
        
        Args:
            save_path: Optional path to save figure
            show_plot: Whether to display the plot (default: True)
            
        Returns:
            Path to saved figure file
        """
        if not self.results:
            logger.warning("No results to visualize")
            return ""
        
        # Create figure with subplots
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Main title
        fig.suptitle('TQQQ Trading Strategies Performance Dashboard', 
                    fontsize=18, fontweight='bold', y=0.995)
        
        # 1. Returns Comparison (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_returns_comparison(ax1)
        
        # 2. Final Value Comparison (top right)
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_final_values(ax2)
        
        # 3. Trade Distribution (middle left)
        ax3 = fig.add_subplot(gs[1, 0])
        self._plot_trade_distribution(ax3)
        
        # 4. Win Rate Analysis (middle right)
        ax4 = fig.add_subplot(gs[1, 1])
        self._plot_win_rates(ax4)
        
        # 5. Price Chart with Trades (bottom - spans both columns)
        ax5 = fig.add_subplot(gs[2, :])
        self._plot_price_with_trades(ax5)
        
        # Save figure
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"TQQQ_strategy_dashboard_{timestamp}.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        logger.info(f"Dashboard saved to: {save_path}")
        
        if show_plot:
            plt.show()
        else:
            plt.close()
        
        return save_path
    
    def _plot_returns_comparison(self, ax):
        """Plot return percentage comparison bar chart."""
        strategies = []
        returns = []
        colors = ['#2ecc71', '#3498db', '#e74c3c', '#95a5a6']
        
        for i, (key, result) in enumerate(self.results.items()):
            strategies.append(result['strategy_name'])
            returns.append(result['return_percentage'])
        
        bars = ax.bar(strategies, returns, color=colors[:len(strategies)])
        ax.set_title('Total Return Comparison', fontsize=14, fontweight='bold')
        ax.set_ylabel('Return (%)', fontsize=11)
        ax.tick_params(axis='x', rotation=15, labelsize=9)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, ret in zip(bars, returns):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{ret:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    def _plot_final_values(self, ax):
        """Plot final portfolio value comparison."""
        strategies = []
        final_values = []
        colors = ['#2ecc71', '#3498db', '#e74c3c', '#95a5a6']
        
        for result in self.results.values():
            strategies.append(result['strategy_name'])
            final_val = result.get('total_final_value', result.get('final_value', 0))
            final_values.append(final_val)
        
        bars = ax.bar(strategies, final_values, color=colors[:len(strategies)])
        ax.set_title('Final Portfolio Value', fontsize=14, fontweight='bold')
        ax.set_ylabel('Value ($)', fontsize=11)
        ax.tick_params(axis='x', rotation=15, labelsize=9)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, val in zip(bars, final_values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${val:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    def _plot_trade_distribution(self, ax):
        """Plot number of completed trades for each strategy."""
        strategies = []
        trade_counts = []
        colors = ['#2ecc71', '#3498db', '#e74c3c']
        
        for key, result in self.results.items():
            if 'completed_trades' in result:
                strategies.append(result['strategy_name'])
                trade_counts.append(len(result['completed_trades']))
        
        if trade_counts:
            bars = ax.bar(strategies, trade_counts, color=colors[:len(strategies)])
            ax.set_title('Number of Completed Trades', fontsize=14, fontweight='bold')
            ax.set_ylabel('Trade Count', fontsize=11)
            ax.tick_params(axis='x', rotation=15, labelsize=9)
            ax.grid(axis='y', alpha=0.3)
            
            # Add value labels
            for bar, count in zip(bars, trade_counts):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{count}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'No trade data available', 
                   ha='center', va='center', transform=ax.transAxes)
    
    def _plot_win_rates(self, ax):
        """Plot win rate percentage for each strategy."""
        strategies = []
        win_rates = []
        colors = ['#2ecc71', '#3498db', '#e74c3c']
        
        for key, result in self.results.items():
            if 'completed_trades' in result and result['completed_trades']:
                trades = result['completed_trades']
                winning = sum(1 for t in trades if t.profit_loss > 0)
                win_rate = (winning / len(trades)) * 100
                strategies.append(result['strategy_name'])
                win_rates.append(win_rate)
        
        if win_rates:
            bars = ax.bar(strategies, win_rates, color=colors[:len(strategies)])
            ax.set_title('Win Rate', fontsize=14, fontweight='bold')
            ax.set_ylabel('Win Rate (%)', fontsize=11)
            ax.set_ylim([0, 100])
            ax.tick_params(axis='x', rotation=15, labelsize=9)
            ax.grid(axis='y', alpha=0.3)
            ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50% benchmark')
            ax.legend()
            
            # Add value labels
            for bar, rate in zip(bars, win_rates):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{rate:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'No trade data available', 
                   ha='center', va='center', transform=ax.transAxes)
    
    def _plot_price_with_trades(self, ax):
        """Plot TQQQ price chart with trade entry/exit markers."""
        # Plot price
        ax.plot(self.data.index, self.data['Close'], 'b-', alpha=0.6, 
               linewidth=1.5, label='TQQQ Price')
        
        # Add trade markers for first strategy only (to avoid clutter)
        for key, result in self.results.items():
            if 'completed_trades' in result and result['completed_trades']:
                trades = result['completed_trades'][:100]  # Limit markers for readability
                
                # Entry points
                entries_x = [t.entry_time for t in trades]
                entries_y = [t.entry_price for t in trades]
                ax.scatter(entries_x, entries_y, c='green', marker='^', 
                          s=30, alpha=0.6, label=f'{result["strategy_name"]} Entries (sample)')
                
                # Exit points
                exits_x = [t.exit_time for t in trades]
                exits_y = [t.exit_price for t in trades]
                ax.scatter(exits_x, exits_y, c='red', marker='v', 
                          s=30, alpha=0.6, label=f'{result["strategy_name"]} Exits (sample)')
                break  # Only plot first strategy
        
        ax.set_title('TQQQ Price Movement with Trade Points', fontsize=14, fontweight='bold')
        ax.set_ylabel('Price ($)', fontsize=11)
        ax.set_xlabel('Date', fontsize=11)
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3)
    
    def create_equity_curve(
        self, 
        save_path: Optional[str] = None,
        show_plot: bool = True
    ) -> str:
        """Create equity curve showing portfolio value over time.
        
        Args:
            save_path: Optional path to save figure
            show_plot: Whether to display the plot
            
        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # For each strategy, calculate running equity
        for key, result in self.results.items():
            if 'completed_trades' not in result:
                continue
            
            trades = result['completed_trades']
            if not trades:
                continue
            
            # Build equity curve
            equity = [result.get('final_cash', 23000)]  # Starting cash
            dates = [self.data.index[0]]
            
            for trade in sorted(trades, key=lambda t: t.exit_time):
                equity.append(equity[-1] + trade.profit_loss)
                dates.append(trade.exit_time)
            
            ax.plot(dates, equity, marker='o', markersize=3, 
                   label=result['strategy_name'], linewidth=2, alpha=0.7)
        
        ax.set_title('Equity Curves - Portfolio Value Over Time', 
                    fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Portfolio Value ($)', fontsize=12)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Save
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"equity_curve_{timestamp}.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        logger.info(f"Equity curve saved to: {save_path}")
        
        if show_plot:
            plt.show()
        else:
            plt.close()
        
        return save_path
    
    def create_profit_distribution(
        self,
        save_path: Optional[str] = None,
        show_plot: bool = True
    ) -> str:
        """Create histogram of profit/loss distribution.
        
        Args:
            save_path: Optional path to save figure
            show_plot: Whether to display the plot
            
        Returns:
            Path to saved figure
        """
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle('Profit/Loss Distribution by Strategy', 
                    fontsize=16, fontweight='bold')
        
        strategy_idx = 0
        for key, result in self.results.items():
            if 'completed_trades' not in result or not result['completed_trades']:
                continue
            
            if strategy_idx >= 3:
                break
            
            profits = [t.profit_loss for t in result['completed_trades']]
            
            ax = axes[strategy_idx]
            ax.hist(profits, bins=30, color='steelblue', alpha=0.7, edgecolor='black')
            ax.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Break-even')
            ax.axvline(x=np.mean(profits), color='green', linestyle='--', 
                      linewidth=2, label=f'Mean: ${np.mean(profits):.2f}')
            ax.set_title(result['strategy_name'], fontsize=12, fontweight='bold')
            ax.set_xlabel('Profit/Loss ($)', fontsize=10)
            ax.set_ylabel('Frequency', fontsize=10)
            ax.legend(fontsize=9)
            ax.grid(axis='y', alpha=0.3)
            
            strategy_idx += 1
        
        # Hide unused subplots
        for idx in range(strategy_idx, 3):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"profit_distribution_{timestamp}.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        logger.info(f"Profit distribution saved to: {save_path}")
        
        if show_plot:
            plt.show()
        else:
            plt.close()
        
        return save_path
