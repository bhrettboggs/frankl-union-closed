# Literature check: is the margin table already known?

Question. For a valid family G on [k] (union-closed, contains ∅ and [k], no singleton members, separating), let

  μ(G) = max_e 2c(e) − |G|.

This repository computes min μ(k) = **1, 2, 3, 3, 4** for k = 3..7, attained by **1, 8, 51, 1, 7** isomorphism classes. Has either sequence, or the underlying question, appeared in the literature?

Search date: 2026-11-12. Every paper listed under "Read" below was opened and its relevant sections read; a search-result snippet alone was never treated as a source. Where only an abstract or a secondary account could be reached, this is stated explicitly.

Evidence tags follow the session ledgers: [PROVED] hand proof, [PROVED-EXH] exhaustive computation with a certificate in `results/`, [OBSERVED] checked only at the stated k, [FALSIFIED] killed by a computed counterexample.

---

## Section A. Direct search

### A.1 What was looked for

Any prior computation, for small universes, of

- the minimum over a class of union-closed families of the top frequency max_e c(e), or of the margin 2·max_e c(e) − |G|, **with the universe size k fixed**, and
- in particular for families that are singleton-free and separating, or
- lists or counts of the families attaining such a minimum.

### A.2 Sources read, and what each computes

| Source | Read | What it computes or proves | Same quantity as min μ(k)? |
|---|---|---|---|
| Bruhn, Schaudt, *The journey of the union-closed sets conjecture*, Graphs Combin. 31 (2015) — [arXiv:1309.3297](https://arxiv.org/abs/1309.3297) | Full text | Survey. Lists verified ranges (universe ≤ 12, ≤ 50 sets), Renaud's sequence φ(n) = min top frequency over families with n sets (1, 1, 2, 2, 3, 4, 4, 4, 5, 6, 7, 7, 8, 8, 8, 8, 9, 10, …), Falgas-Ravry's average-frequency bound for separating families, and Poonen's Conjectures 14 and 15 (see A.3). Reports **no verified cases** of Conjecture 14. | No. No table indexed by universe size; no margin; no singleton-free class. |
| Pulaj, Raymond, Theis, *New conjectures for union-closed families*, Electron. J. Combin. 23(3) (2016) P3.23 — [EJC](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v23i3p23), [arXiv:1512.00083](https://arxiv.org/abs/1512.00083) | Full text | Integer programs (CPLEX) for f(n,a), the most sets in a union-closed family on n elements with every frequency ≤ a, and g(n,m), the minimum top frequency over union-closed families with m sets on n elements. Tables for n ≤ 8 (f up to n = 9), a, m ≤ 16 and beyond in the appendix. | No. Families may contain singletons, need not be separating, need not contain ∅ or [n]. The index is the family size m, not just n; the g(n,·) rows coincide for n ≥ 4 in the printed range, so the universe constraint is essentially inactive there. 2g(n,m) − m is a margin, but over a much larger class, so it is only a (weak) lower bound for ours. |
| Vučković, Živković, *The 12-element case of Frankl's conjecture*, IPSI BgD Trans. Internet Research 13(1) (2017) 65–71 — [record](https://enauka.gov.rs/handle/123456789/228010); algorithm read in Vučković's PhD thesis, Univ. Belgrade (2017) — [PDF](https://fedorabg.bg.ac.rs/fedora/get/o:17784/bdef:Content/download) | Thesis chapter on Frankl (the IPSI article itself was not reachable) | Exhaustive search over weighted hypercube configurations for 33 FC-families, recording minimum "participations" s(G) = w(G) − t(w). Also classifies all families on ≤ 6 elements as FC / Non-FC. Excludes families with 1- or 2-sets. | No. Works with weights and participations, not top frequency; no minima per universe size; no extremal-family counts. |
| Bošnjak, Marković, *The 11-element case of Frankl's conjecture*, Electron. J. Combin. 15 (2008) R88 — [EJC](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v15i1r88) | Full text | Weight-function case analysis for universes of size ≤ 11. | No computed extremal values; singleton-free used only as a standing assumption inside proofs. |
| Poonen, *Union-closed families*, J. Combin. Theory Ser. A 59 (1992) 253–268 — [doi:10.1016/0097-3165(92)90068-6](https://doi.org/10.1016/0097-3165(92)90068-6) | **Not read in full** (publisher page not reachable). Content taken from the Bruhn–Schaudt survey, from Kabela–Polák–Teska, and from Carvalho–Machiavelo, all of which quote it. | Poonen's Theorem (FC characterization by weights); verification for universes ≤ 7 and ≤ 28 sets; Conjectures 14 and 15 (A.3); the family A_k showing a 3-set need not contain an abundant element. | Not as far as the secondary sources report. This is the single largest gap in this check (see Section C). |
| Morris, *FC-families and improved bounds for Frankl's conjecture*, European J. Combin. 27 (2006) 269–282 — [arXiv:math/0702348](https://arxiv.org/abs/math/0702348) | Full text | FC(k,n) values (FC(3,5)=3, FC(4,5)=5, FC(3,6)=4, 7 ≤ FC(4,6) ≤ 8), all proper FC(5)-families, the conjecture for universes ≤ 9. | No. FC-families, not margins. Note the **name clash**: Morris's B(n,3,r) is a family of 3-sets, unrelated to this repository's block families B(…). |
| Falgas-Ravry, *Minimal weight in union-closed families*, Electron. J. Combin. 18 (2011) P95 — [arXiv:1101.2589](https://arxiv.org/abs/1101.2589) | Full text | Separating union-closed families: frequencies in increasing order satisfy d(i) ≥ i − 1, weight ≥ C(n,2) with equality only for the staircase; average degree bounds. | No result on the maximum frequency or on excess over half. |
| Maßberg, *The union-closed sets conjecture for small families*, Graphs Combin. 32 (2016) — [arXiv:1508.05718](https://arxiv.org/abs/1508.05718) | Full text | Conjecture holds for separating families with \|A\| ≤ 2(m + m/(log₂m − log₂log₂m)), m = universe size. | No. "≥ half", not a margin. |
| Kabela, Polák, Teska, *The number of abundant elements in union-closed families without small sets* — [arXiv:2212.09279](https://arxiv.org/abs/2212.09279) | Full text | Families without small sets (∅ excluded); counts of elements in **strictly more** than half the sets; explicit constructions with few abundant elements. Shows Cui–Hu's k = 2 conjecture sits between Frankl's and Poonen's. | Closest in spirit (strict abundance, no small sets) but no margin minimization and no exhaustive search. |
| Carvalho, Machiavelo, *On supratopologies, normalized families and Frankl conjecture* (2024) — [arXiv:2408.11213](https://arxiv.org/abs/2408.11213) | Full text | Normalized families; Theorem 5.3: Poonen's strict conjecture is equivalent to "exactly half ⇒ power set". | No computations, no margin bounds. |
| Tian, *Frankl's union-closed sets conjecture: height four and structural reductions at height five* (2026) — [arXiv:2608.25147](https://arxiv.org/abs/2608.25147) | Full text | Proves strict majority for families of nonempty sets of height ≤ 4; uses a deficit δ_a = t − f(a) for \|F\| = 2t (a sign-flipped half-margin). | Uses a margin-type quantity but never minimizes it over a class; no tables. |
| Jiang, *Entropy bounds and global couplings for union-closed families* (2026) — [arXiv:2609.08291](https://arxiv.org/abs/2609.08291) | Abstract and main theorem | Constant 0.38288525. | Not relevant to small-universe margins. |
| Chen, van der Holst, Kostochka, Li, *Extremal union-closed set families*, Graphs Combin. 35 (2019) 1495–1502 — [PDF](https://par.nsf.gov/servlets/purl/10156762) | Full text | Normal (maximum universe) and irreducible (minimum universe) representatives of a union-closed lattice. | No frequencies. Relevant to Section B. |
| Renaud, *Is the union-closed sets conjecture the best possible?*, J. Austral. Math. Soc. A 51 (1991) 276–283 — [Cambridge](https://doi.org/10.1017/S1446788700034236) | Full text (open PDF) | φ(n), the minimum top frequency over union-closed collections of n nonempty sets, tabulated for n ≤ 17, and Conjecture 1B: some element lies in at least ⌊n/2⌋ + 1 sets, checked to n = 19. | No. Indexed by family size; ∅ excluded; singletons allowed; universe not fixed. With ∅ added back, Conjecture 1B says μ ≥ 1 only when the number of nonempty sets is even, so it is weaker than Poonen's Conjecture 14 on our class. |
| Cui, Hu, *Two stronger versions of the union-closed sets conjecture* — [arXiv:1711.04276](https://arxiv.org/abs/1711.04276) | Full text | S1/S2-Frankl: if the smallest set has size k ≥ 2, at least k (resp. 2) elements lie in at least half the sets. S1 proved for universes ≤ 5 by hand, refuted at universe 9. Hu–Li continue the 6-element case ([arXiv:1809.03836](https://arxiv.org/abs/1809.03836), abstract only). | No. Counts abundant elements with a non-strict threshold; no margin; no computer search. |

Papers citing the five named starting points were found through these papers' reference lists and through keyword search. A citation-graph service (Semantic Scholar) could not be reached from this environment, so the citing-paper sweep is **not exhaustive**.

### A.3 The closest prior statement: Poonen's strict conjecture

Bruhn–Schaudt record two conjectures of Poonen (1992) for separating union-closed families A:

- **Conjecture 14.** Unless A is a power set, some element lies in **strictly more** than half the member-sets.
- **Conjecture 15.** If A has a unique abundant element a, then A = {∅} ∪ {B + a : B ⊆ U − a}.

Every valid family in this repository is separating and, having no singletons, is not a power set. So Conjecture 14 predicts **μ(G) ≥ 1 for every valid G**, i.e. min μ(k) ≥ 1 for all k. The repository's table therefore contains, as its weakest content, a check of Conjecture 14 on the valid class:

- [PROVED-EXH] min μ(k) ≥ 1 for k = 3..7 on valid families (the table values 1, 2, 3, 3, 4 are all ≥ 1). This covers only the valid class, not all separating families on ≤ 7 points (families with singleton members are excluded).
- k = 3 is tight for Conjecture 14: {∅, {0,1}, {0,2}, {1,2}, [3]} has μ = 1.

Bruhn–Schaudt state no verified cases of Conjecture 14. The secondary sources do not say whether Poonen checked it for small universes himself; this could not be confirmed without the full text of Poonen (1992).

### A.4 OEIS

- The OEIS search page refuses automated access (robots), so a direct search of the two sequences could not be run from here. Web searches for the string "1, 8, 51, 1, 7" returned no OEIS hit. The sequence 1, 2, 3, 3, 4 is too short and generic for a search to be informative either way.
- **To do by hand (one minute):** <https://oeis.org/search?q=1%2C8%2C51%2C1%2C7> and <https://oeis.org/search?q=1%2C2%2C3%2C3%2C4+union>.
- Counts of union-closed families by universe size, entries opened and read: [A102894](https://oeis.org/A102894) (labeled, containing ∅ and the universe), [A108798](https://oeis.org/A108798) (unlabeled, same), [A102896](https://oeis.org/A102896), [A193674](https://oeis.org/A193674), [A299116](https://oeis.org/A299116) ("sparse" families, average nonempty set size ≤ n/2; 0, 0, 0, 2, 27, 3133, 5777931). The counts come from Brinkmann and Deklerck, *Generation of union-closed sets and Moore families*, J. Integer Seq. 21 (2018) 18.1.7 ([arXiv:1701.03751](https://arxiv.org/abs/1701.03751)). None of these entries restricts to separating or singleton-free families, and none mentions frequencies or margins.
- For reference, the number of isomorphism classes of **valid** families is 2, 29, 2741 for k = 3, 4, 5 [OBSERVED: counted with `enum_uc_leaves` + `is_valid` + `canon` on 2026-11-12; no certificate in `results/`]. A web search for "2, 29, 2741" found no match.

### A.5 Section A finding

No source read computes min μ(k), or the minimum top frequency, for valid (singleton-free, separating) families at fixed universe size, and none lists or counts the attaining families. The nearest items are (i) Pulaj–Raymond–Theis's g(n,m), a different minimization over a much larger class, and (ii) Poonen's Conjecture 14, which predicts only the lower bound μ ≥ 1. The verdict and its confidence are in Section C.

---

## Section B. Equivalent formulations

*(pending)*

---

## Section C. Verdict

*(pending)*
