# Rooted-gadget witness table

The final self-contained proof does **not** use any instantiated rooted-gadget
switch.  Its infinite tail is obtained entirely from caterpillar cut states,
Thue–Morse annuli, and optional caterpillar cuts.

For audit completeness, the general equal-order replacement lemma is included
in `sw4_self_contained_solution.md`:

If two rooted branches of the same order have internal descendant-side cut
multisets `P0` and `P1`, and

\[
M_j=\sum_{s\in P_1}s^j-\sum_{s\in P_0}s^j,
\]

then replacing the first branch by the second in an `n`-vertex host changes
`SW_4` by

\[
\frac{M_1}{6}n^3
-\frac{M_2+3M_1}{4}n^2
+\frac{2M_3+9M_2+11M_1}{12}n
-\frac{M_4+11M_2}{12}.
\]

Because no rooted switch is a dependency of the final theorem, there are no
rooted-tree witness rows to list.  This file is intentionally explicit so a
reviewer does not mistake a missing rooted witness table for an omitted proof
dependency.  The complete witnesses actually used by the proof are in
`sw4_central_seed_witnesses.csv` and `sw4_central_seed_capacity.csv`.
