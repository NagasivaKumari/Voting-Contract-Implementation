"""
Monitoring script for voting contract health
"""

import time
from algosdk.v2client import algod
from logger import setup_logger
from config import ContractConfig

class ContractMonitor:
    def __init__(self):
        self.logger = setup_logger("monitor")
        self.config = ContractConfig()
        self.algod_client = algod.AlgodClient("", self.config.algod_url)
    
    def check_network_health(self):
        """Check Algorand network connectivity"""
        try:
            status = self.algod_client.status()
            self.logger.info(f"Network status: Round {status['last-round']}")
            return True
        except Exception as e:
            self.logger.error(f"Network check failed: {e}")
            return False
    
    def monitor_contract(self, app_id):
        """Monitor specific contract"""
        try:
            app_info = self.algod_client.application_info(app_id)
            self.logger.info(f"Contract {app_id} is active")
            return app_info
        except Exception as e:
            self.logger.error(f"Contract monitoring failed: {e}")
            return None
    
    def run_monitoring(self, interval=60):
        """Run continuous monitoring"""
        self.logger.info("Starting contract monitoring...")
        
        while True:
            self.check_network_health()
            time.sleep(interval)

if __name__ == "__main__":
    monitor = ContractMonitor()
    monitor.run_monitoring()