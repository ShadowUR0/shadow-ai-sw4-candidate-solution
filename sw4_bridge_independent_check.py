#!/usr/bin/env python3
"""Independent Python audit of the C++ SW_4 bridge certificate.

It checks every CSV interval junction and independently recomputes the six
boundary orders where the three constructions join the prior certificates or
each other.
"""
from __future__ import annotations

import csv
from collections import Counter
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "sw4_complete_bridge_output.txt"


def C(n: int, k: int) -> int:
    return comb(n, k) if n >= k >= 0 else 0


def G(n: int) -> int:
    return (n - 1) * C(n - 1, 3)


def Delta(n: int, a: int) -> int:
    return C(n - 1, 4) - C(a, 4) - C(n - a, 4)


def delta(h: int, x: int) -> int:
    return Delta(2 * h, h + x)


def value(h: int, state: tuple[int, ...]) -> int:
    return sum(delta(h, x) for x in state)


BASE3 = (
    (0, 2, 2, 3, 6, 6, 10, 10, 12, 12),
    (1, 1, 4, 4, 6, 7, 8, 9, 12, 13),
    (1, 1, 4, 5, 5, 7, 7, 11, 11, 13),
)
UNIT = (
    (16, 22, 24, 27, 30, 32, 36),
    (17, 20, 25, 26, 31, 33, 35),
)

SEED51 = (BASE3, UNIT,
    ((23, 28, 32, 49), (18, 25, 42, 45)),
    ((16, 24, 45, 51), (8, 28, 47, 49)),
    ((20, 29, 46, 50), (14, 36, 42, 51)),
    ((9, 39, 39, 46), (23, 29, 37, 50)),
)

SEED65 = (BASE3, UNIT,
    ((23, 28, 32, 49), (18, 25, 42, 45)),
    ((21, 24, 45, 51), (19, 27, 43, 52)),
    ((14, 38, 55, 55), (3, 43, 54, 54)),
    ((9, 39, 39, 46), (23, 29, 37, 50)),
    ((17, 28, 44, 59), (15, 36, 37, 60)),
    ((18, 35, 48, 48), (26, 29, 44, 52)),
    ((20, 40, 58, 65), (16, 42, 60, 63)),
    ((57, 57, 63, 64), (56, 59, 61, 65)),
    ((14, 34, 41, 53), (15, 30, 46, 51)),
)

SEED100 = (BASE3, UNIT,
    ((72,78,85,90), (73,76,88,88)),
    ((8,58,71,73), (45,46,51,84)),
    ((77,83,90,95), (78,81,93,93)),
    ((81,87,94,99), (82,85,97,97)),
    ((22,43,64,71), (25,48,54,75)),
    ((15,28,39,51), (23,23,37,52)),
    ((9,24,64,87), (29,40,40,91)),
    ((14,14,29,35), (18,18,21,37)),
    ((28,31,86,92), (30,33,80,96)),
    ((16,60,66,66), (16,62,62,68)),
    ((55,61,67,70), (57,58,69,69)),
    ((26,41,53,65), (27,38,57,63)),
    ((3,60,67,75), (19,53,68,77)),
    ((13,20,43,47), (15,21,44,45)),
    ((38,50,56,70), (42,46,54,72)),
    ((32,52,76,100), (36,44,84,96)),
)


def tm_states(R: int, q: int, r: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    xs = [R + r + j * q for j in range(8)]
    return (
        tuple(xs[j] for j in range(8) if j.bit_count() % 2 == 0),
        tuple(xs[j] for j in range(8) if j.bit_count() % 2 == 1),
    )


def add_weight(intervals: list[tuple[int, int]], w: int) -> list[tuple[int, int]]:
    shifted = [(a + w, b + w) for a, b in intervals]
    merged_source = sorted(intervals + shifted)
    out: list[list[int]] = []
    for a, b in merged_source:
        if not out or a > out[-1][1] + 1:
            out.append([a, b])
        else:
            out[-1][1] = max(out[-1][1], b)
    return [(a, b) for a, b in out]


def recompute(
    h: int,
    groups: tuple,
    width: int,
    annuli: tuple[tuple[int, int], ...] = (),
) -> tuple[int, int]:
    baseline = G(2 * h)
    demand: Counter[int] = Counter()
    weights: list[int] = []

    for states in groups:
        counters = [Counter(s) for s in states]
        baseline += min(value(h, s) for s in states)
        for x in set().union(*(set(c) for c in counters)):
            demand[x] += max(c[x] for c in counters)

    for R, q in annuli:
        for r in range(q):
            a, b = tm_states(R, q, r)
            va, vb = value(h, a), value(h, b)
            d = abs(va - vb)
            assert d == 8 * q**3 * (2 * (R + r) + 7 * q)
            baseline += min(va, vb)
            weights.append(d)
            for x in set(a) | set(b):
                demand[x] += 1

    for x in range(h - 1):
        capacity = 1 if x == 0 else 2
        assert demand[x] <= capacity
        weights.extend([delta(h, x)] * (capacity - demand[x]))

    intervals = [(0, width)]
    for w in sorted(weights):
        intervals = add_weight(intervals, w)
    best = max(intervals, key=lambda z: z[1] - z[0])
    return baseline + best[0], baseline + best[1]


def main() -> None:
    rows = []
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(line for line in f if not line.startswith("SUMMARY")):
            rows.append(row)

    assert len(rows) == 192
    covered = 292_031_545
    for row in rows:
        lo, hi = int(row["L"]), int(row["U"])
        assert lo <= covered + 1
        covered = max(covered, hi)
    assert covered == 554_860_689_583
    assert covered >= 275_233_782_943

    lookup = {(row["family"], int(row["h"])): (int(row["L"]), int(row["U"])) for row in rows}
    checks = [
        ("seed51", 63, SEED51, 63, ()),
        ("seed51", 66, SEED51, 63, ()),
        ("seed65", 67, SEED65, 2047, ()),
        ("seed65", 206, SEED65, 2047, ()),
        ("seed100_TM", 206, SEED100, 262143, ((101, 5), (141, 8))),
        ("seed100_TM", 253, SEED100, 262143, ((101, 5), (141, 8))),
    ]
    for family, h, groups, width, annuli in checks:
        assert recompute(h, groups, width, annuli) == lookup[(family, h)]

    print("PASS")
    print("csv_rows=192")
    print("independent_boundary_orders=6")
    print("bridge_end=554860689583")


if __name__ == "__main__":
    main()
