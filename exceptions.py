"""
Custom exceptions for Algorand Voting Contract
"""

class VotingContractError(Exception):
    """Base exception for voting contract errors"""
    pass

class InvalidVoteError(VotingContractError):
    """Raised when vote is invalid"""
    def __init__(self, message="Invalid vote option provided"):
        self.message = message
        super().__init__(self.message)

class VotingClosedError(VotingContractError):
    """Raised when trying to vote after voting period ends"""
    def __init__(self, message="Voting period has ended"):
        self.message = message
        super().__init__(self.message)

class DoubleVoteError(VotingContractError):
    """Raised when user tries to vote twice"""
    def __init__(self, message="User has already voted"):
        self.message = message
        super().__init__(self.message)

class InsufficientBalanceError(VotingContractError):
    """Raised when account has insufficient balance"""
    def __init__(self, message="Insufficient account balance"):
        self.message = message
        super().__init__(self.message)

class UnauthorizedError(VotingContractError):
    """Raised when unauthorized action is attempted"""
    def __init__(self, message="Unauthorized action"):
        self.message = message
        super().__init__(self.message)

class ContractNotFoundError(VotingContractError):
    """Raised when contract is not found"""
    def __init__(self, message="Voting contract not found"):
        self.message = message
        super().__init__(self.message)

def handle_contract_error(error, logger=None):
    """Handle and log contract errors"""
    if isinstance(error, VotingContractError):
        if logger:
            logger.error(f"Contract Error: {error.message}")
        return error.message
    else:
        if logger:
            logger.error(f"Unexpected Error: {str(error)}")
        return "An unexpected error occurred"