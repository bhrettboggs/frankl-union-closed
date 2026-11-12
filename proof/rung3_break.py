"""rung3_break.py -- randomised search for a valid family on [k] with mu < ceil(k/2).

Usage:  python3 proof/rung3_break.py k seconds [seed]

NOT exhaustive. A candidate is the union-closure of a list of generator sets (sizes
2..k-1) together with the empty set and Z; it is kept only if it is separating (it has no
singleton by construction). Starts: the generators of M_k / B(2,..,2,3), of the hub
family, of random block families, and random lists; local moves add, drop or change one
generator. The objective is (mu, number of elements with g = mu).
Prints the smallest mu seen. A family with mu < ceil(k/2) is printed as a FAM line and
re-checked with frankl_core.is_valid.
"""
import sys, os, time, random, warnings
warnings.simplefilter("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from frankl_core import is_valid, mu as mu_ref

k = int(sys.argv[1]); T = float(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
rng = random.Random(seed)
FULL = (1 << k) - 1
PC = [bin(m).count("1") for m in range(1 << k)]
MID = [m for m in range(1 << k) if 2 <= PC[m] <= k - 1]
LIMIT = 3000
TARGET = (k + 1) // 2


def closure(gens):
    cl = {0, FULL}
    for g in gens:
        new = {g | a for a in cl}
        cl |= new
        if len(cl) > LIMIT:
            return None
    return cl


def score(gens):
    cl = closure(gens)
    if cl is None:
        return None
    n = len(cl)
    c = [0] * k
    pat = [0] * k
    for i, a in enumerate(cl):
        m = a
        while m:
            b = m & -m
            e = b.bit_length() - 1
            c[e] += 1
            pat[e] ^= hash((i, 7919)) & 0xFFFFFFFFFFFF
            m ^= b
    # separation test (exact)
    cols = [frozenset(a for a in cl if a >> e & 1) for e in range(k)] if len(set(pat)) < k else None
    if cols is not None and len(set(cols)) < k:
        return None
    g = [2 * x - n for x in c]
    m_ = max(g)
    return (m_, sum(1 for x in g if x == m_), n), cl


def block_gens(sizes, perm):
    gens = []; i = 0
    for s in sizes:
        blk = perm[i:i + s]; i += s
        gens.append(sum(1 << e for e in blk))
        for e in blk[1:]:
            gens.append(FULL ^ (1 << e))
    return gens


def start():
    style = rng.randrange(5)
    perm = list(range(k)); rng.shuffle(perm)
    if style == 0:
        sizes = [2] * (k // 2)
        if k % 2:
            sizes[-1] = 3
        return block_gens(sizes, perm)
    if style == 1:
        sizes = []; r = k
        while r > 0:
            s = rng.choice((2, 2, 3)) if r >= 4 else r
            if r - s == 1:
                s = r
            sizes.append(s); r -= s
        return block_gens(sizes, perm)
    if style == 2 and k % 2:
        t = k // 2; h = 1 << perm[-1]
        gens = []
        for i in range(t):
            P = (1 << perm[2 * i]) | (1 << perm[2 * i + 1])
            gens += [P, P | h, FULL ^ (1 << perm[2 * i + 1])]
        return gens
    if style == 3:
        return [rng.choice(MID) for _ in range(rng.randrange(k, 2 * k + 2))]
    small = [m for m in MID if PC[m] <= 3] + [m for m in MID if PC[m] == k - 1]
    return [rng.choice(small) for _ in range(rng.randrange(k, 2 * k + 2))]


def main():
    t0 = time.time(); best = None; evals = 0; restarts = 0; hist = {}
    while time.time() - t0 < T:
        gens = start(); r = score(gens); evals += 1
        if r is None:
            continue
        cur, cl = r; restarts += 1; stall = 0
        while stall < 80 and time.time() - t0 < T:
            g2 = list(gens); mv = rng.randrange(3)
            if mv == 0:
                g2.append(rng.choice(MID))
            elif mv == 1 and len(g2) > 1:
                g2.pop(rng.randrange(len(g2)))
            else:
                i = rng.randrange(len(g2)); g2[i] ^= 1 << rng.randrange(k)
                if not (2 <= PC[g2[i]] <= k - 1):
                    stall += 1; continue
            r2 = score(g2); evals += 1
            if r2 is None:
                stall += 1; continue
            hist[r2[0][0]] = hist.get(r2[0][0], 0) + 1
            if best is None or r2[0][0] < best[0]:
                best = (r2[0][0], tuple(sorted(r2[1])))
            if r2[0][0] < TARGET:
                F = tuple(sorted(r2[1]))
                assert is_valid(F, k) and mu_ref(F, k) == r2[0][0]
                print("FAM", r2[0][0], ",".join(map(str, F)))
                print("valid family with mu < ceil(k/2) found"); return
            if r2[0][:2] <= cur[:2]:
                stall = 0 if r2[0][:2] < cur[:2] else stall + 1
                gens, cur = g2, r2[0]
            else:
                stall += 1
    F = best[1]
    assert is_valid(F, k) and mu_ref(F, k) == best[0]
    print(f"k={k} seed={seed} seconds={T:.0f} evaluations={evals} restarts={restarts} "
          f"min mu seen={best[0]} (ceil(k/2)={TARGET}) lowest mu counts={sorted(hist.items())[:4]} "
          f"no valid family with mu < ceil(k/2) found")


if __name__ == "__main__":
    main()
