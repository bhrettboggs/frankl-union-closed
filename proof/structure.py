"""structure.py -- structure of the minimisers of mu for k = 4..7 (Section F of Phase 8).

Usage:  python3 proof/structure.py > results/proof_structure.txt       (about 1 minute)

Catalogs used
  k = 4, 5 : brute force (frankl_core.enum_uc_leaves + is_valid), all minimisers.
  k = 6    : the M_6 class (ledger 2026-11-09 and docs/THEORY.md D.2, row k = 6).
  k = 7    : results/k7_mu4_core_classes.txt (6 core classes) + lift(M_6).

Part 1  Types. For every minimiser class: is it a block family B(sizes), the hub family
        H_t, a lift of a valid family, or one of the extension families I(t,j), II(t)
        of Proposition F2?  (Statement (i) of Section F.)
Part 2  Deletions. For every class and every element x: is {A minus x} valid on k-1
        elements, and what is its mu? Same for two-element deletions.
        (Statement (ii) of Section F and its weakenings.)
Part 4  Whether a valid one-element deletion lowers mu (all valid families, k = 4, 5;
        one explicit family at k = 6).
Part 3  Proposition F2: the families I(t,j), II(t), B(2,..,2,3), H_t are valid with
        mu = t+1, for t = 2..6, and pairwise non-isomorphic for t = 3, 4.
"""
import sys, os, warnings
warnings.simplefilter("ignore")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from frankl_core import (enum_uc_leaves, is_valid, mu, member_counts, canon, BC,
                         block_family, matching_family, lift)
from collections import Counter, defaultdict
from itertools import combinations

MINMU = {3: 1, 4: 2, 5: 3, 6: 3, 7: 4}


def hub(t):
    k = 2 * t + 1
    h = 1 << (2 * t)
    Z = (1 << k) - 1
    F = {0}
    for I in range(1, 1 << t):
        U = 0
        for i in range(t):
            if I >> i & 1:
                U |= 3 << (2 * i)
        F.add(U); F.add(U | h)
    for i in range(t):
        F.add(Z ^ (1 << (2 * i + 1)))
    return tuple(sorted(F))


def U_of(I, t):
    U = 0
    for i in range(t):
        if I >> i & 1:
            U |= 3 << (2 * i)
    return U


def fam_I(t, j):
    """I(t,j): M_{2t}; the top set Z is kept and Z+x is added; x is added to the
    co-singletons C_0..C_{j-1}. j = 0 is lift(M_{2t})."""
    k = 2 * t
    x = 1 << k
    Z = (1 << k) - 1
    F = {U_of(I, t) for I in range(1 << t)}          # block unions, including 0 and Z
    F.add(Z | x)
    for i in range(t):
        C = Z ^ (1 << (2 * i + 1))
        F.add(C | x if i < j else C)
    return tuple(sorted(F))


def fam_II(t, eps):
    """II(t,eps): x is added to every member of M_{2t} containing the last block and to the
    co-singletons C_i, i < t-1; Z is kept as well as Z+x. C_{t-1} gets x iff eps = 0.
    eps = 0 is the block family B(2,..,2,3)."""
    k = 2 * t
    x = 1 << k
    Z = (1 << k) - 1
    j = t - 1
    F = set()
    for I in range(1 << t):
        U = U_of(I, t)
        if I >> j & 1:
            F.add(U | x)
        else:
            F.add(U)
    F.add(Z)
    for i in range(t):
        C = Z ^ (1 << (2 * i + 1))
        if i != j or eps == 0:
            F.add(C | x)
        else:
            F.add(C)
    return tuple(sorted(F))


def named_classes(k):
    """canon -> name, for the named families on k elements."""
    out = {}

    def put(F, name):
        F = tuple(sorted(F))
        if is_valid(F, k):
            out.setdefault(canon(F, k), name)

    # block families: all partitions of k into parts >= 2
    def parts(n, lo):
        if n == 0:
            yield []
        for p in range(lo, n + 1):
            for rest in parts(n - p, p):
                yield [p] + rest
    for ps in parts(k, 2):
        blocks = []; s = 0
        for p in ps:
            blocks.append(list(range(s, s + p))); s += p
        put(block_family(blocks, k), "B(" + ",".join(map(str, ps)) + ")")
    if k % 2 == 1 and k >= 3:
        t = (k - 1) // 2
        put(hub(t), "H_%d" % t)
        if t >= 2:
            for j in range(t + 1):
                put(fam_I(t, j), "I(%d,%d)" % (t, j) + ("=lift(M_%d)" % (2 * t) if j == 0 else ""))
            put(fam_II(t, 1), "II(%d)" % t)
    return out


def delete(F, k, xs):
    """Delete the elements in xs from every member and relabel to [k-len(xs)]."""
    keep = [e for e in range(k) if e not in xs]
    out = set()
    for A in F:
        B = 0
        for i, e in enumerate(keep):
            if A >> e & 1:
                B |= 1 << i
        out.add(B)
    return tuple(sorted(out))


def catalogs():
    cats = {}
    allvalid = {}
    for k in (3, 4, 5):
        cls = Counter(); val = []

        def cb(F):
            if is_valid(F, k):
                val.append(F)
                if mu(F, k) == MINMU[k]:
                    cls[canon(F, k)] += 1
        enum_uc_leaves(k, cb)
        cats[k] = cls
        allvalid[k] = val
    M6 = tuple(sorted(matching_family(6)))
    cats[6] = Counter({canon(M6, 6): 120})
    c7 = Counter()
    for l in open(os.path.join(ROOT, "results", "k7_mu4_core_classes.txt")):
        p = l.split()
        if p and p[0] == "CLASS":
            F = tuple(int(z) for z in p[p.index("canon") + 1].split(","))
            assert is_valid(F, 7) and mu(F, 7) == 4
            c7[canon(F, 7)] = int(p[p.index("labeled") + 1])
    c7[canon(tuple(sorted(lift(M6, 6))), 7)] = 840
    cats[7] = c7
    return cats


