# Frankl Union-Closed Sets — Exhaustive Search Engine

Computational study of the equality structure of **Frankl's union-closed sets conjecture**: for small universe sizes *k*, exhaustively search all "valid" union-closed families and determine the minimum top-margin

  μ(G) = max_e 2c(e) − |G|

where c(e) is the number of members containing element e.

A family is **valid** at level *k* if it is union-closed on [k], contains ∅ and [k], has no singleton members, and is separating (see `frankl_core.py` for the exact conventions). Frankl's conjecture says some element lies in at least half the members, which is μ ≥ 0. This project asks a finer question: **how small can the margin μ get** for valid families at each *k*, and which families attain the minimum?

## Context and prior work

This repository does **not** re-verify Frankl's conjecture for small universes; that is already known. It studies the margin μ and its extremal families, a question the verifications below don't directly answer. A literature check (2026-11-12, [`docs/LITERATURE.md`](docs/LITERATURE.md)) found no prior computation of these minimum margins or their attainers; the lower bound μ ≥ 1 on this class is the case of Poonen's open strict-majority conjecture.

- **Small universes.** Bošnjak and Marković proved the conjecture for universes of at most 11 elements, and Vučković and Živković gave a computer-assisted proof for 12 elements ("The 12-element case of Frankl's conjecture", IPSI BgD Transactions on Internet Research 13(1), 2017; preprint 2012).
- **Small families.** Combined with Lo Faro's lower bound on the size of a minimal counterexample (also Roberts and Simpson, 2010), this implies the conjecture for families with at most about 50 sets. See Bruhn and Schaudt, *The Journey of the Union-Closed Sets Conjecture*, Graphs and Combinatorics 31 (2015), for a survey.
- **Constant-fraction bounds.** Gilmer (arXiv:2211.09055, 2022) proved the first constant lower bound (0.01). Alweiss, Huang and Sellke (Electron. J. Combin. 31(3), 2024) raised it to (3−√5)/2 ≈ 0.38, and others have since nudged it slightly higher (e.g. Jiang, arXiv:2609.08291, 2026: 0.38288525).
- **Related computation.** Pulaj, Raymond and Theis (Electron. J. Combin. 23(3), 2016) compute the minimum top frequency over union-closed families of a given size by integer programming; those families may contain singletons, so the margin question here is different.

## Results (program-internal)

| k | min μ | how established |
|---|-------|-----------------|
| 3 | 1 | exhaustive enumeration |
| 4 | 2 | exhaustive enumeration |
| 5 | 3 | exhaustive (2,244 μ=3 cores, Python ≡ C node-for-node) |
| 6 | 3 | exhaustive; 120 attainers, all in the orbit of the matching family M₆ |
| 7 | 4 | orbit-quotient search over all co-singleton sectors s=2..7, plus Lemma D for the 20 densest representatives; s=2..6 re-closed with `mu_search2` (2026-11-09) |
| 8 | 4 (independent route only, no certificate) | cap 3 INFEASIBLE by the CP-SAT model in `independent/` (4.0 h, solver log saved); M₈ attains 4. The repo's own search is incomplete: deg-1 sector has μ ≥ 5; core sector s=2 at cap 3 has 99/100 orbit reps closed, 0 found; s=3..8 not started |

**Attainers (2026-11-09).** At k=7 exactly 7 isomorphism classes attain μ=4 (11,340 labeled): six cores (`results/k7_mu4_core_classes.txt`, including B(2,2,3) and the hub family H₃) plus lift(M₆). Counting attainer classes over k=3..7 gives 1, 8, 51, 1, 7. The hub families H_t (`hub_family.py`) are valid at k=2t+1 with μ = t+1, a second infinite family that matches the block-family bound.

These are results of this program, not peer-reviewed claims. Session-by-session details, including falsified ideas, are in `SESSION_*.md`.

