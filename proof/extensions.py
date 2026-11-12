"""extensions.py -- one-element extensions of a valid family (Section F of Phase 8).

Usage:
    python3 proof/extensions.py            # runs the checks for M_4, M_6, M_8 (about 1 minute)
    python3 proof/extensions.py 10         # also M_10 (long; see the session ledger)

Definition. Let H be a valid family on [k]. A ONE-ELEMENT EXTENSION of H is a valid
family G on [k+1] such that {A minus {k} : A in G} = H (deleting the new element x = k
gives back H). Writing
    G_0 = {A in G : x not in A},   G_1 = {A minus x : A in G, x in A},
G is union-closed iff G_0 is union-closed, G_1 is an up-set of (H, inclusion), and
G_0 contains H minus G_1. With B = H minus G_1, D = G_0 & G_1, E = G_1 minus D:
    n(G) = |H| + |D|,  g_G(e) = g_H(e) + g_D(e) for e < k,  g_G(x) = |E| - |B|.

The script enumerates ALL extensions of H = M_{2t} (frankl_core.matching_family), checks
these formulas and validity with frankl_core, and reports
  - the distribution of mu over all extensions (Theorem F1 says mu >= t+1),
  - the isomorphism classes with mu = t+1, in (B, D, E) form,
and, for t = 3, compares the classes with results/k7_mu4_core_classes.txt + lift(M_6).
"""
import sys, os, warnings
warnings.simplefilter("ignore")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from frankl_core import is_valid, mu, member_counts, canon, BC, matching_family, lift
from collections import Counter
from itertools import permutations


def upsets(H, k):
    """Up-sets of (H, inclusion) that contain FULL and do not contain 0, as index sets."""
    FULL = (1 << k) - 1
    m = len(H)
    sup = [[j for j in range(m) if j != i and H[i] & H[j] == H[i]] for i in range(m)]
    order = sorted(range(m), key=lambda i: -BC(H[i]))
    res = []

    def rec(p, cur):
        if p == m:
            res.append(frozenset(cur))
            return
        i = order[p]
        if H[i] == 0:
            rec(p + 1, cur)
            return
        if H[i] == FULL:
            cur.add(i); rec(p + 1, cur); cur.discard(i)
            return
        rec(p + 1, cur)
        if all(j in cur for j in sup[i]):
            cur.add(i); rec(p + 1, cur); cur.discard(i)

    rec(0, set())
    return res


def extensions(H, k, callback):
    """Call callback(B, D, E) (lists of members of H) for every pair (G_0, G_1) with
    G_1 an up-set containing FULL and not 0, G_0 union-closed, G_0 containing H minus G_1.
    Validity (separation of the new element) is NOT tested here."""
    H = sorted(H)
    idx = {A: i for i, A in enumerate(H)}
    m = len(H)
    for U in upsets(H, k):
        base = [i for i in range(m) if i not in U]
        Ul = sorted(U, key=lambda i: -BC(H[i]))      # decide large sets first
        # G_0 = base + D must be union-closed. Unions of two base sets that fall in U are forced into D.
        forced = set()
        ok = True
        for a in range(len(base)):
            for b in range(a + 1, len(base)):
                u = idx[H[base[a]] | H[base[b]]]
                if u in U:
                    forced.add(u)
        S = set(base)

        def rec(p):
            if p == len(Ul):
                # final closure check (unions of base sets with D sets, and forced sets)
                Sl = list(S)
                for a in range(len(Sl)):
                    for b in range(a + 1, len(Sl)):
                        if idx[H[Sl[a]] | H[Sl[b]]] not in S:
                            return
                callback([H[i] for i in base], [H[i] for i in S if i in U], [H[i] for i in U if i not in S])
                return
            i = Ul[p]
            # option: i not in D (only allowed if not already needed)
            need = False
            for j in S:
                if j in U and BC(H[j]) > BC(H[i]):
                    continue
            if i not in forced:
                rec(p + 1)
            # option: i in D: every union with an already chosen LARGER-or-equal member of S that is
            # strictly bigger than both must already be in S (it was decided earlier)
            good = True
            for j in S:
                u = H[i] | H[j]
                if u != H[i] and u != H[j] and idx[u] in U and idx[u] not in S:
                    good = False
                    break
            if good:
                S.add(i); rec(p + 1); S.discard(i)

        rec(0)


