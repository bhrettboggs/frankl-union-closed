# Independent check: findings (2026-11-13)

Everything in this folder was written from the definition of a valid family:
union-closed on [k], ∅ and [k] present, no singleton members, separating (the
k element-membership patterns are distinct). That is the convention of
`frankl_core.is_valid`, which was read once for it and not imported. No file here
imports repo code except `compare_with_core.py`, the final comparison.

**Solvers**, both from pip:
- `ortools` 9.15.6755 (CP-SAT), used for decisions and enumerations;
- `python-sat` 1.9.dev22 with CaDiCaL 1.9.5 (`cadical195`, totalizer cardinality
  encoding), used as a second solver and for DRAT proofs.

The Python version is 3.13.18. Wall times are on a shared 4-core container.

**Model** (`encode.py`): one 0/1 variable x_S per S ⊆ [k], with these constraints:
- union-closure: x_A ∧ x_B → x_{A∪B};
- x_∅ = x_[k] = 1, and x_{{e}} = 0;
- separation: for each pair i < j, a clause saying some set contains exactly one of i, j;
- the cap: Σ_{S∋e} x_S − Σ_{S∌e} x_S ≤ cap for each e.

**Symmetry breaking** (SB): degrees are non-increasing, and for each transposition
(i j) of equal-degree elements the family is lex-≥ its image. The soundness
proof is in the docstring of `encode.py`: the lex-largest of the degree-sorted
relabelings of any family satisfies every constraint. `selftest.py` also checks
it empirically: at k = 4 and k = 5, for every cap, every orbit keeps at least one
member under SB. SB is never on while labeled solutions are being counted.

`selftest.py` checks the model itself. At k = 3 and k = 4, for every cap,
the solution sets of both solvers are identical to brute force over all 2^(2^k)
families.

## Verdicts