**Proof attempt (2026-11-12).** [`docs/PROOF_ATTEMPT.md`](docs/PROOF_ATTEMPT.md) records an attempt to prove lower bounds on μ, with every claim tagged and every failure stated; [`docs/PROOF_SURVEY.md`](docs/PROOF_SURVEY.md) surveys the known proof techniques. Nothing there proves Frankl's conjecture. The main outcomes: every valid one-element extension of M₂ₜ has μ ≥ t+1, and the seven k=7 attainers are exactly the extremal extensions of M₆; (1+ψ)μ ≥ 2k−2−(1−ψ)n for every valid family, ψ = (3−√5)/2, so μ ≥ 1 whenever n < (1+√5)(k−1); the lower bound μ ≥ 1 on all valid families is equivalent to Poonen's strict conjecture and remains open. Scripts are in `proof/`, their outputs in `results/proof_*.txt`.

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
| `lemma_d2.c` | Lemma D′: same test with a μ-cap argument (covered iff α(T) ≤ 3t+4−7·cap) |
| `mu_search3.c`, `orbits3.c` | `mu_search2` / `orbits` with arrays sized for k ≤ 8 (byte-identical output at k ≤ 7) |
| `mu_search4.c` | Experimental all-subsets LP prune (pw=2); admissible but slower, not used |
| `orbit_driver5.py` | `orbit_driver4.py` plus a Lemma-D′ skip file (`L` lines, never counted as searched) |
| `orbit_driver6.py` | `orbit_driver5.py` for k ≤ 8, with orbit-table caching and stride/offset sharding across cores |
| `classify.py` | Re-validate FAM lines and canonicalize them into isomorphism classes with labeled counts |
| `hub_family.py` | Construct and check the hub families H_t |
| `results/` | Certificates: k=7 cap-3 and cap-4 orbit logs, Lemma D′ output, the k=7 μ=4 class list |
| `expected.md5` | Checksums for every source file |

## Build and verify

```bash
md5sum -c expected.md5
for b in mu_search mu_search2 mu_search3 mu_search4 orbits orbits2 orbits3; do gcc -O3 -march=native -w -o $b $b.c; done
gcc -O2 -o lemma_d_check lemma_d_check.c
gcc -O2 -o lemma_d lemma_d.c
gcc -O2 -o lemma_d2 lemma_d2.c
python3 run_A_verify.py        # expect: CALIBRATION RESULT: ALL CHECKS PASS
./lemma_d_check                # expect: max = 2, attained by 7 labeled graphs
```

Requires gcc and Python 3.10+ (uses `int.bit_count`).

## Example: re-close the k=7, s=7 sector

```bash
python3 orbit_driver3.py 7 7 200 1 50000000 3   # rerun until COMPLETE; ~11 min single-core
./orbits 7 127 | awk '$1=="REP"{print $2}' | ./lemma_d > lemma_d_out.txt
```

## Example: the k=7 μ=4 catalog

```bash
for s in 2 3 4 5 6; do python3 orbit_driver5.py 7 $s 3000 1 50000000 3 4; done
./orbits 7 127 | awk '$1=="REP"{print $2}' | ./lemma_d2 4 > ld4.txt
python3 orbit_driver5.py 7 7 3000 1 50000000 3 4 ld4.txt     # ~2 min
python3 classify.py 7 orb3_k7_s2_c4.log orb3_k7_s3_c4.log orb3_k7_s4_c4.log   # 6 classes, 10,500 labeled
```

## Independent check (`independent/`, 2026-11-13)

Every k ≥ 7 result above comes from `mu_search*.c` and the `orbits*` programs, so a bug they share would pass every check in the repo. `independent/` re-derives the main results by a method that shares no code with them: a SAT / pseudo-Boolean model with one 0/1 variable per subset of [k], written from the definition of validity. No file there imports `frankl_core.py` except the final `compare_with_core.py`. The verdicts are in [`independent/FINDINGS.md`](independent/FINDINGS.md).

- **Model** (`encode.py`): union-closed, ∅ and [k] present, no singletons, separating, and 2c(e) − n ≤ cap for every e. Symmetry breaking: degrees non-increasing, plus a lex-leader condition for each transposition of equal-degree elements. Its soundness proof is in the module docstring. It is never used when counting labeled solutions.
- **Solvers** (both pip-installable): OR-Tools CP-SAT (`ortools` 9.15.6755) for the decisions and enumerations, and CaDiCaL 1.9.5 through `python-sat` 1.9.dev22 for cross-checks and DRAT proofs (`proof.py`).

```bash
pip install ortools==9.15.6755 python-sat==1.9.dev22
cd independent
python3 selftest.py        # encoding = brute force over all families at k = 3, 4; symmetry breaking meets every orbit
python3 sectionB.py        # k <= 6: decisions and labeled counts 1, 48, 2484, 120 (~1 min)
python3 decide.py 7 3      # k = 7 cap 3: INFEASIBLE (~2 min on 4 cores)
python3 sectionC.py        # k = 7 cap 4: classes and the labeled count 11,340 (~2.3 h on 2 cores)
python3 sectionD.py        # k = 8 cap 4 feasible (M_8)
python3 decide.py 8 3 --limit 43200 --log results/k8_cap3_cpsat.log   # k = 8 cap 3: INFEASIBLE (~4 h on 4 cores)
python3 sectionE.py        # Phase 8 cross-checks (sector, extensions of M_2t, D4/E1 at k <= 5)
python3 compare_with_core.py   # the only script that imports frankl_core
```

Outputs are in `independent/results/`.

## History and license

The search was developed locally and moved to this repository in a single commit, so the git history starts at the finished state.

MIT. See [LICENSE](LICENSE).
