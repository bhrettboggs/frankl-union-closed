"""growth.py -- Section E of Phase 8: lower bounds on mu that grow with k on slices n <= c k.

Usage:  python3 proof/growth.py > results/proof_growth.txt        (about 30 seconds)

Proposition E1: if every union-closed family with a non-empty member has an element in at
least kappa |F| members (a theorem for kappa = psi = (3 - sqrt 5)/2), then every valid
family on k points with n members has
        (1 + kappa) mu >= 2k - 2 - (1 - kappa) n.
kappa = 1/2 is Proposition D4 (it needs Frankl's conjecture on k-1 points, a theorem for
k <= 13).

Part 1  Check both inequalities on all valid families at k = 3, 4, 5.
Part 2  Table: for k = 8..40, the largest n for which each bound gives mu >= 1 and
        mu >= ceil(k/2), next to the sizes of the known extremal families.
"""
import sys, os, math, warnings
warnings.simplefilter("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from frankl_core import enum_uc_leaves, is_valid, mu

PSI = (3 - 5 ** 0.5) / 2


def part1():
    print("== 1. Exhaustive check, k = 3..5 ==")
    for k in (3, 4, 5):
        tot = bad_psi = bad_half = 0
        minslack = None

        def cb(F):
            nonlocal tot, bad_psi, bad_half, minslack
            if not is_valid(F, k):
                return
            tot += 1
            m_, n = mu(F, k), len(F)
            s = (1 + PSI) * m_ - (2 * k - 2 - (1 - PSI) * n)
            if s < -1e-9:
                bad_psi += 1
            if 3 * m_ < 4 * k - 4 - n:
                bad_half += 1
            if minslack is None or s < minslack:
                minslack = s
        enum_uc_leaves(k, cb)
        print(f"k={k}: {tot} valid families; violations of E1 with kappa=psi: {bad_psi} "
              f"(smallest slack {minslack:.3f}); violations with kappa=1/2: {bad_half}")
        assert bad_psi == 0 and bad_half == 0


def largest_n(k, kappa, target):
    """largest n such that the bound forces mu >= target for ALL n' <= n (no parity refinement)."""
    n = k + 1
    while (2 * k - 2 - (1 - kappa) * (n + 1)) / (1 + kappa) > target - 1:
        n += 1
    ok = (2 * k - 2 - (1 - kappa) * n) / (1 + kappa) > target - 1
    return n if ok else None


def part2():
    print("== 2. Ranges of n covered ==")
    print("  k | mu>=1: n <= (psi, all k) | n <= (1/2; theorem for k <= 13) | "
          "mu>=ceil(k/2): n <= (psi) | n <= (1/2) | n(M_k) or n(B(2..2,3)) | n(H_t)")
    for k in list(range(8, 14)) + [16, 20, 30, 40]:
        t = k // 2
        nM = 2 ** t + t if k % 2 == 0 else 2 ** t + t + 1
        nH = 2 ** (t + 1) + t - 1 if k % 2 else "-"
        tg = (k + 1) // 2
        print(f" {k:2d} | {largest_n(k, PSI, 1)} | {largest_n(k, 0.5, 1)} | "
              f"{largest_n(k, PSI, tg)} | {largest_n(k, 0.5, tg)} | {nM} | {nH}")
    print("  thresholds: n < (1+sqrt5)(k-1) = 3.236(k-1) for kappa = psi; n <= 4k-5 for kappa = 1/2")


if __name__ == "__main__":
    part1()
    part2()
    print("ALL GROWTH CHECKS PASS")
