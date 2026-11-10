"""classify.py k log [log ...] — read FAM lines from orbit-driver logs, re-check each
family independently (frankl_core.is_valid, mu, min_degree), canonicalize under S_k,
and print one line per isomorphism class:
  CLASS <id> mu <mu> n <|G|> s <#co-singletons> sizes <a_2..a_{k-1}> deg <sorted c(e)> labeled <orbit size under S_k> hits <#FAM lines> canon <members>
Orbit size is computed as k!/|Aut(G)| so the labeled total can be checked against direct counts.
"""
import sys
from itertools import permutations
from math import factorial
sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from frankl_core import is_valid, mu, member_counts, BC

k = int(sys.argv[1])
FULL = (1 << k) - 1
perms = list(permutations(range(k)))


def apply(p, s):
    t = 0
    while s:
        b = s & -s
        t |= 1 << p[b.bit_length() - 1]
        s ^= b
    return t


def canon_aut(F):
    best = None; aut = 0
    for p in perms:
        img = tuple(sorted(apply(p, s) for s in F))
        if best is None or img < best:
            best = img; aut = 1
        elif img == best:
            aut += 1
    # aut counts perms mapping F to its canonical image = |Aut(F)|
    return best, aut


fams = []
for fn in sys.argv[2:]:
    for l in open(fn):
        p = l.split()
        if p and p[0] == "FAM":
            fams.append(tuple(sorted(int(x) for x in p[2].split(","))))

classes = {}
for F in fams:
    assert len(set(F)) == len(F), F
    assert is_valid(F, k), F
    c = member_counts(F, k)
    assert min(c) >= 2, "not a core"
    cf, aut = canon_aut(F)
    if cf not in classes:
        classes[cf] = [mu(F, k), aut, 0]
    classes[cf][2] += 1

print(f"FAMLINES {len(fams)} CLASSES {len(classes)}")
tot = 0
for i, (cf, (m, aut, hits)) in enumerate(sorted(classes.items(), key=lambda x: (x[1][0], len(x[0]), x[0]))):
    c = member_counts(cf, k)
    s = sum(1 for x in cf if BC(x) == k - 1)
    sizes = [sum(1 for x in cf if BC(x) == j) for j in range(2, k)]
    lab = factorial(k) // aut
    tot += lab
    print(f"CLASS {i} mu {m} n {len(cf)} s {s} sizes {sizes} deg {sorted(c)} aut {aut} labeled {lab} hits {hits} canon {','.join(map(str, cf))}")
print(f"LABELED_TOTAL {tot}")
