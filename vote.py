from algosdk import account
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCallTxn, wait_for_confirmation
import os
from dotenv import load_dotenv

load_dotenv()

def create_proposal(app_id, proposal_title):
    """Create a new voting proposal"""
    
    algod_client = algod.AlgodClient("", "https://testnet-api.algonode.cloud")
    private_key = os.getenv('PRIVATE_KEY')
    sender = account.address_from_private_key(private_key)
    
    params = algod_client.suggested_params()
    
    txn = ApplicationCallTxn(
        sender=sender,
        sp=params,
        index=app_id,
        on_complete=0,
        app_args=["create_proposal", proposal_title]
    )
    
    signed_txn = txn.sign(private_key)
    tx_id = algod_client.send_transaction(signed_txn)
    
    wait_for_confirmation(algod_client, tx_id)
    print(f"Proposal '{proposal_title}' created successfully!")

def cast_vote(app_id, vote_option):
    """Cast a vote on the current proposal"""
    
    algod_client = algod.AlgodClient("", "https://testnet-api.algonode.cloud")
    private_key = os.getenv('PRIVATE_KEY')
    sender = account.address_from_private_key(private_key)
    
    params = algod_client.suggested_params()
    
    txn = ApplicationCallTxn(
        sender=sender,
        sp=params,
        index=app_id,
        on_complete=0,
        app_args=["vote", vote_option]
    )
    
    signed_txn = txn.sign(private_key)
    tx_id = algod_client.send_transaction(signed_txn)
    
    wait_for_confirmation(algod_client, tx_id)
    print(f"Vote cast for option: {vote_option}")

if __name__ == "__main__":
    app_id = int(input("Enter Application ID: "))
    action = input("Enter action (create/vote): ")
    
    if action == "create":
        title = input("Enter proposal title: ")
        create_proposal(app_id, title)
    elif action == "vote":
        option = input("Enter vote option (yes/no): ")
        cast_vote(app_id, option)