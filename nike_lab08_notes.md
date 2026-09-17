# Lab 08 — Nike deal evidence and valuation triangulation

**Target:** NIKE, Inc. (NYSE: NKE)  
**Comparison date:** September 3, 2026  
**Week 3 DCF date/range:** $19.97–$34.34 per Nike share

## 1. Start with your own policy

Your lab specifically requires this paragraph to be your own writing before AI selection. Write it here after reading Nike's 10-K:

> **My peer policy:** I will compare Nike with publicly traded companies that earn money from designing, marketing, and selling athletic footwear and apparel. A peer should have global consumer-brand exposure and sell through wholesale partners and direct-to-consumer channels. I will qualify companies with meaningful size differences, product variety, growth, and geography, and exclude the companies that have noticible differences in product mix, geography, size and currency, or business model. 

Useful check before choosing: a familiar brand is not enough; explain why each company's earnings drivers resemble Nike's.

## 2. Candidate evidence log — verify these sources yourself

| Candidate | Initial decision | Business-model evidence | Important difference from Nike | Latest annual diluted EPS public by Sep. 3, 2026 | What you must personally verify |
| --- | --- | --- | --- | --- | --- |
| Deckers Outdoor (DECK) | **Qualify** | [FY2026 Form 10-K, Business](https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm) — designs, markets and distributes footwear, apparel and accessories; HOKA and UGG brands; direct-to-consumer and wholesale channels. | It is much smaller and its UGG lifestyle/sheepskin franchise makes its mix less directly athletic than Nike's. | **$7.02**, FY ended Mar. 31, 2026; reported May 21, 2026. See [FY2026 results](https://www.sec.gov/Archives/edgar/data/910521/000091052126000007/deckex991pressrelease-3312.htm) and [10-K EPS table](https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm). | Open the links, locate the quoted sections/table, and decide whether *qualify* is your decision. |
| adidas AG (ADS.DE) | **Exclude from this first U.S.-dollar calculator; investigate** | [2025 annual report](https://report.adidas-group.com/2025/en/at-a-glance/about-this-report.html) and [EPS note](https://report.adidas-group.com/2025/en/consolidated-financial-statements/notes/notes-to-the-consolidated-income-statement/earnings-per-share.html). It is a global sportswear/footwear brand, making its core consumer economics relevant. | Its ordinary shares and EPS are euro-denominated and it reports under IFRS. A valid P/E can be computed in euros, but price and EPS must use the same listing/currency before its multiple is brought into this work. | **€7.46**, FY ended Dec. 31, 2025; annual-report publication shown as Mar. 3, 2026. | Open the report and find the business section, EPS note, and a same-date German-exchange close if you decide to include it. |

## 3. Inputs entered in the calculator

All prices use the **September 3, 2026 closing price**; EPS is annual reported diluted EPS, not quarterly or adjusted EPS.

| Company | Price | Annual diluted EPS | Fiscal year-end | Earnings publication | Source / locator |
| --- | ---: | ---: | --- | --- | --- |
| Nike (NKE) | $38.77 | $2.10 | May 31, 2026 | June 30, 2026 results; July 15, 2026 10-K | [Price history](https://stockanalysis.com/stocks/nke/history/), Sep. 3 close; [Nike FY2026 10-K](https://www.sec.gov/Archives/edgar/data/320187/000032018726000088/nke-20260531.htm), Consolidated Statements of Income / EPS table. |
| Deckers (DECK) | $84.50 | $7.02 | Mar. 31, 2026 | May 21, 2026 | [Price history](https://www.klickanalytics.com/symbol_performance?sid=1176), Sep. 3 close; [Deckers FY2026 results](https://www.sec.gov/Archives/edgar/data/910521/000091052126000007/deckex991pressrelease-3312.htm), FY2026 diluted EPS. |

## 4. Calculator result and validation

Run:

```text
python nike_lab08_pe_comps.py
```

Expected checked arithmetic: Deckers P/E = **$84.50 ÷ $7.02 = 12.0370x**. Applied to Nike: **12.0370x × $2.10 = $25.28** per Nike share.

Because one peer is currently admitted, this is a **reference estimate, not a range**. Removing Deckers leaves no estimate. Do not describe this as a robust market consensus.

## 5. Compare it with your DCF — complete after pasting your range

| Method | Nike result and date | Main assumption or limitation |
| --- | --- | --- |
| Week 3 DCF | **[paste your saved DCF range and date]** | Your forecast and discount-rate assumptions. |
| Peer P/E | $25.28 reference estimate, Sep. 3, 2026 | One qualified peer; its HOKA/UGG mix and Deckers' higher growth/profitability may limit transferability. |

## 6. Skeptical review and your judgment

**Skeptical question:** Deckers' P/E is based on a company with very strong HOKA/UGG earnings growth, while Nike's FY2026 earnings reflect a turnaround. Why should Deckers' multiple be transferable to Nike, rather than evidence that this single-peer estimate is too weak for a firm valuation range?

**My response after checking sources:** **[accept / reject / unresolved]** Accept - Deckers is a useful peer because it sells branded footwear through direct-to-consumer and wholesale channels, but is not interchangeable with Nike. They have a smaller business with a wide brand mix, including HOKA and UGG, while Nike has a broader business. Because Deckers is the only admitted peer, its $23.90 implied value is a reference estimate, rather than a dependable range. I would change my view if I found another company with closely comparable economics and same-date price data.

## 7. Reflection draft prompts 

1.  I qualified Deckers because it sells branded footwear and apprel through wholesale and direct-to-consumer channels. They are not a direct match because they are smaller and have different major brands, including HOKA and UGG.
2.  The $23.90 P/E reference is inside the DCF range of $19.97-$34.34, so the methods support each other. Both are found below Nike's $36.62 market price, but the P/E result is limited because only qualified peer is used.
3. I would watch-defer. I would also reconsider if Nike's Direct and digital sales see improvement, Greater China starts to stabilize, and Nike shows stronger margins. 

## Sources used in this setup

- [Nike FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/320187/000032018726000088/nke-20260531.htm), filed July 15, 2026.
- [Deckers FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm), filed May 22, 2026.
- [Deckers FY2026 earnings release](https://www.sec.gov/Archives/edgar/data/910521/000091052126000007/deckex991pressrelease-3312.htm), May 21, 2026.
- [adidas 2025 annual report](https://report.adidas-group.com/2025/en/at-a-glance/about-this-report.html), published March 3, 2026.
