"""Lab 08 comparable-company P/E calculator: NIKE, Inc.

All amounts are per share in U.S. dollars.  The frozen comparison date is
September 10, 2026, matching the saved Nike DCF model date.  Run: python nike_lab08_pe_comps.py
"""

from statistics import median


TARGET = {
    "ticker": "NKE",
    "name": "NIKE, Inc.",
    "price": 36.62,
    "diluted_eps": 2.10,
}

# Include only candidates that you have personally marked Use or Qualify.
PEERS = [
    {
        "ticker": "DECK",
        "name": "Deckers Outdoor",
        "price": 79.88,
        "diluted_eps": 7.02,
    },
]


def valid_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def pe_multiple(company):
    if not valid_number(company.get("price")) or not valid_number(company.get("diluted_eps")):
        return None
    return company["price"] / company["diluted_eps"]


def label(company):
    return f"{company.get('name', 'Unnamed company')} ({company.get('ticker', 'no ticker')})"


def remaining_estimate(peers, target_eps):
    multiples = [pe_multiple(peer) for peer in peers]
    valid_multiples = [multiple for multiple in multiples if multiple is not None]
    if not valid_multiples or not valid_number(target_eps):
        return None
    return median(valid_multiples) * target_eps


def main():
    print("Comparable-Company P/E Analysis — NIKE")
    print("=" * 37)
    target_multiple = pe_multiple(TARGET)
    print(f"Target: {label(TARGET)} P/E: {target_multiple:.6f}x (context only)")
    print()

    valid_peers = []
    for peer in PEERS:
        multiple = pe_multiple(peer)
        if multiple is None:
            print(f"Peer: {label(peer)} P/E: not meaningful")
        else:
            valid_peers.append(peer)
            print(f"Peer: {label(peer)} P/E: {multiple:.6f}x")

    if not valid_peers:
        print("\nImplied prices: no usable peers.")
        return

    multiples = [pe_multiple(peer) for peer in valid_peers]
    full_estimate = median(multiples) * TARGET["diluted_eps"]
    print(f"\nPeer median P/E: {median(multiples):.6f}x")
    if len(valid_peers) == 1:
        print(f"Reference estimate (one peer; no range): ${full_estimate:.2f}")
    else:
        print(f"Implied price range: ${min(multiples) * TARGET['diluted_eps']:.2f}-${max(multiples) * TARGET['diluted_eps']:.2f}")
        print(f"Implied price at peer median: ${full_estimate:.2f}")

    print("\nLeave-one-peer-out sensitivity")
    for removed_peer in valid_peers:
        remaining = [peer for peer in valid_peers if peer is not removed_peer]
        estimate = remaining_estimate(remaining, TARGET["diluted_eps"])
        if estimate is None:
            print(f"Remove {removed_peer['ticker']}: no estimate (no valid peers remain).")
        else:
            print(f"Remove {removed_peer['ticker']}: ${estimate:.2f}")


if __name__ == "__main__":
    main()
