"""
API handler for voting contract interactions
"""

from flask import Flask, request, jsonify
from algosdk.v2client import algod
from utils import validate_address, VotingUtils
from logger import setup_logger
import json

app = Flask(__name__)
logger = setup_logger("api")

@app.route('/api/proposals', methods=['GET'])
def get_proposals():
    """Get all active proposals"""
    try:
        # Mock data for now
        proposals = [
            {"id": 1, "title": "Upgrade Protocol", "status": "active"},
            {"id": 2, "title": "Change Governance", "status": "closed"}
        ]
        return jsonify({"proposals": proposals})
    except Exception as e:
        logger.error(f"Error fetching proposals: {e}")
        return jsonify({"error": "Failed to fetch proposals"}), 500

@app.route('/api/vote', methods=['POST'])
def cast_vote():
    """Cast a vote via API"""
    try:
        data = request.get_json()
        proposal_id = data.get('proposal_id')
        vote_option = data.get('vote_option')
        voter_address = data.get('voter_address')
        
        if not VotingUtils.validate_vote_option(vote_option):
            return jsonify({"error": "Invalid vote option"}), 400
            
        if not validate_address(voter_address):
            return jsonify({"error": "Invalid address"}), 400
        
        # Process vote (mock for now)
        result = {"tx_id": "mock_tx_123", "status": "success"}
        logger.info(f"Vote cast: {vote_option} by {voter_address}")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error casting vote: {e}")
        return jsonify({"error": "Failed to cast vote"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)