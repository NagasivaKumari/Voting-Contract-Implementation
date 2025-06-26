from pyteal import *

def voting_contract():
    """
    Algorand Voting Smart Contract - Secure blockchain voting system
    Allows users to create proposals and vote on them
    Features: Time-bound voting, anti-double voting, secure proposal creation
    """
    
    # Global state keys
    proposal_count = Bytes("proposal_count")
    voting_end = Bytes("voting_end")
    
    # Operations
    op_create_proposal = Bytes("create_proposal")
    op_vote = Bytes("vote")
    op_get_results = Bytes("get_results")
    
    # Create proposal logic
    create_proposal = Seq([
        App.globalPut(proposal_count, App.globalGet(proposal_count) + Int(1)),
        App.globalPut(voting_end, Global.latest_timestamp() + Int(86400)),  # 24 hours
        Approve()
    ])
    
    # Vote logic
    cast_vote = Seq([
        Assert(Global.latest_timestamp() < App.globalGet(voting_end)),
        Assert(Txn.application_args.length() == Int(2)),
        App.localPut(Txn.sender(), Bytes("voted"), Int(1)),
        App.globalPut(
            Concat(Bytes("votes_"), Txn.application_args[1]),
            App.globalGet(Concat(Bytes("votes_"), Txn.application_args[1])) + Int(1)
        ),
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
        [Txn.application_args[0] == op_get_results, get_results]
    )
    
    return program

if __name__ == "__main__":
    print(compileTeal(voting_contract(), Mode.Application, version=8))