"""Five-year three-statement pro-forma: Asbury Automotive Group base case.

All values are USD millions except per-share values and share count.

Run: python proforma.py
Proof of the required refusal: python proforma.py --break-test
"""

import sys

YEARS = range(2026, 2031)

ASSUMPTIONS = {
    "growth": 0.018,
    "gross_margin": 0.1705,
    "sga_to_gross_profit": [0.665, 0.655, 0.645, 0.645, 0.645],
    "depreciation_to_opening_ppe": 82.4 / 3070.4,
    "impairment": 120.0,
    "capex": 250.0,
    "tax_rate": 0.255,
    "inventory_days": 2135.8 / (17999.0 - 3071.7) * 365,
    "floor_plan_to_inventory": 2027.0 / 2135.8,
    "other_working_capital_to_revenue_change": 0.008,
    "minimum_cash": 25.0,
    "revolver_limit": 850.0,
    "revolver_rate": 0.06,
    "debt_repayment": 150.0,
    "share_buyback": 150.0,
    "floor_plan_rate": 0.0467,
    "term_debt_rate": 0.0544,
    "cost_of_equity": 0.10,
    "terminal_growth": 0.025,
    "shares_outstanding": 17.951349,
}

OPENING = {
    "revenue": 17999.0,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "cash": 40.4,
    "floor_plan": 2027.0,
    "term_debt": 3572.0,
    "revolver": 0.0,
    "other_liabilities": 2127.5,
    "equity": 3891.7,
}


def assert_balanced(year, statement, tolerance=0.05):
    """Stop the model if a projected balance sheet or cash covenant is invalid."""
    gap = statement["assets"] - statement["liabilities"] - statement["equity"]
    if abs(gap) > tolerance:
        raise ValueError(f"FY{year}E is not balanced: gap {gap:.1f}")
    if statement["cash"] < ASSUMPTIONS["minimum_cash"] - tolerance:
        raise ValueError(f"FY{year}E cash is below the minimum: {statement['cash']:.1f}")


def project():
    prior = OPENING.copy()
    results = []

    for index, year in enumerate(YEARS):
        revenue = prior["revenue"] * (1 + ASSUMPTIONS["growth"])
        gross_profit = revenue * ASSUMPTIONS["gross_margin"]
        sga = gross_profit * ASSUMPTIONS["sga_to_gross_profit"][index]
        depreciation = prior["ppe"] * ASSUMPTIONS["depreciation_to_opening_ppe"]
        impairment = ASSUMPTIONS["impairment"]
        operating_income = gross_profit - sga - depreciation - impairment
        interest = (
            prior["floor_plan"] * ASSUMPTIONS["floor_plan_rate"]
            + prior["term_debt"] * ASSUMPTIONS["term_debt_rate"]
            + prior["revolver"] * ASSUMPTIONS["revolver_rate"]
        )
        pretax_income = operating_income - interest
        taxes = max(0.0, pretax_income) * ASSUMPTIONS["tax_rate"]
        net_income = pretax_income - taxes

        inventory = (revenue - gross_profit) * ASSUMPTIONS["inventory_days"] / 365
        floor_plan = inventory * ASSUMPTIONS["floor_plan_to_inventory"]
        ppe = prior["ppe"] + ASSUMPTIONS["capex"] - depreciation
        other_working_capital_change = (
            ASSUMPTIONS["other_working_capital_to_revenue_change"]
            * (revenue - prior["revenue"])
        )
        other_assets = prior["other_assets"] + other_working_capital_change - impairment
        term_debt = prior["term_debt"] - ASSUMPTIONS["debt_repayment"]
        other_liabilities = prior["other_liabilities"]
        equity = prior["equity"] + net_income - ASSUMPTIONS["share_buyback"]

        fcfe = (
            net_income + depreciation + impairment - ASSUMPTIONS["capex"]
            - (inventory - prior["inventory"])
            - other_working_capital_change
            + (floor_plan - prior["floor_plan"])
            - ASSUMPTIONS["debt_repayment"]
        )
        pre_revolver_cash = prior["cash"] + fcfe - ASSUMPTIONS["share_buyback"]
        revolver = prior["revolver"]
        if pre_revolver_cash < ASSUMPTIONS["minimum_cash"]:
            draw = ASSUMPTIONS["minimum_cash"] - pre_revolver_cash
            revolver += draw
            if revolver > ASSUMPTIONS["revolver_limit"]:
                raise ValueError(f"FY{year}E revolver limit exceeded: {revolver:.1f}")
            cash = ASSUMPTIONS["minimum_cash"]
        else:
            repayment = min(revolver, pre_revolver_cash - ASSUMPTIONS["minimum_cash"])
            revolver -= repayment
            cash = pre_revolver_cash - repayment

        statement = {
            "year": year, "revenue": revenue, "gross_profit": gross_profit, "sga": sga,
            "depreciation": depreciation, "impairment": impairment,
            "operating_income": operating_income, "interest": interest,
            "pretax_income": pretax_income, "taxes": taxes, "net_income": net_income,
            "inventory": inventory, "ppe": ppe, "other_assets": other_assets,
            "cash": cash, "floor_plan": floor_plan, "term_debt": term_debt,
            "revolver": revolver, "other_liabilities": other_liabilities, "equity": equity,
            "fcfe": fcfe,
        }
        statement["assets"] = inventory + ppe + other_assets + cash
        statement["liabilities"] = floor_plan + term_debt + revolver + other_liabilities
        statement["liabilities_and_equity"] = statement["liabilities"] + equity
        statement["balance_sheet_gap"] = statement["assets"] - statement["liabilities"] - equity
        assert_balanced(year, statement)
        results.append(statement)
        prior = {**prior, **statement}
    return results


