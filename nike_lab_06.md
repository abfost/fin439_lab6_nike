# Lab 06 — NIKE, Inc. (NKE): Sensitivity, Reverse DCF, and Conditional Recommendation

**Model date:** September 10, 2026.  **Currency:** USD millions, except per-share amounts.

## Inputs and sources

| Input | Model value | Status | As-of date and exact locator | Basis |
|---|---:|---|---|---|
| Starting FCFF | $2,441.4M | Calculated | May 31, 2026; NIKE FY2026 Form 10-K, Consolidated Statements of Cash Flows, p. 58 | Operating cash flow $2,868M + after-tax interest paid $257.4M − capex $684M. Interest paid was $323M; tax rate is $792M / $3,900M = 20.31%. |
| Years 1–5 FCFF growth | 2%, 3%, 4%, 4%, 3% | **Estimate** | September 10, 2026; 10-K Item 7 MD&A, pp. 42–51 | A deliberately gradual recovery path: fiscal 2026 revenue was essentially flat, while management describes an ongoing reset and expects Greater China and Converse pressure through 2027. This is a forecast, not company guidance. |
| WACC | 9.36% | **Estimate** | September 9–10, 2026; sources below | Cost of equity = 4.79% 10-year Treasury + 1.11 beta × 5% equity premium = 10.34%. After-tax debt cost = 3.16% blended note coupon × (1 − 20.31%) = 2.52%. Weights: $55.41B equity market value and $7.942B debt book value. |
| Terminal growth | 2.5% | **Estimate** | September 10, 2026 | Conservative long-run nominal-economy assumption; it is below WACC. |
| Cash | $7,563M | Sourced | May 31, 2026; 10-K Consolidated Balance Sheets, p. 57 | Cash and equivalents. |
| Debt | $7,942M | Sourced | May 31, 2026; 10-K Note 6, p. 70 | Total corporate term debt book value. |
| Diluted shares | 1,481.0M | Sourced | Year ended May 31, 2026; 10-K Note 10, p. 77 | Diluted weighted-average common shares outstanding. |
| Share price | $37.35 | Sourced | September 9, 2026, 4:00 p.m. ET close; checked September 10, 2026 | NKE NYSE closing price. |

## Base case and reasonableness

Before the NIKE run, I set `USE_TRAINING_CASE = True` in `dcf.py`. The training sensitivity grid reproduces the required table cell-for-cell and the reverse DCF solves to **+1.78 percentage points**. I then returned the setting to `False` for the NIKE results below.

Run `python dcf.py` to produce the detailed base case. The result is **$25.08 per diluted share**, beside the September 9 close of **$37.35**. The model is **inside** the 0.5×–2× reasonableness band (the band is $18.68–$74.70), though it is below the market price.

The input I distrust most is the five-year FCFF growth path. It is an estimate constructed during a turnaround: fiscal 2026 revenue was flat, while NIKE Direct revenue fell 6%, NIKE Digital fell 12%, Greater China revenue fell 11%, and Converse revenue fell 32%. A single five-year recovery path can be wrong even if the accounting inputs are correct.

## Sensitivity and reverse DCF

The sensitivity grid uses WACC values of 8.36%, 9.36%, and 10.36%, with terminal-growth values of 1.5%, 2.5%, and 3.5%. Value falls as WACC rises and rises as terminal growth rises. The corners give a range of **$19.97–$34.34** per share.

| WACC \ terminal growth | 1.5% | 2.5% | 3.5% |
|---|---:|---:|---:|
| 8.36% | $25.94 | $29.43 | $34.34 |
| 9.36% | $22.58 | **$25.08** | $28.44 |
| 10.36% | $19.97 | $21.84 | $24.25 |

The reverse DCF targets **$37.35** and solves for a uniform shift to all five explicit growth rates, using bisection between −5 and +10 percentage points. It requires a **+9.50 percentage-point** shift (about 9.498 points). It holds starting FCFF, WACC, terminal growth, cash, debt, diluted shares, and the cash-flow bridge fixed. The resulting shift is one assumption set consistent with the price; it does not prove mispricing.

## Conditional call

**Watch-defer. Initiate if NIKE demonstrates sustained NIKE Direct and digital growth, stabilization in Greater China, and margin improvement not driven mainly by discounting — and the observed results support at least the model’s recovery path. Otherwise, defer. Monitor next quarter’s NIKE Direct revenue and gross margin.**

## Sources

1. [NIKE FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/320187/000032018726000088/nke-20260531.htm), filed July 15, 2026. Cash flow statement p. 58; balance sheet p. 57; debt note p. 70; EPS note p. 77.
2. [Federal Reserve H.15, September 9, 2026](https://www.federalreserve.gov/releases/h15/), 10-year Treasury constant maturity of 4.79%.
3. [NIKE statistics](https://stockanalysis.com/stocks/nke/statistics/), checked September 10, 2026: beta 1.11 and equity market value $55.41B, data attributed to S&P Global Market Intelligence.
4. [NKE price history](https://stockanalysis.com/stocks/nke/history/), checked September 10, 2026: September 9, 2026 closing price $37.35.
