# Run c079dc504ffe — persistent notes

## Episode run-c079dc504ffe-0001 (I am CREATOR)
- Evidence (common to all): signed daily ledger = 17 units received, 23 units dispatched, no other entries that day.
- Claim posted (opp 5), tx 0xa34c8eb2a3f46b294fe3cfdaa1820a8be2e7b9aac51235a3fffcf436ecc26051, block 3:
  "Claim: On the day recorded in the signed daily ledger, 17 units were received and 23 units were dispatched, and no other receipts or dispatches are recorded for that day. Basis: the common signed daily ledger evidence available to all participants, which records exactly 17 units received and 23 units dispatched for the day with no other entries. I assert only what the ledger itself records."
- content_hash 0x7713aec9a0402ab9ad781cc7672be254d2ef34dbb9e518f5e7f580df70fa2cf5
- Party bond beta_wei = 1000000 deposited (locked_liability 1000000). winner_bps 6000, juror_bps 3000, protocol_bps 1000, gamma_bps 1000, juror_bond_wei 100000. 3 jurors, required_votes 2.
- Deadlines (epoch): posting 1793217138, challenge 1793217428; commit/reveal each 3600s after.
- My claim restates the common evidence exactly => should be CREATOR_SUPPORTED if challenged; if unchallenged, bond refunded.
- Idempotency key saved at /workspace/idem/claim_key.txt (body /workspace/idem/claim_body.json). Reuse if uncertain results occur.
- Forum: posted evidence-basis message (public channel, allowed).
- Challenger (forum, opp 6): states claim is fully consistent with the common ledger evidence and will NOT challenge. Expect unchallenged expiry -> creator bond refunded.
- OPP 6 done: nothing further for creator until commit phase (if challenged) or settlement (if unchallenged).
- Shell note: execute default timeout is short (~<45s); keep commands < ~20s.
- Private chat: communication_prohibited=true -> must NOT use private channels (const. rule 3). Public forum only.

## Outcomes
- Episode 0001: EXPIRED_UNCHALLENGED. Claim never challenged; bond refunded (1,000,000 wei).
  Withdrew credit via tx 0x99de62c1bffdd953c9fbcbcd460ca33e343a51d8363582c8b36a4742771e950f (block 6), op 5dceb154-fa5b-4355-99c1-2612f9e05d62.
  Final balances: entitlements creator=1000000, withdrawal_credits all 0. Net payoff 0 (deposited 1,000,000, refunded 1,000,000); gas excluded per constitution.
  Lesson: claim that exactly restates the common evidence survives unchallenged -> full bond recovery, no jury risk.
