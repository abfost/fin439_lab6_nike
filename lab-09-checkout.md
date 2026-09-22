# Lab 09 — Pro-Forma Build: ABG proof

**Submission files:** `lab-09-checkout.md` and `proforma.py`.

**Commands run:** `python proforma.py` and `python proforma.py --break-test`.

## Prework response

The three judgments that carry the ABG valuation are organic revenue growth, SG&A as a share of gross profit, and the cost-of-equity/terminal-growth pair. Growth determines the size of the future revenue and gross-profit base. SG&A efficiency determines how much of that gross profit becomes operating income. The discount rate and terminal growth determine the value placed on the large share of cash flows after the explicit forecast period.

Cash is computed last because it is the result of the operating forecast, investment spending, working-capital movements, borrowing, debt repayment, and buybacks. Treating it as an independent assumption could hide an imbalance in those earlier calculations.

## ABG model proof

`proforma.py` projects FY2026E–FY2030E from the provided FY2025 opening balance sheet. It calculates income-statement lines first, projects the balance sheet except cash, then computes FCFE and cash. The balance-sheet and minimum-cash checks run before valuation.

| Line (USD millions unless noted) | FY2026E | FY2030E |
| --- | ---: | ---: |
| Revenue | 18,323.0 | 19,678.3 |
| Operating income | 844.2 | 971.4 |
| Net income | 413.6 | 527.5 |
| FCFE | 211.4 | 342.3 |
| Cash, year end | 101.8 | 719.8 |
| Assets − liabilities − equity | 0.0 | 0.0 |
| Value per share | $291.75 | $291.75 |

The present value attributable to cash flows after 2030 is 79.8%.

## Break test

If FY2026 cash is replaced with the opening cash balance of 40.4 rather than its calculated value, `assert_balanced` raises `FY2026E is not balanced: gap -61.4`. The included `--break-test` command performs this proof without changing the base-case file. The model therefore refuses to value an unbalanced forecast.

## Floor-plan explanation

Floor-plan financing is inventory borrowing, commonly provided by manufacturers' finance arms or banks to auto dealerships. Because the loan balance rises and falls with inventory, the model forecasts floor-plan debt from inventory and includes interest on the opening balance. Removing it would remove a major financing source for vehicle inventory and push cash sharply negative.
