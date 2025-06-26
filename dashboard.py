"""
Web dashboard for voting contract management
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from datetime import datetime
from analytics import VotingAnalytics
from logger import setup_logger

app = Flask(__name__)
logger = setup_logger("dashboard")

@app.route('/')
def index():
    """Main dashboard page"""
    try:
        # Mock dashboard data
        stats = {
            'total_proposals': 15,
            'active_proposals': 3,
            'total_votes': 1250,
            'active_voters': 89
        }
        
        recent_proposals = [
            {'id': 1, 'title': 'Protocol Upgrade', 'votes': 45, 'status': 'active'},
            {'id': 2, 'title': 'Governance Change', 'votes': 78, 'status': 'completed'},
            {'id': 3, 'title': 'New Feature', 'votes': 23, 'status': 'active'}
        ]
        
        logger.info("Dashboard accessed")
        return render_template('dashboard.html', stats=stats, proposals=recent_proposals)
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return f"Dashboard error: {e}", 500

@app.route('/proposal/<int:proposal_id>')
def proposal_detail(proposal_id):
    """Detailed view of a specific proposal"""
    try:
        # Mock proposal data
        proposal = {
            'id': proposal_id,
            'title': f'Proposal {proposal_id}',
            'description': 'This is a detailed description of the proposal.',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'voting_end': '2024-07-01 12:00:00',
            'total_votes': 67,
            'yes_votes': 40,
            'no_votes': 20,
            'abstain_votes': 7,
            'status': 'active'
        }
        
        logger.info(f"Viewing proposal {proposal_id}")
        return render_template('proposal.html', proposal=proposal)
    except Exception as e:
        logger.error(f"Proposal detail error: {e}")
        return f"Error: {e}", 500

@app.route('/api/dashboard/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    try:
        stats = {
            'proposals': {
                'total': 15,
                'active': 3,
                'completed': 12
            },
            'votes': {
                'total': 1250,
                'today': 45,
                'this_week': 234
            },
            'participation': {
                'unique_voters': 89,
                'average_participation': 75.5
            }
        }
        
        logger.info("Stats API accessed")
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Stats API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/analytics')
def analytics_page():
    """Analytics and charts page"""
    try:
        analytics = VotingAnalytics()
        
        # Mock analytics data
        chart_data = {
            'vote_distribution': [40, 25, 10],
            'labels': ['Yes', 'No', 'Abstain'],
            'participation_trend': [20, 25, 30, 35, 40, 45, 50]
        }
        
        logger.info("Analytics page accessed")
        return render_template('analytics.html', chart_data=chart_data)
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        return f"Analytics error: {e}", 500

@app.route('/create_proposal', methods=['GET', 'POST'])
def create_proposal():
    """Create new proposal page"""
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            description = request.form.get('description')
            duration = request.form.get('duration', 24)
            
            # Mock proposal creation
            proposal_id = 999
            
            logger.info(f"Proposal created: {title}")
            return redirect(url_for('proposal_detail', proposal_id=proposal_id))
        except Exception as e:
            logger.error(f"Proposal creation error: {e}")
            return f"Error: {e}", 500
    
    return render_template('create_proposal.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)