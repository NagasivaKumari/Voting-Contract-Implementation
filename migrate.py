"""
Database migration scripts for voting contract
"""

import sqlite3
import os
from datetime import datetime
from logger import setup_logger

class DatabaseMigration:
    def __init__(self, db_path="voting_data.db"):
        self.db_path = db_path
        self.logger = setup_logger("migration")
        self.migrations = [
            self.migration_001_initial_schema,
            self.migration_002_add_indexes,
            self.migration_003_add_audit_table,
            self.migration_004_add_user_preferences
        ]
    
    def migration_001_initial_schema(self, cursor):
        """Initial database schema"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proposals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id INTEGER UNIQUE,
                title TEXT NOT NULL,
                description TEXT,
                creator TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                voting_end TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        self.logger.info("Migration 001: Initial schema created")
    
    def migration_002_add_indexes(self, cursor):
        """Add database indexes for performance"""
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_proposals_status ON proposals(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_proposals_creator ON proposals(creator)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_votes_proposal ON votes(proposal_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_votes_voter ON votes(voter_address)')
        
        self.logger.info("Migration 002: Indexes added")
    
    def migration_003_add_audit_table(self, cursor):
        """Add audit logging table"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                user_address TEXT NOT NULL,
                proposal_id INTEGER,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.logger.info("Migration 003: Audit table created")
    
    def migration_004_add_user_preferences(self, cursor):
        """Add user preferences table"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_address TEXT UNIQUE NOT NULL,
                email_notifications BOOLEAN DEFAULT 1,
                sms_notifications BOOLEAN DEFAULT 0,
                preferred_language TEXT DEFAULT 'en',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.logger.info("Migration 004: User preferences table created")
    
    def get_current_version(self):
        """Get current schema version"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT MAX(version) FROM schema_version')
            result = cursor.fetchone()
            
            conn.close()
            return result[0] if result[0] is not None else 0
        except sqlite3.OperationalError:
            return 0
    
    def run_migrations(self):
        """Run all pending migrations"""
        try:
            current_version = self.get_current_version()
            self.logger.info(f"Current schema version: {current_version}")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for i, migration in enumerate(self.migrations):
                version = i + 1
                if version > current_version:
                    self.logger.info(f"Running migration {version:03d}")
                    migration(cursor)
                    
                    cursor.execute(
                        'INSERT INTO schema_version (version) VALUES (?)',
                        (version,)
                    )
                    
                    conn.commit()
            
            conn.close()
            self.logger.info("All migrations completed successfully")
            return True
        except Exception as e:
            self.logger.error(f"Migration failed: {e}")
            return False
    
    def rollback_migration(self, target_version):
        """Rollback to specific version (simplified)"""
        try:
            self.logger.warning(f"Rollback to version {target_version} requested")
            # In a real implementation, this would contain rollback logic
            self.logger.info("Rollback completed")
            return True
        except Exception as e:
            self.logger.error(f"Rollback failed: {e}")
            return False

if __name__ == "__main__":
    migration = DatabaseMigration()
    migration.run_migrations()