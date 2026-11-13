"""FINAL COMPARISON -- the only file in independent/ that imports repo code.

Compares the independent results with frankl_core.py and the repo's result
files.  Run after sectionB/C/E have produced their outputs.
 1. The two validity predicates agree: frankl_core.is_valid / mu versus
    common.check_family on every family at k = 3 (2^8) and k = 4 (2^16),
    and on 20,000 random families at k = 5, 6.
 2. Every family the independent enumeration found at k = 7, mu <= 4 is valid
    and has mu = 4 according to frankl_core; its classes, canonicalised
    with frankl_core.canon, equal the six core classes in
    results/k7_mu4_core_classes.txt plus lift(M_6), with the same labelled
    counts.
 3. families.matching_family(t) is isomorphic to frankl_core.matching_family.
"""
import os, sys, random, ast
from itertools import permutations
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import frankl_core as fc                                   # noqa: E402
from common import check_family, relabel                   # noqa: E402
from families import matching_family                       # noqa: E402

ok = True
# 1
for k in (3, 4):
    N = 1 << k
    bad = 0
    for bits in range(1 << N):
        fam = [S for S in range(N) if bits >> S & 1]
        mine = check_family(fam, k)[0] if fam else False
        theirs = fc.is_valid(fam, k) if fam else False
        bad += mine != theirs
        if mine and theirs and check_family(fam, k)[1] != fc.mu(fam, k):
            bad += 1
    print(f"1. k={k}: all {1 << N} families, disagreements in validity/mu: {bad}")
    ok &= bad == 0
rng = random.Random(20261113)
for k in (5, 6):
    N, bad, nval = 1 << k, 0, 0
    for _ in range(20000):
        # random union-closed-ish families: close a few random sets under union
        gens = [rng.randrange(N) for _ in range(rng.randrange(1, 8))]
        fam = {0, N - 1}
        for g in gens:
            fam |= {g | f for f in fam} | {g}
        if rng.random() < 0.3:
            fam.discard(rng.choice(sorted(fam)))
        fam = sorted(fam)
        mine = check_family(fam, k)[0]
        nval += mine
        bad += mine != fc.is_valid(fam, k)
    print(f"1. k={k}: 20000 random families ({nval} valid), disagreements: {bad}")
    ok &= bad == 0

# 2
path = os.path.join(HERE, "results", "k7_cap4_classes.txt")
mine = [ast.literal_eval(l.split("members=")[1]) for l in open(path) if "members=" in l]
perms = list(permutations(range(7)))
mine_c = {}
for f in mine:
    assert fc.is_valid(f, 7) and fc.mu(f, 7) == 4
    orb = {relabel(f, p) for p in perms}
    mine_c[tuple(sorted(fc.canon(f, 7)))] = len(orb)
repo = {}
for l in open(os.path.join(os.path.dirname(HERE), "results", "k7_mu4_core_classes.txt")):
    if l.startswith("CLASS"):
        w = l.split()
        can = tuple(sorted(int(x) for x in w[w.index("canon") + 1].split(",")))
        repo[tuple(sorted(fc.canon(list(can), 7)))] = int(w[w.index("labeled") + 1])
liftM6 = fc.lift(fc.matching_family(6), 6)
repo[tuple(sorted(fc.canon(list(liftM6), 7)))] = 7 * 120
print(f"2. k=7: independent {len(mine_c)} classes / {sum(mine_c.values())} labelled; "
      f"repo {len(repo)} classes / {sum(repo.values())} labelled; identical classes and "
      f"per-class counts: {mine_c == repo}")
ok &= mine_c == repo

# 3
for t in (2, 3, 4):
    a = matching_family(t)
    b = tuple(sorted(fc.matching_family(2 * t)))
    iso = fc.canon(list(a), 2 * t) == fc.canon(list(b), 2 * t)
    print(f"3. M_{2*t}: independent n={len(a)}, frankl_core n={len(b)}, isomorphic: {iso}")
    ok &= iso
print("COMPARISON:", "ALL AGREE" if ok else "DISAGREEMENT FOUND")
