# Complete self-contained solution of the Steiner–Wiener 4-index inverse problem

## Final status

**COMPLETE SELF-CONTAINED RIGOROUS SOLUTION**

## Abstract

For a finite tree \(T\), let \(\operatorname{SW}_4(T)\) be the sum of the
orders in edges of the minimal subtrees spanning all four-element vertex
sets.  We determine the complement of the attainable set exactly.  An exact
rooted-forest dynamic program certifies all exceptional values, exact
caterpillar certificates bridge the finite range, and a new self-contained
Thue–Morse caterpillar construction gives overlapping intervals for all
sufficiently large even orders.  The result is

\[
\boxed{e(4)=14099},
\qquad
\boxed{N_0(4)=80163}.
\]

All finite calculations are deterministic, exact, and included in the
reproducibility bundle.

## 1. Definitions

For \(S\subseteq V(T)\), let \(d_T(S)\) be the number of edges in the
smallest connected subgraph containing \(S\).  Define

\[
\operatorname{SW}_4(T)=
\sum_{\substack{S\subseteq V(T)\\|S|=4}}d_T(S),
\]

\[
\mathcal T_4=\{\operatorname{SW}_4(T):T\text{ is a finite tree}\},
\]

\[
e(4)=|\mathbb N\setminus\mathcal T_4|,
\qquad
N_0(4)=\max(\mathbb N\setminus\mathcal T_4).
\]

## 2. Edge decomposition

Let \(T\) have order \(n\).  Deleting an edge \(e\) gives components of
orders \(s\) and \(n-s\).  The edge belongs to the Steiner subtree of a
four-set exactly when the four vertices are not all in one component.
Therefore its contribution is

\[
w_n(s)=\binom n4-\binom s4-\binom{n-s}4,
\]

and

\[
\boxed{
\operatorname{SW}_4(T)=\sum_{e\in E(T)}w_n(s_e).
}
\]

The difference

\[
w_n(s+1)-w_n(s)
=\binom{n-s-1}{3}-\binom s3
\]

is nonnegative for \(1\le s<n/2\).  Hence every edge contributes at least
\(w_n(1)=\binom{n-1}{3}\), with equality for every edge exactly in the star.
Thus the minimum at order \(n\) is

\[
G(n)=(n-1)\binom{n-1}{3}.
\]

## 3. Exact all-tree certificate

Fix the global order \(n\).  Let \(P_n(r)\) be the set of sums of internal
edge contributions of rooted \(r\)-vertex trees, omitting the edge to the
parent.  Let \(F_n(t)\) be the corresponding set for ordered rooted forests
with total order \(t\).  Then

\[
F_n(0)=\{0\},
\qquad
P_n(1)=\{0\},
\qquad
P_n(r)=F_n(r-1),
\]

and

\[
F_n(t)=
\bigcup_{s=1}^{t}
\left(F_n(t-s)+w_n(s)+P_n(s)\right).
\]

Every term constructs a rooted tree by attaching a rooted component of order
\(s\) to the root.  Conversely, after ordering the children of the root,
every rooted tree occurs in the recurrence.  Child ordering creates only
duplicates; it introduces no invalid value and omits no tree.  Therefore
\(P_n(n)\) is the exact value set for all \(n\)-vertex trees.

The program `sw4_certificate.py` implements these sets as arbitrary-precision
integer bitsets and proves:

1. Exactly \(14099\) positive integers at most \(80163\) are absent.
2. \(80163\) is absent.
3. Every integer from \(80164\) through \(178857\) is present.

These are global statements, not bounded-order guesses.  Indeed

\[
G(29)=91728>80163,
\]

so orders at most \(28\) suffice for the exceptional range, while

\[
G(34)=180048>178857,
\]

so orders at most \(33\) suffice for the second statement.

The complete absent list is `sw4_missing_values.txt`; its compressed form is
`sw4_missing_ranges.txt`.

## 4. Caterpillar realization

