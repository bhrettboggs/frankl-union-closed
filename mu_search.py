"""mu_search.py — Lemma-C-structured targeted search for low-mu cores.

By Lemma C every proper member of a core lies under a maximal member, and all
maximal members are co-singletons. So a core G on [k] with co-singleton set
exactly S (|S| = s >= 2) decomposes as G = {0, Z} u {Z\{x} : x in S} u M,
where every m in M has popcount 2..k-2 and misses at least one element of S.
Closure constraints live entirely among M; a union of popcount k-1 must be a
chosen co-singleton. Min degree is automatic for s >= 2.
"""

import sys

sys.setrecursionlimit(20000)
BC = int.bit_count


def search_S(k, S, mu_cap=3, node_limit=None):
    FULL = (1 << k) - 1
    S_mask = 0
    for x in S:
        S_mask |= 1 << x
    s = len(S)
    assert s >= 2
    cos = [FULL ^ (1 << x) for x in S]
    cos_set = set(cos)
    out_elems = [e for e in range(k) if not (S_mask >> e) & 1]

    cands = [m for m in range(3, FULL)
             if 2 <= BC(m) <= k - 2 and (m & S_mask) != S_mask]
    cands.sort(key=lambda m: (-BC(m), m))
    nc = len(cands)

    cnt_not = [[0] * k for _ in range(nc + 1)]
    suf_dec = [0] * (nc + 1)
    for i in range(nc - 1, -1, -1):
        m = cands[i]
        row, prev = cnt_not[i], cnt_not[i + 1]
        for e in range(k):
            row[e] = prev[e] + (0 if (m >> e) & 1 else 1)
        d = 2 * BC(m) - k
        suf_dec[i] = suf_dec[i + 1] + (d if d < 0 else 0)

    g = [0] * k
    for mem in [0, FULL] + cos:
        for e in range(k):
            g[e] += 1 if (mem >> e) & 1 else -1
    sum_g0 = sum(g)
    cap_sum = k * mu_cap

    chosen = []
    chosen_set = set()
    found = []
    stats = {"nodes": 0, "leaves": 0, "pruneA": 0, "pruneB": 0,
             "closure_rej": 0, "sep_fail": 0}

    def rec(i, sum_g):
        stats["nodes"] += 1
        if node_limit is not None and stats["nodes"] > node_limit:
            raise RuntimeError("node_limit")
        cn = cnt_not[i]
        for e in range(k):
            if g[e] - cn[e] > mu_cap:
                stats["pruneA"] += 1
                return
        if sum_g + suf_dec[i] > cap_sum:
            stats["pruneB"] += 1
            return
        if i == nc:
            stats["leaves"] += 1
            if len(out_elems) >= 2:
                pats = {}
                for e in out_elems:
                    p = 0
                    for j, m in enumerate(chosen):
                        if (m >> e) & 1:
                            p |= 1 << j
                    if p in pats:
                        stats["sep_fail"] += 1
                        return
                    pats[p] = e
            fam = tuple(sorted([0, FULL] + cos + chosen))
            found.append((fam, max(g)))
            return
        rec(i + 1, sum_g)
        m = cands[i]
        for x in chosen:
            u = m | x
            if (u != m and u != x and u != FULL
                    and u not in chosen_set and u not in cos_set):
                stats["closure_rej"] += 1
                return
        chosen.append(m)
        chosen_set.add(m)
        for e in range(k):
            g[e] += 1 if (m >> e) & 1 else -1
        rec(i + 1, sum_g + 2 * BC(m) - k)
        for e in range(k):
            g[e] -= 1 if (m >> e) & 1 else -1
        chosen.pop()
        chosen_set.discard(m)

    rec(0, sum_g0)
    return found, stats


def search_all_S(k, mu_cap=3, node_limit=None, sizes=None):
    from itertools import combinations
    all_found = []
    per_stats = []
    for s in (sizes or range(2, k + 1)):
        for S in combinations(range(k), s):
            fnd, st = search_S(k, S, mu_cap=mu_cap, node_limit=node_limit)
            all_found.extend(fnd)
            per_stats.append((S, st))
    return all_found, per_stats