def part1(cats):
    print("== 1. Types of the minimiser classes ==")
    for k in (4, 5, 6, 7):
        names = named_classes(k)
        prev = set(cats[k - 1]) if k - 1 in cats else set()
        tally = Counter()
        rows = []
        for c in sorted(cats[k], key=lambda z: (len(z), z)):
            name = names.get(c)
            lifted = False
            cnt = member_counts(c, k)
            if min(cnt) == 1:
                lifted = True
            if name is None and lifted:
                name = "lift of a k-1 minimiser"
            tally["named" if name else "unnamed"] += 1
            rows.append((len(c), sorted(cnt), name or "-"))
        print(f"k={k}: {len(cats[k])} minimiser classes; named {tally['named']}, unnamed {tally['unnamed']}")
        if len(rows) <= 10:
            for n, d, nm in rows:
                print(f"     n={n:3d} deg={d} type={nm}")
        else:
            c = Counter(nm for _, _, nm in rows)
            print("     " + ", ".join(f"{a}: {b}" for a, b in sorted(c.items())))


def part2(cats):
    print("== 2. Deletions ==")
    print("one-element deletion G-x = {A minus x}; 'valid' means frankl_core.is_valid on k-1 elements")
    for k in (4, 5, 6, 7):
        tot = len(cats[k])
        a = b = c = d = e2 = 0
        for cl in cats[k]:
            vals = []
            for x in range(k):
                H = delete(cl, k, [x])
                if is_valid(H, k - 1):
                    vals.append(mu(H, k - 1))
            if vals:
                a += 1
                if min(vals) == MINMU[k - 1]:
                    b += 1
                if min(vals) <= MINMU[k]:
                    c += 1
                if min(vals) <= MINMU[k] - 1:
                    d += 1
            v2 = []
            if k - 2 >= 3:
                for xs in combinations(range(k), 2):
                    H = delete(cl, k, list(xs))
                    if is_valid(H, k - 2):
                        v2.append(mu(H, k - 2))
                if (vals and min(vals) == MINMU[k - 1]) or (v2 and min(v2) == MINMU[k - 2]):
                    e2 += 1
        print(f"k={k}: classes {tot} | some valid deletion {a} | deletion is a k-1 minimiser {b} | "
              f"valid deletion with mu <= mu(G) {c} | with mu <= mu(G)-1 {d}"
              + (f" | one- or two-element deletion is a minimiser {e2}" if k >= 5 else ""))


def part3():
    print("== 3. Proposition F2 ==")
    for t in range(2, 7):
        k = 2 * t + 1
        fams = [("I(%d,%d)" % (t, j), fam_I(t, j)) for j in range(t + 1)]
        fams.append(("II(%d)" % t, fam_II(t, 1)))
        fams.append(("II(%d,0)=B(2,..,2,3)" % t, fam_II(t, 0)))
        fams.append(("H_%d" % t, hub(t)))
        ok = True
        for name, F in fams:
            v = is_valid(F, k)
            m = mu(F, k) if v else None
            g = sorted(2 * c - len(F) for c in member_counts(F, k))
            if not v or m != t + 1:
                ok = False
            if t <= 3:
                print(f"   t={t} {name:22s} n={len(F):3d} valid={v} mu={m} g={g}")
        line = f"t={t} (k={k}): {len(fams)} families, all valid with mu = t+1 = {t+1}: {ok}"
        if t <= 4:
            cl = {canon(F, k) for _, F in fams}
            line += f"; isomorphism classes {len(cl)}"
            Bc = canon(tuple(sorted(block_family([[2*i, 2*i+1] for i in range(t-1)] + [[2*t-2, 2*t-1, 2*t]], k))), k)
            line += f"; II(t,0) is B(2,..,2,3): {canon(fam_II(t,0), k) == Bc}"
        print(line)
        assert ok


def part4():
    print("== 4. Does a valid one-element deletion lower mu? ==")
    for k in (4, 5):
        diff = Counter()

        def cb(F):
            if not is_valid(F, k):
                return
            m = mu(F, k)
            for x in range(k):
                H = delete(F, k, [x])
                if is_valid(H, k - 1):
                    diff[m - mu(H, k - 1)] += 1
        enum_uc_leaves(k, cb)
        print(f"k={k}: all valid G and all x with G-x valid: distribution of mu(G) - mu(G-x) = {sorted(diff.items())}")
    # a k = 6 family whose deletion of element 5 is valid and has LARGER mu
    G = (0, 6, 14, 24, 30, 38, 46, 49, 55, 57, 59, 61, 62, 63)
    H = delete(G, 6, [5])
    assert is_valid(G, 6) and is_valid(H, 5)
    print(f"k=6 example: G = {list(G)}, mu(G) = {mu(G, 6)}; G-5 = {list(H)}, mu(G-5) = {mu(H, 5)}")
    assert mu(G, 6) == mu(H, 5) - 1
    print("=> 'mu(G) >= mu(G-x) + 1' fails at k = 5 (difference 0 occurs); "
          "'mu(G) >= mu(G-x)' holds for all valid G at k = 4, 5 and fails at k = 6")


if __name__ == "__main__":
    cats = catalogs()
    print("minimiser classes: " + ", ".join(f"k={k}: {len(cats[k])}" for k in (3, 4, 5, 6, 7)))
    part1(cats)
    part2(cats)
    part3()
    part4()
    print("ALL STRUCTURE CHECKS PASS")
