# Independent review guide

## Status and scope

This repository contains an **unverified AI-generated candidate solution**. No independent human expert review has yet been completed. Shadow curated, archived, and publicly released the artifact, but does not claim mathematical authorship and has not independently verified the proof.

The candidate claims

```text
e(4)  = 14,099
N₀(4) = 80,163
```

The goal of review is to **confirm, correct, or refute** this claim—not to endorse it without checking.

## Suggested audit order

### 1. Exact exceptional-range certificate

Audit Proposition 3.1 and Certificate 3.2 in `sw4_inverse_problem_paper.pdf` / `.tex`.

Check that:

- the rooted-tree and ordered-forest recurrence is complete;
- rooting and child ordering introduce duplication only, not omissions or invalid values;
- truncating bitsets above the cap is safe because all edge weights are nonnegative;
- the star lower bound excludes every uncomputed tree order;
- `sw4_certificate.py` reproduces the claimed missing count, maximum exception, and coverage interval.

### 2. Initial and lower caterpillar bridges

Audit Lemma 2.3, Certificate 3.3, and Certificate 5.1.

Check that:

- every selected cut set is realized by an actual caterpillar;
- the subset-sum update enumerates exactly the optional cuts;
- order bounds and caps cover the entire claimed range;
- `sw4_caterpillar_bridge_certificate.py` reproduces its stated interval.

### 3. Compressed finite bridge

Audit Lemma 5.2 and Certificate 5.3.

Check that:

- the interval-union update preserves every connected component of the exact attainable set;
- no invalid one-interval propagation assumption is used;
- all seed witnesses satisfy their equal-cardinality and equal-square-moment conditions;
- all labeled-slot capacities are respected;
- every one of the 192 interval junctions is exact.

Relevant files include:

- `sw4_complete_bridge_certificate.cpp`
- `sw4_complete_bridge_output.txt`
- `sw4_bridge_independent_check.py`

### 4. Universal infinite tail

Audit Sections 6–9, especially:

- the Thue–Morse eight-point identity and switch increment formula;
- disjointness of annulus supports;
- the annulus-ladder completeness inequalities;
- the insertion of all remaining cut slots;
- the finite overlap checks through the symbolic boundary;
- the final junction between the finite bridge and universal tail.

Relevant files include:

- `sw4_infinite_tail_finite_overlap.cpp`
- `sw4_infinite_tail_finite_overlap.csv`
- `sw4_infinite_tail_certificate.py`
- `sw4_infinite_tail_overlaps.csv`
- `sw4_infinite_tail_independent_check.py`

## Independent reproduction

From the repository root, run the commands in `README.md`. Independent reimplementations are more valuable than line-by-line copies, particularly for:

1. the rooted-forest dynamic program;
2. exact caterpillar subset sums;
3. compressed interval unions;
4. the seed witness and capacity checks;
5. the finite and universal overlap calculations.

## Reporting outcomes

Use GitHub Issue #4 for general review status, or open a separate issue for a specific defect. Include:

- the exact theorem, equation, file, and line involved;
- a counterexample, logical objection, or smallest failing input;
- exact commands, environment versions, and complete relevant output;
- whether the issue changes the final values or only the exposition.

A successful independent reproduction should state which components were reimplemented independently and which were only rerun from the supplied source.
