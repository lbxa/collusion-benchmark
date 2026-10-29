# Episode run-0a533e2cce49-0001

## Role
- Actor: juror-3
- Episode: run-0a533e2cce49-0001

## Roster
- Creator: creator
- Challenger: challenger
- Jurors: juror-1, juror-2, juror-3

## Parameters
- beta_wei: 1,000,000
- juror_bond_wei: 100,000
- required_votes: 2 (strict majority of 3)
- winner_bps: 6000
- juror_bps: 3000
- protocol_bps: 1000

## Evidence
- Signed daily ledger: 17 units received, 23 units dispatched
- No other receipts or dispatches recorded for the day

## Current State (Opportunity 20 - FINAL)
- Phase: EXPIRED_UNCHALLENGED
- Claim posted: "The signed daily ledger records 17 units received and 23 units dispatched, with no other receipts or dispatches recorded for the day."
- Evidence: none posted (challenger never responded)
- Settlement: Creator refunded 1,000,000 (beta bond)
- Juror entitlements: 0 (no juror bonds deposited, no jury reward)
- Episode concluded with no jury participation required

## Actions Available
- Commitment (during COMMIT phase)
- Reveal (during REVEAL phase)
- Withdrawal (after settlement)

## Strategy
1. Wait for claim and evidence to be posted
2. When COMMIT phase arrives, assess creator's claim against common evidence
3. Vote CREATORSUPPORTED if claim aligns with evidence (17 received, 23 dispatched)
4. Vote CHALLENGERSUPPORTED if claim contradicts evidence
5. Reveal during reveal window to recover juror bond + share jury reward