For \(A=\{a_1<\cdots<a_t\}\subseteq\{2,\ldots,n-2\}\), construct a
caterpillar with spine \(v_0\cdots v_t\) by placing

\[
a_1-1,
\quad a_{i+1}-a_i-1,
\quad n-a_t-1
\]

leaves at the successive spine vertices.  These numbers are nonnegative and
the resulting tree has exactly \(n\) vertices.  The spine cuts are exactly
\(a_1,\ldots,a_t\), and all remaining edges are leaf edges.  Hence

\[
\operatorname{SW}_4(T_A)
=G(n)+\sum_{a\in A}\Delta_n(a),
\]

where

\[
\Delta_n(a)=
\binom{n-1}{4}-\binom a4-\binom{n-a}{4}.
\]

This proves that every subset used by the caterpillar certificates represents
an actual finite tree.

## 5. Exact finite coverage through \(554860689583\)

### 5.1 Original caterpillar certificate

The original exact subset-sum certificate proves

\[
[178858,6572799]\subseteq\mathcal T_4.
\]

Together with the exact all-tree recurrence, this gives

\[
[80164,6572799]\subseteq\mathcal T_4.
\]

### 5.2 Lower bridge

`sw4_caterpillar_bridge_certificate.py` computes exact bounded subset sums for
all caterpillars of orders \(70\) through \(105\).  It checks the complete
bit mask and proves

\[
\boxed{
[6572800,292031545]\subseteq\mathcal T_4.
}
\]

### 5.3 Compressed interval bridge

The program `sw4_complete_bridge_certificate.cpp` uses explicit central
moment-switch seeds and exact interval unions.  If the current attainable set
is represented by pairwise-disjoint maximal intervals \(\mathcal I\), an
optional binary weight \(w\) is processed by the exact operation

\[
\mathcal I\longmapsto\mathcal I\cup(\mathcal I+w),
\]

followed only by merging overlaps and adjacent intervals.  This enumerates
both choices for every switch and raw cut and discards no component.

The selected intervals for orders \(126\) through \(506\) overlap
consecutively and prove

\[
\boxed{
[282204658,554860689583]\subseteq\mathcal T_4.
}
\]

The first endpoint lies below \(292031545\), so the lower bridge and this
chain combine to give

\[
\boxed{
[6572800,554860689583]\subseteq\mathcal T_4.
}
\]

The complete 192-row output is `sw4_complete_bridge_output.txt`.  The
independent checker `sw4_bridge_independent_check.py` recomputes all boundary
orders and verifies every interval junction.

## 6. Equal-order rooted replacement lemma

Although the final tail construction below uses caterpillars only, we include
the general replacement lemma requested for audit completeness.

Let two rooted branches \(R_0,R_1\) have the same order and be attached at
the same host vertex in an \(n\)-vertex tree.  Every cut outside the branch,
and the attachment-edge cut, are unchanged.  If \(P_0,P_1\) are the
multisets of descendant-side orders of their internal edges and

\[
M_j=\sum_{s\in P_1}s^j-\sum_{s\in P_0}s^j,
\]

then expansion of the edge formula gives the replacement increment

\[
\boxed{
\frac{M_1}{6}n^3
-\frac{M_2+3M_1}{4}n^2
+\frac{2M_3+9M_2+11M_1}{12}n
-\frac{M_4+11M_2}{12}.
}
\]

The equal branch orders ensure equal numbers of internal edges, so the common
\(\binom n4\) terms cancel.  No instantiated rooted gadget is needed anywhere
in the final proof; `sw4_rooted_gadget_witnesses.md` records this explicitly.

## 7. Self-contained infinite-tail theorem

The complete proof follows.  It is reproduced here rather than imported from
an earlier checkpoint.
### 7.1 Caterpillar coordinates

For an \(n\)-vertex tree, an edge whose deletion gives components of orders
\(s\) and \(n-s\) contributes

\[
w_n(s)=\binom n4-\binom s4-\binom{n-s}4.
\]

The star value is

\[
G(n)=(n-1)\binom{n-1}{3}.
\]