def build(B, D, E, k):
    x = 1 << k
    return tuple(sorted(B + D + [A | x for A in D] + [A | x for A in E]))


def describe(A, t):
    """Name a member of M_{2t}: U{blocks} or C{i} (co-singleton missing 2i+1)."""
    k = 2 * t
    FULL = (1 << k) - 1
    if BC(A) == k - 1:
        return "C%d" % ((FULL ^ A).bit_length() // 2)
    I = [i for i in range(t) if A >> (2 * i) & 1]
    return "U" + "".join(map(str, I)) if I else "0"


def run(t, compare=False):
    k = 2 * t
    H = tuple(sorted(matching_family(k)))
    gH = [2 * c - len(H) for c in member_counts(H, k)]
    dist = Counter()
    eq = {}
    stats = {"pairs": 0, "valid": 0, "formula_bad": 0}

    def cb(B, D, E):
        stats["pairs"] += 1
        G = build(B, D, E, k)
        # formulas
        n = len(H) + len(D)
        gD = [sum(1 if A >> e & 1 else -1 for A in D) for e in range(k)]
        g = [gH[e] + gD[e] for e in range(k)] + [len(E) - len(B)]
        m_ = max(g)
        if m_ <= t + 2 or stats["pairs"] % 97 == 0:      # full re-check on all small-mu cases and a sample
            if not is_valid(G, k + 1):
                return
            if len(G) != n or mu(G, k + 1) != m_:
                stats["formula_bad"] += 1
        else:
            # validity = separation of x from every old element (everything else is automatic)
            pats = set()
            xp = frozenset(i for i, A in enumerate(G) if A >> k & 1)
            twin = any(frozenset(i for i, A in enumerate(G) if A >> e & 1) == xp for e in range(k))
            if twin:
                return
        stats["valid"] += 1
        dist[m_] += 1
        if m_ == t + 1:
            c = canon(G, k + 1)
            eq.setdefault(c, []).append((B, D, E))

    extensions(H, k, cb)
    print(f"== M_{k} (t = {t}): {stats['pairs']} pairs (G_0, G_1), {stats['valid']} valid extensions, "
          f"formula mismatches {stats['formula_bad']} ==")
    print(f"mu distribution over valid extensions: {sorted(dist.items())}")
    print(f"minimum mu = {min(dist)}; t+1 = {t+1}; Theorem F1 (mu >= t+1) holds: {min(dist) >= t+1}")
    assert stats["formula_bad"] == 0 and min(dist) >= t + 1
    print(f"classes with mu = t+1: {len(eq)}")
    for c, lst in sorted(eq.items(), key=lambda z: (len(z[0]), z[0])):
        B, D, E = lst[0]
        s = sum(1 for A in c if BC(A) == k)
        print(f"  n={len(c):3d} s={s} deg={sorted(member_counts(c, k+1))} extensions={len(lst)}")
        print(f"      B={sorted(describe(A,t) for A in B)}")
        print(f"      D={sorted(describe(A,t) for A in D)}")
        print(f"      E={sorted(describe(A,t) for A in E)}")
    if compare:
        fn = os.path.join(ROOT, "results", "k7_mu4_core_classes.txt")
        cat = set()
        for l in open(fn):
            p = l.split()
            if p and p[0] == "CLASS":
                cat.add(tuple(int(z) for z in p[p.index("canon") + 1].split(",")))
        cat.add(canon(tuple(sorted(lift(H, k))), k + 1))
        print(f"k = 7 catalog: {len(cat)} classes (6 cores + lift(M_6)); "
              f"equal to the mu = 4 extension classes of M_6: {cat == set(eq)}")
        assert cat == set(eq)
    return eq


if __name__ == "__main__":
    run(2)
    run(3, compare=True)
    run(4)
    if len(sys.argv) > 1 and sys.argv[1] == "10":
        run(5)
    print("ALL EXTENSION CHECKS PASS")
