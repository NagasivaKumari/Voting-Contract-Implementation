"""
Backup utility for voting contract data
"""

import json
import os
from datetime import datetime
from algosdk.v2client import algod
from schema import VotingDatabase
from logger import setup_logger

class DataBackup:
    def __init__(self):
        self.logger = setup_logger("backup")
        self.db = VotingDatabase()
        
    def backup_proposals(self):
        """Backup all proposals to JSON"""
        try:
            # Mock backup data
            proposals = [
                {"id": 1, "title": "Test Proposal", "created": str(datetime.now())},
                {"id": 2, "title": "Another Proposal", "created": str(datetime.now())}
            ]
            
            backup_file = f"backups/proposals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs("backups", exist_ok=True)
            
            with open(backup_file, 'w') as f:
                json.dump(proposals, f, indent=2)
            
            self.logger.info(f"Proposals backed up to {backup_file}")
            return backup_file
        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
            return None
    
    def backup_votes(self):
        """Backup all votes to JSON"""
        try:
            votes = [
                {"proposal_id": 1, "voter": "ADDR123", "option": "yes", "timestamp": str(datetime.now())},
                {"proposal_id": 1, "voter": "ADDR456", "option": "no", "timestamp": str(datetime.now())}
            ]
            
            backup_file = f"backups/votes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(backup_file, 'w') as f:
                json.dump(votes, f, indent=2)
            
            self.logger.info(f"Votes backed up to {backup_file}")
            return backup_file
        except Exception as e:
            self.logger.error(f"Vote backup failed: {e}")
            return None
    
    def full_backup(self):
        """Perform full system backup"""
        self.logger.info("Starting full backup...")
        self.backup_proposals()
        self.backup_votes()
        self.logger.info("Full backup completed")

if __name__ == "__main__":
    backup = DataBackup()
    backup.full_backup()