"""
Notification system for voting contract events
"""

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from logger import setup_logger

class NotificationManager:
    def __init__(self):
        self.logger = setup_logger("notifications")
        self.subscribers = []
    
    def add_subscriber(self, email, notification_types=None):
        """Add email subscriber for notifications"""
        try:
            subscriber = {
                'email': email,
                'types': notification_types or ['all'],
                'added_at': datetime.now().isoformat()
            }
            self.subscribers.append(subscriber)
            self.logger.info(f"Added subscriber: {email}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add subscriber: {e}")
            return False
    
    def send_proposal_notification(self, proposal_title, proposal_id):
        """Send notification for new proposal"""
        try:
            message = f"""
            New Voting Proposal Created!
            
            Title: {proposal_title}
            Proposal ID: {proposal_id}
            Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Visit the voting platform to cast your vote.
            """
            
            self.logger.info(f"Sending proposal notification for: {proposal_title}")
            # Mock email sending
            return self._mock_send_email("New Proposal", message)
        except Exception as e:
            self.logger.error(f"Proposal notification failed: {e}")
            return False
    
    def send_voting_reminder(self, proposal_id, hours_remaining):
        """Send voting deadline reminder"""
        try:
            message = f"""
            Voting Deadline Reminder
            
            Proposal ID: {proposal_id}
            Time Remaining: {hours_remaining} hours
            
            Don't forget to cast your vote before the deadline!
            """
            
            self.logger.info(f"Sending voting reminder for proposal {proposal_id}")
            return self._mock_send_email("Voting Reminder", message)
        except Exception as e:
            self.logger.error(f"Voting reminder failed: {e}")
            return False
    
    def send_results_notification(self, proposal_id, results):
        """Send voting results notification"""
        try:
            message = f"""
            Voting Results Available
            
            Proposal ID: {proposal_id}
            Results: {json.dumps(results, indent=2)}
            
            Thank you for participating in the vote!
            """
            
            self.logger.info(f"Sending results notification for proposal {proposal_id}")
            return self._mock_send_email("Voting Results", message)
        except Exception as e:
            self.logger.error(f"Results notification failed: {e}")
            return False
    
    def _mock_send_email(self, subject, message):
        """Mock email sending for demonstration"""
        self.logger.info(f"Email sent - Subject: {subject}")
        return True

if __name__ == "__main__":
    notifier = NotificationManager()
    notifier.add_subscriber("user@example.com")
    notifier.send_proposal_notification("Test Proposal", 1)