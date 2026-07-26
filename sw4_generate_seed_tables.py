from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

S0=(0,2,2,3,6,6,10,10,12,12)
S1=(1,1,4,4,6,7,8,9,12,13)
S2=(1,1,4,5,5,7,7,11,11,13)
X=(16,22,24,27,30,32,36)
Y=(17,20,25,26,31,33,35)
PAIRS={
4: ((72,78,85,90),(73,76,88,88)),
8: ((8,58,71,73),(45,46,51,84)),
16: ((77,83,90,95),(78,81,93,93)),
32: ((81,87,94,99),(82,85,97,97)),
64: ((22,43,64,71),(25,48,54,75)),
128: ((15,28,39,51),(23,23,37,52)),
256: ((9,24,64,87),(29,40,40,91)),
512: ((14,14,29,35),(18,18,21,37)),
1024: ((28,31,86,92),(30,33,80,96)),
2048: ((16,60,66,66),(16,62,62,68)),
4096: ((55,61,67,70),(57,58,69,69)),
8192: ((26,41,53,65),(27,38,57,63)),
16384: ((3,60,67,75),(19,53,68,77)),
32768: ((13,20,43,47),(15,21,44,45)),
65536: ((38,50,56,70),(42,46,54,72)),
131072: ((32,52,76,100),(36,44,84,96)),
}

def sq(s): return sum(x*x for x in s)
def fourth(s): return sum(x**4 for x in s)
def fmt(s): return ' '.join(map(str,s))

rows=[]
# Three-state base, normalized against maximum fourth sum.
states=[S0,S1,S2]
mx=max(map(fourth,states))
for i,s in enumerate(states):
    rows.append((f'base3_state_{i}',(mx-fourth(s))//12,len(s),sq(s),fourth(s),fmt(s)))
mx=max(fourth(X),fourth(Y))
for i,s in enumerate((X,Y)):
    rows.append((f'unit_pair_state_{i}',(mx-fourth(s))//12,len(s),sq(s),fourth(s),fmt(s)))
for d,(a,b) in PAIRS.items():
    mx=max(fourth(a),fourth(b))
    rows.append((f'digit_{d}_state_0',(mx-fourth(a))//12,len(a),sq(a),fourth(a),fmt(a)))
    rows.append((f'digit_{d}_state_1',(mx-fourth(b))//12,len(b),sq(b),fourth(b),fmt(b)))

out=ROOT / 'sw4_central_seed_witnesses.csv'
out.write_text('group_state,normalized_increment,cardinality,square_sum,fourth_sum,distances\n'+'\n'.join(','.join(map(str,r)) for r in rows)+'\n')

# Capacity for the universal seed: through 65536, not 131072.
groups=[states,[X,Y]]+[list(PAIRS[d]) for d in sorted(PAIRS) if d<=65536]
demand=Counter()
for group in groups:
    counters=[Counter(s) for s in group]
    for x in set().union(*(set(c) for c in counters)):
        demand[x]+=max(c[x] for c in counters)
assert demand[0] <= 1
assert all(v<=2 for x,v in demand.items() if x>0)
(ROOT / 'sw4_central_seed_capacity.csv').write_text(
    'distance,demand,capacity\n'+'\n'.join(f'{x},{demand[x]},{1 if x==0 else 2}' for x in sorted(demand))+'\n'
)
print('PASS')
print('universal_seed_max_distance=',max(demand))
print('universal_seed_width=131071')
print('full_seed_width=262143')

# Full finite-junction seed, including the 131072 pair.
full_groups=[states,[X,Y]]+[list(PAIRS[d]) for d in sorted(PAIRS)]
full_demand=Counter()
for group in full_groups:
    counters=[Counter(s) for s in group]
    for x in set().union(*(set(c) for c in counters)):
        full_demand[x]+=max(c[x] for c in counters)
assert full_demand[0] <= 1
assert all(v <= (1 if x == 0 else 2) for x,v in full_demand.items())
(ROOT / 'sw4_full_seed_capacity.csv').write_text(
    'distance,demand,capacity\n'+'\n'.join(
        f'{x},{full_demand[x]},{1 if x==0 else 2}' for x in sorted(full_demand)
    )+'\n'
)
