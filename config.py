"""
Configuration settings for Algorand Voting Contract
"""

# Network Configuration
ALGORAND_TESTNET_URL = "https://testnet-api.algonode.cloud"
ALGORAND_MAINNET_URL = "https://mainnet-api.algonode.cloud"

# Contract Configuration
DEFAULT_VOTING_PERIOD = 86400  # 24 hours in seconds
MIN_VOTES_REQUIRED = 10
MAX_PROPOSAL_LENGTH = 256

# Gas and Fee Configuration
MIN_BALANCE = 100000  # Minimum balance in microAlgos
TRANSACTION_FEE = 1000  # Transaction fee in microAlgos

# Voting Options
VALID_VOTE_OPTIONS = ["yes", "no", "abstain"]

# Security Settings
MAX_VOTES_PER_ADDRESS = 1
REQUIRE_OPT_IN = True

class ContractConfig:
    """Contract configuration class"""
    
    def __init__(self, network="testnet"):
        self.network = network
        self.algod_url = ALGORAND_TESTNET_URL if network == "testnet" else ALGORAND_MAINNET_URL
        self.voting_period = DEFAULT_VOTING_PERIOD
        self.min_votes = MIN_VOTES_REQUIRED
    
    def get_network_params(self):
        """Get network-specific parameters"""
        return {
            "url": self.algod_url,
            "voting_period": self.voting_period,
            "min_votes": self.min_votes
        }