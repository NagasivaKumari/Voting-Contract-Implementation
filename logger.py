"""
Logging module for Algorand Voting Contract
"""

import logging
import os
from datetime import datetime

def setup_logger(name="voting_contract", level=logging.INFO):
    """Setup logger with file and console handlers"""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # File handler
    log_filename = f"logs/voting_contract_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_transaction(logger, tx_id, operation, details=None):
    """Log transaction details"""
    message = f"Transaction {operation}: {tx_id}"
    if details:
        message += f" - {details}"
    logger.info(message)

def log_error(logger, error, context=None):
    """Log error with context"""
    message = f"Error: {str(error)}"
    if context:
        message += f" - Context: {context}"
    logger.error(message)