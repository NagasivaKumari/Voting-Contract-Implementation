"""
Input validation module for voting contract
"""

import re
from datetime import datetime, timedelta
from algosdk import encoding
from logger import setup_logger

class InputValidator:
    def __init__(self):
        self.logger = setup_logger("validation")
    
    def validate_algorand_address(self, address):
        """Validate Algorand address format"""
        try:
            if not address or len(address) != 58:
                return False
            
            # Check if address is valid base32
            encoding.decode_address(address)
            return True
        except Exception:
            return False
    
    def validate_proposal_title(self, title):
        """Validate proposal title"""
        if not title or len(title.strip()) == 0:
            return False, "Title cannot be empty"
        
        if len(title) > 200:
            return False, "Title too long (max 200 characters)"
        
        # Check for malicious content
        forbidden_chars = ['<', '>', '{', '}', '&', ';']
        if any(char in title for char in forbidden_chars):
            return False, "Title contains forbidden characters"
        
        return True, "Valid title"
    
    def validate_vote_option(self, option):
        """Validate vote option"""
        valid_options = ['yes', 'no', 'abstain']
        
        if not option:
            return False, "Vote option required"
        
        if option.lower() not in valid_options:
            return False, f"Invalid option. Must be one of: {', '.join(valid_options)}"
        
        return True, "Valid vote option"
    
    def validate_voting_duration(self, hours):
        """Validate voting duration"""
        try:
            duration = int(hours)
            
            if duration < 1:
                return False, "Duration must be at least 1 hour"
            
            if duration > 168:  # 1 week
                return False, "Duration cannot exceed 168 hours (1 week)"
            
            return True, "Valid duration"
        except ValueError:
            return False, "Duration must be a number"
    
    def validate_proposal_description(self, description):
        """Validate proposal description"""
        if not description:
            return True, "Description is optional"
        
        if len(description) > 2000:
            return False, "Description too long (max 2000 characters)"
        
        # Basic HTML/script injection check
        dangerous_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe.*?>',
            r'<object.*?>'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, description, re.IGNORECASE):
                return False, "Description contains potentially dangerous content"
        
        return True, "Valid description"
    
    def validate_email(self, email):
        """Validate email address format"""
        if not email:
            return False, "Email required"
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        if len(email) > 254:
            return False, "Email too long"
        
        return True, "Valid email"
    
    def validate_transaction_id(self, tx_id):
        """Validate Algorand transaction ID"""
        if not tx_id:
            return False, "Transaction ID required"
        
        if len(tx_id) != 52:
            return False, "Invalid transaction ID length"
        
        # Check if it's valid base32
        try:
            import base64
            base64.b32decode(tx_id + '======')
            return True, "Valid transaction ID"
        except Exception:
            return False, "Invalid transaction ID format"
    
    def sanitize_input(self, text):
        """Sanitize user input"""
        if not text:
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>&"\'`]', '', str(text))
        
        # Limit length
        sanitized = sanitized[:1000]
        
        # Strip whitespace
        sanitized = sanitized.strip()
        
        return sanitized

if __name__ == "__main__":
    validator = InputValidator()
    
    # Test validations
    print(validator.validate_proposal_title("Test Proposal"))
    print(validator.validate_vote_option("yes"))
    print(validator.validate_email("test@example.com"))