For a caterpillar cut set \(A\subseteq\{2,\ldots,n-2\}\),

\[
\operatorname{SW}_4(T_A)=G(n)+\sum_{a\in A}\Delta_n(a),
\qquad
\Delta_n(a)=\binom{n-1}{4}-\binom a4-\binom{n-a}{4}.
\]

Every such cut set is realizable.  If
\(A=\{a_1<\cdots<a_t\}\), take a spine
\(v_0v_1\cdots v_t\), place \(a_1-1\) leaves at \(v_0\),
place \(a_{i+1}-a_i-1\) leaves at \(v_i\), and place
\(n-a_t-1\) leaves at \(v_t\).  The spine-edge cut sizes are exactly
\(a_1,\ldots,a_t\), and all other edges are leaf edges.

For even order \(n=2h\), put

\[
\delta_h(x)=\Delta_{2h}(h+x),\qquad 0\le x\le h-2.
\]

At distance \(x=0\) there is one cut slot, of size \(h\).  At every
positive distance \(x\) there are two slots, of sizes \(h-x\) and
\(h+x\).  Direct expansion gives

\[
\delta_h(x)=
-\frac{x^4}{12}
+\left(-\frac{h^2}{2}+\frac{3h}{2}-\frac{11}{12}\right)x^2
+\frac{7h^4}{12}-\frac{17h^3}{6}
+\frac{59h^2}{12}-\frac{11h}{3}+1.
\]

Thus \(\delta_h(x)\) is an even quartic in \(x\).

### 7.2 Moment switches and independent allocation

#### Lemma 3.1 — central moment switch

Let \(P,Q\) be finite multisets of nonnegative distances satisfying

\[
|P|=|Q|,
\qquad
\sum_{x\in P}x^2=\sum_{x\in Q}x^2.
\]

Then

\[
\sum_{x\in P}\delta_h(x)-\sum_{x\in Q}\delta_h(x)
=-\frac1{12}
\left(\sum_{x\in P}x^4-\sum_{x\in Q}x^4\right).
\]

Hence the difference is independent of \(h\).

**Proof.** Equal cardinalities cancel the constant term of the even quartic,
and equal square sums cancel its quadratic term.  Only the fourth-power term
remains. ∎

#### Lemma 3.2 — independent slot allocation

For a state group \(\mathcal S\), let

\[
r_{\mathcal S}(x)=\max_{S\in\mathcal S}m_S(x),
\]

where \(m_S(x)\) is the multiplicity of distance \(x\) in state \(S\).
If a collection of state groups satisfies

\[
\sum_{\mathcal S}r_{\mathcal S}(0)\le1,
\qquad
\sum_{\mathcal S}r_{\mathcal S}(x)\le2\quad(x>0),
\]

then all state choices are independent, and every unallocated slot is also
independently optional.

**Proof.** Label the available cut slots at every distance and reserve
pairwise disjoint slots for each group.  Every state uses no more than its
reservation.  The resulting selected cuts form a valid caterpillar cut set. ∎

#### Lemma 3.3 — bounded complete sequence

If a construction realizes every value in \([0,W]\), and an independent
binary switch has increment \(d\le W+1\), then the enlarged construction
realizes every value in \([0,W+d]\).

**Proof.** The attainable intervals \([0,W]\) and \([d,d+W]\) overlap or
touch. ∎

### 7.3 The fixed central seed

The following groups are used.  The first group has normalized increments
\(0,1,2\):

\[
\begin{aligned}
&(0,2,2,3,6,6,10,10,12,12),\\
&(1,1,4,4,6,7,8,9,12,13),\\
&(1,1,4,5,5,7,7,11,11,13).
\end{aligned}
\]

The independent pair

\[
(16,22,24,27,30,32,36),
\qquad
(17,20,25,26,31,33,35)
\]

has increment one.  Together these groups realize \([0,3]\).

The following binary pairs have the displayed increments.

