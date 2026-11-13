"""Section C: k = 7.  Feasibility at cap 4 and enumeration of all labelled
families with mu <= 4 (repo: 11,340 labelled in 7 classes).  The cap-3
infeasibility is decided by decide.py (results/k7_cap3_cpsat.*).

Enumeration method (orbit blocking): solve with symmetry breaking (SB1+SB2
of encode.py); for each solution found, generate its whole S_7-orbit and
exclude every orbit member (one blocking clause per member that satisfies
SB1+SB2; the others are already excluded); repeat until infeasible.  The
blocked set is a union of orbits, so the remaining solution set is still
S_7-invariant and the soundness argument for symmetry breaking in encode.py
applies to it unchanged: the formula stays satisfiable while an unfound
orbit remains.  The labelled count is the sum of the orbit sizes.

  python3 sectionC.py [--workers W]
Writes results/k7_cap4_classes.txt (one representative per class)."""
import sys, time, os
from itertools import permutations
from common import cpsat_solve, check_family, relabel
from encode import Encoding


def sb_ok(fam, k):
    """Direct check of (SB1)+(SB2) of encode.py for a family."""
    fs = set(fam)
    c = [sum(1 for S in fs if S >> e & 1) for e in range(k)]
    if any(c[i] < c[i + 1] for i in range(k - 1)):
        return False
    x = [S in fs for S in range(1 << k)]
    for i in range(k):
        for j in range(i + 1, k):
            if c[i] != c[j]:
                continue
            a, b = 1 << i, 1 << j
            for S in range(1 << k):
                if S & a and not S & b and x[S] != x[S ^ a ^ b]:
                    if not x[S]:
                        return False
                    break
    return True


W = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
k, cap = 7, 4
perms = list(permutations(range(k)))
E = Encoding(k, cap, sb=True, sb_level=2)
classes = []
T = time.time()
while True:
    st, fam, dt = cpsat_solve(E, workers=W)
    print(f"solve {len(classes)+1}: {st} {dt:.1f}s", flush=True)
    if fam is None:
        assert st == "INFEASIBLE", st
        break
    v, mu = check_family(fam, k)
    assert v and mu <= cap
    orb = {relabel(fam, p) for p in perms}
    classes.append((fam, len(orb), mu))
    # Block the whole orbit.  Images that violate (SB1)/(SB2) are already
    # excluded by the formula, so only the images passing sb_ok need a
    # blocking clause; the effect is the same as blocking every image.
    passing = [g for g in orb if sb_ok(g, k)]
    assert passing, "symmetry breaking excluded a whole orbit: unsound"
    for g in passing:
        E.clauses.append(E.block(g))
    print(f"   class {len(classes)}: n={len(fam)} mu={mu} orbit {len(orb)}, "
          f"{len(passing)} images pass symmetry breaking", flush=True)
total = sum(o for _, o, _ in classes)
print(f"k=7 cap=4: {len(classes)} classes, {total} labelled families, mu values "
      f"{sorted(set(m for _, _, m in classes))}  [{time.time()-T:.0f}s]")
print("repo: 7 classes, 11340 labelled ->",
      "MATCH" if (len(classes), total) == (7, 11340) else "MISMATCH")
os.makedirs("results", exist_ok=True)
with open(os.path.join("results", "k7_cap4_classes.txt"), "w") as f:
    f.write(f"# k=7, mu<=4: {len(classes)} classes, {total} labelled (independent/sectionC.py)\n")
    for fam, o, mu in sorted(classes, key=lambda c: (len(c[0]), c[0])):
        f.write(f"n={len(fam)} mu={mu} orbit={o} members={list(fam)}\n")
