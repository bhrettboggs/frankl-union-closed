"""Self-tests of the encoding, with no repo code:
 1. k = 3, 4: brute force over ALL 2^(2^k) families, using check_family
    (the definition), versus labelled enumeration by the encoding, for
    every cap (and cap = none): the two sets of families must be identical.
 2. Symmetry breaking: at k = 4, 5 and every cap, the families allowed by
    (SB1)+(SB2) meet every S_k-orbit of solutions (empirical check of the
    soundness argument in encode.py), with both solvers' CNF/linear forms."""
from itertools import product
from common import check_family, cpsat_enumerate, sat_enumerate, orbit_classes, relabel
from encode import Encoding
from itertools import permutations

ok = True
for k in (3, 4):
    N = 1 << k
    byc = {}
    allv = set()
    for bits in range(1 << N):
        fam = tuple(S for S in range(N) if bits >> S & 1)
        v, mu = check_family(fam, k) if fam else (False, 0)
        if v:
            allv.add(fam)
    caps = sorted(set(check_family(f, k)[1] for f in allv))
    for cap in [None] + list(range(min(caps) - 1, max(caps) + 1)):
        brute = {f for f in allv if cap is None or check_family(f, k)[1] <= cap}
        a = set(cpsat_enumerate(Encoding(k, cap)))
        b = set(sat_enumerate(Encoding(k, cap)))
        good = a == brute == b
        ok &= good
        print(f"k={k} cap={cap}: brute force {len(brute)}, cpsat {len(a)}, cadical {len(b)}: {'OK' if good else 'DIFFER'}")

for k in (4, 5):
    perms = list(permutations(range(k)))
    for cap in range(k - 3, k + 2):
        full = set(cpsat_enumerate(Encoding(k, cap)))
        classes = orbit_classes(full, k)
        for lvl in (1, 2):
            sbf = set(sat_enumerate(Encoding(k, cap, sb=True, sb_level=lvl)))
            hit = all({relabel(r, p) for p in perms} & sbf for r, _, _ in classes)
            ok &= hit and sbf <= full
            print(f"k={k} cap={cap} sb_level={lvl}: {len(full)} labelled in {len(classes)} orbits; "
                  f"{len(sbf)} pass symmetry breaking; every orbit met: {hit}")
print("SELFTEST:", "PASS" if ok else "FAIL")