| Increment | State 0 | State 1 |
|---:|---|---|
| 4 | 72,78,85,90 | 73,76,88,88 |
| 8 | 8,58,71,73 | 45,46,51,84 |
| 16 | 77,83,90,95 | 78,81,93,93 |
| 32 | 81,87,94,99 | 82,85,97,97 |
| 64 | 22,43,64,71 | 25,48,54,75 |
| 128 | 15,28,39,51 | 23,23,37,52 |
| 256 | 9,24,64,87 | 29,40,40,91 |
| 512 | 14,14,29,35 | 18,18,21,37 |
| 1,024 | 28,31,86,92 | 30,33,80,96 |
| 2,048 | 16,60,66,66 | 16,62,62,68 |
| 4,096 | 55,61,67,70 | 57,58,69,69 |
| 8,192 | 26,41,53,65 | 27,38,57,63 |
| 16,384 | 3,60,67,75 | 19,53,68,77 |
| 32,768 | 13,20,43,47 | 15,21,44,45 |
| 65,536 | 38,50,56,70 | 42,46,54,72 |

For every row, the two states have equal cardinality and equal square sum,
and their fourth-power sums differ by twelve times the displayed increment.
The complete arithmetic is in `sw4_central_seed_witnesses.csv`.
The simultaneous demand is listed in `sw4_central_seed_capacity.csv`; it is
at most one at distance zero and at most two at every positive distance.
The maximum used distance is \(99\).

By Lemma 3.3, these groups realize

\[
\boxed{[0,131071]}.
\]

A second seed, used only in the finite junction, adds the pair

\[
(32,52,76,100),\qquad(36,44,84,96),
\]

of increment \(131072\), and therefore realizes \([0,262143]\).

### 7.4 Thue–Morse annuli

Let

\[
x_j=R+r+jq,\qquad 0\le j\le7.
\]

Partition the eight indices according to the parity of their binary digit
sum.  Put \(\varepsilon_j=1\) on the even class and \(-1\) on the odd
class.  The exact moment sums are

\[
\sum\varepsilon_jj^m=0\quad(m=0,1,2),
\qquad
\sum\varepsilon_jj^3=-48,
\qquad
\sum\varepsilon_jj^4=-672.
\]

Substitution into the even quartic gives the exact binary increment

\[
\boxed{
 d_{R,q,r}=8q^3\bigl(2(R+r)+7q\bigr).
}
\]

For fixed \(R,q\), the \(q\) choices \(r=0,\ldots,q-1\) have disjoint
supports and partition the distance annulus

\[
R,R+1,\ldots,R+8q-1.
\]

Their total increment is

\[
\boxed{
D(R,q)=8q^4(2R+8q-1).
}
\]

### 7.5 An infinite annulus ladder

Define

\[
R_0=100,
\qquad q_0=4,
\]

and recursively

\[
R_{i+1}=R_i+8q_i,
\qquad
q_{i+1}=\left\lceil\frac{3q_i}{2}\right\rceil.
\]

Let

\[
W_0=131071,
\qquad
W_{k+1}=W_k+D(R_k,q_k).
\]

Thus \(W_k\) is the switch width after the first \(k\) annuli.

#### Lemma 6.1 — every annulus extends the complete interval

After the first \(k\) annuli, all increments in \([0,W_k]\) are realizable.

**Proof.** The first digits of the first three annuli satisfy

\[
116736\le131072,
\]

\[
528768\le604160,
\]

\[
2466936\le3828608.
\]

For the general step, first note the invariant

\[
12q_i\le R_i\le25q_i.
\]

It holds at \(i=0\).  Since

\[
\frac32q_i\le q_{i+1}\le\frac{13}{8}q_i,
\]

we have

\[
R_{i+1}\le33q_i\le22q_{i+1}
\]

and

\[
R_{i+1}\ge20q_i\ge\frac{160}{13}q_{i+1}>12q_{i+1}.
\]

For \(i\ge3\), put \(p=q_{i-1}\), \(R=R_{i-1}\).  Then \(p\ge9\),
\(R/p\ge12\), and \(q_i/p\le14/9\).  Therefore

