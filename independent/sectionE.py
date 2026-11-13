"""Section E: independent re-check of the Phase 8 computational claims
(docs/PROOF_ATTEMPT.md, SESSION_2026-11-12b.md).

  E.1  all-co-singleton sector: min mu = k-2 for k = 3..7; labelled counts
       of mu = k-2 sector families at k = 3..6 (repo 1, 8, 124, 452 in
       1, 4, 9, 14 classes) and the sector sizes at k = 3, 4, 5 (1, 64,
       118314).
  E.2  one-point extensions of M_4, M_6, M_8: counts 58, 1272, 123126;
       minimum mu 3, 4, 5; mu distributions for M_4, M_6; number of classes
       at mu = t+1 (8, 7, and t+4 = 8 at t = 4 by F3); and the seven k = 7
       attainer classes equal the mu = 4 extension classes of M_6 (needs
       results/k7_cap4_classes.txt from sectionC.py).
  E.3  D4 (3mu >= 4k-4-n) and E1 with kappa = psi = (3-sqrt5)/2
       ((1+psi)mu >= 2k-2-(1-psi)n) on every valid family at k = 3, 4, 5
       (repo: 4, 304, 235749 valid families).
  E.4  the W2 counterexample at k = 6; D4 tight on M_6 and on six of the
       seven k = 7 classes.

  python3 sectionE.py [E1|E2|E2cmp|E3|E4 ...]      (default: all)
"""
import sys, time, os, ast
from fractions import Fraction
from itertools import permutations
from common import (cpsat_solve, sat_solve, cpsat_enumerate, check_family,
                    orbit_classes, relabel)
from encode import Encoding
from families import matching_family, extension_constraints, delete_point, named_extensions

parts = sys.argv[1:] or ["E1", "E2", "E2cmp", "E3", "E4"]
HERE = os.path.dirname(os.path.abspath(__file__))
verdicts = []


def verdict(name, ok, detail):
    v = "VERIFIED" if ok else "MISMATCH"
    verdicts.append((name, v, detail))
    print(f"  ==> {name}: {v}  ({detail})", flush=True)


def norm(st):
    return {"INFEASIBLE": "UNSAT", "OPTIMAL": "SAT", "FEASIBLE": "SAT"}.get(st, st)


# ------------------------------------------------------------------ E.1
if "E1" in parts:
    print("== E.1 all-co-singleton sector ==", flush=True)
    ok_all = True
    for k in range(3, 8):
        for cap, expect in ((k - 3, "UNSAT"), (k - 2, "SAT")):
            E = Encoding(k, cap, sb=True, cosingletons=True)
            st, fam, dt = cpsat_solve(E)
            st = norm(st)
            line = f"k={k} cap={cap} sector cpsat(sb): {st} {dt:.1f}s"
            good = st == expect
            if fam:
                v, mu = check_family(fam, k)
                cs = all(((1 << k) - 1) ^ (1 << e) in fam for e in range(k))
                line += f" witness valid={v} mu={mu} cosingletons={cs}"
                good = good and v and cs and mu <= cap
            if k <= 6:
                st2, _, dt2 = sat_solve(Encoding(k, cap, sb=False, cosingletons=True))
                line += f"; cadical(no sb): {st2} {dt2:.1f}s"
                good = good and st2 == expect
            print(line, flush=True)
            ok_all &= good
    verdict("E1(1a) sector min mu = k-2, k=3..7", ok_all, "UNSAT at cap k-3, SAT at cap k-2")

    REPO = {3: (1, 1), 4: (8, 4), 5: (124, 9), 6: (452, 14)}
    ok_all = True
    for k in range(3, 7):
        t = time.time()
        fams = cpsat_enumerate(Encoding(k, k - 2, cosingletons=True))
        chk = [check_family(f, k) for f in fams]
        assert all(v for v, _ in chk)
        cls = orbit_classes(fams, k)
        closed = all(o == m for _, o, m in cls)
        sizes = sorted((len(r), o) for r, o, _ in cls)
        print(f"k={k} cap={k-2} sector: {len(fams)} labelled, mu values "
              f"{sorted(set(m for _, m in chk))}, {len(cls)} classes, closed {closed}, "
              f"(n, orbit size) {sizes}  [{time.time()-t:.1f}s]", flush=True)
        ok_all &= (len(fams), len(cls)) == REPO[k] and closed
    verdict("E1(1b) labelled mu=k-2 sector counts 1, 8, 124, 452 / classes 1, 4, 9, 14",
            ok_all, "k = 3..6")
    sizes = []
    for k in (3, 4, 5):
        sizes.append(len(cpsat_enumerate(Encoding(k, None, cosingletons=True))))
    print(f"sector sizes k=3,4,5: {sizes}")
    verdict("E1(1c) sector sizes 1, 64, 118314", sizes == [1, 64, 118314], str(sizes))

