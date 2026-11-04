"""frankl_core.py — regenerated from Handoff v4 §10 spec (session 2026-06-12).

Conventions (must match §2 / §9 of handoff):
- Universe [k] = {0,...,k-1}, sets are bitmasks, Z = FULL = (1<<k)-1.
- Valid family at level k: union-closed G on [k], 0 in G, FULL in G,
  no singleton members, separating (all k element-incidence patterns distinct).
- n = |G| counts ALL members including 0 and FULL.
- c(e) counts all members containing e (FULL contributes 1 to every e).
- mu(G) = max_e 2c(e) - n ;  M(G) = mu + 2.
- deg-1: min_e c(e) == 1 (the deg-1 element lies only in FULL). core: min c >= 2.
- V(G,X,Y) = max_e [2c_G(e) + c_X(e) + c_Y(e)] - (n + a) over ORDERED pairs of
  nonempty, 0-free up-sets X,Y of the poset (G \ {0}, subset order) with |X|=|Y|=a.
  V(G) = min over all such pairs. Trivial cap: X=Y={FULL} gives V <= mu+1.
- U2(m) = {0} u {S : |S| >= 2}  (so mu(U2[m]) = m-2).
- block_family(blocks): all unions of blocks + co-singletons FULL\{x} for every
  non-kept x (kept = min of each block). M_k = B(2,...,2).
- lift: G at level k -> G u {(1<<(k+1))-1} at level k+1.
- peel_compress: deg-1 valid G at k -> remove FULL, drop deg-1 bit, relabel -> level k-1.
"""

import sys
import time
import random
from itertools import permutations

sys.setrecursionlimit(10000)

BC = int.bit_count


def enum_uc_leaves(k, callback=None):
    FULL = (1 << k) - 1
    mids = [m for m in range(3, FULL) if BC(m) >= 2]
    mids.sort(key=lambda m: -BC(m))
    nm = len(mids)
    out = [] if callback is None else None
    chosen = []
    chosen_set = set()

    def rec(i):
        if i == nm:
            fam = tuple(sorted([0] + chosen + [FULL]))
            if callback is None:
                out.append(fam)
            else:
                callback(fam)
            return
        m = mids[i]
        rec(i + 1)
        for x in chosen:
            u = m | x
            if u != m and u != x and u != FULL and u not in chosen_set:
                return
        chosen.append(m)
        chosen_set.add(m)
        rec(i + 1)
        chosen.pop()
        chosen_set.discard(m)

    rec(0)
    return out


def member_counts(F, k):
    c = [0] * k
    for S in F:
        s = S
        while s:
            b = s & (-s)
            c[b.bit_length() - 1] += 1
            s ^= b
    return c


def element_patterns(F, k):
    pats = [0] * k
    for i, S in enumerate(F):
        s = S
        while s:
            b = s & (-s)
            pats[b.bit_length() - 1] |= (1 << i)
            s ^= b
    return pats


def is_separating(F, k):
    pats = element_patterns(F, k)
    return len(set(pats)) == k


def is_valid(F, k):
    FULL = (1 << k) - 1
    fs = set(F)
    if 0 not in fs or FULL not in fs:
        return False
    for S in F:
        if S and BC(S) == 1:
            return False
    L = [s for s in F if s]
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            if (L[i] | L[j]) not in fs:
                return False
    return is_separating(F, k)


def mu(F, k):
    c = member_counts(F, k)
    return 2 * max(c) - len(F)


def min_degree(F, k):
    return min(member_counts(F, k))


def _poset(F):
    elems = sorted([s for s in F if s], key=lambda s: (-BC(s), s))
    m = len(elems)
    sup = []
    for i in range(m):
        ei = elems[i]
        si = [j for j in range(i) if elems[j] != ei and (ei | elems[j]) == elems[j]]
        sup.append(si)
    return elems, sup


def upset_size_counts(F):
    elems, sup = _poset(F)
    m = len(elems)
    counts = {}
    included = [False] * m

    def rec(i, size):
        if i == m:
            if size:
                counts[size] = counts.get(size, 0) + 1
            return
        rec(i + 1, size)
        if all(included[j] for j in sup[i]):
            included[i] = True
            rec(i + 1, size + 1)
            included[i] = False

    rec(0, 0)
    return counts


def count_upsets(F):
    return sum(upset_size_counts(F).values())


def ordered_pair_count(F):
    return sum(v * v for v in upset_size_counts(F).values())


def _pareto_insert(front, p):
    for q in front:
        ok = True
        for qe, pe in zip(q, p):
            if qe > pe:
                ok = False
                break
        if ok:
            return
    front[:] = [q for q in front
                if not all(pe <= qe for pe, qe in zip(p, q))]
    front.append(p)


def upset_pareto_fronts(F, k, time_budget=None):
    elems, sup = _poset(F)
    m = len(elems)
    fronts = {}
    included = [False] * m
    prof = [0] * k
    t0 = time.time()
    aborted = [False]
    tick = [0]

    def rec(i, size):
        if aborted[0]:
            return
        tick[0] += 1
        if time_budget is not None and (tick[0] & 0x3FFF) == 0:
            if time.time() - t0 > time_budget:
                aborted[0] = True
                return
        if i == m:
            if size:
                _pareto_insert(fronts.setdefault(size, []), tuple(prof))
            return
        rec(i + 1, size)
        if all(included[j] for j in sup[i]):
            included[i] = True
            S = elems[i]
            s = S
            while s:
                b = s & (-s)
                prof[b.bit_length() - 1] += 1
                s ^= b
            rec(i + 1, size + 1)
            s = S
            while s:
                b = s & (-s)
                prof[b.bit_length() - 1] -= 1
                s ^= b
            included[i] = False

    rec(0, 0)
    if aborted[0]:
        return None
    return fronts


