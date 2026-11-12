"""sector_break.py -- try to break "mu >= k-2 on the all-co-singleton sector".

Usage:  python3 proof/sector_break.py k seconds [seed]

Randomised search, NOT exhaustive. A family in the sector is
    G = {0, Z} + all co-singletons + cl(gens),
where cl(gens) is the set of unions of the generator sets that have size <= k-2
(unions of size k-1 or k are co-singletons or Z and are already present).
The search does random restarts and local moves on the generator list (add, drop or
change one generator), minimising (mu, number of elements with g = mu).
It prints the smallest mu seen and stops with a FAM line if mu < k-2 is found.
Every reported family is re-checked with frankl_core.is_valid.
"""
import sys, os, time, random, warnings
warnings.simplefilter("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from frankl_core import is_valid, mu as mu_ref

k = int(sys.argv[1]); T = float(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
rng = random.Random(seed)
FULL = (1 << k) - 1
PC = [bin(m).count("1") for m in range(1 << k)]
MID = [m for m in range(1 << k) if 2 <= PC[m] <= k - 2]
LIMIT = 4000   # cap on |cl(gens)| to keep one evaluation cheap


def closure(gens):
    cl = set()
    for g in gens:
        new = {g}
        for a in cl:
            u = a | g
            if PC[u] <= k - 2:
                new.add(u)
        # close the additions among themselves: unions with g are absorbed since g is in every new set
        cl |= new
        if len(cl) > LIMIT:
            return None
    # one more pass to be safe (generators added later may combine with later unions)
    changed = True
    while changed:
        changed = False
        L = list(cl)
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                u = L[i] | L[j]
                if PC[u] <= k - 2 and u not in cl:
                    cl.add(u); changed = True
        if len(cl) > LIMIT:
            return None
    return cl


def score(gens):
    cl = closure(gens)
    if cl is None:
        return None
    n = len(cl) + k + 2
    c = [k] * k           # Z and the k-1 co-singletons containing e
    for a in cl:
        m = a
        while m:
            b = m & -m
            c[b.bit_length() - 1] += 1
            m ^= b
    g = [2 * x - n for x in c]
    m_ = max(g)
    return (m_, sum(1 for x in g if x == m_), n), cl


def family(cl):
    return tuple(sorted({0, FULL} | {FULL ^ (1 << x) for x in range(k)} | cl))


def random_gens():
    style = rng.randrange(4)
    if style == 0:
        return [rng.choice(MID) for _ in range(rng.randrange(1, 9))]
    if style == 1:   # small sets only
        small = [m for m in MID if PC[m] <= (k + 1) // 2]
        return [rng.choice(small) for _ in range(rng.randrange(2, 12))]
    if style == 2:   # blocks of a random partition plus noise
        perm = list(range(k)); rng.shuffle(perm)
        gens = []; i = 0
        while i < k:
            s = rng.choice((2, 2, 3)); blk = perm[i:i + s]; i += s
            if len(blk) >= 2:
                gens.append(sum(1 << e for e in blk))
        gens += [rng.choice(MID) for _ in range(rng.randrange(0, 3))]
        return gens
    # sets of size about k/2
    half = [m for m in MID if abs(2 * PC[m] - k) <= 1]
    return [rng.choice(half) for _ in range(rng.randrange(2, 10))]


def main():
    t0 = time.time(); best = None; evals = 0; restarts = 0; hist = {}
    while time.time() - t0 < T:
        gens = random_gens(); r = score(gens); evals += 1
        if r is None:
            continue
        cur, cl = r; restarts += 1
        stall = 0
        while stall < 60 and time.time() - t0 < T:
            g2 = list(gens); mv = rng.randrange(3)
            if mv == 0 or not g2:
                g2.append(rng.choice(MID))
            elif mv == 1 and len(g2) > 1:
                g2.pop(rng.randrange(len(g2)))
            else:
                i = rng.randrange(len(g2)); g2[i] ^= 1 << rng.randrange(k)
                if not (2 <= PC[g2[i]] <= k - 2):
                    continue
            r2 = score(g2); evals += 1
            if r2 is None:
                stall += 1; continue
            if r2[0][:2] <= cur[:2]:
                if r2[0][:2] < cur[:2]:
                    stall = 0
                else:
                    stall += 1
                gens, cur, cl = g2, r2[0], r2[1]
            else:
                stall += 1
            hist[r2[0][0]] = hist.get(r2[0][0], 0) + 1
            if best is None or r2[0][0] < best[0]:
                best = (r2[0][0], family(r2[1]))
            if r2[0][0] < k - 2:
                F = family(r2[1])
                assert is_valid(F, k) and mu_ref(F, k) == r2[0][0]
                print("FAM", r2[0][0], ",".join(map(str, F)))
                print("COUNTEREXAMPLE to mu >= k-2 found"); return
    F = best[1]
    assert is_valid(F, k) and mu_ref(F, k) == best[0]
    low = sorted(hist.items())[:4]
    print(f"k={k} seed={seed} seconds={T:.0f} evaluations={evals} restarts={restarts} "
          f"min mu seen={best[0]} (k-2={k-2}) lowest mu counts={low} no family with mu < k-2 found")


if __name__ == "__main__":
    main()
