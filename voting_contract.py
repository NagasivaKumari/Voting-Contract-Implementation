from pyteal import *

def voting_contract():
    """
    Algorand Voting Smart Contract
    Allows users to create proposals and vote on them
    """
    
    # Global state keys
    proposal_count = Bytes("proposal_count")
    voting_end = Bytes("voting_end")
    proposal_title = Bytes("proposal_title")
    min_votes_required = Bytes("min_votes")
    admin_address = Bytes("admin")
    voting_active = Bytes("active")
    
    # Operations
    op_create_proposal = Bytes("create_proposal")
    op_vote = Bytes("vote")
    op_get_results = Bytes("get_results")
    op_close_voting = Bytes("close_voting")
    
    # Create proposal logic
    create_proposal = Seq([
        App.globalPut(proposal_count, App.globalGet(proposal_count) + Int(1)),
        App.globalPut(voting_end, Global.latest_timestamp() + Int(86400)),  # 24 hours
        App.globalPut(min_votes_required, Int(10)),  # Minimum 10 votes needed
        App.globalPut(admin_address, Txn.sender()),  # Set creator as admin
        App.globalPut(voting_active, Int(1)),  # Activate voting
        Approve()
    ])
    
    # Vote logic
    cast_vote = Seq([
        Assert(Global.latest_timestamp() < App.globalGet(voting_end)),
        Assert(App.globalGet(voting_active) == Int(1)),  # Ensure voting is still active
        Assert(Txn.application_args.length() == Int(2)),
        Assert(App.localGet(Txn.sender(), Bytes("voted")) == Int(0)),  # Prevent double voting
        App.localPut(Txn.sender(), Bytes("voted"), Int(1)),
        App.globalPut(
            Concat(Bytes("votes_"), Txn.application_args[1]),
            App.globalGet(Concat(Bytes("votes_"), Txn.application_args[1])) + Int(1)
        ),
        App.globalPut(Bytes("total_votes"), App.globalGet(Bytes("total_votes")) + Int(1)),
        Approve()
    ])
    
    # Close voting logic
    close_voting = Seq([
        Assert(Txn.sender() == App.globalGet(admin_address)),  # Only admin can close
        App.globalPut(voting_active, Int(0)),  # Deactivate voting
        Approve()
    ])
    
    # Get results logic
    get_results = Approve()
    
    # Main program logic
    program = Cond(
        [Txn.application_id() == Int(0), Approve()],  # Contract creation
        [Txn.on_completion() == OnCall.OptIn, Approve()],  # Opt-in
        [Txn.application_args[0] == op_create_proposal, create_proposal],
        [Txn.application_args[0] == op_vote, cast_vote],
        [Txn.application_args[0] == op_get_results, get_results],
        [Txn.application_args[0] == op_close_voting, close_voting]
    )
    
    return program

if __name__ == "__main__":
    print(compileTeal(voting_contract(), Mode.Application, version=8))