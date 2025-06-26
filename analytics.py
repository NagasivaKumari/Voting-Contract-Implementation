"""
Analytics module for voting contract data
"""

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from schema import VotingDatabase
from logger import setup_logger

class VotingAnalytics:
    def __init__(self):
        self.logger = setup_logger("analytics")
        self.db = VotingDatabase()
    
    def generate_vote_summary(self, proposal_id):
        """Generate vote summary for a proposal"""
        try:
            # Mock data for demonstration
            vote_data = {
                'yes': 45,
                'no': 23,
                'abstain': 12
            }
            
            total_votes = sum(vote_data.values())
            percentages = {k: (v/total_votes)*100 for k, v in vote_data.items()}
            
            summary = {
                'total_votes': total_votes,
                'vote_counts': vote_data,
                'percentages': percentages,
                'winner': max(vote_data, key=vote_data.get)
            }
            
            self.logger.info(f"Generated summary for proposal {proposal_id}")
            return summary
        except Exception as e:
            self.logger.error(f"Summary generation failed: {e}")
            return None
    
    def create_vote_chart(self, proposal_id):
        """Create pie chart for vote distribution"""
        try:
            summary = self.generate_vote_summary(proposal_id)
            if not summary:
                return None
            
            plt.figure(figsize=(8, 6))
            plt.pie(summary['vote_counts'].values(), 
                   labels=summary['vote_counts'].keys(),
                   autopct='%1.1f%%',
                   startangle=90)
            plt.title(f'Vote Distribution - Proposal {proposal_id}')
            
            chart_file = f"charts/proposal_{proposal_id}_votes.png"
            os.makedirs("charts", exist_ok=True)
            plt.savefig(chart_file)
            plt.close()
            
            self.logger.info(f"Chart saved to {chart_file}")
            return chart_file
        except Exception as e:
            self.logger.error(f"Chart creation failed: {e}")
            return None
    
    def voting_trends(self, days=30):
        """Analyze voting trends over time"""
        try:
            # Mock trend data
            dates = [datetime.now() - timedelta(days=i) for i in range(days)]
            votes_per_day = [10 + (i % 5) for i in range(days)]
            
            trend_data = {
                'dates': dates,
                'daily_votes': votes_per_day,
                'average_daily': sum(votes_per_day) / len(votes_per_day)
            }
            
            self.logger.info(f"Generated {days}-day voting trends")
            return trend_data
        except Exception as e:
            self.logger.error(f"Trend analysis failed: {e}")
            return None

if __name__ == "__main__":
    analytics = VotingAnalytics()
    summary = analytics.generate_vote_summary(1)
    print(f"Vote Summary: {summary}")