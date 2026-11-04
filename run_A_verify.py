"""run_A_verify.py — re-verify §9 calibration constants from Handoff v4."""

import time
from frankl_core import (
    enum_uc_leaves, is_valid, member_counts, mu, min_degree,
    V_exact, V_naive, count_upsets, ordered_pair_count,
    lift, peel_compress, block_family, matching_family, U2, canon,
    maximal_members, lemma_c_holds, census, is_tight, is_boolean,
)

FAILS = []


def check(name, got, expected):
    ok = (got == expected)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got!r}"
          + ("" if ok else f" (expected {expected!r})"))
    if not ok:
        FAILS.append(name)
    return ok


t_start = time.time()

for m, (tot_exp, tight_exp) in [(3, (113, 14)), (4, (4943, 51))]:
    fams = census(m)
    tights = [F for F in fams if is_tight(F, m)]
    check(f"census m={m} total (|F|>=2)", len(fams), tot_exp)
    check(f"census m={m} tight", len(tights), tight_exp)
    check(f"census m={m} all tight Boolean",
          all(is_boolean(F, m) for F in tights), True)

k = 3
leaves3 = enum_uc_leaves(k)
valid3 = [F for F in leaves3 if is_valid(F, k)]
check("k=3 leaves", len(leaves3), 8)
check("k=3 valid", len(valid3), 4)
V3 = {F: V_exact(F, k) for F in valid3}
Vn3 = {F: V_naive(F, k) for F in valid3}
check("k=3 V_exact == V_naive (all)", all(V3[F] == Vn3[F] for F in valid3), True)
check("k=3 minV", min(V3.values()), 2)
check("k=3 feasible (V<=0)", sum(1 for v in V3.values() if v <= 0), 0)
check("k=3 minmu", min(mu(F, k) for F in valid3), 1)
check("k=3 ordered pairs", sum(ordered_pair_count(F) for F in valid3), 38)
check("k=3 Lemma C (max members are co-singletons)",
      all(lemma_c_holds(F, k) for F in valid3), True)

k = 4
leaves4 = enum_uc_leaves(k)
valid4 = [F for F in leaves4 if is_valid(F, k)]
check("k=4 leaves", len(leaves4), 378)
check("k=4 valid", len(valid4), 304)
deg1_4 = [F for F in valid4 if min_degree(F, k) == 1]
check("k=4 deg1", len(deg1_4), 16)
check("k=4 cores", len(valid4) - len(deg1_4), 288)
mu4 = {F: mu(F, k) for F in valid4}
dist4 = {}
for v in mu4.values():
    dist4[v] = dist4.get(v, 0) + 1
check("k=4 mu-dist", dist4, {2: 48, 3: 128, 4: 96, 5: 28, 6: 4})
V4 = {F: V_exact(F, k) for F in valid4}
Vn4 = {F: V_naive(F, k) for F in valid4}
check("k=4 V_exact == V_naive (all 304)", all(V4[F] == Vn4[F] for F in valid4), True)
check("k=4 minV", min(V4.values()), 3)
check("k=4 feasible (V<=0)", sum(1 for v in V4.values() if v <= 0), 0)
check("k=4 ordered pairs", sum(ordered_pair_count(F) for F in valid4), 27249)
check("k=4 Lemma C", all(lemma_c_holds(F, k) for F in valid4), True)
tri_ok = True
for F in valid4:
    mm = maximal_members(F, k)
    cos = [s for s in F if bin(s).count('1') == k - 1]
    if sorted(mm) != sorted(cos):
        tri_ok = False
        break
    if (len(mm) == 1) != (min_degree(F, k) == 1):
        tri_ok = False
        break
check("k=4 trichotomy (#max = #co-singletons; =1 iff deg1)", tri_ok, True)

V3_cache = {F: V3[F] for F in valid3}
mu3_cache = {F: mu(F, 3) for F in valid3}
l_ok, peel_targets = True, set()
for G in deg1_4:
    H, kk = peel_compress(G, 4)
    if kk != 3 or not is_valid(H, 3):
        l_ok = False
        break
    peel_targets.add(H)
    if V4[G] != min(V3_cache[H] + 2, mu3_cache[H] + 2):
        l_ok = False
        break
