#!/usr/bin/env python3
"""Exact certificate for the finite part of the SW_4 inverse problem.

Run:
    python sw4_certificate.py

It proves exactly:
  * the 14,099 listed integers are precisely the unattainable values <= 80,163;
  * 80,163 is unattainable;
  * every integer 80,164..178,857 is attained by some tree;
  * caterpillars attain every integer 178,858..6,572,799.

It does not claim an infinite-tail proof.
"""
from math import comb
from itertools import combinations
from pathlib import Path

LIMIT_GAPS = 80163
LIMIT_ALL_TREES = 178857
CATERPILLAR_N = 80

def C(n,k): return comb(n,k) if n >= k >= 0 else 0
def edge_weight(n,s): return C(n,4)-C(s,4)-C(n-s,4)
def star_value(n): return (n-1)*C(n-1,3)
def path_value(n): return 3*C(n+1,5)
def mask(cap): return (1 << (cap+1))-1

def sumset_bits(a,b,cap):
    if not a or not b: return 0
    if a.bit_count() > b.bit_count(): a,b=b,a
    out=0
    while a:
        low=a & -a
        out |= b << (low.bit_length()-1)
        a ^= low
    return out & mask(cap)

def exact_values_for_n(n,cap):
    M=mask(cap)
    F=[0]*n
    P=[0]*(n+1)
    F[0]=1
    P[1]=1
    for t in range(1,n):
        z=0
        for s in range(1,t+1):
            component=(P[s] << edge_weight(n,s)) & M
            z |= sumset_bits(F[t-s],component,cap)
        F[t]=z & M
        P[t+1]=F[t]
    return P[n]

def exact_union(max_n,cap):
    z=0
    for n in range(4,max_n+1):
        z |= exact_values_for_n(n,cap)
    return z & mask(cap)

def caterpillar_increment(n,a):
    return C(n-1,4)-C(a,4)-C(n-a,4)

def caterpillar_values(n,cap):
    base=star_value(n)
    if base > cap: return 0
    lc=cap-base
    B=1
    M=mask(lc)
    for a in range(2,n-1):
        w=caterpillar_increment(n,a)
        if 0 < w <= lc:
            B=(B | (B << w)) & M
    return (B << base) & mask(cap)

def caterpillar_union(max_n,cap):
    z=0
    for n in range(4,max_n+1):
        z |= caterpillar_values(n,cap)
    return z & mask(cap)

def missing(bits,cap):
    return [x for x in range(1,cap+1) if not ((bits >> x) & 1)]

def main():
    assert star_value(29) == 91728 > LIMIT_GAPS
    A=exact_union(28,LIMIT_GAPS)
    gaps=missing(A,LIMIT_GAPS)
    assert len(gaps)==14099 and gaps[-1]==80163

    assert star_value(34)==180048 > LIMIT_ALL_TREES
    B=exact_union(33,LIMIT_ALL_TREES)
    assert missing(B,LIMIT_ALL_TREES)==gaps

    cap=star_value(CATERPILLAR_N+1)-1
    assert cap==6572799
    D=caterpillar_union(CATERPILLAR_N,cap)
    miss=(mask(cap) & ~D)
    assert miss.bit_length()-1==178857
    print("PASS")
    print("candidate e(4) = 14099")
    print("candidate N0(4) = 80163")
    print("exact all-tree coverage: 80164..178857")
    print("caterpillar coverage: 178858..6572799")

if __name__ == "__main__":
    main()
