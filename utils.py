"""
Utility functions for Algorand Voting Contract
"""

import time
from algosdk import encoding
from algosdk.v2client import algod

def validate_address(address):
    """Validate Algorand address format"""
    try:
        encoding.decode_address(address)
        return True
    except Exception:
        return False

def get_current_timestamp():
    """Get current Unix timestamp"""
    return int(time.time())

def calculate_voting_deadline(hours=24):
    """Calculate voting deadline timestamp"""
    return get_current_timestamp() + (hours * 3600)

def format_vote_count(votes):
    """Format vote count for display"""
    return f"Total votes: {votes}"

def check_voting_period_active(start_time, end_time):
    """Check if voting period is currently active"""
    current_time = get_current_timestamp()
    return start_time <= current_time <= end_time

def get_account_balance(algod_client, address):
    """Get account balance in microAlgos"""
    try:
        account_info = algod_client.account_info(address)
        return account_info.get('amount', 0)
    except Exception as e:
        print(f"Error getting balance: {e}")
        return 0

class VotingUtils:
    """Utility class for voting operations"""
    
    @staticmethod
    def validate_vote_option(option):
        """Validate vote option"""
        valid_options = ["yes", "no", "abstain"]
        return option.lower() in valid_options
    
    @staticmethod
    def calculate_vote_percentage(yes_votes, total_votes):
        """Calculate percentage of yes votes"""
        if total_votes == 0:
            return 0
        return (yes_votes / total_votes) * 100