| Item | Result | Verdict |
|---|---|---|
| B: infeasible at (3,0), (4,1), (5,2), (6,2) | UNSAT, with both solvers and with SB on and off | VERIFIED |
| B: feasible at (3,1), (4,2), (5,3), (6,3) | SAT; every witness re-checked directly | VERIFIED |
| B: labeled attainers at k = 3..6 | 1, 48, 2,484, 120, in 1, 8, 51, 1 classes; both solvers enumerate the identical set | MATCH |
| C: k = 7, cap 3 | INFEASIBLE (CP-SAT, SB on, 96.8 s, `results/k7_cap3_cpsat.*`) | VERIFIED |
| C: k = 7, cap 4 | feasible; enumeration: 7 classes, 11,340 labeled (orbits 2520, 2520, 2520, 1260, 840, 840, 840; n = 12 in six classes, n = 18 in one). The final no-8th-class solve was INFEASIBLE in 8,328 s on 2 workers (`results/sectionC.txt`, `results/k7_cap4_classes.txt`) | MATCH |
| D: k = 8, cap 4 | M₈ is valid with μ = 4, and the encoding accepts it (both solvers) | VERIFIED |
| D: k = 8, cap 3 | INFEASIBLE (CP-SAT 9.15.6755, SB on, 4 workers, 14,475 s wall; `results/k8_cap3_cpsat.out`, full solver log `results/k8_cap3_cpsat.log`). With M₈ at cap 4 this gives **min μ(8) = 4**, by a route sharing no code with `mu_search*.c`. Caveats: it rests on CP-SAT's correctness and on the SB soundness proof in `encode.py`; there is no proof certificate (CP-SAT logs `LRAT_status: NA`). Re-check: `python3 decide.py 8 3 --log k8.log` (about 4 h on 4 cores), ideally also with a DRAT-producing SAT solver on `python3 encode.py 8 3 --sb` | VERIFIED (no certificate) |
| E(1) sector minimum k − 2, k = 3..7 | UNSAT at cap k−3 and SAT at cap k−2 for every k (k = 7: UNSAT in 36 s) | VERIFIED |
| E(1) k = 6 sector: none at cap 3, 452 families in 14 classes at cap 4 | UNSAT; 452 labeled, 14 classes, the same (n, orbit) table as `results/proof_sector_full.txt` | VERIFIED |
| E(1), also: μ = k−2 sector counts 1, 8, 124 in 1, 4, 9 classes; sector sizes 1, 64, 118,314 (k = 3, 4, 5) | identical, row for row | VERIFIED |
| E(2) extensions of M₄, M₆, M₈ | 58, 1,272, 123,126; min μ 3, 4, 5; μ distributions identical to the repo's | VERIFIED |
| E(2) extremal extensions | 8, 7, 8 classes; the F2 families I(t,j), II(t), B(2..2,3), H_t are exactly the extremal classes at t = 3 and t = 4 | VERIFIED |
| E(2) the seven k = 7 attainer classes are the μ = 4 extensions of M₆ | the 7 classes from Section C equal, as sets of S₇-classes, the 7 μ = 4 extension classes of M₆ (`results/sectionE_E2cmp_E4.txt`) | VERIFIED |
| E(3) D4 and E1 at k = 3, 4, 5 | 4, 304, 235,749 valid families (the repo's counts). D4, E1 and μ ≥ 2k − n have 0 violations. E1 was checked exactly in ℚ(√5). | VERIFIED |
| E, also: the W2 counterexample (SESSION_2026-11-12b §7) | μ(G) = 4, μ(G − 5) = 5 | VERIFIED |
| E, also: D4 is tight on M₆ and on 6 of the 7 k = 7 classes | 3μ = 4k − 4 − n holds on M₆ and on the six n = 12 classes; it fails on the n = 18 class (H₃) | VERIFIED |
| Final comparison with `frankl_core` | 7 classes, 11,340 labeled (orbits 2520, 2520, 2520, 1260, 840, 840, 840; n = 12 in six classes, n = 18 in one). The final no-8th-class solve was INFEASIBLE in 8,328 s on 2 workers (`results/sectionC.txt`, `results/k7_cap4_classes.txt`)MP | 7 classes, 11,340 labeled (orbits 2520, 2520, 2520, 1260, 840, 840, 840; n = 12 in six classes, n = 18 in one). The final no-8th-class solve was INFEASIBLE in 8,328 s on 2 workers (`results/sectionC.txt`, `results/k7_cap4_classes.txt`)MP_V |

No mismatch was found.

## Certificates and how to re-check

- **CP-SAT gives no proof certificate.** An INFEASIBLE verdict from it, such as
  k = 7 cap 3 or k = 8 cap 3, can only be re-checked by re-running it:
  `python3 decide.py K CAP --log FILE`. Each output records the solver
  version, the worker count and the time limit, and CP-SAT's own log is
  saved next to it. To use a solver with a proof trail instead, run
  `python3 encode.py K CAP --sb > f.cnf` and give the file to any DIMACS SAT
  solver that emits DRAT.
- **DRAT proofs** (`proof.py`). This writes the CNF and, on UNSAT, CaDiCaL's DRAT
  proof. The re-check recipe is in its docstring: the CNF's md5 must match
  `encode.py`'s output, then `drat-trim f.cnf f.drat` should print
  `s VERIFIED`.
  - Tested on k = 6 cap 2: UNSAT in 9.3 s, a proof of 599,458 lines (30 MB),
    and the CNF md5 matched.
  - **The proof was not checked in this session.** Running a locally built
    drat-trim was refused by the session's permission classifier, so no DRAT
    check was done here.
  - Proofs were not produced for k = 7 or k = 8. CaDiCaL through python-sat
    keeps the proof in memory and is much slower than CP-SAT on this model:
    about 20 s at k = 6 cap 2, against 0.24 s.

## Claims in docs/PROOF_ATTEMPT.md that these checks contradict

None.

## Claims in docs/PROOF_ATTEMPT.md these checks do not reach

The checks cover only finite computations at the sizes listed above. Not reached:

- **Hand proofs at general k or t:** B1, B2, C1, C2, C3, C4, C5, Lemma E,
  F1 and F2 for t ≥ 5, D1–D5, E1/E2 beyond k ≤ 5, and the conditional
  statements under FC(k).
- **C6** (sector μ ≥ k − 2 for all k) at k ≥ 8, and **F3** (completeness of
  the F2 list) at t ≥ 5.
- **The sum-method material in Section C:** the graph lemmas D₅ and D₆
  (max |F| − p(F) = 3 and max |F| − q(F) = 5), the identities
  a₃ ≥ p(F) and a₄ ≥ q(F), the k = 7 count of 1,044 top-layer
  representatives with its α bounds, the G_W and G_{W',T} tables of C.5,
  and the power construction C4.
- **Statistical and randomized items:** D3's 69.8% figure, and the randomized
  searches `sector_break` and `rung3_break`.
- **The falsified statements (i), (ii), W1 and W3:** their exact counts
  (38 of 51 classes unnamed at k = 5, 6 of 8 at k = 4, 9 of 51 with no valid
  deletion) were not recomputed. Only the W2 counterexample was.
- **The scope check of Section B.3, and the E.2/E.3 range tables.**
- **The repo's own k = 8 sector searches** (the deg-1 sector and the s = 2 orbit
  shards) were not re-run piece by piece; the cap 3 run above covers the whole
  of k = 8 at once. The D5 corollary at k = 8 was not checked.

## Files

- `encode.py`: the model and its CNF and CP-SAT back ends.
- `common.py`: the direct validity and μ check, solve and enumerate
  wrappers, and orbits.
- `families.py`: M₂ₜ, the extension constraints, and the named F2 families.
- `selftest.py`, `sectionB.py`, `sectionC.py`, `sectionD.py`, `sectionE.py`,
  `decide.py`, `proof.py`: the checks and tools listed above.
- `compare_with_core.py`: the only script that imports `frankl_core`.
- `results/`: every output quoted above, with the CP-SAT logs.
