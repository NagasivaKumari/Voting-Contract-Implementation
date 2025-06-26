from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCreateTxn, wait_for_confirmation
from voting_contract import voting_contract
from pyteal import compileTeal, Mode
import os
from dotenv import load_dotenv

load_dotenv()

def deploy_contract():
    """Deploy the voting smart contract to Algorand testnet
    Returns the application ID for interaction
    """
    
    # Algorand client setup
    algod_address = "https://testnet-api.algonode.cloud"
    algod_token = ""
    algod_client = algod.AlgodClient(algod_token, algod_address)
    
    # Account setup (use environment variables in production)
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("Please set PRIVATE_KEY in .env file")
        return
    
    sender = account.address_from_private_key(private_key)
    
    # Compile contract
    approval_program = compileTeal(voting_contract(), Mode.Application, version=8)
    clear_program = compileTeal(Approve(), Mode.Application, version=8)
    
    # Contract parameters
    global_schema = StateSchema(num_uints=10, num_byte_slices=10)
    local_schema = StateSchema(num_uints=5, num_byte_slices=5)
    
    # Get suggested parameters
    params = algod_client.suggested_params()
    
    # Create transaction
    txn = ApplicationCreateTxn(
        sender=sender,
        sp=params,
        on_complete=0,
        approval_program=approval_program.encode(),
        clear_program=clear_program.encode(),
        global_schema=global_schema,
        local_schema=local_schema
    )
    
    # Sign and send transaction
    signed_txn = txn.sign(private_key)
    tx_id = algod_client.send_transaction(signed_txn)
    
    # Wait for confirmation
    result = wait_for_confirmation(algod_client, tx_id)
    app_id = result['application-index']
    
    print(f"Contract deployed successfully!")
    print(f"Application ID: {app_id}")
    print(f"Transaction ID: {tx_id}")
    
    return app_id

if __name__ == "__main__":
    deploy_contract()