# ------------------------------------------------------------------ E.2
if "E2" in parts:
    print("== E.2 one-point extensions of M_2t ==", flush=True)
    REPO = {2: (58, 3, {3: 16, 4: 23, 5: 15, 6: 4}, 8),
            3: (1272, 4, {4: 21, 5: 131, 6: 330, 7: 408, 8: 276, 9: 94, 10: 12}, 7),
            4: (123126, 5, None, 8)}
    ext_classes = {}
    for t in (2, 3, 4):
        k = 2 * t
        M = matching_family(t)
        fix, cls_ = extension_constraints(M, k)
        T0 = time.time()
        fams = cpsat_enumerate(Encoding(k + 1, None, fix=fix, clauses=cls_))
        chk = [check_family(f, k + 1) for f in fams]
        assert all(v for v, _ in chk)
        assert all(delete_point(f, k) == M for f in fams)
        dist = {}
        for _, m in chk:
            dist[m] = dist.get(m, 0) + 1
        mn = min(dist)
        extremal = [f for f, (_, m) in zip(fams, chk) if m == mn]
        T1 = time.time()
        # classes under S_{2t+1}; for t = 4 (9! perms) use a cheap invariant
        # to split first, then explicit orbits inside each bucket.
        if t <= 3:
            cl = orbit_classes(extremal, k + 1)
            reps = [r for r, _, _ in cl]
        else:
            reps = classes_large = None
            buckets = {}
            for f in extremal:
                degs = tuple(sorted(sum(1 for S in f if S >> e & 1) for e in range(k + 1)))
                sz = tuple(sorted(bin(S).count("1") for S in f))
                buckets.setdefault((len(f), degs, sz), []).append(f)
            perms = list(permutations(range(k + 1)))
            reps = []
            for key, L in buckets.items():
                rem = set(L)
                while rem:
                    r = min(rem)
                    orb = {relabel(r, p) for p in perms}
                    rem -= orb
                    reps.append(r)
        rl, rmin, rdist, rcls = REPO[t]
        print(f"t={t}: {len(fams)} valid extensions of M_{k} (repo {rl}), mu distribution "
              f"{sorted(dist.items())}, min mu {mn} (repo {rmin}), classes at min {len(reps)} "
              f"(repo {rcls})  [enum {T1-T0:.1f}s, classes {time.time()-T1:.1f}s]", flush=True)
        ok = len(fams) == rl and mn == rmin and len(reps) == rcls and mn == t + 1
        if rdist:
            ok = ok and dist == rdist
        verdict(f"E2 extensions of M_{k}: count, min mu, classes at min", ok,
                f"{len(fams)}, {mn}, {len(reps)}")
        if t >= 3:   # Prop. F2 / F3: the t+4 named families are the extremal classes
            perms = list(permutations(range(k + 1)))
            canon = lambda f: min(relabel(f, p) for p in perms)
            named = named_extensions(t)
            good = True
            for nm, G in named.items():
                v, m = check_family(G, k + 1)
                good &= v and m == t + 1 and delete_point(G, k) == M
                print(f"   {nm:16} n={len(G):3} valid={v} mu={m} extension-of-M_{k}={delete_point(G, k) == M}")
            Cn = {canon(G) for G in named.values()}
            Cr = {canon(r) for r in reps}
            print(f"   named families: {len(named)}, distinct classes {len(Cn)}; equal to the "
                  f"{len(Cr)} extremal classes: {Cn == Cr}", flush=True)
            verdict(f"E2 F2/F3 at t={t}: the t+4 named families are exactly the extremal extensions",
                    good and Cn == Cr and len(Cn) == t + 4, f"{len(Cn)} named, {len(Cr)} found")
        ext_classes[t] = reps

    with open(os.path.join(HERE, "results", "m6_ext_mu4_classes.txt"), "w") as f:
        f.write("# one representative per class of mu=4 one-point extensions of M_6 (sectionE.py E2)\n")
        for r in sorted(ext_classes[3]):
            f.write(f"n={len(r)} members={list(r)}\n")

