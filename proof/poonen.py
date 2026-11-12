"""poonen.py -- Section D of Phase 8: what Frankl's conjecture (FC) gives for rung 1
(mu >= 1 on valid families), and where the induction breaks.

Usage:  python3 proof/poonen.py > results/proof_poonen.txt        (about 2 minutes)

FC is a theorem for universes of at most 12 points, so everything below is unconditional
at the sizes tested; the script checks the inequalities and counts how often they decide
rung 1.

For a valid G let Irr(G) be its join-irreducible members (non-empty members that are not
the union of two other members). For J a subset of Irr(G), G minus J is union-closed, and
FC applied to it gives an element e with
        g_G(e) >= g_J(e) + p_J,     p_J = 1 if |G| - |J| is odd, else 0,
where g_J(e) = #{A in J : e in A} - #{A in J : e not in A}. Hence
        mu(G) >= beta(G) := max over J of ( min_e g_J(e) + p_J ),
the minimum being over the universe of G minus J.

Part 1  For all valid families at k = 3, 4, 5: check mu >= beta, tabulate mu - beta, and
        count the families for which beta >= 1 (rung 1 follows from FC by deletion and
        parity) and those with beta <= 0, split by the parity of n.
Part 2  Corollary: mu >= j - 2, j = number of join-irreducible co-singletons.
Part 3  The induction step that loses 1: pairs (G, B), B join-irreducible, G and G minus B
        both valid, with mu(G) = mu(G minus B) - 1. Counts at k = 4, 5 and the cases where
        G is a minimiser.
Part 4  The same quantities on the k = 6, 7 minimiser catalogs.
Part 5  Proposition D4 (the Lo Faro / Hu staircase argument in margin form):
        3 mu >= 4k - 4 - n, checked on all valid families at k = 3, 4, 5 and on the catalogs.
"""
import sys, os, warnings
warnings.simplefilter("ignore")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from frankl_core import enum_uc_leaves, is_valid, mu, member_counts, canon, BC, matching_family, lift
from collections import Counter

MINMU = {3: 1, 4: 2, 5: 3, 6: 3, 7: 4}


def irreducibles(F):
    fs = [A for A in F if A]
    out = []
    for A in fs:
        subs = [B for B in fs if B != A and B & A == B]
        red = False
        for i in range(len(subs)):
            for j in range(i, len(subs)):
                if subs[i] | subs[j] == A:
                    red = True
                    break
            if red:
                break
        if not red:
            out.append(A)
    return out


def beta(F, k):
    """max over subsets J of Irr(F) of min_e g_J(e) + parity bonus. Exact (subset DP)."""
    irr = irreducibles(F)
    n = len(F)
    FULL = (1 << k) - 1
    m = len(irr)
    best = n % 2            # J empty
    # g_J(e) as vectors; enumerate subsets by Gray-like incremental update
    vec = [[1 if A >> e & 1 else -1 for e in range(k)] for A in irr]
    cur = [0] * k
    size = 0
    inJ = [False] * m
    topidx = irr.index(FULL) if FULL in irr else -1
    # the element lying only in FULL (if FULL is irreducible, the family is degree-1)
    cnt = member_counts(F, k)
    for code in range(1, 1 << m):
        low = (code & -code).bit_length() - 1
        if inJ[low]:
            inJ[low] = False; size -= 1
            for e in range(k):
                cur[e] -= vec[low][e]
        else:
            inJ[low] = True; size += 1
            for e in range(k):
                cur[e] += vec[low][e]
        # code runs through all subsets in Gray order when we flip bit 'low' of the Gray code:
        # (standard reflected Gray code: flipping the lowest set bit position of the counter)
        if topidx >= 0 and inJ[topidx]:
            mn = min(cur[e] for e in range(k) if cnt[e] > 1)
        else:
            mn = min(cur)
        v = mn + ((n - size) % 2)
        if v > best:
            best = v
    return best, irr


def part1_2_3():
    for k in (3, 4, 5):
        diff = Counter(); cert = Counter(); jdiff = Counter(); viol = 0; total = 0
        drop = Counter(); drop_min = 0; ex = None
        vset = set()
        fams = []

        def cb(F):
            if is_valid(F, k):
                fams.append(F)
        enum_uc_leaves(k, cb)
        vset = set(fams)
        # work up to isomorphism for beta (expensive), weights = labeled counts
        classes = Counter(canon(F, k) for F in fams) if k <= 4 else None
        if k == 5:
            classes = Counter()
            rep = {}
            for F in fams:
                c = canon(F, k)
                classes[c] += 1
        for c, wgt in classes.items():
            m_ = mu(c, k)
            b, irr = beta(c, k)
            total += wgt
            if m_ < b:
                viol += wgt
            diff[m_ - b] += wgt
            key = ("beta>=1" if b >= 1 else "beta<=0") + (", n odd" if len(c) % 2 else ", n even")
            cert[key] += wgt
            j = sum(1 for A in irr if BC(A) == k - 1)
            jdiff[m_ - (j - 2)] += wgt
            if m_ < j - 2:
                viol += wgt
            # part 3: remove one irreducible B
            for B in irr:
                H = tuple(A for A in c if A != B)
                if is_valid(H, k):
                    d = m_ - mu(H, k)
                    drop[d] += wgt
                    if d == -1 and m_ == MINMU[k]:
                        drop_min += wgt
                        if ex is None:
                            ex = (c, B)
        print(f"== k = {k}: {total} valid families ({len(classes)} classes) ==")
        print(f"  violations of mu >= beta or mu >= j-2: {viol}")
        print(f"  mu - beta distribution (labeled): {sorted(diff.items())}")
        print(f"  rung 1 decided by FC + deletion + parity: {sorted(cert.items())}")
        print(f"  mu - (j-2) distribution, j = join-irreducible co-singletons: {sorted(jdiff.items())}")
        print(f"  pairs (G, B), B join-irreducible, G-B valid: mu(G) - mu(G-B) distribution {sorted(drop.items())}")
        print(f"  of these with mu(G) = mu(G-B) - 1 and G a minimiser: {drop_min}")
        if ex:
            c, B = ex
            H = tuple(A for A in c if A != B)
            print(f"  example: G = {list(c)}, mu(G) = {mu(c,k)}; B = {B}; mu(G-B) = {mu(H,k)}")
        assert viol == 0


