from pyteal import *

def voting_contract():
    """
    Algorand Voting Smart Contract - Secure blockchain voting system
    Allows users to create proposals and vote on them
    Features: Time-bound voting, anti-double voting, secure proposal creation
    """
    
    # Global state keys - Store voting data on blockchain - Store voting data on blockchain
    # proposal_count: tracks number of proposals created
    # voting_end: timestamp when voting period ends
    proposal_count = Bytes("proposal_count")
    voting_end = Bytes("voting_end")
    proposal_title = Bytes("proposal_title")
    total_votes = Bytes("total_votes")
    
    # Operations - Define contract function calls
    # Each operation represents a different contract interaction
    op_create_proposal = Bytes("create_proposal")
    op_vote = Bytes("vote")
    op_get_results = Bytes("get_results")
    
    # Create proposal logic
    create_proposal = Seq([
        App.globalPut(proposal_count, App.globalGet(proposal_count) + Int(1)),
        App.globalPut(voting_end, Global.latest_timestamp() + Int(86400)),  # 24 hours
        App.globalPut(proposal_title, Txn.application_args[1]),  # Store proposal title
        App.globalPut(total_votes, Int(0)),  # Initialize vote counter
        Approve()
    ])
    
    # Vote logic
    cast_vote = Seq([
        Assert(Global.latest_timestamp() < App.globalGet(voting_end)),  # Check voting deadline
        Assert(App.localGet(Txn.sender(), Bytes("voted")) == Int(0)),  # Prevent double voting
        Assert(Txn.application_args.length() == Int(2)),  # Ensure vote option provided
        Assert(App.localGet(Txn.sender(), Bytes("voted")) == Int(0)),  # Prevent double voting
        App.localPut(Txn.sender(), Bytes("voted"), Int(1)),
        App.globalPut(
            Concat(Bytes("votes_"), Txn.application_args[1]),
            App.globalGet(Concat(Bytes("votes_"), Txn.application_args[1])) + Int(1)
        ),
        Approve()
    ])
    
    # Get results logic
    get_results = Seq([
        Assert(Global.latest_timestamp() > App.globalGet(voting_end)),  # Voting must be ended
        App.globalPut(Bytes("voting_closed"), Int(1)),  # Mark voting as closed
        Approve()
    ])
    
    # Main program logic
    program = Cond(
        [Txn.application_id() == Int(0), Approve()],  # Contract creation
        [Txn.on_completion() == OnCall.OptIn, Approve()],  # Opt-in
        [Txn.application_args[0] == op_create_proposal, create_proposal],
        [Txn.application_args[0] == op_vote, cast_vote],
        [Txn.application_args[0] == op_get_results, get_results]
    )
    
    return program

if __name__ == "__main__":
    print(compileTeal(voting_contract(), Mode.Application, version=8))