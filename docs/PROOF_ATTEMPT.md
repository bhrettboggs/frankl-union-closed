# Phase 8: proof attempt log

Started 2026-11-12. This file is filled in section by section. It holds
three running logs (delegations, novelty checks, claims attempted) and, at
the end of the phase, the report.

Evidence tags: [PROVED] hand proof, [PROVED-EXH] exhaustive computation with
a certificate in `results/`, [OBSERVED] checked only at the stated k,
[FALSIFIED] killed by a computed counterexample, [CONJECTURE] unproved.

Nothing here proves or verifies Frankl's conjecture.

## 1. Delegation log

"Verified" says what I re-checked myself before the result entered a doc.

| # | Section | Task | Model | Why that model | Verified by me? |
|---|---|---|---|---|---|
| 1 | A | Literature sweep of the entropy method: Gilmer, the four ψ papers, Yu, Cambie, Liu, Jiang, and the barrier. Bound: 12 papers. | Sonnet | Bounded reading task with a precise question list. | **Partly.** I re-opened Chase–Lovett (Thm 1.3, Claim 4.1, Example 1.4), Sawin (Thms 1–2, Examples 4–5, Prop. 6, §2, Question 9) and Jiang (Thm 1.1, Prop. 4.1, Prop. 10.3) and they match. Gilmer, Alweiss–Huang–Sellke, Pebody, Yu, Cambie, Liu and Ellis were not re-opened; they are labelled [helper] in `PROOF_SURVEY.md`. |
| 2 | A | Literature sweep of the lattice formulation, FC-families, small universes, small and large families, Poonen's strict conjectures. Bound: 14 sources. | Sonnet | Same. | **Partly.** I re-opened Bruhn–Schaudt §2, §3.1–3.2, §4, §5, §6.1–6.5, §7–8 (Conj. 1, Thms 3, 16, 17, 21–26, 30, Lemma 18, Conj. 14–15), Tian (Thm 1.1, Lemmas 2.1–2.4, Prop. 2.5, §7), Carvalho–Machiavelo (Thm 4.11, Conj. 5.1–5.2, Thm 5.3 with proof) and Kabela–Polák–Teska (Thms 5–6, Prop. 7, Conj. 1–4). Morris, Pulaj–Wood, Karpas, Eccles and Falgas-Ravry were not re-opened. The helper's inference "Falgas-Ravry is strict when n ≤ 2m − 1" I re-derived from the proof of Bruhn–Schaudt Thm 23 as μ ≥ 2k − n and checked by brute force at k = 3..5. |
| 3 | A | Literature sweep of averaging results and of false strengthenings; why induction and compression fail. Bound: 14 sources. | Sonnet | Same. | **Partly.** Re-opened in Bruhn–Schaudt: Reimer's theorem and its proof outline, the Hungarian family (Thm 26 and proof), Duffus–Sands, the induction paragraph in §4, the compression paragraph in §6.4, Poonen's family A_k. Not re-opened: Balla, Maßberg, Ellis–Ivan–Leader, Cui–Hu, Pulaj–Raymond–Theis. The helper corrected two wrong arXiv identifiers in my brief (1106.0369 is Balla; Ellis–Ivan–Leader is 2201.11484). |
| 4 | A | Open the full text of Poonen (1992) and Abe (2002) and extract the conjectures, the weights theorem and any small-case checks. | Haiku | Mechanical: try a list of URLs and copy stated results. | **Yes, the negative result.** The helper reported that math.mit.edu, sciencedirect.com, doi.org and link.springer.com do not resolve. I had already confirmed with my own request that the session's proxy refuses math.mit.edu and sciencedirect.com (HTTP 403 on CONNECT). Neither paper was opened; nothing is quoted from either. |

No proof step, novelty verdict or choice of claim was delegated.

## 2. Novelty-check log

One entry per specific claim, made before any proof attempt. Verdicts:
KNOWN (cited), PARTLY KNOWN (which part), NOT FOUND (which means only that
I did not find it).

*(No claim has been selected yet. Section A is a survey; the first entries
are made in Section C.)*

Standing notes from the survey that every later check must take into
account:

- "Deleting any set of join-irreducible members keeps union-closure" is
  standard (Bruhn–Schaudt §2; Tian §7; Norton–Sarvate). Any μ-bound obtained
  by deleting co-singletons or other basis sets uses a known device.
- "μ ≥ 2k − n for separating families" is implicit in the proof of
  Bruhn–Schaudt Thm 23 (Falgas-Ravry). It is not new.
- Hu's cloning-plus-co-singleton construction (Bruhn–Schaudt Thm 24) is the
  published relative of M_k and of any "add all co-singletons" reduction.

## 3. Claims attempted

*(Filled in from Section B onward.)*

## 4. Report

*(Written in Section G.)*