def print_table(title, rows, results, decimals=1):
    print(f"\n{title}")
    print(f"{'USD millions':<30}" + "".join(f"FY{x['year']}E".rjust(12) for x in results))
    for label, key in rows:
        print(f"{label:<30}" + "".join(f"{x[key]:>12,.{decimals}f}" for x in results))


def value_equity(results):
    cost = ASSUMPTIONS["cost_of_equity"]
    terminal = ((results[-1]["fcfe"] + ASSUMPTIONS["debt_repayment"])
                * (1 + ASSUMPTIONS["terminal_growth"])) / (cost - ASSUMPTIONS["terminal_growth"])
    pv_fcfe = sum(row["fcfe"] / (1 + cost) ** number
                  for number, row in enumerate(results, start=1))
    pv_terminal = terminal / (1 + cost) ** len(results)
    equity_value = pv_fcfe + pv_terminal
    return equity_value, pv_terminal / equity_value, equity_value / ASSUMPTIONS["shares_outstanding"]


def break_test():
    """Intentionally replace FY2026 cash with opening cash and prove the guard fires."""
    first_year = project()[0].copy()
    first_year["cash"] = OPENING["cash"]
    first_year["assets"] = (
        first_year["inventory"] + first_year["ppe"]
        + first_year["other_assets"] + first_year["cash"]
    )
    try:
        assert_balanced(first_year["year"], first_year)
    except ValueError as error:
        print(f"Break test passed: {error}")
        return
    raise AssertionError("Break test failed: valuation guard did not reject broken cash.")


def main():
    results = project()
    print_table("INCOME STATEMENT", [
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
        ("Depreciation", "depreciation"), ("Impairment", "impairment"),
        ("Operating income", "operating_income"), ("Interest", "interest"),
        ("Taxes", "taxes"), ("Net income", "net_income"),
    ], results)
    print_table("BALANCE SHEET", [
        ("Inventory", "inventory"), ("PP&E", "ppe"), ("Other assets", "other_assets"),
        ("Cash", "cash"), ("Assets", "assets"), ("Floor plan", "floor_plan"),
        ("Term debt", "term_debt"), ("Revolver", "revolver"),
        ("Other liabilities", "other_liabilities"), ("Equity", "equity"),
        ("Liabilities + equity", "liabilities_and_equity"),
    ], results)
    print_table("CASH FLOW", [("Free cash flow to equity", "fcfe")], results)
    print_table("CHECKS", [
        ("Assets - liabilities - equity", "balance_sheet_gap"), ("Cash at or above minimum", "cash"),
    ], results)
    equity_value, terminal_share, value_per_share = value_equity(results)
    print(f"\nEquity value: ${equity_value:,.1f} million")
    print(f"Share of value after 2030: {terminal_share:.1%}")
    print(f"Value per share: ${value_per_share:,.2f}")


if __name__ == "__main__":
    if "--break-test" in sys.argv:
        break_test()
    else:
        main()
