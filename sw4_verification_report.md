# Verification report for the self-contained SW4 solution

## Newly closed logical gap

The earlier complete-solution draft relied on an unavailable infinite-tail
checkpoint.  The updated package removes that dependency.

A new caterpillar-only theorem proves

\[
[272308250181,\infty)\subseteq\mathcal T_4.
\]

It consists of:

1. an exact finite interval chain for half-orders `h=253..365`;
2. a universal annulus construction for every `h>=365`;
3. exact overlap checks for `h=365..1171`;
4. an explicit positive polynomial proving all later overlaps.

The first tail interval is already inside the certified finite bridge, so the
combined coverage is continuous from `6,572,800` to infinity.

## Independent checks performed

- Rechecked every central witness cardinality, square sum, fourth sum, and
  normalized increment.
- Rechecked simultaneous cut capacity through distance 99.
- Recomputed the finite tail junction with exact interval unions.
- Recomputed all 807 finite universal intervals and their overlap margins.
- Independently parsed both generated CSV files and checked their junctions.
- Rechecked the closed form for the outer raw-cut sum.
- Rechecked the boundary of the symbolic overlap inequality.
- Re-ran the independent checker for the earlier 192-row finite bridge.

## Corrected dependency statement

No earlier conversation, checkpoint, external theorem, or unlisted rooted
witness is needed for the infinite tail.  Every construction and proof needed
for the final deduction appears in `sw4_self_contained_solution.md` and the
included certificate files.
