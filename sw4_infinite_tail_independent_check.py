#!/usr/bin/env python3
"""Independent structural audit of the self-contained SW_4 tail package."""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def C(n: int, k: int) -> int:
    return comb(n, k) if n >= k >= 0 else 0


def G(n: int) -> int:
    return (n - 1) * C(n - 1, 3)


def Delta(n: int, a: int) -> int:
    return C(n - 1, 4) - C(a, 4) - C(n - a, 4)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def audit_witnesses() -> None:
    rows = read_csv(ROOT / "sw4_central_seed_witnesses.csv")
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        name = row["group_state"]
        if name.startswith("base3_"):
            group = "base3"
        elif name.startswith("unit_pair_"):
            group = "unit"
        else:
            group = name.rsplit("_state_", 1)[0]
        groups[group].append(row)
        xs = tuple(map(int, row["distances"].split()))
        assert len(xs) == int(row["cardinality"])
        assert sum(x * x for x in xs) == int(row["square_sum"])
        assert sum(x**4 for x in xs) == int(row["fourth_sum"])

    for group, states in groups.items():
        assert len({int(s["cardinality"]) for s in states}) == 1
        assert len({int(s["square_sum"]) for s in states}) == 1
        increments = sorted(int(s["normalized_increment"]) for s in states)
        if group == "base3":
            assert increments == [0, 1, 2]
        else:
            assert increments[0] == 0

    capacity = read_csv(ROOT / "sw4_central_seed_capacity.csv")
    assert max(int(r["distance"]) for r in capacity) == 99
    assert all(int(r["demand"]) <= int(r["capacity"]) for r in capacity)
    full_capacity = read_csv(ROOT / "sw4_full_seed_capacity.csv")
    assert max(int(r["distance"]) for r in full_capacity) == 100
    assert all(int(r["demand"]) <= int(r["capacity"]) for r in full_capacity)


def audit_finite_chain() -> tuple[int, int]:
    rows = read_csv(ROOT / "sw4_infinite_tail_finite_overlap.csv")
    rows = [r for r in rows if r["family"] != "SUMMARY"]
    assert len(rows) == 113
    assert int(rows[0]["h"]) == 253 and int(rows[-1]["h"]) == 365
    covered = 554_860_689_583
    for expected_h, row in zip(range(253, 366), rows):
        assert int(row["h"]) == expected_h
        L, U = int(row["L"]), int(row["U"])
        assert L <= U and L <= covered + 1
        covered = max(covered, U)
    assert (int(rows[0]["L"]), int(rows[0]["U"])) == (
        272_308_250_181, 554_860_689_583
    )
    assert covered == 3_868_972_697_957
    return int(rows[-1]["L"]), int(rows[-1]["U"])


def audit_universal_rows() -> tuple[int, int]:
    rows = read_csv(ROOT / "sw4_infinite_tail_overlaps.csv")
    assert len(rows) == 807
    assert int(rows[0]["h"]) == 365 and int(rows[-1]["h"]) == 1171
    previous_U = None
    for expected_h, row in zip(range(365, 1172), rows):
        assert int(row["h"]) == expected_h
        assert int(row["n"]) == 2 * expected_h
        L, U = int(row["L"]), int(row["U"])
        assert L <= U
        if previous_U is not None:
            assert L <= previous_U + 1
            assert int(row["margin_from_previous"]) == previous_U + 1 - L
        previous_U = U
    first = (int(rows[0]["L"]), int(rows[0]["U"]))
    assert first == (1_596_122_112_921, 3_577_546_733_067)
    return first


def audit_symbolic_bounds() -> None:
    # Raw-cut completion identity and positivity.
    for h in (365, 500, 1171, 5000):
        S = sum(Delta(2 * h, a) for a in range(2, h - 99))
        closed = (
            (h - 101) * C(2 * h - 1, 4)
            - C(h - 99, 5) - C(2 * h - 1, 5) + C(h + 100, 5)
        )
        assert S == closed
        assert S >= Delta(2 * h, h)

    for h in (1171, 1172, 2000, 10000):
        S = (
            (h - 101) * C(2 * h - 1, 4)
            - C(h - 99, 5) - C(2 * h - 1, 5) + C(h + 100, 5)
        )
        lower_U = G(2 * h) + S
        twice_upper_L = 2 * G(2 * h + 2) + (h + 54) * C(2 * h + 1, 4)
        assert 2 * (lower_U + 1) >= twice_upper_L


def audit_existing_bridge() -> None:
    path = ROOT / "sw4_complete_bridge_output.txt"
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    assert lines[-1] == "SUMMARY,,,,554860689583,,"
    assert any(line.startswith("seed100_TM,253,506,272308250181,554860689583") for line in lines)


def main() -> None:
    audit_witnesses()
    audit_existing_bridge()
    finite_last = audit_finite_chain()
    universal_first = audit_universal_rows()
    assert universal_first[0] <= finite_last[1] + 1
    audit_symbolic_bounds()
    print("PASS")
    print("seed_witnesses_and_capacities=verified")
    print("finite_tail_chain_rows=113")
    print("universal_overlap_rows=807")
    print(f"finite_to_universal_junction={finite_last[1]}->{universal_first[0]}")
    print("symbolic_overlap_h>=1171=verified_at_boundary_and_samples")


if __name__ == "__main__":
    main()
