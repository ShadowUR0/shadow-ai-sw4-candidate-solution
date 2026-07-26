# AI-Generated Candidate Solution to the Steiner–Wiener 4-Index Inverse Problem

> **Status: unverified AI-generated candidate solution.**
>
> No independent human expert review has yet been completed.

This repository preserves a candidate computer-assisted solution to the Steiner–Wiener 4-index inverse problem for finite trees.

The mathematical derivations, proof construction, manuscript, verification programs, certificates, and internal checks were generated through extended ChatGPT sessions initiated by **Shadow**. Shadow curated, archived, and first publicly released the resulting materials, but does **not** claim mathematical authorship and has **not** independently verified the proof.

The purpose of this release is to establish a public, timestamped, reproducible record and invite qualified mathematicians to independently examine, reproduce, confirm, correct, or refute the claimed result.

## Claimed result

The manuscript claims

```text
e(4)  = 14,099
N₀(4) = 80,163
```

Equivalently, it claims that exactly 14,099 positive integers are not realizable as the Steiner–Wiener 4-index of a finite tree, and that 80,163 is the largest such integer.

This must be treated as a **candidate result**, not as an accepted theorem, until it has received independent expert verification.

## Manuscript status

- `sw4_inverse_problem_paper.tex` — corrected public LaTeX manuscript source
- `sw4_inverse_problem_paper.pdf` — compiled 21-page public manuscript
- `sw4_self_contained_solution.md` — self-contained solution draft
- `sw4_infinite_tail_proof.md` — standalone infinite-tail argument
- `sw4_verification_report.md` — internal verification report

The public manuscript includes a transparent AI-provenance notice, identifies Shadow as curator and public releaser, and contains no placeholder author fields.

## Verification programs

### Python

- `sw4_certificate.py`
- `sw4_caterpillar_bridge_certificate.py`
- `sw4_bridge_independent_check.py`
- `sw4_generate_seed_tables.py`
- `sw4_infinite_tail_certificate.py`
- `sw4_infinite_tail_independent_check.py`

### C++

- `sw4_complete_bridge_certificate.cpp`
- `sw4_infinite_tail_finite_overlap.cpp`

## Exact data and outputs

The repository also contains:

- exact interval outputs and run logs;
- central-seed witness and capacity tables;
- the complete list of claimed missing values;
- compressed missing-value ranges;
- SHA-256 manifests and verification logs.

The files are intentionally kept together in the repository root because the verification scripts, output readers, and original SHA-256 manifest use same-directory relative paths. Moving only some files into folders would break reproducibility or invalidate the original manifest.

## Reproduction

Use Python 3.10 or later and a C++20 compiler. From the repository root, run:

```bash
python sw4_certificate.py
python sw4_caterpillar_bridge_certificate.py

g++ -O3 -std=c++20 -Wall -Wextra -pedantic \
  sw4_complete_bridge_certificate.cpp \
  -o sw4_complete_bridge_certificate
./sw4_complete_bridge_certificate
python sw4_bridge_independent_check.py

g++ -O3 -std=c++20 -Wall -Wextra -pedantic \
  sw4_infinite_tail_finite_overlap.cpp \
  -o sw4_infinite_tail_finite_overlap
./sw4_infinite_tail_finite_overlap
python sw4_infinite_tail_certificate.py
python sw4_infinite_tail_independent_check.py
```

To check the original reproducibility-bundle manifest:

```bash
sha256sum -c sw4_self_contained_sha256.txt
```

The public manuscript metadata and repository metadata were added after the original bundle was generated, so they are not part of that original manifest.

## How to review the claim

A useful independent review should address both parts:

1. **Mathematical proof audit** — check every universal lemma, construction, capacity condition, and infinite-overlap inequality.
2. **Independent computational reproduction** — run the supplied certificates and preferably reimplement the critical finite computations independently.

Please report suspected errors through GitHub Issues and include:

- the exact file and line or theorem involved;
- a counterexample, failing input, or logical objection;
- commands and output when the issue concerns computation.

## Attribution and provenance

Preferred description:

> AI-generated candidate solution, curated, archived, and publicly released by Shadow for independent verification.

Shadow is the curator and public releaser of this artifact, not the claimed mathematical author of the proof.

## Citation

Citation metadata is provided in `CITATION.cff`. Until independent verification occurs, citations should clearly describe the item as an **AI-generated candidate solution**.

## License

- Verification source code (`.py`, `.cpp`): MIT License — see `LICENSE-CODE`.
- Manuscript, documentation, tables, and research text: CC BY 4.0 — see `LICENSE-PAPER`.

These licenses do not imply verification or endorsement of the mathematical claim.
