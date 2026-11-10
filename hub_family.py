"""hub_family.py — the hub family H_t on k = 2t+1 points (found as the n=18 mu=4 class at k=7).
Pairs P_i = {2i, 2i+1} (i < t), hub h = 2t. Members: emptyset; for every nonempty I subset [t]:
U_I = union of P_i (i in I) and U_I + {h}; plus co-singletons Z - {2i+1} (non-kept element of
each pair). Predicted: n = 2^(t+1) + t - 1, mu = t + 1 = ceil(k/2)."""
import sys
from frankl_core import is_valid, mu, member_counts, canon

def hub_family(t):
    k = 2 * t + 1; Z = (1 << k) - 1; h = 1 << (2 * t)
    S = {0}
    for I in range(1, 1 << t):
        u = 0
        for i in range(t):
            if I >> i & 1: u |= 3 << (2 * i)
        S |= {u, u | h}
    for i in range(t): S.add(Z ^ (1 << (2 * i + 1)))
    return tuple(sorted(S)), k

if __name__ == "__main__":
    for t in range(1, 6):
        F, k = hub_family(t)
        print(f"t={t} k={k} valid={is_valid(F, k)} n={len(F)} pred_n={2**(t+1)+t-1} mu={mu(F, k)} pred_mu={t+1} deg={sorted(member_counts(F, k))}")