check("Thm L identity all 16 deg-1 at k=4", l_ok, True)
check("Thm L peel image = all 4 valid k=3", len(peel_targets), 4)

M4 = matching_family(4)
check("M4 valid", is_valid(M4, 4), True)
check("M4 (n,mu,V)", (len(M4), mu(M4, 4), V_exact(M4, 4)), (6, 2, 3))
check("M4 V_naive", V_naive(M4, 4), 3)
M6 = matching_family(6)
check("M6 valid", is_valid(M6, 6), True)
check("M6 (n,mu,V)", (len(M6), mu(M6, 6), V_exact(M6, 6)), (11, 3, 4))
check("M6 V_naive", V_naive(M6, 6), 4)
M8 = matching_family(8)
check("M8 valid", is_valid(M8, 8), True)
check("M8 (n,mu,V)", (len(M8), mu(M8, 8), V_exact(M8, 8)), (20, 4, 5))
B223 = block_family([[0, 1], [2, 3], [4, 5, 6]], 7)
check("B(2,2,3)@7 valid", is_valid(B223, 7), True)
check("B(2,2,3)@7 (n,mu,V)", (len(B223), mu(B223, 7), V_exact(B223, 7)), (12, 4, 5))
B34 = block_family([[0, 1, 2], [3, 4, 5, 6]], 7)
check("B(3,4)@7 valid", is_valid(B34, 7), True)
check("B(3,4)@7 (n,mu,V)", (len(B34), mu(B34, 7), V_exact(B34, 7)), (9, 5, 6))
LM6 = lift(M6, 6)
check("liftM6@7 valid", is_valid(LM6, 7), True)
check("liftM6@7 V", V_exact(LM6, 7), 5)
check("liftM6@7 identity min(V+2,mu+2)", min(4 + 2, 3 + 2), 5)

W = tuple(sorted([0, 12, 18, 30, 31, 33, 45, 47, 51, 55, 63]))
check("witness valid@6", is_valid(W, 6), True)
cW = sorted(member_counts(W, 6), reverse=True)
check("witness counts", cW, [7, 7, 7, 6, 6, 6])
check("witness mu", mu(W, 6), 3)
check("witness V_exact", V_exact(W, 6), 4)
check("witness V_naive", V_naive(W, 6), 4)
check("witness in M6 orbit", canon(W, 6) == canon(M6, 6), True)
check("witness lift@7 V", V_exact(lift(W, 6), 7), 5)

for m in range(3, 10):
    check(f"mu(U2[{m}])", mu(U2(m), m), m - 2)
check("V(U2[3])", V_exact(U2(3), 3), 2)
check("V(U2[4])", V_exact(U2(4), 4), 3)
check("Vn(U2[3])", V_naive(U2(3), 3), 2)
check("Vn(U2[4])", V_naive(U2(4), 4), 3)
check("#upsets(U2[5])", count_upsets(U2(5)), 6893)
check("V(U2[5])", V_exact(U2(5), 5), 4)

T4 = lift(U2(3), 3)
check("T4=liftU2[3] (mu,V)", (mu(T4, 4), V_exact(T4, 4)), (2, 3))
T5 = lift(T4, 4)
check("T5 (mu,V)", (mu(T5, 5), V_exact(T5, 5)), (3, 4))

SIG = tuple(sorted([0, 12, 20, 24, 28, 30, 31]))
check("sigma valid@5", is_valid(SIG, 5), True)
check("sigma (mu,V)", (mu(SIG, 5), V_exact(SIG, 5)), (3, 4))
H1, k1 = peel_compress(SIG, 5)
H2, k2 = peel_compress(H1, k1)
check("sigma peel^2 == U2[3] (canon)", canon(H2, 3) == canon(U2(3), 3), True)

print()
if FAILS:
    print(f"CALIBRATION RESULT: {len(FAILS)} FAILURE(S): {FAILS}")
else:
    print("CALIBRATION RESULT: ALL CHECKS PASS")
print(f"total time {time.time()-t_start:.1f}s")
