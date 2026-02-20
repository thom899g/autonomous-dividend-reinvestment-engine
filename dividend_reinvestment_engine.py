from typing import Dict, Optional
import logging
from datetime import datetime

from portfolio_manager import PortfolioManager
from asset_allocator import AssetAllocator
from risk_management import RiskManager
from configuration_manager import ConfigurationManager
from data_feeder import DataFeeder

logger = logging.getLogger(__name__)

class DividendReinvestmentEngine:
    def __init__(self):
        self.config = ConfigurationManager()
        self.portfolio_manager = PortfolioManager()
        self.asset_allocator = AssetAllocator()
        self.risk_manager = RiskManager()
        self.data_feeder = DataFeeder()

    def process_dividends(self) -> None:
        """Process dividends and reinvest them according to the strategy."""
        try:
            # Step 1: Fetch dividend data
            dividend_data = self.data_feeder.get_dividend_data()
            
            if not dividend_data:
                logger.info("No new dividend data available.")
                return

            # Step 2: Check portfolio holdings
            current_holdings = self.portfolio_manager.get_current_holdings()

            for symbol, dividend in dividend_data.items():
                if symbol not in current_holdings:
                    continue  # Skip non-holding assets
                
                amount = dividend['amount']
                logger.info(f"Processing dividend of {amount} for {symbol}")

                # Step 3: Allocate the dividend proceeds
                allocation = self.asset_allocator.allocate(amount, 
                                                          current_holdings[symbol])
                
                if not allocation:
                    continue  # No suitable asset found

                # Step 4: Check risk parameters
                if not self.risk_manager.is_safe_allocation(allocation):
                    logger.warning(f"Skipping risky allocation for {symbol}")
                    continue
                
                # Step 5: Execute the trade
                self.portfolio_manager.execute_trade(symbol, allocation['amount'], 
                                                    allocation['type'])

                # Update portfolio and log the transaction
                self.portfolio_manager.update_holdings()
                logger.info(f"Invested {allocation['amount']} in {allocation['symbol']} from dividends of {symbol}")

        except Exception as e:
            logger.error(f"Error processing dividends: {str(e)}", exc_info=True)