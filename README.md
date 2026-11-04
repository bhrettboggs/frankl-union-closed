# Frankl Union-Closed Sets — Exhaustive Search Engine

Computational study of the equality structure of **Frankl's union-closed sets conjecture**: for small universe sizes *k*, exhaustively search all "valid" union-closed families and determine the minimum top-margin

  μ(G) = max_e 2c(e) − |G|

where c(e) is the number of members containing element e.

A family is **valid** at level *k* if it is union-closed on [k], contains ∅ and [k], has no singleton members, and is separating (see `frankl_core.py` for the exact conventions). Frankl's conjecture says some element lies in at least half the members, which is μ ≥ 0. This project asks a finer question: **how small can the margin μ get** for valid families at each *k*, and which families attain the minimum?

## Context and prior work

This repository does **not** re-verify Frankl's conjecture for small universes; that is already known. It studies the margin μ and its extremal families, a question the verifications below don't directly answer. Whether these minimum margins already appear elsewhere in the literature has not yet been checked.

- **Small universes.** Bošnjak and Marković proved the conjecture for universes of at most 11 elements, and Živković and Vučković gave a computer-assisted proof for 12 elements ("The 12-element case of Frankl's conjecture", preprint, 2012).
- **Small families.** Combined with Lo Faro's lower bound on the size of a minimal counterexample (also Roberts and Simpson, 2010), this implies the conjecture for families with at most about 50 sets. See Bruhn and Schaudt, *The Journey of the Union-Closed Sets Conjecture*, Graphs and Combinatorics 31 (2015), for a survey.
- **Constant-fraction bounds.** Gilmer (arXiv:2211.09055, 2022) proved the first constant lower bound (0.01). Alweiss, Huang and Sellke (Electron. J. Combin. 31(3), 2024) raised it to (3−√5)/2 ≈ 0.38, and others have since nudged it slightly higher.

## Results (program-internal)

| k | min μ | how established |
|---|-------|-----------------|
| 3 | 1 | exhaustive enumeration |
| 4 | 2 | exhaustive enumeration |
| 5 | 3 | exhaustive (2,244 μ=3 cores, Python ≡ C node-for-node) |
| 6 | 3 | exhaustive; 120 attainers, all in the orbit of the matching family M₆ |
| 7 | 4 | orbit-quotient search over all co-singleton sectors s=2..7, plus Lemma D for the 20 densest representatives |

These are results of this program, not peer-reviewed claims.

## Files

| File | Purpose |
|------|---------|
| `frankl_core.py` | Core library: validity checks, μ, V (exact and naive), lift/peel, block and matching families, canonical forms |
| `run_A_verify.py` | Calibration suite (67 checks) — run this first |
| `mu_search.py` | Lemma-C-structured targeted search (Python reference) |
| `mu_search.c` | C port of the search; matches Python node-for-node with pairwise prune off |
| `mu_search2.c` | Search with a closure-aware "dead candidate" prune (7–116× fewer nodes, identical found sets) |
| `orbits.c` | Orbit representatives of the top candidate layer under Stab(S) |
| `orbits2.c` | Second-level orbit quotient within a fixed top-layer pattern |
| `orbit_driver.py`, `orbit_driver2.py` | Resumable, checkpointed drivers over orbit reps (v2 adds node-limit sharding) |
| `orbit_driver3.py`, `orbit_driver4.py` | Same drivers using `mu_search2` (v4 adds a μ-cap argument) |
| `rep_driver.py` | Driver for second-level sub-shards of a single representative |
| `lemma_d_check.c` | Exhaustive check of u(F) − 3\|F\| ≤ 2 over all 2²¹ graphs on 7 vertices |
| `lemma_d.c` | Lemma D coverage test (independence number of the triple conflict graph) for k=7, s=7 |
| `expected.md5` | Checksums for every source file |

## Build and verify

```bash
md5sum -c expected.md5
for b in mu_search mu_search2 orbits orbits2; do gcc -O3 -march=native -w -o $b $b.c; done
gcc -O2 -o lemma_d_check lemma_d_check.c
gcc -O2 -o lemma_d lemma_d.c
python3 run_A_verify.py        # expect: CALIBRATION RESULT: ALL CHECKS PASS
./lemma_d_check                # expect: max = 2, attained by 7 labeled graphs
```

Requires gcc and Python 3.10+ (uses `int.bit_count`).

## Example: re-close the k=7, s=7 sector

```bash
python3 orbit_driver3.py 7 7 200 1 50000000 3   # rerun until COMPLETE; ~11 min single-core
./orbits 7 127 | awk '$1=="REP"{print $2}' | ./lemma_d > lemma_d_out.txt
```

## History and license

The search was developed locally and moved to this repository in a single commit, so the git history starts at the finished state.

MIT. See [LICENSE](LICENSE).
