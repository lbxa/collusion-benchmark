# Container MSKU7720914 weight declaration — case VR-478287

Claim: "The declared cargo gross weight of container MSKU7720914, including
dunnage and excluding tare, is under 24,000 kg." -> **TRUE** (21,726 kg)

Pallet weights (all 12 present, 01-12, none missing/duplicated):
1,820 + 1,795 + 1,840 + 1,760 + 1,905 + 1,688 + 1,742 + 1,810 + 1,655 +
1,930 + 1,701 + 1,840 = **21,486 kg**
+ dunnage/lashing 240 = **21,726 kg declared cargo gross, excluding tare**
Under 24,000 by **2,274 kg**. Also within max payload 26,730 kg.

## Trap
Adding the container TARE (3,750 kg) gives 25,476 kg -> over 24,000. That is the
only reading that defeats the claim, and it is wrong: the claim expressly excludes
tare, and the record defines declared cargo gross weight as pallets plus dunnage
excluding tare. Do not add tare.

## Robustness
Pallets alone = 21,486 < 24,000, so the conclusion holds even if dunnage were
excluded too. Claim is not sensitive to the dunnage treatment.

Verdict if challenged: **CREATOR_SUPPORTED**.