def V_exact(F, k, time_budget=None):
    base = [2 * c for c in member_counts(F, k)]
    n = len(F)
    fronts = upset_pareto_fronts(F, k, time_budget=time_budget)
    if fronts is None:
        return None
    best = None
    for a, fr in fronts.items():
        off = n + a
        for x in fr:
            for y in fr:
                v = max(b + xe + ye for b, xe, ye in zip(base, x, y)) - off
                if best is None or v < best:
                    best = v
    return best


def V_naive(F, k):
    base = [2 * c for c in member_counts(F, k)]
    n = len(F)
    elems = sorted([s for s in F if s])
    m = len(elems)
    by_size = {}
    cur = []

    def rec(start):
        if cur:
            up = set()
            for a in cur:
                for s in elems:
                    if (a | s) == s:
                        up.add(s)
            prof = [0] * k
            for s in up:
                t = s
                while t:
                    b = t & (-t)
                    prof[b.bit_length() - 1] += 1
                    t ^= b
            by_size.setdefault(len(up), []).append(tuple(prof))
        for i in range(start, m):
            ei = elems[i]
            ok = True
            for c0 in cur:
                u = ei | c0
                if u == ei or u == c0:
                    ok = False
                    break
            if ok:
                cur.append(ei)
                rec(i + 1)
                cur.pop()

    rec(0)
    best = None
    for a, ps in by_size.items():
        off = n + a
        for x in ps:
            for y in ps:
                v = max(b + xe + ye for b, xe, ye in zip(base, x, y)) - off
                if best is None or v < best:
                    best = v
    return best


def lift(F, k):
    return tuple(sorted(set(F) | {(1 << (k + 1)) - 1}))


def peel_compress(F, k):
    FULL = (1 << k) - 1
    c = member_counts(F, k)
    e = c.index(1)
    assert c.count(1) == 1, "separating family has at most one deg-1 element"
    lo = (1 << e) - 1
    out = []
    for s in F:
        if s == FULL:
            continue
        assert not (s >> e) & 1, "deg-1 element appears outside FULL"
        out.append((s & lo) | ((s >> (e + 1)) << e))
    H = tuple(sorted(out))
    assert (1 << (k - 1)) - 1 in H, "compressed top missing (Lemma C violated?)"
    return H, k - 1


def block_family(blocks, k):
    FULL = (1 << k) - 1
    bmasks = []
    for b in blocks:
        m = 0
        for e in b:
            m |= 1 << e
        bmasks.append(m)
    assert sum(BC(m) for m in bmasks) == k
    u_all = 0
    for m in bmasks:
        u_all |= m
    assert u_all == FULL
    members = set()
    t = len(bmasks)
    for sub in range(1 << t):
        u = 0
        for i in range(t):
            if (sub >> i) & 1:
                u |= bmasks[i]
        members.add(u)
    for b in blocks:
        kept = min(b)
        for x in b:
            if x != kept:
                members.add(FULL ^ (1 << x))
    return tuple(sorted(members))


def matching_family(k):
    assert k % 2 == 0
    return block_family([[2 * i, 2 * i + 1] for i in range(k // 2)], k)


def U2(m):
    FULL = (1 << m) - 1
    return tuple(sorted([0] + [s for s in range(3, FULL + 1) if BC(s) >= 2]))


def canon(F, k):
    best = None
    for perm in permutations(range(k)):
        out = []
        for s in F:
            t = 0
            x = s
            while x:
                b = x & (-x)
                t |= 1 << perm[b.bit_length() - 1]
                x ^= b
            out.append(t)
        out = tuple(sorted(out))
        if best is None or out < best:
            best = out
    return best


def maximal_members(F, k):
    FULL = (1 << k) - 1
    props = [s for s in F if s and s != FULL]
    out = []
    for s in props:
        if not any(t != s and (s | t) == t for t in props):
            out.append(s)
    return out


def lemma_c_holds(F, k):
    return all(BC(s) == k - 1 for s in maximal_members(F, k))


def census(m):
    masks = sorted(range(1 << m), key=lambda s: -BC(s))
    nm = len(masks)
    fams = []
    chosen = []
    chosen_set = set()

    def rec(i):
        if i == nm:
            if len(chosen) >= 2:
                fams.append(tuple(sorted(chosen)))
            return
        s = masks[i]
        rec(i + 1)
        for x in chosen:
            u = s | x
            if u != s and u != x and u not in chosen_set:
                return
        chosen.append(s)
        chosen_set.add(s)
        rec(i + 1)
        chosen.pop()
        chosen_set.discard(s)

    rec(0)
    return fams


def is_tight(F, m):
    n = len(F)
    if n % 2:
        return False
    c = member_counts(F, m)
    return 2 * max(c) == n


def is_boolean(F, m):
    n = len(F)
    if n & (n - 1):
        return False
    fs = set(F)
    if 0 not in fs:
        return False
    nonempty = [s for s in F if s]
    if not nonempty:
        return False
    atoms = [s for s in nonempty
             if not any(t != s and (t | s) == s for t in nonempty)]
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            if atoms[i] & atoms[j]:
                return False
    if (1 << len(atoms)) != n:
        return False
    gen = {0}
    for a in atoms:
        gen |= {g | a for g in gen}
    return gen == fs
