# Contributing and independent verification

This repository contains an **unverified AI-generated candidate solution**.
Contributions should focus on verification, correction, or refutation rather
than endorsement without review.

## Reporting a mathematical issue

Open a GitHub Issue and include:

1. the theorem, lemma, equation, file, and line involved;
2. the exact logical gap or counterexample;
3. a corrected statement or proof when available;
4. whether the issue affects the finite certificate, the infinite-tail proof,
   or only exposition.

## Reporting a computational issue

Include:

1. operating system and compiler/interpreter versions;
2. the exact command used;
3. complete relevant output;
4. the smallest failing input or row;
5. whether the failure reproduces with exact arithmetic.

## Independent implementations

Independent reimplementations of the rooted-forest recurrence, caterpillar
bitsets, compressed interval unions, or infinite-overlap checks are especially
valuable. Please avoid copying the implementation line-for-line when the goal
is independent confirmation.

## Pull requests

Pull requests should clearly separate:

- mathematical corrections;
- implementation corrections;
- documentation changes;
- new independent verification.

Do not remove the provenance and unverified-status notices unless qualified
human review has occurred and the change is documented publicly.
