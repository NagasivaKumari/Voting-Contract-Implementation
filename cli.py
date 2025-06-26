"""
Command Line Interface for voting contract
"""

import click
import json
from algosdk.v2client import algod
from config import ContractConfig
from utils import validate_address
from logger import setup_logger

@click.group()
def cli():
    """Algorand Voting Contract CLI"""
    pass

@cli.command()
@click.option('--title', required=True, help='Proposal title')
@click.option('--duration', default=24, help='Voting duration in hours')
def create_proposal(title, duration):
    """Create a new voting proposal"""
    try:
        logger = setup_logger("cli")
        logger.info(f"Creating proposal: {title}")
        
        # Mock proposal creation
        proposal_id = 123
        click.echo(f"✅ Proposal created successfully!")
        click.echo(f"Proposal ID: {proposal_id}")
        click.echo(f"Title: {title}")
        click.echo(f"Duration: {duration} hours")
        
    except Exception as e:
        click.echo(f"❌ Error creating proposal: {e}")

@cli.command()
@click.option('--proposal-id', required=True, type=int, help='Proposal ID')
@click.option('--vote', required=True, type=click.Choice(['yes', 'no', 'abstain']), help='Vote option')
@click.option('--address', required=True, help='Voter address')
def cast_vote(proposal_id, vote, address):
    """Cast a vote on a proposal"""
    try:
        logger = setup_logger("cli")
        
        if not validate_address(address):
            click.echo("❌ Invalid address format")
            return
        
        logger.info(f"Casting vote: {vote} for proposal {proposal_id}")
        
        # Mock vote casting
        tx_id = "MOCK_TX_123456"
        click.echo(f"✅ Vote cast successfully!")
        click.echo(f"Transaction ID: {tx_id}")
        click.echo(f"Proposal: {proposal_id}")
        click.echo(f"Vote: {vote}")
        
    except Exception as e:
        click.echo(f"❌ Error casting vote: {e}")

@cli.command()
@click.option('--proposal-id', required=True, type=int, help='Proposal ID')
def get_results(proposal_id):
    """Get voting results for a proposal"""
    try:
        logger = setup_logger("cli")
        logger.info(f"Fetching results for proposal {proposal_id}")
        
        # Mock results
        results = {
            'proposal_id': proposal_id,
            'total_votes': 100,
            'yes': 60,
            'no': 30,
            'abstain': 10,
            'status': 'completed'
        }
        
        click.echo(f"📊 Voting Results for Proposal {proposal_id}")
        click.echo(f"Total Votes: {results['total_votes']}")
        click.echo(f"Yes: {results['yes']} ({results['yes']/results['total_votes']*100:.1f}%)")
        click.echo(f"No: {results['no']} ({results['no']/results['total_votes']*100:.1f}%)")
        click.echo(f"Abstain: {results['abstain']} ({results['abstain']/results['total_votes']*100:.1f}%)")
        
    except Exception as e:
        click.echo(f"❌ Error fetching results: {e}")

@cli.command()
def list_proposals():
    """List all active proposals"""
    try:
        logger = setup_logger("cli")
        logger.info("Fetching all proposals")
        
        # Mock proposals
        proposals = [
            {'id': 1, 'title': 'Upgrade Protocol', 'status': 'active'},
            {'id': 2, 'title': 'Change Governance', 'status': 'completed'},
            {'id': 3, 'title': 'New Feature', 'status': 'active'}
        ]
        
        click.echo("📋 Active Proposals:")
        for proposal in proposals:
            status_icon = "🟢" if proposal['status'] == 'active' else "🔴"
            click.echo(f"{status_icon} ID: {proposal['id']} - {proposal['title']} ({proposal['status']})")
            
    except Exception as e:
        click.echo(f"❌ Error listing proposals: {e}")

if __name__ == '__main__':
    cli()