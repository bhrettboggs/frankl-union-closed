"""sector_full.py -- the all-co-singleton sector S(G) = [k] (Section C of Phase 8).

Usage:
    python3 proof/sector_full.py [path-to-mu_search2-binary] > results/proof_sector_full.txt

Everything is deterministic. Without the binary the k = 6 search part is skipped.
Runtime: about 1 minute with the binary (k = 5 brute force dominates).

Parts
  A  k = 3,4,5: brute force over all valid families (frankl_core.enum_uc_leaves),
     restricted to the sector. Checks the sum identity
         sum_e g(e) = k(k-2) + sum_{j=2}^{k-2} (2j-k) a_j,
     and reports the mu distribution, the minimum of sum_e g(e), and the families
     with mu = k-2 by isomorphism class.
  B  k = 5 analogue of Lemma D:  a_3 >= p(F), max_F (|F| - p(F)) over all graphs.
  C  k = 6 analogue of Lemma D:  a_4 >= q(F), max_F (|F| - q(F)) over all graphs.
  D  k = 6: mu_search2 on S = [6] at caps 3 and 4 (needs the binary).
  E  k = 7: what Lemma D's ingredients give for sum_e g(e) without a cap, from
     results/lemma_d2_k7_s7_cap4.txt.
  F  The families G_W = {0, Z, co-singletons} + {A subset of W, |A| >= 2}, |W| = k-2:
     sum_e g(e) and mu for k = 5..12 (formula, and direct count for k <= 10).
  F2 The same with W' of size k-3 and an arbitrary top layer T: the sum method is
     vacuous for every T once k >= 11.
  G  The power construction of Proposition C4, checked on small valid families.
"""
import sys, os, subprocess, itertools, warnings
warnings.simplefilter("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, ROOT)
from frankl_core import (enum_uc_leaves, is_valid, mu, member_counts, canon, BC,
                         block_family, matching_family)
from collections import Counter
from math import comb


def gvec(F, k):
    n = len(F)
    return [2 * c - n for c in member_counts(F, k)]


def sizes(F, k):
    a = [0] * (k + 1)
    for A in F:
        a[BC(A)] += 1
    return a


def in_sector(F, k):
    return sum(1 for A in F if BC(A) == k - 1) == k


def identity_ok(F, k):
    a = sizes(F, k)
    return sum(gvec(F, k)) == k * (k - 2) + sum((2 * j - k) * a[j] for j in range(2, k - 1))


def edges_of(k):
    return [(i, j) for i in range(k) for j in range(i + 1, k)]


def no_isolated(Fmask_edges, W):
    """Fmask_edges: list of edges as bitmasks; W: vertex bitmask. True if the graph
    induced on W has no isolated vertex (W is then the union of the edges inside it)."""
    cov = 0
    for e in Fmask_edges:
        if e & W == e:
            cov |= e
    return cov == W


# ---------------------------------------------------------------- part A
def part_A():
    print("== A. Brute force, k = 3..5 ==")
    out = {}
    for k in (3, 4, 5):
        dist = Counter()
        sums = Counter()
        eq = Counter()
        bad_id = 0
        store = []

        def cb(F):
            nonlocal bad_id
            if not is_valid(F, k) or not in_sector(F, k):
                return
            if not identity_ok(F, k):
                bad_id += 1
            m = mu(F, k)
            dist[m] += 1
            sums[sum(gvec(F, k))] += 1
            if m == k - 2:
                eq[canon(F, k)] += 1
            if k == 5:
                store.append(F)

        enum_uc_leaves(k, cb)
        tot = sum(dist.values())
        print(f"k={k}: sector families {tot}, identity violations {bad_id}, "
              f"min mu {min(dist)} (k-2 = {k-2}), mu distribution {sorted(dist.items())}")
        print(f"      min sum_e g(e) = {min(sums)}, so N_max({k}) = k(k-2) - min = {k*(k-2)-min(sums)}")
        print(f"      families with mu = k-2: {sum(eq.values())} labeled in {len(eq)} classes")
        for c, v in sorted(eq.items(), key=lambda x: (len(x[0]), x[0])):
            a = sizes(c, k)
            print(f"        n={len(c):3d} labeled={v:3d} a_2..a_{k-2}={a[2:k-1]} g={sorted(gvec(c,k))}")
        assert bad_id == 0 and min(dist) == k - 2
        out[k] = store
    return out[5]


# ---------------------------------------------------------------- part B
def part_B(fams5):
    print("== B. k = 5: Lemma D_5 ==")
    k = 5
    E = edges_of(k)
    Em = [(1 << i) | (1 << j) for i, j in E]
    triples = [m for m in range(1 << k) if BC(m) == 3]
    best = -10
    arg = []
    for code in range(1 << len(E)):
        F = [Em[i] for i in range(len(E)) if code >> i & 1]
        p = sum(1 for W in triples if no_isolated(F, W))
        v = len(F) - p
        if v > best:
            best, arg = v, [code]
        elif v == best:
            arg.append(code)
    print(f"max over all 2^10 graphs F on 5 vertices of |F| - p(F) = {best}, attained by {len(arg)} labeled graphs")
    print("   p(F) = number of 3-sets W such that F[W] has no isolated vertex")
    viol = 0
    for G in fams5:
        F = [A for A in G if BC(A) == 2]
        a3 = sum(1 for A in G if BC(A) == 3)
        p = sum(1 for W in triples if no_isolated(F, W))
        if a3 < p or len(F) - a3 > best:
            viol += 1
    print(f"checked a_3 >= p(F) and a_2 - a_3 <= {best} on all {len(fams5)} sector families at k=5: violations {viol}")
    assert viol == 0
    print(f"=> sum_e g(e) = 15 - a_2 + a_3 >= {15-best}, so mu >= ceil({15-best}/5) = {-(-(15-best)//5)}  (true minimum 3)")
    return best


# ---------------------------------------------------------------- part C
def part_C():
    print("== C. k = 6: Lemma D_6 ==")
    k = 6
    E = edges_of(k)
    Em = [(1 << i) | (1 << j) for i, j in E]
    quads = [m for m in range(1 << k) if BC(m) == 4]
    best = -10
    cnt = 0
    for code in range(1 << len(E)):
        F = [Em[i] for i in range(len(E)) if code >> i & 1]
        q = sum(1 for W in quads if no_isolated(F, W))
        v = len(F) - q
        if v > best:
            best, cnt = v, 1
        elif v == best:
            cnt += 1
    print(f"max over all 2^15 graphs F on 6 vertices of |F| - q(F) = {best}, attained by {cnt} labeled graphs")
    print("   q(F) = number of 4-sets W such that F[W] has no isolated vertex")
    lo = 24 - 2 * best
    print(f"=> sum_e g(e) = 24 - 2a_2 + 2a_4 >= {lo}, so mu >= ceil({lo}/6) = {-(-lo//6)}  (true minimum 4, part D)")
    return best


# ---------------------------------------------------------------- part D
def part_D(binary, bestC):
    print("== D. k = 6: search of the sector S = [6] ==")
    if not binary:
        print("skipped (no mu_search2 binary given)")
        return
    k = 6
    for cap in (3, 4):
        r = subprocess.run([binary, "6", str(cap), "6", "1"], capture_output=True, text=True)
        fams = []
        sline = ""
        for l in r.stdout.splitlines():
            p = l.split()
            if p and p[0] == "FAM":
                fams.append(tuple(sorted(int(x) for x in p[2].split(","))))
            if p and p[0] == "S":
                sline = l
        print(f"cap {cap}: {sline}")
        cls = Counter()
        viol = 0
        E = edges_of(k)
        quads = [m for m in range(1 << k) if BC(m) == 4]
        for F in fams:
            assert is_valid(F, k) and in_sector(F, k) and identity_ok(F, k)
            assert mu(F, k) <= cap
            cls[canon(F, k)] += 1
            ed = [A for A in F if BC(A) == 2]
            a4 = sum(1 for A in F if BC(A) == 4)
            q = sum(1 for W in quads if no_isolated(ed, W))
            if a4 < q or len(ed) - a4 > bestC:
                viol += 1
        print(f"        families found {len(fams)}, all re-validated; classes {len(cls)}; "
              f"violations of a_4 >= q(F) or a_2 - a_4 <= {bestC}: {viol}")
        assert viol == 0
        if cap == 3:
            assert len(fams) == 0
        for c, v in sorted(cls.items(), key=lambda x: (len(x[0]), x[0])):
            a = sizes(c, k)
            print(f"        mu={mu(c,k)} n={len(c):3d} labeled={v:3d} a_2..a_4={a[2:5]} g={sorted(gvec(c,k))}")
    print("=> min mu on the sector S = [6] is 4 = k-2")


# ---------------------------------------------------------------- part E
def part_E():
    print("== E. k = 7: Lemma D's ingredients without a cap ==")
    fn = os.path.join(ROOT, "results", "lemma_d2_k7_s7_cap4.txt")
    worst = None
    rows = 0
    neg = 0
    for l in open(fn):
        p = l.split()
        if len(p) == 8 and p[0] == "T":
            t, al = int(p[3]), int(p[5])
            lb = 35 + 3 * t - 30 - al        # lower bound on sum_e g(e)
            rows += 1
            if lb <= 0:
                neg += 1
            if worst is None or lb < worst[0]:
                worst = (lb, int(p[1]), t, al)
    print(f"{rows} top-layer representatives; lower bound sum_e g(e) >= 5 + 3t - alpha(T)")
    print(f"smallest value of the bound: {worst[0]} at T={worst[1]} (t={worst[2]}, alpha={worst[3]}); "
          f"bound <= 0 for {neg} representatives")
    print("=> at k = 7 the sum method gives mu >= ceil((5 + 3t - alpha(T))/7); it proves mu >= 1 "
          f"for {rows-neg} of {rows} representatives and nothing for the rest")


# ---------------------------------------------------------------- part F
def part_F():
    print("== F. The families G_W ==")
    print("k  n   sum_e g(e)   k(k-2)  N(G_W)=2^(k-1)-k-(k-2)^2   mu(G_W)=2k-5   direct")
    for k in range(5, 13):
        w = k - 2
        N = 2 ** (k - 1) - k - (k - 2) ** 2
        n = 2 + k + (2 ** w - 1 - w)
        s = k * (k - 2) - N
        direct = ""
        if k <= 10:
            FULL = (1 << k) - 1
            W = (1 << w) - 1
            G = {0, FULL} | {FULL ^ (1 << x) for x in range(k)} | {A for A in range(W + 1) if BC(A) >= 2}
            G = tuple(sorted(G))
            assert is_valid(G, k) and in_sector(G, k) and len(G) == n
            assert sum(gvec(G, k)) == s and mu(G, k) == 2 * k - 5
            direct = "ok"
        print(f"{k:2d} {n:4d} {s:8d} {k*(k-2):8d} {N:10d} {2*k-5:18d}   {direct}")
    print("=> for k >= 8, sum_e g(e) < 0 on G_W although mu(G_W) = 2k-5 >= k-2")


def part_F2():
    print("== F2. The families G_{W',T} = G_0 + T + {A subset of W', |A| >= 2}, |W'| = k-3 ==")
    print("   T = all (k-2)-sets, the top layer that maximises sum_e g(e) for this lower part")
    print("k  t=C(k,2)  N = 3*2^(k-3) - k - (k-2)(k-3) - (k-4)t   U(k) = k(k-2) - N   direct")
    for k in range(7, 14):
        t = comb(k, 2)
        N = 3 * 2 ** (k - 3) - k - (k - 2) * (k - 3) - (k - 4) * t
        U = k * (k - 2) - N
        direct = ""
        if k <= 11:
            FULL = (1 << k) - 1
            W = (1 << (k - 3)) - 1
            G = {0, FULL} | {FULL ^ (1 << x) for x in range(k)}
            G |= {FULL ^ (1 << x) ^ (1 << y) for x in range(k) for y in range(x + 1, k)}
            G |= {A for A in range(W + 1) if BC(A) >= 2}
            G = tuple(sorted(G))
            assert is_valid(G, k) and in_sector(G, k)
            assert sum(gvec(G, k)) == U
            direct = "ok, mu = %d" % mu(G, k)
        print(f"{k:2d} {t:6d} {N:28d} {U:22d}   {direct}")
    print("=> for k >= 11 and EVERY top layer T there is a sector family with top layer T and")
    print("   sum_e g(e) < 0 (replace 'all (k-2)-sets' by T: the sum only decreases), so the")
    print("   sum method gives no positive lower bound on mu for any T")


# ---------------------------------------------------------------- part G
def power(F, k, r):
    """r-fold product on r disjoint copies of [k]."""
    out = [0]
    for i in range(r):
        out = [A | (B << (k * i)) for A in out for B in F]
    return out


def part_G():
    print("== G. Power construction (Proposition C4) ==")
    tests = [("U2[3]", (0, 3, 5, 6, 7), 3), ("M4", matching_family(4), 4),
             ("B(2,3)", block_family([[0, 1], [2, 3, 4]], 5), 5)]
    for name, F, k in tests:
        F = tuple(sorted(F))
        n = len(F)
        gF = gvec(F, k)
        for r in (1, 2, 3):
            K = r * k
            if n ** r > 200000:
                continue
            P = set(power(F, k, r))
            assert len(P) == n ** r
            FULL = (1 << K) - 1
            cos = [FULL ^ (1 << x) for x in range(K)]
            added = [c for c in cos if c not in P]
            G = tuple(sorted(P | set(cos)))
            assert is_valid(G, K) and in_sector(G, K)
            gG = gvec(G, K)
            for e in range(K):
                base = gF[e % k] * n ** (r - 1)
                plus = sum(1 if c >> e & 1 else -1 for c in added)
                assert gG[e] == base + plus
                assert gG[e] <= base + K
            print(f"{name}: r={r}, K={K}, |F^r|={n**r}, added co-singletons {len(added)}, "
                  f"mu(F^r)={mu(tuple(sorted(P)),K)} = mu(F)*n^(r-1) = {max(gF)*n**(r-1)}, mu(G)={max(gG)}")
    print("=> g_G(e) = g_F(e) n^(r-1) + (added co-singletons containing e) - (added avoiding e) <= g_F(e) n^(r-1) + rk")


def main():
    binary = sys.argv[1] if len(sys.argv) > 1 else None
    fams5 = part_A()
    b5 = part_B(fams5)
    b6 = part_C()
    part_D(binary, b6)
    part_E()
    part_F()
    part_F2()
    part_G()
    print("ALL SECTOR CHECKS PASS")


if __name__ == "__main__":
    main()
