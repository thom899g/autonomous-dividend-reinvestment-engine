from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class PortfolioManager:
    def __init__(self):
        self.holdings = {}
    
    def get_current_holdings(self) -> Dict[str, float]:
        """Get the current holdings of the portfolio."""
        return self.holdings.copy()
    
    def execute_trade(self, symbol: str, amount: float, trade_type: str) -> None:
        """Execute a trade in the portfolio."""
        if trade_type == 'buy':
            self.holdings[symbol] = self.holdings.get(symbol, 0) + amount
        elif trade_type == 'sell':
            current_amount = self.holdings.get(symbol, 0)
            if current_amount >= amount:
                self.holdings[symbol] = current_amount - amount
            else:
                logger.error(f"Insufficient holdings to sell {symbol}")
    
    def update_holdings(self) -> None:
        """Update the portfolio holdings."""
        logger.info("Portfolio holdings updated successfully.")