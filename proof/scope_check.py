"""scope_check.py -- brute-force checks for the Section B scope statements.

Usage:  python3 proof/scope_check.py [kmax]      (default kmax = 4; kmax = 4 takes a few seconds)

For every union-closed family F of subsets of [k] (all 2^(2^k) candidate families are
tested for union-closure, so this is exhaustive for k <= kmax), other than {} and {0}:

 B1  Run the standard reduction (add the empty set, merge twins, stop at a singleton)
     and check that it ends either at a family with a singleton member, whose element is
     then abundant in F, or at a family that frankl_core.is_valid accepts on k' >= 3
     elements, with |G| = |F| + [0 not in F] and the same maximum frequency.

 B2  For separating F with universe exactly [k]:
     (a) if 0 not in F:  F has a strict-majority element  <=>  mu(F + {0}) >= 0;
     (b) if 0 in F and {x} in F and A -> A+x is a bijection from the members avoiding x
         onto the members containing x, then F = F' (+) {0,{x}} with F' separating on
         [k]-x and mu(F) = max(0, 2 mu(F'));
     (c) Poonen's Conjecture 14 itself: F not a power set => some element lies in
         strictly more than half of the members.

Sets are bitmasks, as in frankl_core.py.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import warnings
warnings.simplefilter("ignore")
from frankl_core import is_valid, mu, member_counts, BC


def union_closed(F):
    fs = set(F)
    L = list(F)
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            if (L[i] | L[j]) not in fs:
                return False
    return True


def patterns(F, elems):
    return {e: frozenset(i for i, A in enumerate(F) if A >> e & 1) for e in elems}


def universe(F):
    u = 0
    for A in F:
        u |= A
    return u


def elems_of(mask):
    return [e for e in range(mask.bit_length()) if mask >> e & 1]


def compress(F, keep):
    """Relabel the elements in `keep` (sorted) to 0..len(keep)-1."""
    pos = {e: i for i, e in enumerate(keep)}
    out = []
    for A in F:
        B = 0
        for e in keep:
            if A >> e & 1:
                B |= 1 << pos[e]
        out.append(B)
    return tuple(sorted(out))


def reduce_family(F):
    """Standard reduction. Returns (kind, G, kprime, survivors):
    kind = 'singleton' or 'valid'."""
    G = set(F)
    G.add(0)
    U = elems_of(universe(G))
    # merge twins: keep one representative per incidence pattern
    G = sorted(G)
    pats = patterns(G, U)
    rep = {}
    for e in U:
        rep.setdefault(pats[e], e)
    keep = sorted(rep.values())
    mask = sum(1 << e for e in keep)
    H = sorted(set(A & mask for A in G))
    assert len(H) == len(G), "twin deletion must be injective on members"
    if any(BC(A) == 1 for A in H):
        return "singleton", H, len(keep), keep
    return "valid", compress(H, keep), len(keep), keep


def main():
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    for k in range(1, kmax + 1):
        nsub = 1 << k
        FULL = nsub - 1
        n_uc = n_single = n_valid = 0
        n_sep = n_sep_noempty = n_sep_biject = n_c14 = 0
        for code in range(1, 1 << nsub):
            F = tuple(A for A in range(nsub) if code >> A & 1)
            if F == (0,):
                continue
            if not union_closed(F):
                continue
            n_uc += 1
            n = len(F)
            cF = member_counts(F, k)
            maxc = max(cF)
            # ---- B1
            kind, G, kp, keep = reduce_family(F)
            assert len(G) == n + (0 not in F)
            if kind == "singleton":
                n_single += 1
                x = [A for A in G if BC(A) == 1][0].bit_length() - 1
                assert 2 * cF[x] >= len(G) >= n, ("singleton element not abundant", F)
            else:
                n_valid += 1
                assert kp >= 3, ("valid end with k' < 3", F)
                assert is_valid(G, kp), ("reduction did not end at a valid family", F)
                assert max(member_counts(G, kp)) == maxc
                # so  mu(G) >= 0  <=>  2 maxc >= |G| >= n  =>  F satisfies Frankl
                assert mu(G, kp) == 2 * maxc - len(G)
            # ---- B2: separating families with universe exactly [k]
            if universe(F) != FULL:
                continue
            if len(set(patterns(F, range(k)).values())) != k:
                continue
            n_sep += 1
            strict = 2 * maxc > n
            if 0 not in F:
                n_sep_noempty += 1
                G0 = tuple(sorted(F + (0,)))
                assert strict == (2 * maxc - len(G0) >= 0)
            else:
                for x in range(k):
                    if (1 << x) in F:
                        Fx = [A for A in F if A >> x & 1]
                        Fn = [A for A in F if not A >> x & 1]
                        if len(Fx) == len(Fn):
                            n_sep_biject += 1
                            assert set(A | (1 << x) for A in Fn) == set(Fx)
                            rest = [e for e in range(k) if e != x]
                            Fp = compress(Fn, rest)
                            if k - 1 >= 1:
                                assert universe(Fp) == (1 << (k - 1)) - 1
                                assert len(set(patterns(Fp, range(k - 1)).values())) == k - 1
                                mup = 2 * max(member_counts(Fp, k - 1)) - len(Fp)
                            else:
                                mup = -len(Fp)
                            assert 2 * maxc - n == max(0, 2 * mup), (F, x)
            if n != nsub:  # not the power set
                n_c14 += 1
                assert strict, ("Conjecture 14 fails", F)
        print(f"k={k}: union-closed families {n_uc} | B1: end at singleton {n_single}, "
              f"end at valid {n_valid} | B2: separating on [k] {n_sep}, without 0 {n_sep_noempty}, "
              f"bijective singleton cases {n_sep_biject}, Conjecture 14 instances checked {n_c14}")
    print("ALL SCOPE CHECKS PASS")


if __name__ == "__main__":
    main()