if "E2cmp" in parts:
    print("== E.2 k=7 attainer classes vs mu=4 extensions of M_6 ==", flush=True)
    files = [os.path.join(HERE, "results", n) for n in ("k7_cap4_classes.txt", "m6_ext_mu4_classes.txt")]
    if all(os.path.exists(p) for p in files):
        att, ext = ([ast.literal_eval(l.split("members=")[1]) for l in open(p) if "members=" in l]
                    for p in files)
        perms = list(permutations(range(7)))
        canon = lambda f: min(relabel(f, p) for p in perms)
        A = {canon(f) for f in att}
        B = {canon(f) for f in ext}
        print(f"k=7 attainer classes (sectionC.py): {len(A)}; mu=4 extension classes of M_6: "
              f"{len(B)}; equal as sets of classes: {A == B}")
        verdict("E2 the 7 k=7 attainer classes = mu-4 extensions of M_6", A == B and len(A) == 7,
                f"{len(A)} vs {len(B)}")
    else:
        print("missing input: run sectionC.py and sectionE.py E2 first")

# ------------------------------------------------------------------ E.3
if "E3" in parts:
    print("== E.3 inequalities D4 and E1 on all valid families, k = 3, 4, 5 ==", flush=True)
    REPO = {3: 4, 4: 304, 5: 235749}

    def sign_a_plus_b_sqrt5(a, b):
        """sign of a + b*sqrt(5) for rationals a, b, exactly."""
        if a >= 0 and b >= 0:
            return (a > 0 or b > 0) and 1 or 0
        if a <= 0 and b <= 0:
            return -1 if (a < 0 or b < 0) else 0
        d = a * a - 5 * b * b      # same sign as |a| - |b|sqrt5
        if a > 0:
            return 1 if d > 0 else (-1 if d < 0 else 0)
        return -1 if d > 0 else (1 if d < 0 else 0)

    for k in (3, 4, 5):
        fams = cpsat_enumerate(Encoding(k, None))
        viol_d4 = viol_e1 = viol_2k = eq_d4 = eq_e1 = 0
        min_d4 = None
        for f in fams:
            v, mu = check_family(f, k)
            assert v
            n = len(f)
            s4 = 3 * mu - (4 * k - 4 - n)
            min_d4 = s4 if min_d4 is None else min(min_d4, s4)
            viol_d4 += s4 < 0
            eq_d4 += s4 == 0
            # (1+psi)mu - (2k-2) + (1-psi)n, psi = (3-sqrt5)/2:
            # 1+psi = 5/2 - sqrt5/2, 1-psi = -1/2 + sqrt5/2
            a = Fraction(5, 2) * mu - (2 * k - 2) - Fraction(1, 2) * n
            b = Fraction(-1, 2) * mu + Fraction(1, 2) * n
            sg = sign_a_plus_b_sqrt5(a, b)
            viol_e1 += sg < 0
            eq_e1 += sg == 0
            viol_2k += mu < 2 * k - n
        print(f"k={k}: {len(fams)} valid families (repo {REPO[k]}); D4 violations {viol_d4} "
              f"(min slack {min_d4}, equality {eq_d4}); E1 violations {viol_e1} (equality {eq_e1}); "
              f"mu >= 2k-n violations {viol_2k}", flush=True)
        verdict(f"E3 D4 and E1 at k={k}", len(fams) == REPO[k] and viol_d4 == 0 and viol_e1 == 0,
                f"{len(fams)} families")

# ------------------------------------------------------------------ E.4
if "E4" in parts:
    print("== E.4 other small Phase 8 statements ==", flush=True)
    # W2 counterexample, SESSION_2026-11-12b.md section 7
    G = (0, 6, 14, 24, 30, 38, 46, 49, 55, 57, 59, 61, 62, 63)
    v, m = check_family(G, 6)
    Gd = delete_point(G, 5)
    vd, md = check_family(Gd, 5)
    print(f"W2: G valid={v} mu={m} (claim 4); G-5 valid={vd} mu={md} (claim 5)")
    verdict("E4 W2 counterexample at k=6", v and vd and m == 4 and md == 5, f"{m}, {md}")
    # D4 equality on M_6 and on the k = 7 classes ("attained by M_6 and six
    # of the seven k = 7 minimiser classes")
    M6 = matching_family(3)
    _, m6 = check_family(M6, 6)
    eq_m6 = 3 * m6 == 4 * 6 - 4 - len(M6)
    path = os.path.join(HERE, "results", "k7_cap4_classes.txt")
    if os.path.exists(path):
        att = [ast.literal_eval(l.split("members=")[1]) for l in open(path) if "members=" in l]
        eq = sum(1 for f in att if 3 * check_family(f, 7)[1] == 4 * 7 - 4 - len(f))
        print(f"D4 equality: M_6 {eq_m6}; k=7 classes with equality {eq} of {len(att)}")
        verdict("E4 D4 tight on M_6 and on 6 of the 7 k=7 classes", eq_m6 and eq == 6 and len(att) == 7,
                f"{eq}/{len(att)}")

print()
print("SECTION E SUMMARY")
for name, v, d in verdicts:
    print(f"  {v:9} {name}  [{d}]")
