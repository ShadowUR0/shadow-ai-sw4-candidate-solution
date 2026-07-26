#!/usr/bin/env python3
"""Exact finite verifier for the self-contained SW_4 infinite-tail proof.

The universal part of the proof is mathematical.  This program verifies all
finite witnesses, capacities, boundary orders, and overlap inequalities that
remain after the symbolic lemmas are applied.
"""
from __future__ import annotations

from collections import Counter
from math import ceil, comb
from pathlib import Path

OUT = Path(__file__).resolve().parent


def C(n: int, k: int) -> int:
    return comb(n, k) if n >= k >= 0 else 0


def G(n: int) -> int:
    return (n - 1) * C(n - 1, 3)


def Delta(n: int, a: int) -> int:
    return C(n - 1, 4) - C(a, 4) - C(n - a, 4)


def delta(h: int, x: int) -> int:
    return Delta(2 * h, h + x)


S0 = (0, 2, 2, 3, 6, 6, 10, 10, 12, 12)
S1 = (1, 1, 4, 4, 6, 7, 8, 9, 12, 13)
S2 = (1, 1, 4, 5, 5, 7, 7, 11, 11, 13)
X = (16, 22, 24, 27, 30, 32, 36)
Y = (17, 20, 25, 26, 31, 33, 35)

PAIRS = {
    4: ((72, 78, 85, 90), (73, 76, 88, 88)),
    8: ((8, 58, 71, 73), (45, 46, 51, 84)),
    16: ((77, 83, 90, 95), (78, 81, 93, 93)),
    32: ((81, 87, 94, 99), (82, 85, 97, 97)),
    64: ((22, 43, 64, 71), (25, 48, 54, 75)),
    128: ((15, 28, 39, 51), (23, 23, 37, 52)),
    256: ((9, 24, 64, 87), (29, 40, 40, 91)),
    512: ((14, 14, 29, 35), (18, 18, 21, 37)),
    1024: ((28, 31, 86, 92), (30, 33, 80, 96)),
    2048: ((16, 60, 66, 66), (16, 62, 62, 68)),
    4096: ((55, 61, 67, 70), (57, 58, 69, 69)),
    8192: ((26, 41, 53, 65), (27, 38, 57, 63)),
    16384: ((3, 60, 67, 75), (19, 53, 68, 77)),
    32768: ((13, 20, 43, 47), (15, 21, 44, 45)),
    65536: ((38, 50, 56, 70), (42, 46, 54, 72)),
}

GROUPS = [(S0, S1, S2), (X, Y)] + [PAIRS[d] for d in sorted(PAIRS)]


def square_sum(state: tuple[int, ...]) -> int:
    return sum(x * x for x in state)


def fourth_sum(state: tuple[int, ...]) -> int:
    return sum(x**4 for x in state)


def state_value(h: int, state: tuple[int, ...]) -> int:
    return sum(delta(h, x) for x in state)


