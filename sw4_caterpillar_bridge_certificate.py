#!/usr/bin/env python3
"""Exact caterpillar certificate for SW_4 coverage 6,572,800..292,031,545.

For each n=70..105, every subset A of {2,...,n-2} defines a valid
caterpillar and has value G(n)+sum_{a in A} Delta_n(a).  A Python integer
encodes the exact bounded subset-sum set.  Arbitrary-precision arithmetic
prevents overflow.
"""
from math import comb

LOW = 6_572_800
HIGH = 292_031_545
N_MIN = 70
N_MAX = 105


def C(n: int, k: int) -> int:
    return comb(n, k) if n >= k >= 0 else 0


def G(n: int) -> int:
    return (n - 1) * C(n - 1, 3)


def Delta(n: int, a: int) -> int:
    return C(n - 1, 4) - C(a, 4) - C(n - a, 4)


def exact_caterpillar_values(n: int, global_cap: int) -> int:
    local_cap = global_cap - G(n)
    if local_cap < 0:
        return 0
    local_mask = (1 << (local_cap + 1)) - 1
    bits = 1
    for a in range(2, n - 1):
        weight = Delta(n, a)
        if weight <= local_cap:
            bits = (bits | (bits << weight)) & local_mask
    return bits << G(n)


def main() -> None:
    attained = 0
    per_order = []
    for n in range(N_MIN, N_MAX + 1):
        values = exact_caterpillar_values(n, HIGH)
        attained |= values
        per_order.append((n, values.bit_count()))

    required = ((1 << (HIGH + 1)) - 1) ^ ((1 << LOW) - 1)
    assert attained & required == required

    print("PASS")
    print(f"orders={N_MIN}..{N_MAX}")
    print(f"coverage={LOW}..{HIGH}")
    print(f"covered_count={HIGH - LOW + 1}")
    print("per_order_distinct_bounded_values:")
    for n, count in per_order:
        print(f"{n},{count}")


if __name__ == "__main__":
    main()
