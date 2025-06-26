"""
Database schema for storing voting contract data
"""

import sqlite3
from datetime import datetime

class VotingDatabase:
    """Database handler for voting contract data"""
    
    def __init__(self, db_path="voting_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Proposals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proposals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id INTEGER UNIQUE,
                title TEXT NOT NULL,
                creator TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                voting_end TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Votes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proposal_id INTEGER,
                voter_address TEXT NOT NULL,
                vote_option TEXT NOT NULL,
                voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tx_id TEXT,
                FOREIGN KEY (proposal_id) REFERENCES proposals (id)
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tx_id TEXT UNIQUE NOT NULL,
                operation TEXT NOT NULL,
                sender TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_proposal(self, app_id, title, creator, voting_end):
        """Add new proposal to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO proposals (app_id, title, creator, voting_end)
            VALUES (?, ?, ?, ?)
        ''', (app_id, title, creator, voting_end))
        
        conn.commit()
        conn.close()
    
    def record_vote(self, proposal_id, voter, option, tx_id):
        """Record a vote in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO votes (proposal_id, voter_address, vote_option, tx_id)
            VALUES (?, ?, ?, ?)
        ''', (proposal_id, voter, option, tx_id))
        
        conn.commit()
        conn.close()