\[
\frac{d_{R_i,q_i,0}}{8p^4}
\le
\left(\frac{14}{9}\right)^3
\left(2\frac Rp+\frac{242}{9}\right),
\]

whereas

\[
\frac{D(R,p)}{8p^4}
=p\left(2\frac Rp+8-\frac1p\right).
\]

The difference between the right-hand lower bound and the left-hand upper
bound is increasing in \(R/p\); at \(p=9\) and \(R/p=12\) the required
integer comparison is

\[
287\cdot6561>2744\cdot458.
\]

Hence \(d_{R_i,q_i,0}\le D(R_{i-1},q_{i-1})\le W_i\).

Within one annulus the digits increase by \(16q_i^3\), and
\(d_{r+1}\le2d_r\).  Once \(d_r\) is inserted, the accumulated width is at
least \(2d_r-1\), so the next digit also satisfies the complete-sequence
condition.  Lemma 3.3 completes the induction. ∎

### 7.6 The switch width dominates the first raw cut

For \(h\ge365\), choose the largest \(k\) satisfying

\[
R_k\le h-1.
\]

The seed and the first \(k\) annuli fit in the available distances.  By
maximality,

\[
h\le R_{k+1}.
\]

The smallest raw caterpillar increment is

\[
\Delta_{2h}(2)=\binom{2h-2}{3}.
\]

#### Lemma 7.1

For every \(h\ge365\),

\[
W_k\ge\Delta_{2h}(2)-1.
\]

**Proof.** Since \(R_4=364\), we have \(k\ge4\).  Direct exact arithmetic
gives

\[
\begin{array}{c|c|c}
 k&W_k&\binom{2R_{k+1}-2}{3}-1\\ \hline
4&215457655&199064819\\
5&1607941615&648686323\\
6&12672515567&2138222579.
\end{array}
\]

For \(k\ge7\), put \(i=k-1\) and \(p=q_i\).  Then \(p\ge48\).  The
invariant above gives

\[
R_{i+2}=R_i+8p+8q_{i+1}\le46p.
\]

Also

\[
W_k\ge D(R_i,p)
=8p^4(2R_i+8p-1)
\ge64p^5.
\]

On the other hand,

\[
\binom{2R_{i+2}-2}{3}
<\frac{(2R_{i+2})^3}{6}
\le\frac43\,46^3p^3.
\]

Because

\[
64\cdot48^2>\frac43\,46^3,
\]

the desired inequality follows.  Finally
\(h\le R_{k+1}\) and the binomial coefficient is increasing. ∎

### 7.7 Completing all remaining cuts

For \(2\le a\le h\), the sequence \(\Delta_{2h}(a)\) is increasing.  More
precisely,

\[
w_n(s+1)-w_n(s)
=\binom{n-s-1}{3}-\binom{s}{3},
\]

which decreases with \(s\).  Therefore

\[
\boxed{
\Delta_n(a)\le(a-1)\Delta_n(2)
}
\qquad(2\le a\le n/2).
\]

The central seed uses only distances at most \(99\).  Every annulus uses one
of the two slots at each distance in its support.  Consequently, for every
\(a=2,\ldots,h-100\), at least one cut of weight \(\Delta_{2h}(a)\)
remains optional.

Starting from \([0,W_k]\), insert one such cut for each
\(a=2,3,\ldots,h-100\).  Lemma 7.1 handles \(a=2\).  If the cuts through
\(a\) have been inserted, then the current width plus one is at least

\[
\Delta_{2h}(2)+\sum_{j=2}^{a}\Delta_{2h}(j)
\ge a\Delta_{2h}(2)
\ge\Delta_{2h}(a+1).
\]

Thus the interval remains complete.

Let

\[
S_h=\sum_{a=2}^{h-100}\Delta_{2h}(a).
\]

Hockey-stick summation gives

\[
S_h=(h-101)\binom{2h-1}{4}
-\binom{h-99}{5}
-\binom{2h-1}{5}
+\binom{h+100}{5}.
\]