def part4():
    print("== minimiser catalogs k = 6, 7 ==")
    M6 = tuple(sorted(matching_family(6)))
    cats = [(6, "M_6", M6)]
    for l in open(os.path.join(ROOT, "results", "k7_mu4_core_classes.txt")):
        p = l.split()
        if p and p[0] == "CLASS":
            F = tuple(int(z) for z in p[p.index("canon") + 1].split(","))
            cats.append((7, "class " + p[1], F))
    cats.append((7, "lift(M_6)", tuple(sorted(lift(M6, 6)))))
    for k, name, F in cats:
        b, irr = beta(F, k)
        j = sum(1 for A in irr if BC(A) == k - 1)
        print(f"  k={k} {name:10s} n={len(F):2d} mu={mu(F,k)} beta={b} irreducibles={len(irr)} "
              f"join-irreducible co-singletons j={j} (j-2={j-2})")
        assert mu(F, k) >= b


def staircase_check(F, k):
    """Return (ok_bound, ok_lemma, slack) for Proposition D4 on the valid family F:
    bound: 3 mu >= 4k - 4 - n;  lemma: with u a most frequent element and B the members
    avoiding u, some element a of maximum frequency in B lies in at least k-1 members
    containing u, so c(a) >= phi_B + k - 1."""
    n = len(F)
    c = member_counts(F, k)
    m_ = 2 * max(c) - n
    ok_bound = 3 * m_ >= 4 * k - 4 - n
    ok_lemma = True
    for u in range(k):
        if c[u] != max(c):
            continue
        Bf = [A for A in F if not A >> u & 1]
        cB = member_counts(Bf, k)
        phi = max(cB)
        if phi == 0:
            continue
        with_u = [A for A in F if A >> u & 1]
        good = any(cB[a] == phi and sum(1 for A in with_u if A >> a & 1) >= k - 1
                   for a in range(k) if a != u)
        if not good or 2 * phi < len(Bf):
            ok_lemma = False
    return ok_bound, ok_lemma, 3 * m_ - (4 * k - 4 - n)


def part5():
    print("== 5. Proposition D4: 3 mu >= 4k - 4 - n ==")
    for k in (3, 4, 5):
        bad_b = bad_l = tot = tight = 0
        tight_min = 0

        def cb(F):
            nonlocal bad_b, bad_l, tot, tight, tight_min
            if not is_valid(F, k):
                return
            tot += 1
            b, l, sl = staircase_check(F, k)
            bad_b += (not b); bad_l += (not l)
            if 0 <= sl <= 2:
                tight += 1
                if mu(F, k) == MINMU[k]:
                    tight_min += 1
        enum_uc_leaves(k, cb)
        print(f"  k={k}: {tot} valid families; violations of the bound {bad_b}, of the staircase step {bad_l}; "
              f"families where ceil((4k-4-n)/3) = mu: {tight} (minimisers among them: {tight_min})")
        assert bad_b == 0 and bad_l == 0
    M6 = tuple(sorted(matching_family(6)))
    cats = [(6, "M_6", M6), (8, "M_8", tuple(sorted(matching_family(8))))]
    for l in open(os.path.join(ROOT, "results", "k7_mu4_core_classes.txt")):
        p = l.split()
        if p and p[0] == "CLASS":
            cats.append((7, "class " + p[1], tuple(int(z) for z in p[p.index("canon") + 1].split(","))))
    cats.append((7, "lift(M_6)", tuple(sorted(lift(M6, 6)))))
    for k, name, F in cats:
        b, l, sl = staircase_check(F, k)
        n = len(F)
        print(f"  k={k} {name:10s} n={n:2d} mu={mu(F,k)} ceil((4k-4-n)/3)={-((n+4-4*k)//3)} bound holds {b} staircase step holds {l}")
        assert b and l


if __name__ == "__main__":
    part1_2_3()
    part4()
    part5()
    print("ALL POONEN CHECKS PASS")
