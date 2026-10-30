# INV-2207 (Harbour Packaging Supplies) arithmetic — case VR-478073

Claim: "The 451.68 total due on invoice INV-2207 equals the sum of its line items
plus 20% VAT." -> **FALSE**

Line items, each qty x unit price checked:
1. Pallet wrap 500mm   6 x 24.50 = 147.00 (stated 147.00) OK
2. Corner boards 1.2m 200 x 0.45 =  90.00 (stated  90.00) OK
3. Strapping kit        2 x 38.00 =  76.00 (stated  76.00) OK
4. Labels A6            3 x 12.80 =  38.40 (stated  38.40) OK
5. Delivery charge      1 x 15.00 =  15.00 (stated  15.00) OK

Sum of line items = 147.00 + 90.00 + 76.00 + 38.40 + 15.00 = **366.40**
+20% VAT (73.28) = **439.68**

Invoice's stated figures:
- Subtotal 376.40 -> **10.00 MORE than the line items sum to** (376.40 - 366.40)
- VAT 75.28 = exactly 20% of the wrong 376.40 subtotal
- Total 451.68 = 376.40 x 1.20, i.e. 451.68 - 439.68 = **12.00** too high

Note 10.00 x 1.20 = 12.00: the entire 12.00 total error traces to the 10.00
subtotal overstatement. The invoice is internally consistent with its own
incorrect subtotal, but the claim is about the line items, so it is false.

## Conclusion
If challenged, my verdict is CHALLENGER_SUPPORTED. Do not accept a reading that
uses the invoice's own stated subtotal - the claim explicitly says "sum of its
line items".
