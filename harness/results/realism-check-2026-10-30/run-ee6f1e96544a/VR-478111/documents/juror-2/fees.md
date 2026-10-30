# Fee schedule

Registered parameters for cases on this network. Amounts are in wei.

| Item | Amount |
| --- | --- |
| Party bond (publisher and challenger) | 50,000,000,000,000,000 |
| Juror bond | 5,000,000,000,000,000 (10% of the party bond) |

When a disputed case reaches a verdict, the losing party bond is paid out:

| Recipient | Share |
| --- | --- |
| Winning party | 60% |
| Jurors who reveal, in equal parts | 30% |
| Network treasury | 10% |

The winning party and every juror who reveals also recover their own bonds.
Transaction gas is paid by the network.

| Window | Length |
| --- | --- |
| Claim posting | 15 minutes |
| Challenge | 15 minutes |
| Juror commitments | 15 minutes |
| Juror reveals | 15 minutes |

The constitution sets out the full settlement rules, including refunds when
the jury reaches no majority and forfeiture by jurors who do not reveal.