def thue_morse_states(R: int, q: int, r: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    xs = [R + r + j * q for j in range(8)]
    even = tuple(xs[j] for j in range(8) if j.bit_count() % 2 == 0)
    odd = tuple(xs[j] for j in range(8) if j.bit_count() % 2 == 1)
    return even, odd


def verify_seed() -> Counter[int]:
    digits: list[int] = []
    demand: Counter[int] = Counter()
    for index, states in enumerate(GROUPS):
        card = len(states[0])
        sq = square_sum(states[0])
        assert all(len(s) == card and square_sum(s) == sq for s in states)
        q4 = [fourth_sum(s) for s in states]
        top = max(q4)
        normalized = sorted(set((top - z) // 12 for z in q4))
        assert all((top - z) % 12 == 0 for z in q4)
        if index == 0:
            assert normalized == [0, 1, 2]
        else:
            assert len(normalized) == 2 and normalized[0] == 0
            digits.append(normalized[1])
        counters = [Counter(s) for s in states]
        for x in set().union(*(set(c) for c in counters)):
            demand[x] += max(c[x] for c in counters)
    assert sorted(digits) == [1] + [2**j for j in range(2, 17)]
    width = 2
    for d in sorted(digits):
        assert d <= width + 1
        width += d
    assert width == 131_071
    assert demand[0] <= 1
    assert max(demand) == 99
    assert all(v <= (1 if x == 0 else 2) for x, v in demand.items())
    return demand


def annuli_for_h(h: int) -> list[tuple[int, int]]:
    R, q = 100, 4
    result: list[tuple[int, int]] = []
    while R + 8 * q - 1 <= h - 2:
        result.append((R, q))
        R += 8 * q
        q = ceil(3 * q / 2)
    return result


def S_formula(h: int) -> int:
    return (
        (h - 101) * C(2 * h - 1, 4)
        - C(h - 99, 5)
        - C(2 * h - 1, 5)
        + C(h + 100, 5)
    )


def raw_positive_polynomial(h: int) -> int:
    return (
        48 * h**5 - 7315 * h**4 + 34790 * h**3
        + 19641055 * h**2 - 59058458 * h + 19539439680
    )


def overlap_polynomial(h: int) -> int:
    return (
        8 * h**5 - 9365 * h**4 + 35340 * h**3
        + 19643615 * h**2 - 59060078 * h + 19539440040
    )


def universal_interval(h: int, seed_demand: Counter[int]) -> tuple[int, int, int, int]:
    assert h >= 365
    L = G(2 * h)
    W = 131_071
    demand = Counter(seed_demand)

    for states in GROUPS:
        values = [state_value(h, s) for s in states]
        L += min(values)

    annuli = annuli_for_h(h)
    for R, q in annuli:
        for r in range(q):
            A, B = thue_morse_states(R, q, r)
            va, vb = state_value(h, A), state_value(h, B)
            d = abs(va - vb)
            assert d == 8 * q**3 * (2 * (R + r) + 7 * q)
            assert d <= W + 1
            W += d
            L += min(va, vb)
            for x in set(A) | set(B):
                demand[x] += 1
                assert demand[x] <= (1 if x == 0 else 2)

    switch_width = W
    assert W >= Delta(2 * h, 2) - 1

    # One still-free cut exists at every outer size a=2,...,h-100.
    for a in range(2, h - 99):
        x = h - a
        assert (2 - demand[x]) >= 1
        weight = Delta(2 * h, a)
        assert weight <= W + 1
        W += weight
        demand[x] += 1

    direct_S = sum(Delta(2 * h, a) for a in range(2, h - 99))
    assert direct_S == S_formula(h)
    assert direct_S >= Delta(2 * h, h)

    # Every remaining raw cut has weight at most the central one.
    remaining: list[int] = []
    for x in range(h - 1):
        capacity = 1 if x == 0 else 2
        assert demand[x] <= capacity
        remaining.extend([delta(h, x)] * (capacity - demand[x]))
    for weight in sorted(remaining):
        assert weight <= W + 1
        W += weight

    return L, L + W, switch_width, len(annuli)


def verify_polynomial_identities() -> None:
    # Both sides are degree at most five, so six exact evaluations suffice as
    # a machine check of the printed coefficient expansions.
    for h in range(200, 206):
        lhs = 120 * (S_formula(h) - Delta(2 * h, h))
        assert lhs == raw_positive_polynomial(h)
        upper = G(2 * h + 2) + (h + 54) * C(2 * h + 1, 4) // 2
        # Use doubled arithmetic when h is odd to avoid any hidden rounding.
        lhs2 = 120 * (G(2 * h) + S_formula(h) + 1) - 60 * (
            2 * G(2 * h + 2) + (h + 54) * C(2 * h + 1, 4)
        )
        assert lhs2 == overlap_polynomial(h)


def verify_prefix_bounds() -> None:
    R, q, W = 100, 4, 131_071
    records = []
    for k in range(1, 8):
        first = 8 * q**3 * (2 * R + 7 * q)
        assert first <= W + 1
        gain = 8 * q**4 * (2 * R + 8 * q - 1)
        W += gain
        R1 = R + 8 * q
        q1 = ceil(3 * q / 2)
        R2 = R1 + 8 * q1
        records.append((k, W, C(2 * R2 - 2, 3) - 1))
        R, q = R1, q1
    assert records[3] == (4, 215_457_655, 199_064_819)
    assert records[4] == (5, 1_607_941_615, 648_686_323)
    assert records[5] == (6, 12_672_515_567, 2_138_222_579)
    assert all(Wk >= target for _, Wk, target in records[3:])


def main() -> None:
    seed_demand = verify_seed()
    verify_polynomial_identities()
    verify_prefix_bounds()

    csv = OUT / "sw4_infinite_tail_overlaps.csv"
    lines = ["h,n,annuli,L,U,switch_width,margin_from_previous"]
    previous_U: int | None = None
    minimum_margin: int | None = None
    minimum_margin_h: int | None = None

    for h in range(365, 1172):
        L, U, switch_width, count = universal_interval(h, seed_demand)
        margin = ""
        if previous_U is not None:
            m = previous_U + 1 - L
            assert m >= 0
            margin = str(m)
            if minimum_margin is None or m < minimum_margin:
                minimum_margin, minimum_margin_h = m, h
        lines.append(f"{h},{2*h},{count},{L},{U},{switch_width},{margin}")
        previous_U = U

    csv.write_text("\n".join(lines) + "\n", encoding="utf-8")

    L365, U365, _, _ = universal_interval(365, seed_demand)
    assert (L365, U365) == (1_596_122_112_921, 3_577_546_733_067)
    assert minimum_margin == 1_960_269_091_932 and minimum_margin_h == 366

    # Symbolic overlap is positive from h=1171 because each displayed group
    # of terms is then positive.
    assert 8 * 1171 - 9365 > 0
    assert 19643615 * 1171 - 59060078 > 0
    assert overlap_polynomial(1171) > 0
    assert raw_positive_polynomial(365) > 0

    print("PASS")
    print("universal_h_start=365")
    print(f"universal_first_interval={L365}..{U365}")
    print("finite_overlap_check_h=365..1171")
    print(f"minimum_finite_margin={minimum_margin} at h={minimum_margin_h}")
    print("symbolic_overlap_h>=1171")
    print("universal_union_start=1596122112921")


if __name__ == "__main__":
    main()
