# -*- coding: utf-8 -*-
#: Operation ids
ops = [
    "vote",
    "comment",
    "transfer",
    "transfer_to_vesting",
    "withdraw_vesting",
    "account_create",
    "account_update",
    "witness_update",
    "account_witness_vote",
    "account_witness_proxy",
    "custom",
    "delete_comment",
    "custom_json",
    "comment_options",
    "set_withdraw_vesting_route",
    "claim_account",
    "create_claimed_account",
    "request_account_recovery",
    "recover_account",
    "change_recovery_account",
    "escrow_transfer",
    "escrow_dispute",
    "escrow_release",
    "escrow_approve",
    "transfer_to_savings",
    "transfer_from_savings",
    "cancel_transfer_from_savings",
    "custom_binary",
    "decline_voting_rights",
    "reset_account",
    "set_reset_account",
    "claim_reward_balance",
    "delegate_vesting_shares",
    "witness_set_properties",
    "create_proposal",
    "update_proposal_votes",
    "remove_proposal",
    "author_reward",
    "curation_reward",
    "comment_reward",
    "fill_vesting_withdraw",
    "shutdown_witness",
    "fill_transfer_from_savings",
    "hardfork",
    "comment_payout_update",
    "return_vesting_delegation",
    "comment_benefactor_reward",
    "producer_reward",
    "clear_null_account_balance",
    "proposal_pay",
    "sps_fund"
]

operations = {o: ops.index(o) for o in ops}


def getOperationNameForId(i):
    """ Convert an operation id into the corresponding string
    """
    for key in operations:
        if int(operations[key]) is int(i):
            return key
    return "Unknown Operation ID %d" % i
