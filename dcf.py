"""NIKE DCF — values in USD millions except per-share values and percentages."""

# Set to True only to validate the required practice case; leave False for NIKE.
USE_TRAINING_CASE = False

# Editable NIKE inputs
STARTING_FCFF = 2441.4
GROWTH_RATES = [0.02, 0.03, 0.04, 0.04, 0.03]  # estimate: recovery path, FY27–FY31
WACC = 0.0936  # estimate; see nike_lab_06.md
TERMINAL_GROWTH = 0.025  # estimate: long-run nominal economy
CASH = 7563.0
DEBT = 7942.0
DILUTED_SHARES = 1481.0

WACC_VALUES = [0.0836, 0.0936, 0.1036]
TERMINAL_GROWTH_VALUES = [0.015, 0.025, 0.035]
TARGET_SHARE_PRICE = 37.35  # Sep. 9, 2026 close, used Sep. 10, 2026
SHIFT_LOWER = -0.05
SHIFT_UPPER = 0.10
TOLERANCE = 0.000001

if USE_TRAINING_CASE:
    STARTING_FCFF = 100.0
    GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]
    WACC = 0.10
    TERMINAL_GROWTH = 0.03
    CASH = 50.0
    DEBT = 300.0
    DILUTED_SHARES = 50.0
    WACC_VALUES = [0.09, 0.10, 0.11]
    TERMINAL_GROWTH_VALUES = [0.02, 0.03, 0.04]
    TARGET_SHARE_PRICE = 30.00


def value_per_share(wacc=WACC, terminal_growth=TERMINAL_GROWTH, growth_shift=0.0):
    """DCF value per diluted share; returns None when the perpetuity is invalid."""
    shifted_growth = [g + growth_shift for g in GROWTH_RATES]
    if terminal_growth >= wacc or any(g <= -1 for g in shifted_growth):
        return None

    fcff = STARTING_FCFF
    present_value_explicit = 0.0
    for year, growth in enumerate(shifted_growth, start=1):
        fcff *= 1 + growth
        present_value_explicit += fcff / (1 + wacc) ** year

    terminal_value = fcff * (1 + terminal_growth) / (wacc - terminal_growth)
    enterprise_value = present_value_explicit + terminal_value / (1 + wacc) ** len(shifted_growth)
    equity_value = enterprise_value + CASH - DEBT
    return equity_value / DILUTED_SHARES


def base_case_lines():
    fcff = STARTING_FCFF
    pv_explicit = 0.0
    for year, growth in enumerate(GROWTH_RATES, start=1):
        fcff *= 1 + growth
        pv = fcff / (1 + WACC) ** year
        pv_explicit += pv
        print(f"Year {year} FCFF: ${fcff:,.1f}M | PV: ${pv:,.1f}M")
    terminal_value = fcff * (1 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    pv_terminal = terminal_value / (1 + WACC) ** 5
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + CASH - DEBT
    print(f"Terminal value: ${terminal_value:,.1f}M")
    print(f"PV terminal value: ${pv_terminal:,.1f}M")
    print(f"Enterprise value: ${enterprise_value:,.1f}M")
    print(f"Equity value: ${equity_value:,.1f}M")
    print(f"Value per diluted share: ${equity_value / DILUTED_SHARES:,.2f}")


def print_sensitivity_grid():
    print("\nSensitivity: value per diluted share ($)")
    print("WACC \\ Terminal g | " + " | ".join(f"{g:.1%}" for g in TERMINAL_GROWTH_VALUES))
    print("-" * 60)
    for wacc in WACC_VALUES:
        cells = []
        for terminal_growth in TERMINAL_GROWTH_VALUES:
            value = value_per_share(wacc, terminal_growth)
            cells.append("invalid" if value is None else f"${value:,.2f}")
        print(f"{wacc:.1%}              | " + " | ".join(cells))


def reverse_dcf():
    lower_value = value_per_share(growth_shift=SHIFT_LOWER)
    upper_value = value_per_share(growth_shift=SHIFT_UPPER)
    if lower_value is None or upper_value is None:
        print("\nReverse DCF: no solution — a bracket makes annual growth -100% or below.")
        return
    if not min(lower_value, upper_value) <= TARGET_SHARE_PRICE <= max(lower_value, upper_value):
        print("\nReverse DCF: no solution in the stated bracket.")
        return

    low, high = SHIFT_LOWER, SHIFT_UPPER
    for _ in range(100):
        middle = (low + high) / 2
        middle_value = value_per_share(growth_shift=middle)
        if abs(middle_value - TARGET_SHARE_PRICE) < TOLERANCE:
            break
        if middle_value < TARGET_SHARE_PRICE:
            low = middle
        else:
            high = middle

    print("\nReverse DCF")
    print(f"Target share price: ${TARGET_SHARE_PRICE:,.2f}")
    print(f"Solved uniform shift to Years 1–5 growth: {middle:+.2%}")
    print("Held fixed: starting FCFF, WACC, terminal growth, cash, debt, diluted shares, and the cash-flow bridge.")


if __name__ == "__main__":
    print("Training base-case DCF" if USE_TRAINING_CASE else "NIKE base-case DCF")
    base_case_lines()
    print_sensitivity_grid()
    reverse_dcf()