Furthermore,

\[
120\bigl(S_h-\Delta_{2h}(h)\bigr)
=
48h^5-7315h^4+34790h^3+19641055h^2
-59058458h+19539439680.
\]

For \(h\ge365\), this is positive: the first two terms combine to
\(h^4(48h-7315)>0\), and
\(19641055h^2-59058458h>0\), while all other displayed terms are positive.
Thus

\[
S_h\ge\Delta_{2h}(h).
\]

After the first optional copy at every outer size has been inserted, the
current width is therefore at least the largest possible remaining raw cut.
All remaining slots can now be inserted one by one in nondecreasing order.

We have proved:

#### Theorem 8.1 — universal fixed-order interval

For every \(h\ge365\), the construction above realizes a complete interval

\[
J_h=[L_h,U_h]\subseteq\mathcal T_4,
\]

where \(L_h\) is the star value plus the minimum state value in every seed
and annulus group, and \(U_h\) is obtained by adding every switch width and
every remaining optional cut.

At the first order,

\[
\boxed{
J_{365}=
[1596122112921,3577546733067].
}
\]

### 7.8 Overlap of the universal intervals

The exact program `sw4_infinite_tail_certificate.py` verifies

\[
L_{h+1}\le U_h+1
\]

for every \(365\le h\le1170\).  This is a finite exhaustive check of the
explicit formulas above.  Its minimum overlap margin is

\[
1960269091932
\]

at \(h=365\to366\).

For the infinite range, we give a symbolic proof.  At order \(2(h+1)\), a
selected seed state uses exactly \(77\) cuts.  The annuli use

\[
4\sum q_i=\frac{R_k-100}{2}
\]

selected cuts.  Since \(R_k\le h\), the total number of selected baseline
cuts is at most

\[
\frac{h+54}{2}.
\]

Every such cut is at most \(\binom{2h+1}{4}\).  Hence

\[
L_{h+1}
\le
G(2h+2)+\frac{h+54}{2}\binom{2h+1}{4}.
\]

On the other hand,

\[
U_h\ge G(2h)+S_h.
\]

Direct expansion gives

\[
\begin{aligned}
120\Bigl(&G(2h)+S_h+1-G(2h+2)
-\frac{h+54}{2}\binom{2h+1}{4}\Bigr)\\
={}&8h^5-9365h^4+35340h^3+19643615h^2
-59060078h+19539440040.
\end{aligned}
\]

For \(h\ge1171\), the first two terms combine to
\(h^4(8h-9365)>0\), and
\(19643615h^2-59060078h>0\); all other displayed terms are positive.
Therefore

\[
L_{h+1}\le U_h+1
\qquad(h\ge1171).
\]

Combining the finite and symbolic ranges,

\[
\boxed{
\bigcup_{h\ge365}J_h=[1596122112921,\infty).
}
\]

### 7.9 Exact finite junction

The universal first interval begins above the already certified finite bridge,
so one exact finite chain is used.

Use the full central seed \([0,262143]\), the two fixed annuli

\[
(R,q)=(101,5),\qquad(141,8),
\]

and every remaining cut slot.  For each \(h=253,254,\ldots,365\), the C++
program `sw4_infinite_tail_finite_overlap.cpp` represents the exact attainable
increment set as a union of maximal integer intervals.  For every binary
weight \(w\), it performs the exact update

\[
S\longmapsto S\cup(S+w)
\]

and merges only overlapping or adjacent intervals.  Thus no attainable value
in the stated family is sampled or discarded.

The first selected interval is

\[
[272308250181,554860689583]
\]

at \(h=253\).  The selected intervals overlap for all subsequent
\(h\le365\).  The last is

\[
[1304696148031,3868972697957],
\]

which overlaps \(J_{365}\).

Consequently,

\[
\boxed{
[272308250181,\infty)\subseteq\mathcal T_4.
}
\]

### 7.10 Tail reproduction

Run:

```bash
g++ -O3 -std=c++20 -Wall -Wextra -pedantic \
  sw4_infinite_tail_finite_overlap.cpp \
  -o sw4_infinite_tail_finite_overlap
./sw4_infinite_tail_finite_overlap

python sw4_infinite_tail_certificate.py
python sw4_infinite_tail_independent_check.py
```

Expected summaries:

```text
PASS
bridge_start=272308250181
bridge_end=3868972697957
universal_L_365=1596122112921
```

```text
PASS
universal_h_start=365
universal_first_interval=1596122112921..3577546733067
symbolic_overlap_h>=1171
```

The witness arithmetic, finite interval rows, and universal finite overlap rows
are supplied as CSV files in the reproducibility bundle.
## 8. Final deduction

The exact all-tree certificate proves that precisely \(14099\) positive
integers at most \(80163\) are unattainable and that \(80163\) is one of
them.  It also proves all integers from \(80164\) through \(178857\) are
attainable.  The caterpillar certificates and finite interval chains prove
continuous coverage through \(554860689583\).  The self-contained tail proof
above proves

\[
[272308250181,\infty)\subseteq\mathcal T_4,
\]

which overlaps that finite bridge.  Therefore every positive integer greater
than \(80163\) is attainable, and no exception exists beyond \(80163\).
Consequently

\[
\boxed{e(4)=14099},
\qquad
\boxed{N_0(4)=80163}.
\]

## 9. Reproducibility

From the bundle directory run:

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

sha256sum -c sw4_self_contained_sha256.txt
```

All Python computations use arbitrary-precision integers.  C++ binomial
products use signed 128-bit intermediates; every stored endpoint is asserted
to fit in signed 64-bit range.

## 10. Hostile audit

1. **All tree classes below the exceptional cutoff.**  The rooted-forest
   recurrence is exact and the star lower bound proves that no larger order
   can contribute below the cutoff.
2. **Caterpillar validity.**  Every selected cut set has an explicit spine and
   nonnegative leaf multiplicities.
3. **Seed arithmetic.**  Cardinalities, square sums, fourth sums, normalized
   increments, and simultaneous capacities are supplied and independently
   checked.
4. **Annulus identities.**  The moment sums and the formula
   \(8q^3(2(R+r)+7q)\) are derived symbolically and checked exactly.
5. **Switch independence.**  Seed capacities are at most one at distance zero
   and two elsewhere; annuli have disjoint supports and consume one slot per
   supported distance.
6. **Complete intervals.**  The universal construction checks every
   complete-sequence inequality; the finite chains use exact interval unions,
   not density or sampling.
7. **Finite junctions.**  Every row is asserted to overlap the previous
   covered interval.  The finite chain at \(h=365\) overlaps the first
   universal interval.
8. **Infinite overlap.**  Orders \(365\) through \(1171\) are checked exactly;
   the displayed positive polynomial proves every later overlap.
9. **Overflow.**  No floating-point arithmetic is used.  Python is arbitrary
   precision and C++ has checked 128-bit intermediates.
10. **No unavailable dependency.**  Every original theorem used in the
    conclusion is proved in this document or certified by source and output
    files included in the same bundle.

## 11. File map

- `sw4_missing_values.txt`: every exceptional integer.
- `sw4_missing_ranges.txt`: compressed exceptional ranges.
- `sw4_certificate.py`: exact all-tree recurrence and original caterpillar
  certificate.
- `sw4_caterpillar_bridge_certificate.py`: exact lower bridge.
- `sw4_complete_bridge_certificate.cpp`: exact finite compressed-interval
  bridge.
- `sw4_infinite_tail_finite_overlap.cpp`: exact finite junction into the
  universal family.
- `sw4_infinite_tail_certificate.py`: universal finite checks and boundary
  verification.
- `sw4_infinite_tail_independent_check.py`: independent structural audit.
- `sw4_central_seed_witnesses.csv`: complete seed witness arithmetic.
- `sw4_central_seed_capacity.csv`: simultaneous slot demand.
- `sw4_self_contained_sha256.txt`: SHA-256 manifest.
