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
| 5 | B | Referee the complete proofs of Propositions B1 and B2 (no reasoning supplied) and find the flaw; brute force allowed. | Sonnet | The rule asks for a different model from the one that wrote the proof; the task is a bounded check of two short proofs. | **Yes.** No flaw found in either. The referee asked for the k = 0 convention to be stated explicitly, which is now done in B1(i). Its own script (all separating union-closed families on at most 4 points) agrees with `proof/scope_check.py`. Its remarks on the literature were from memory and are not used. |
| 6 | C | Referee the complete proofs of C1, C2 (with the k = 5 and k = 6 computations), C5 and C4, and recompute every number by its own brute force. | Sonnet | Different model from the author of the proofs; bounded check with explicit numbers. | **Yes.** No flaw found. Its independent scripts reproduced max(\|F\| − q₃) = 3 on 5 vertices, max(\|F\| − q₄) = 5 on 6 vertices, the 118,314 sector families at k = 5 with min Σg = 12, the G_W values for k = 5..9 and U(10) = 32, U(11) = −201. It checked C4 by hand only. It noted that N(G) can be negative, which the text now says. |
| 7 | F | Referee the complete proofs of Lemma E, Theorem F1 and Proposition F2; test each numbered step of F1 by brute force on all pairs (G₀, G₁) for M₄ and M₆. | Sonnet | Different model from the author; the proof has many cases and explicit counts, which a bounded brute-force check can test step by step. | **Yes.** No flaw found. Its own enumeration gave 62 and 1,278 pairs and 58 and 1,272 valid extensions for t = 2, 3, the same as `proof/extensions.py`. It confirmed that the only pairs satisfying the proof's hypotheses (α) and (β) are the non-separating ones the proof identifies (4 and 6 pairs). It did not run t = 4; `proof/extensions.py` does. It asked for the validity argument in F2 to be written out, which is done. |
| 8 | D | Referee the complete proofs of D1, D2 and D3, and test them by brute force. | Sonnet | Different model from the author; short proofs with parity bookkeeping, which is where slips happen. | **Yes.** No flaw found. Its script tested D2 for every J and D3(a), (b) on all 4, 304 and 235,749 valid families at k = 3, 4, 5. It pointed out that D3(c) is vacuous on these sizes (no family has μ ≤ 0), so (c) rests on the proof alone; and that D1's last sentence needs the base case k = 3, now stated. It completed the "Z join-irreducible ⇒ degree-1" step from Lemma C, as now written. |
| 9 | D | Referee the complete proofs of Lemma S and Proposition D4; test every numbered claim by brute force. | Sonnet | Same reason; the proof is an adaptation of a published argument, so a step-by-step check against data is the main safeguard. | **Yes.** No flaw found. Its script tested (S1)–(S4), both cases of D4 and the corollary on all valid families at k = 3, 4, 5 and every tie-breaking order, with 0 violations. (S5) was exhaustive only for subfamilies of at most 10 members and sampled otherwise. `proof/poonen.py` part 5 repeats the check of D4 and of the step c(a) ≥ φ + k − 1. |
| 10 | E | Referee the complete proof of Proposition E1 and Corollaries E2, E3 (Lemma S taken as given, since it was refereed in delegation 9); answer three pointed questions about the use of the cited constant-fraction theorem. | Sonnet | Different model from the author; a short proof whose risk is misuse of a cited theorem's hypotheses. | **Yes.** No flaw found. It confirmed that the cited theorem needs only "union-closed with a non-empty member", so applying it to the sub-family B is legitimate, and that the strict inequality in E2 is exactly what is needed. Its script covered k = 3, 4 only; `proof/growth.py` covers k = 3, 4, 5. |

No proof step, novelty verdict or choice of claim was delegated.

## 2. Novelty-check log

One entry per specific claim, made before any proof attempt. Verdicts:
KNOWN (cited), PARTLY KNOWN (which part), NOT FOUND (which means only that
I did not find it).

| # | Claim | Queries and sources | Verdict |
|---|---|---|---|
| N1 | B1: Frankl's conjecture is equivalent to μ ≥ 0 on valid families. | Bruhn–Schaudt §2 (separating; ∅) and §4 (singleton), re-read; Tian Lemma 2.1 (twin deletion); Kabela–Polák–Teska Prop. 10(3)–(4). | **KNOWN.** Each step is a standard reduction. Only the packaging as "valid" is this repository's. |
| N2 | B2: Poonen's strict conjecture for all separating families is equivalent to μ ≥ 1 on valid families. | Web search "Poonen conjecture union-closed strictly more than half separating reduce to families without singletons equivalent"; Bruhn–Schaudt §4; Carvalho–Machiavelo §5 (Thm 5.3 is a different equivalence, via normalized families); Kabela–Polák–Teska Props 7, 9, 10 (the ∅-free step is their Prop. 10(4) pattern). | **PARTLY KNOWN.** The ∅-free case and the singleton injection are standard. The induction that peels a singleton in the bijective case, and the resulting equivalence, were NOT FOUND. It is elementary and could well be folklore or in Poonen (1992), which is unread. |
| N3 | C1–C3: the sum identity at general k, and the k = 5, 6 analogues of Lemma D. | `PROOF_SURVEY.md` §2.3 (Poonen's weights theorem; Morris's use of Σ(2\|A∩[k]\| − k)), re-read. No new search: this is the repository's own Lemma D at other k. | **Method KNOWN** (weighted averaging). The specific inequalities at k = 5, 6 were NOT FOUND and are routine. |
| N4 | C2: a set W whose induced 2-set graph has no isolated vertex is a member. | Bruhn–Schaudt §6.5 (families generated by 2-sets: Imrich–Sauer–Woess; Leck–Roberts–Simpson), re-read. | **KNOWN** device (union-closure of a graph). |
| N5 | C4: Frankl's conjecture holds iff it holds for valid families containing all co-singletons. Lattice form: iff it holds for atomistic lattices (dually, coatomistic). | Web search "Frankl conjecture union-closed atomistic lattices sufficient reduction"; paper search "reduces to atomistic lattices / families containing all complements of singletons"; opened Bouchard, [arXiv:2503.00277](https://arxiv.org/abs/2503.00277) (minimal counterexample in the lattice form: no such reduction) and Marigo–Schipani, [arXiv:1603.01215](https://arxiv.org/abs/1603.01215) ("reduced families": a different condition); Bruhn–Schaudt Thm 24 (Hu's cloning plus sets U′ − x); Wang, [arXiv:2609.25101](https://arxiv.org/abs/2609.25101), footnote 1 (Cartesian powers). | **PARTLY KNOWN.** Both ingredients are published: padding with co-singletons (Hu) and amplification by powers (Polymath11 discussion, as used by Wang). The statement itself was NOT FOUND. I rate it about 50% likely to be folklore. |
| N6 | C6: every valid family containing all co-singletons has μ ≥ k − 2. | Same searches as N5; `docs/LITERATURE.md` A.2 sources. | **NOT FOUND.** By C4 it is at least as strong as Frankl's conjecture, so it is recorded as a question, not attempted. |
| N7 | F1, F2: every valid one-element extension of M₂ₜ has μ ≥ t + 1; the families I(t,j), II(t). | Web search "union-closed family one-element extension adding a new element up-set frequency margin separating co-singletons doubled power set extremal"; `docs/LITERATURE.md` B.6 (M_k, B(…), H_t not found under any name); Bruhn–Schaudt §6.4 (Lo Faro's restricted up-compression, the nearest published "add an element to some members" operation). | **NOT FOUND.** Unsurprising: M_k itself was not found in the literature. The decomposition of Lemma E (members with and without x) is the standard A_x / A_x̄ splitting. |
| N8 | Deletion statements W1–W3 about μ(G) versus μ(G − x). | Bruhn–Schaudt §4 (induction paragraph), Tian Prop. 6.2 and Problem 6.4 (projection along a critical coordinate in a minimal counterexample), re-read. | **PARTLY KNOWN in spirit.** That deleting an element does not behave monotonically is the standard reason induction fails; Tian's projection formula is Lemma E read backwards. The specific statements and counterexamples were NOT FOUND. |
| N9 | D2, D3: deleting join-irreducible members plus parity; consequences of Frankl's conjecture for a valid family with μ = 0. | Norton–Sarvate via Bruhn–Schaudt §7; Tian Lemma 2.2 and Prop. 7.2 (critical join-cover number ≥ 3); Bouchard Thm 1.4, Lemma 2.5, Thm 2.6; all re-read. | **KNOWN device**, used in every minimal-counterexample paper. Those papers apply it to a smallest counterexample to Frankl's conjecture. Its use for families at margin 0 under the hypothesis that Frankl's conjecture holds was NOT FOUND, and is a routine transfer. |
| N10 | D4: 3μ ≥ 4k − 4 − n for valid families, given Frankl's conjecture on k − 1 points. | Bruhn–Schaudt Lemma 18 and Thms 22–24 (Lo Faro; Roberts–Simpson; Falgas-Ravry; Hu); Tian Lemma 2.4 and Prop. 2.5 (the staircase argument, with proof), re-read. Hu, Discrete Math. 346 (2023) 113430 was **not opened**. | **PARTLY KNOWN.** The argument is Hu's staircase as reproduced by Tian; at μ = −1 the inequality is exactly the Lo Faro bound n ≥ 4k − 1. The statement for general μ, and its tightness on the small minimisers, were NOT FOUND. Hu's paper may contain it; I rate that about 35% likely. |
| N11 | E1, E2: (1+κ)μ ≥ 2k − 2 − (1−κ)n; in particular every separating family with fewer than (1+√5)(k−1) members has an element in strictly more than half. | Web search "union-closed sets conjecture holds for separating families with at most c·m sets small families after Gilmer constant improvement of Maßberg bound"; Cambie's 2023 survey [arXiv:2306.12351](https://arxiv.org/abs/2306.12351) read in full (no small-family result); Bruhn–Schaudt Thms 23–24 (2m; Hu's converse); Maßberg's bound via the Section A sweep. Hu (2023) not opened. | **NOT FOUND.** The two ingredients are published (the staircase argument; the constant-fraction theorem). Their combination is a short step, so I rate it about 50% likely that it appears somewhere, most plausibly in Hu (2023) or a 2023–2026 preprint. If new, it improves the range "n ≤ 2k(1 + o(1))" of Falgas-Ravry and Maßberg to n < 3.236(k − 1) for large k. |

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

### Section B. Scope: does restricting to valid families lose generality?

**Short answer.** No, for both conjectures that matter here. Frankl's
conjecture is equivalent to μ ≥ 0 on valid families (B1, standard), and
Poonen's strict conjecture is equivalent to μ ≥ 1 on valid families (B2).
The restriction **does** matter for everything quantitative: min μ(k), the
attainer lists and rungs 2–3 are statements about the valid class only, and
B.3 says what they do not imply.

Notation. For a finite family F of distinct finite sets, U(F) is the union
of its members, n = |F|, c_F(e) the number of members containing e,
g_F(e) = 2c_F(e) − n and μ(F) = max_{e ∈ U(F)} g_F(e). "Valid" is as in
`docs/THEORY.md` A.3: union-closed, ∅ ∈ G, U(G) ∈ G, no member of size 1,
separating.

- **FC** (Frankl): every union-closed F ≠ {∅} has μ(F) ≥ 0.
- **PC** (Poonen's Conjecture 14, in the wording of Bruhn–Schaudt): every
  separating union-closed F ≠ {∅} with F ≠ 2^{U(F)} has μ(F) ≥ 1.
- **R0**: every valid G has μ(G) ≥ 0.  **R1** (rung 1): every valid G has
  μ(G) ≥ 1.

#### B.1 Proposition B1 [PROVED; KNOWN, standard reductions]

(i) Valid families exist only on universes of size k ≥ 3. (ii) FC ⇔ R0.

*Proof.* (i) For k = 0 the definition admits only G = {∅}, where μ is
undefined; **by convention this family is not valid**, so R0 and R1
quantify over k ≥ 1. For k = 1, Z = {x} is a member of size 1. For k = 2,
separating x from y needs a member containing exactly one of them; it is
neither ∅ nor Z, so it has size 1. For k = 3, {∅, 01, 02, 12, 012} is valid.

(ii) FC ⇒ R0 is immediate. For R0 ⇒ FC let F be union-closed, F ≠ {∅}.

1. *Add ∅.* F₁ = F ∪ {∅} is union-closed, c is unchanged and |F₁| ≥ |F|, so
   μ(F) ≥ μ(F₁).
2. *Merge twins.* Call x, y twins if they lie in exactly the same members;
   this is an equivalence relation on U(F₁). Pick one representative per
   class, let K be the set of representatives and F₂ = {A ∩ K : A ∈ F₁}.
   Every member of F₁ is a union of twin classes, so A ↦ A ∩ K is injective.
   It commutes with union. Hence F₂ is union-closed, |F₂| = |F₁|, ∅ ∈ F₂,
   and c is unchanged on K. Every element has the frequency of its
   representative, so μ(F₂) = μ(F₁). Distinct representatives are not twins,
   so F₂ is separating with U(F₂) = K, and K ≠ ∅ because F has a non-empty
   member.
3. *Top.* K is the union of all members of F₂, hence a member.
4. *Singletons.* If {x} ∈ F₂, then A ↦ A ∪ {x} injects the members avoiding
   x into those containing x, so g(x) ≥ 0. Otherwise F₂ is valid on K and R0
   applies.

In both cases μ(F) ≥ μ(F₁) = μ(F₂) ≥ 0. ∎

Sources for the steps: Bruhn–Schaudt §2 (steps 1–2, "it suffices to prove
the conjecture for separating families"; "we may always assume a
union-closed family to include the empty set") and §4 (step 4,
Sarvate–Renaud). The reduction never enlarges the universe, so **FC for
universes of size ≤ k is equivalent to min μ(j) ≥ 0 for all 3 ≤ j ≤ k.**

#### B.2 Proposition B2 [PROVED; PARTLY KNOWN, see N2]

PC ⇔ R1.

*Proof.* PC ⇒ R1: a valid G is separating, union-closed and ≠ {∅}, and it
is not a power set, because 2^Z has members of size 1.

R1 ⇒ PC. Assume R1. Then R0 holds, hence FC by B1. Let F be separating,
union-closed, F ≠ {∅}, F ≠ 2^{U}, U = U(F). Induct on |U| ≥ 1.

- *Case A: ∅ ∉ F.* F ∪ {∅} is union-closed and ≠ {∅}; FC gives e with
  2c(e) ≥ n + 1 > n. So μ(F) ≥ 1.
- *Case B: ∅ ∈ F, no member of size 1.* U ∈ F, so F is valid and R1 applies.
- *Case C: ∅ ∈ F and {x} ∈ F.* Let N be the members avoiding x and P those
  containing x. j : N → P, A ↦ A ∪ {x} is injective. If j is not onto,
  |P| > |N| and g(x) ≥ 1. If j is a bijection, then F = N ∪ {A ∪ {x} : A ∈
  N}, so n = 2|N|, g_F(x) = 0 and g_F(e) = 2g_N(e) for e ≠ x. Here N is
  union-closed, contains ∅, has U(N) = U ∖ {x} and is separating (a member
  of F splitting y, z ≠ x is A or A ∪ {x} with A ∈ N, and A splits them
  too). N ≠ {∅}, since otherwise F = {∅, {x}} is a power set; and N is not a
  power set, since otherwise F = 2^U. By induction μ(N) ≥ 1, so μ(F) ≥ 2.

Base |U| = 1: F is {{x}} (Case A) or {∅, {x}} (a power set, excluded). ∎

So μ(F) = max(0, 2μ(N)) in the bijective sub-case, which is the only place
where a separating family with ∅ can fail to be valid and still need an
argument.

#### B.3 Checks, and the attempt to break B1 and B2

- `proof/scope_check.py 4` tests every union-closed family on at most 4
  points (2, 12, 120 and 4,958 families for k = 1..4): the reduction of B1
  ends at a singleton or at a family accepted by `frankl_core.is_valid` with
  k′ ≥ 3, with the stated counts; Case A's equivalence and Case C's identity
  μ(F) = max(0, 2μ(N)) hold in all 2,078 and 152 instances; and PC itself
  holds on all 4,152 separating non-power-set families on exactly 1..4
  points. **[OBSERVED, universes ≤ 4]**: no certificate file, and a universe
  of 4 points is far too small to test anything except the bookkeeping.
- Best argument that B2 is false: a separating family with a singleton
  might have every other element pinned at exactly half through a mechanism
  that valid families do not see. Case C answers this: equality at x forces
  the product structure F = N ⊎ {∅, {x}}, and then the other elements carry
  exactly twice their margin in N. I found no way around it.
- Independent referee (delegation 5): no flaw in either proof.

#### B.4 What later results would and would not imply

| If this were proved | It would imply | It would not imply |
|---|---|---|
| R1 for all k (rung 1, Section D) | PC in full (B2) and FC (B1). **Rung 1 is exactly Poonen's strict conjecture, and is at least as strong as Frankl's.** | Anything about how large μ is. |
| min μ(k) ≥ f(k) → ∞ (rung 2, Section E) | FC for all universes of size ≥ k₀ where f ≥ 0, hence FC, since universes ≤ 12 are known. PC likewise if f ≥ 1 eventually and small k are checked. | A bound on the excess for families with singleton members or without ∅ (for those μ can be 0 or 1 at every k: power sets, staircases). |
| min μ(k) = ⌈k/2⌉ (rung 3) | All of the above. | The same caveat. |
| R1 for k ≤ K only | PC for universes ≤ K **provided** FC is known there (it is, for K ≤ 12): the induction in B2 only passes to smaller universes. With the table, PC holds for universes ≤ 7 **[PROVED-EXH for the valid part, k = 3..7; the reduction is B2]**. | Anything for larger universes. |
| A bound on a sector (Section C) or a structure theorem for minimisers (Section F) | Statements about valid families in that sector or about minimisers only. | FC or PC, unless a separate reduction shows the sector is general. Section C must check this for the all-co-singleton sector. |
| FC (if someone else proves it) | R0. | R1: "FC ⇒ PC" is not known (Carvalho–Machiavelo Thm 5.3 goes the other way). Whether FC implies rung 1 is itself a question for Section D. |

Three further limits on every later claim:

1. μ is not a lattice invariant (`docs/LITERATURE.md` Proposition L), so no
   result here transfers to the lattice form beyond μ ≥ λ.
2. The table min μ(k) = 1, 2, 3, 3, 4 belongs to the valid class. Dropping
   "no singletons" or "∅ ∈ G" changes the minimum: for separating families
   with singletons it is 0 at every k (power sets) and, excluding power
   sets, PC predicts ≥ 1 with equality for staircases.
3. The line "PC holds for universes ≤ 7" is new to this repository only as
   a consequence of the table plus B2. Whether Poonen (1992) already
   contains it is unknown, because that paper is unread.

### Section C. The all-co-singleton sector at general k

**Short answer.** The sum method of Lemma D generalises as an identity, and
it reproduces the true minimum at k = 5 and comes within 1 of it at k = 6.
It does **not** extend to a theorem for general k. Two things are proved
instead: the method gives no information for any top layer once k ≥ 11
(C5), and no method can give a uniform bound μ ≥ 0 on this sector without
proving Frankl's conjecture (C4). The data suggest the sharp statement
μ ≥ k − 2 (C6), which is left as a question.

Setting. The **sector** at level k ≥ 3 is the class of valid families on
[k] that contain all k co-singletons, S(G) = [k]. For G in the sector,
R(G) is the set of members of size 2..k−2, a_j the number of members of
size j, T(G) the members of size k−2 (the top layer, t = |T|), and

  N(G) = Σ_{A ∈ R(G)} (k − 2|A|).

N(G) can be negative: sets larger than k/2 count negatively.

Certificates: `results/proof_sector_full.txt` is the output of
`proof/sector_full.py` (deterministic, about 10 s with the `mu_search2`
binary). `results/proof_sector_break.txt` is the output of the randomised
search `proof/sector_break.py`.

#### C.1 The sum identity at general k [PROVED]

**Lemma C1.** For G in the sector, Σ_e g(e) = k(k−2) − N(G). Hence
μ(G) ≥ ⌈(k(k−2) − N(G))/k⌉.

*Proof.* Σ_e g(e) = Σ_{A∈G} (2|A| − k). ∅ gives −k, Z gives +k, each of the
k co-singletons gives k − 2, and the members of size 2..k−2 give −N(G). The
maximum is at least the average, and μ is an integer. ∎

For k = 7 this is `docs/THEORY.md` Lemma C.2: N = 3a₂ + a₃ − a₄ − 3t. The
identity was checked on every sector family at k = 3, 4, 5 (1, 64 and
118,314 families) and on the 452 families found at k = 6.

#### C.2 Forcing, and the cases k = 5 and k = 6 [PROVED-EXH]

**Lemma C2 [PROVED; KNOWN device, N4].** Let G be union-closed and F the
graph whose edges are the 2-element members of G. If F[W] has a vertex and
no isolated vertex, then W ∈ G. So for G in the sector and 3 ≤ j ≤ k−2,
a_j ≥ q_j(F), the number of j-sets W with F[W] free of isolated vertices.

*Proof.* W is the union of the edges of F inside W. ∎

At k = 7, `docs/THEORY.md` C.3 uses only the special case "two disjoint
edges" (a perfect matching of a 4-set).

**k = 5.** N = a₂ − a₃. By C2, a₃ ≥ q₃(F), so N ≤ |F| − q₃(F). Over all
2¹⁰ graphs on 5 vertices the maximum of |F| − q₃(F) is 3 (10 labeled
graphs: a triangle plus a disjoint edge). So Σ_e g(e) ≥ 12 and

> **Lemma D₅ [PROVED-EXH].** Every valid family on [5] with all five
> co-singletons has μ ≥ ⌈12/5⌉ = 3.

Brute force over all 118,314 sector families: no violation of a₃ ≥ q₃(F) or
of a₂ − a₃ ≤ 3; min Σ_e g(e) = 12 and min μ = 3. **The method is exact at
k = 5.**

**k = 6.** N = 2a₂ − 2a₄ (3-sets have weight 0). By C2, a₄ ≥ q₄(F). Over
all 2¹⁵ graphs on 6 vertices the maximum of |F| − q₄(F) is 5 (21 labeled
graphs). So Σ_e g(e) ≥ 14 and

> **Lemma D₆ [PROVED-EXH].** Every valid family on [6] with all six
> co-singletons has μ ≥ ⌈14/6⌉ = 3.

The true minimum is 4: `mu_search2 6 3 6 1` finds 0 families (7,051,581
nodes) and `mu_search2 6 4 6 1` finds 452, in 14 classes, all with μ = 4.
**The method loses 1 at k = 6.** The loss is intrinsic to averaging: a
triangle of 2-sets has N = 6 − 0, but its three vertices have g well above
the average.

**k = 7.** Lemma D's ingredients, used without a cap, give
Σ_e g(e) ≥ 5 + 3t − α(T). Read off the existing certificate
`results/lemma_d2_k7_s7_cap4.txt`, this is positive for 1,042 of the 1,044
top-layer representatives and is ≤ 0 for two (T = ∅ with α = 5, and one
T with t = 1, α = 10). So already at k = 7 the sum method cannot prove
μ ≥ 1 for every top layer.

#### C.3 What the method gives at general k

**Proposition C3 [PROVED, immediate from C1].** For a set T of
(k−2)-subsets of [k] let ν_k(T) be the maximum of N(G) over sector families
with top layer T. Then every such G has

  μ(G) ≥ ⌈(k(k−2) − ν_k(T))/k⌉,

and a top layer T is *covered at cap c* (no sector family with top layer T
has μ ≤ c) whenever ν_k(T) < k(k−2) − kc.

This is the exact general form of Lemma D. Everything depends on bounding
ν_k(T) from above. Known values and bounds:

| k | bound on ν_k(T) | source | consequence |
|---|---|---|---|
| 5 | ν ≤ 3 for all T | C.2, exact | μ ≥ 3 = k − 2 |
| 6 | ν ≤ 10 for all T | C.2 | μ ≥ 3 = k − 3 |
| 7 | ν ≤ 30 + α(T) − 3t | `docs/THEORY.md` C.3–C.4 | Lemma D and D′ |

For k ≥ 8 the two forcing rules of Lemma D lose their force, for the reason
the 2026-11-09 ledger gave: 4-sets no longer have positive weight. The
natural replacements are C2 in full (all j), and the conflict rule "two
members whose union is a (k−2)-set outside T cannot both be present". I did
not derive a usable bound from them, and C5 shows why none can work for
large k.

#### C.4 The sector is as hard as the whole conjecture [PROVED; PARTLY KNOWN, N5]

**Proposition C4.** Frankl's conjecture holds if and only if every family in
the sector, for every k ≥ 3, has μ ≥ 0.

*Proof.* "Only if" is trivial. Suppose FC fails. By B1 there is a valid F on
some [k] with n members and μ(F) ≤ −1. For r ≥ 1 let F^r be the family on r
disjoint copies of [k] whose members are the sets A₁ ⊔ … ⊔ A_r with
A_i ∈ F. It is union-closed, has n^r members, contains ∅ and its universe
Z_r, and has no member of size 1. An element e in one copy lies in
c_F(e)·n^{r−1} members, so g_{F^r}(e) = g_F(e)·n^{r−1} ≤ −n^{r−1}.

Let G = F^r ∪ {all co-singletons of Z_r}. A co-singleton united with any
set is itself or Z_r, so G is union-closed. It has no member of size 1, and
it is separating because x is the only element missing from Z_r ∖ {x}. So G
is in the sector on K = rk elements. At most K sets were added and each
changes g(e) by ±1, so g_G(e) ≤ rk − n^{r−1}. Since n ≥ 2, this is negative
for large r. ∎

Checked numerically on U2[3], M₄ and B(2,3) with r = 1, 2, 3: the formula
g_G(e) = g_F(e)·n^{r−1} + (added co-singletons containing e) − (added ones
avoiding e) holds exactly (`proof/sector_full.py`, part G).

Remarks.

1. The same proof works if, besides the co-singletons, one adds any
   polynomially many prescribed sets that keep union-closure, for example
   all (k−2)-sets. So **"dense top layer" sub-sectors are also as hard as
   the whole conjecture.**
2. Lattice form: a union-closed family containing all co-singletons
   corresponds, after complementing, to an intersection-closed family
   containing all singletons, i.e. to an atomistic lattice with the elements
   as atoms. So C4 says that Frankl's conjecture is equivalent to its
   restriction to atomistic lattices, with the rare join-irreducible
   required to be an atom.
3. Consequence for this section: **no argument can prove μ ≥ 0 on the
   whole sector for all k without proving Frankl's conjecture.** Lemma D's
   partial coverage at k = 7 (578 of 1,044 representatives at cap 3) is
   therefore the kind of result one should expect, not a defect of the
   method.

#### C.5 The sum method is vacuous for k ≥ 11 [PROVED]

**Proposition C5.**

(a) For k ≥ 5 let W = {0, …, k−3} and G_W = {∅, Z} ∪ {co-singletons} ∪
{A ⊆ W : |A| ≥ 2}. Then G_W is in the sector, N(G_W) = 2^{k−1} − k −
(k−2)², μ(G_W) = 2k − 5, and Σ_e g(e) < 0 for every k ≥ 8.

(b) For k ≥ 7 let W′ = {0, …, k−4} and let T be any set of (k−2)-subsets.
Then G_{W′,T} = {∅, Z} ∪ {co-singletons} ∪ T ∪ {A ⊆ W′ : |A| ≥ 2} is in
the sector, has top layer exactly T, and

  N(G_{W′,T}) = 3·2^{k−3} − k − (k−2)(k−3) − (k−4)t.

Hence ν_k(T) ≥ 3·2^{k−3} − k − (k−2)(k−3) − (k−4)·C(k,2) for every T, and
k(k−2) − ν_k(T) ≤ U(k), where U(10) = 32 and U(k) < 0 for all k ≥ 11
(U(11) = −201).

*Proof.* (a) Subsets of W are closed under union, and a co-singleton united
with anything is itself or Z. There are no singletons, and the
co-singletons separate. With w = k − 2, N = Σ_{j=2}^{w} C(w,j)(k − 2j) =
k(2^w − 1 − w) − 2(w2^{w−1} − w) = 2^{k−1} − k − (k−2)². For e ∈ W the
sets ∅, Z and the co-singletons contribute k − 2 to g(e), and e lies in
2^{w−1} − 1 of the 2^w − 1 − w subsets, which adds w − 1. So g(e) = 2k − 5;
for e ∉ W it is smaller. Finally N(G_W) > k(k−2) is the inequality
2^{k−1} > 2k² − 5k + 4, which holds at k = 8 (128 > 92) and then for all
larger k by induction, since the left side doubles and the right side
grows by 4k − 3 < 2k² − 5k + 4.

(b) Two distinct (k−2)-sets have a union of size ≥ k−1. A (k−2)-set united
with a subset of W′ is that set or has size ≥ k−1. Subsets of W′ have size
≤ k−3, so the top layer is exactly T. The W′ part contributes
Σ_{j=2}^{k−3} C(k−3,j)(k − 2j) = 3·2^{k−3} − k − (k−2)(k−3), and each
member of T contributes −(k−4). The sum Σ_e g(e) increases with t, so
t = C(k,2) is the best case. ∎

So **for k ≥ 11, for every top layer T, there is a sector family with that
top layer whose average of g is negative.** A lower bound on μ that uses
only Σ_e g(e) and T cannot be positive. For k = 8, 9, 10 the method can
only cover dense top layers. Lemma D is a small-k phenomenon: the gain
(k−4)t from the top layer is cubic in k, while the lower layers can cost
3·2^{k−3}.

What would be needed instead is a weighted average Σ_e w_e g(e) with
weights adapted to the family (Poonen's theorem, `PROOF_SURVEY.md` §2.3).
In G_W the right weights are obvious (put all weight on W, where
g = 2k − 5). By C4, finding such weights for every family in the sector is
equivalent to Frankl's conjecture.

#### C.6 The sharp statement, as a question [CONJECTURE]

> **Question C6.** Does every valid family on [k] that contains all k
> co-singletons have μ ≥ k − 2?

Equivalently: if R ∪ {∅, Z} is closed under every union of size ≤ k−2 and
has no 1-sets or (k−1)-sets, does some element lie in at least half of its
members? This is Frankl's conjecture with union-closure relaxed at the top.

- [PROVED-EXH, k = 3..7] The minimum of μ over the sector is exactly k − 2.
  k = 3, 4, 5: brute force. k = 6: `mu_search2` at caps 3 and 4. k = 7: the
  existing cap-4 closure of s = 7 (`results/orb3_k7_s7_c4.log` and
  `results/lemma_d2_k7_s7_cap4.txt`) gives μ ≥ 5, and {∅, Z} with the seven
  co-singletons has μ = 5.
- [OBSERVED, k = 8, 9, 10] A randomised search (random generator sets with
  local moves, 150 s per run, 1.6–2.3×10⁷ evaluations each) found no family
  with μ < k − 2. This is weak evidence: the search space is enormous and
  the search is not tuned.
- Equality is common: 1, 8, 124 and 452 labeled families at k = 3, 4, 5, 6
  (1, 4, 9 and 14 classes). In all but two of these classes **every**
  element has g = k − 2, i.e. the middle part R is perfectly balanced. The
  extremes are R = ∅ and R = all sets of size 2..k−2. This is material for
  Section F.
- It implies Frankl's conjecture (take μ ≥ k − 2 ≥ 0 and apply C4), so I
  did not try to prove it.
- Best argument that it is false: C4 shows the sector contains a
  counterexample to μ ≥ 0 as soon as Frankl's conjecture fails, and even if
  Frankl's conjecture is true, C6 asks for more (it drops the co-singleton
  contribution k − 2 entirely). I know of no derivation of C6 from Frankl's
  conjecture. What Frankl's conjecture does give is weaker: if J is the set
  of x whose co-singleton is not a union of smaller members, deleting those
  co-singletons keeps union-closure and yields μ ≥ |J| − 2 (to be stated
  and checked in Section D).
- Confidence that C6 is true: about 55%, conditional on Frankl's
  conjecture being true about 65%.

#### C.7 Summary of Section C

| Claim | Tag |
|---|---|
| C1 sum identity, all k | [PROVED] |
| C2 forcing by 2-sets | [PROVED], known device |
| D₅: sector at k = 5 has μ ≥ 3, exact | [PROVED-EXH] |
| D₆: sector at k = 6 has μ ≥ 3 by the sum method; true minimum 4 | [PROVED-EXH] |
| Sector minimum is k − 2 for k = 3..7 | [PROVED-EXH] |
| C4: a uniform μ ≥ 0 on the sector is equivalent to Frankl's conjecture | [PROVED], partly known |
| C5: the sum method is vacuous for every T once k ≥ 11 | [PROVED] |
| C6: μ ≥ k − 2 on the sector for all k | [CONJECTURE], implies Frankl's conjecture |
| A Lemma-D-type bound for k ≥ 8 | **Not obtained.** |

Tried and failed: extending rules (ii) and (iii) of Lemma D to k = 8. With
weights −4, −2, 0, +2, +4 on sizes 2..6, the 4-sets forced by disjoint
2-sets have weight 0, and the only forced sets of positive weight are
5-sets (2-set ∪ disjoint 3-set, two 3-sets meeting in a point) and 6-sets.
The family G_W with |W| = 6 has N = 84 against k(k−2) + 4t = 52, so any
such bound must depend on more than the sizes a_j; I did not find the right
dependence.

### Section F. Structure of the minimisers

**Short answer.** Statement (i) is false as posed and statement (ii) and
three natural weakenings are false. What survives is sharper than either:

- **[PROVED] Theorem F1.** Every valid family on 2t + 1 points whose deletion
  of one point is M₂ₜ has μ ≥ t + 1.
- **[PROVED-EXH] The seven minimiser classes at k = 7 are exactly the
  one-element extensions of M₆ with μ = 4.** So the observation "all 7
  classes become M₆ after one deletion" has half a reason: F1 explains why
  no extension of M₆ does better, and the list of those that reach 4 is a
  finite computation. Why every minimiser at k = 7 must be an extension of
  M₆ is still only known from the exhaustive search.
- **[PROVED] Proposition F2.** The four previously unnamed classes at k = 7
  belong to infinite families I(t,j) and II(t) with μ = t + 1 = ⌈k/2⌉ at
  every odd k = 2t + 1.

Certificates: `results/proof_extensions.txt` (output of
`proof/extensions.py`, about 2 minutes) and `results/proof_structure.txt`
(output of `proof/structure.py`, about 1 minute).

Notation. G − x = {A ∖ {x} : A ∈ G}. M₂ₜ has blocks P_i = {a_i, b_i},
i ∈ [t], members U_J = ⋃_{i∈J} P_i for J ⊆ [t] and C_i = Z ∖ {b_i}; a_i is
the kept element. By `docs/THEORY.md` A.9, g(a_i) = t and g(b_i) = t − 2.

#### F.1 One-element extensions

**Lemma E [PROVED; standard splitting].** Let H be valid on Z and G valid
on Z ∪ {x} with G − x = H. Put G₀ = {A ∈ G : x ∉ A},
G₁ = {A ∖ {x} : x ∈ A ∈ G}, B = H ∖ G₁, D = G₀ ∩ G₁, E = G₁ ∖ D. Then

- (E1) G₀ is union-closed and G₁ is an up-set of (H, ⊆);
- (E2) Z ∈ G₁ and ∅ ∉ G₁;
- (E3) |G| = |H| + |D|, g_G(e) = g_H(e) + g_D(e) for e ∈ Z, and
  g_G(x) = |E| − |B|,

where g_D(e) = #{A ∈ D : e ∈ A} − #{A ∈ D : e ∉ A}.

*Proof.* (E1) If A ∈ G₁ and A ⊆ A′ ∈ H, then A′ ∈ G₁, or A′ ∈ G₀ and
(A ∪ {x}) ∪ A′ = A′ ∪ {x} ∈ G. (E2) Z ∪ {x} ∈ G and {x} ∉ G. (E3) G is the
disjoint union of B, D, {A ∪ {x} : A ∈ D} and {A ∪ {x} : A ∈ E}, and H is
the disjoint union of B, D, E. ∎

Conversely, a pair (G₀, G₁) with G₀ ∪ G₁ = H, G₀ union-closed, G₁ an up-set
containing Z and not ∅ gives a union-closed family with ∅, the top set and
no singleton, in which elements of Z are separated as in H. It is valid
exactly when x is not a twin of an element of Z. `proof/extensions.py`
enumerates all such pairs and checks (E3) against `frankl_core`.

D is the set of members that occur both with and without x. It is
union-closed and does not contain ∅.

#### F.2 Theorem F1 [PROVED]

**Theorem F1.** Let t ≥ 2 and let G be valid on 2t + 1 points with
G − x = M₂ₜ for some x. Then μ(G) ≥ t + 1.

*Proof.* Suppose μ(G) ≤ t. By (E3),

 (α) g_D(a_i) ≤ 0 for all i,  (β) |E| − |B| ≤ t.

Let 𝒥₁ = {J : U_J ∈ G₁}, 𝒥_B = {J : U_J ∉ G₁}, 𝒢₀ = {J : U_J ∈ G₀},
D_U = 𝒢₀ ∩ 𝒥₁ and d_C = #{i : C_i ∈ D}. Then 𝒥₁ is an up-set of 2^[t] with
[t] ∈ 𝒥₁, ∅ ∉ 𝒥₁; 𝒥_B is a down-set; 𝒢₀ is union-closed and contains 𝒥_B.
Every C_j contains every a_i, so

 g_D(a_i) = d_C + γ(i),  γ(i) = #{J ∈ D_U : i ∈ J} − #{J ∈ D_U : i ∉ J}.

Let V = {i : {i} ∈ 𝒥_B}; then 𝒥_B ⊆ 2^V.

*Claim 1.* If C_j ∉ G₁ then V ⊇ [t] ∖ {j}: every U_J with j ∉ J lies below
C_j, hence outside the up-set G₁.

*Case A: V = ∅.* Then 𝒥_B = {∅}, and by Claim 1 (t ≥ 2) every C_j ∈ G₁.
So B = {∅} and D_U = 𝒢₀ ∖ {∅} is a union-closed family of non-empty sets.
Let m be the number of non-empty J missing from D_U and m_i the number of
those containing i. Then |E| = m + t − d_C, so (β) gives m ≤ d_C + 1, and
γ(i) = 1 + m − 2m_i. By (α), 2m_i ≥ d_C + 1 + m ≥ 2m, so m_i = m for all i
and m = d_C + 1 ≥ 1. Every missing set contains every i, so the only
missing set is [t], and D_U is the set of all non-empty proper subsets of
[t]. That is not union-closed for t ≥ 2. Contradiction.

*Case B: V ≠ ∅.* 𝒢₀ contains ∅ and every {i}, i ∈ V, so 2^V ⊆ 𝒢₀ and
J ∪ S ∈ 𝒢₀ for J ∈ 𝒢₀, S ⊆ V. Split D_U into fibres
Φ_W = {J ∈ D_U : J ∖ V = W}, W ⊆ [t] ∖ V. For W ≠ ∅, Φ_W = {J ∈ 𝒢₀ :
J ∖ V = W}; and Φ_∅ = 2^V ∖ 𝒥_B. Each fibre is closed under J ↦ J ∪ {i}
for i ∈ V (for Φ_∅ because 𝒥_B is a down-set). So within each fibre
J ↦ J ∪ {i} injects the sets without i into the sets with i. Hence
γ(i) ≥ 0 for i ∈ V, with equality only if every fibre is also closed under
J ↦ J ∖ {i}.

By (α), d_C = 0 and γ(i) = 0 for all i ∈ V. So every non-empty fibre is
{S ∪ W : S ⊆ V}. A non-empty Φ_∅ would contain ∅ ∉ D_U, so Φ_∅ = ∅ and
𝒥_B = 2^V; in particular V ≠ [t]. Let u = t − |V| ≥ 1, v = |V|, and
𝒲 = {J ∖ V : J ∈ 𝒢₀}, a union-closed family on [t] ∖ V containing ∅, with
w members. Then 𝒢₀ = {S ∪ W : S ⊆ V, W ∈ 𝒲} and D_U = {S ∪ W : S ⊆ V,
W ∈ 𝒲 ∖ {∅}}.

- *B1: some C_j ∉ G₁.* By Claim 1, V = [t] ∖ {j} and 𝒲 ⊆ {∅, {j}}. If
  {j} ∈ 𝒲 then γ(j) = 2^v > 0, against (α). So D = ∅ and G₀ = B. No other
  C_i is outside G₁. Hence G₀ = {A ∈ H : b_j ∉ A}, G₁ = {A ∈ H : b_j ∈ A},
  and x is a twin of b_j. Contradiction with separation.
- *B2: every C_i ∈ G₁.* All t of them are in E, |B| = 2^v, and the U_J in E
  are those with J ∖ V ∉ 𝒲, so |E| − |B| = t + 2^v(2^u − w − 1). By (β),
  w ≥ 2^u − 1.
  - w = 2^u: for j ∉ V, γ(j) = 2^v > 0. Contradiction.
  - w = 2^u − 1: the missing set M is non-empty, and it cannot have two
    elements (it would be a union of two members of 𝒲). So M = {j}.
    If u = 1, then D = ∅, G₀ = {U_J : j ∉ J} and G₁ = {A ∈ H : a_j ∈ A},
    so x is a twin of a_j. Contradiction. If u ≥ 2, some j′ ∉ V, j′ ≠ j,
    has γ(j′) = 2^{v+1} > 0. Contradiction. ∎

**Computer check [PROVED-EXH for t = 2, 3, 4].** All valid extensions of
M₄, M₆, M₈ were enumerated (58, 1,272 and 123,126). The minimum of μ is
3, 4, 5. The referee's script also confirmed, for t = 2, 3, that the only
pairs (G₀, G₁) satisfying (α) and (β) are the non-separating ones found in
B1 and B2.

**Attempt to break it first.** The enumeration for t = 2, 3 was run before
the proof was written and is what suggested the statement. Best argument
that it could fail for large t: D_U can a priori be any union-closed family
of non-empty subsets of [t], and asking that some i lies in more than half
of it is Frankl's conjecture for D_U. The proof avoids this because (β)
forces D_U to be almost everything in Case A, and the down-set 𝒥_B forces
the product structure in Case B. So F1 needs no unproved hypothesis.

**What F1 does and does not say.** It is a statement about families one
step above M₂ₜ. It shows that min μ(2t + 1) cannot be attained below t + 1
*by an extension of M₂ₜ*. It says nothing about valid families on 2t + 1
points that have no deletion equal to M₂ₜ, so it does not give
min μ(2t + 1) ≥ t + 1.

#### F.3 The extremal extensions [PROVED for the list; classification PROVED-EXH for t = 3, 4]

**Proposition F2 [PROVED].** For t ≥ 2 the following are valid, are
extensions of M₂ₜ, and have μ = t + 1. In the notation (B, D, E):

| Name | D | E | B | g(x) |
|---|---|---|---|---|
| I(t,j), 0 ≤ j ≤ t | {Z} | {C₀, …, C_{j−1}} | the rest | 2j + 1 − 2^t − t |
| II(t) | {Z} | {U_J : t−1 ∈ J, J ≠ [t]} ∪ {C₀, …, C_{t−2}} | {U_J : t−1 ∉ J} ∪ {C_{t−1}} | t − 3 |
| B(2,…,2,3) | {Z} | {U_J : t−1 ∈ J, J ≠ [t]} ∪ {C₀, …, C_{t−1}} | {U_J : t−1 ∉ J} | t − 1 |
| H_t | {U_J : J ≠ ∅} | {C₀, …, C_{t−1}} | {∅} | t − 1 |

In words: I(t,j) is M₂ₜ with the new point put into the top set and into j
of the co-singletons, the old top set being kept as a new co-singleton;
I(t,0) is lift(M₂ₜ). II(t) is B(2,…,2,3) with one co-singleton replaced by
a (k−2)-set.

*Proof.* In each row G₁ = D ∪ E is an up-set of M₂ₜ containing Z and not
∅, and G₀ = B ∪ D is union-closed: for I(t,j) it consists of the block
unions and some C_i, with C_i ∪ C_{i′} = Z and C_i ∪ U_J ∈ {C_i, Z}; for
II(t) and B(2,…,2,3) of the U_J with t−1 ∉ J, possibly C_{t−1}, and Z; for
H_t of all block unions. So G is union-closed with ∅, the top set and no
singleton. The new point x is a twin of some e ∈ Z only if every member of G₀
avoids e. In the first three rows Z ∈ D ⊆ G₀ contains every e, and for H_t
every e lies in some U_J ∈ D ⊆ G₀. So G is separating, hence valid.
(Validity is also checked directly for t = 2..6 by `proof/structure.py`,
and by the referee for t = 2, 3, 4.)
By (E3): if D = {Z} then g(a_i) = t + 1 and g(b_i) = t − 1; for H_t,
g_D ≡ 1 on Z, giving the same values. The last column is |E| − |B|, which
is below t + 1 in every row. ∎

That the third row is the block family B(2,…,2,3) and the fourth is the
hub family of the 2026-11-09 ledger is checked by canonical form for
t = 2, 3, 4.

**Classification.** [PROVED-EXH, t = 3 and t = 4] The valid extensions of
M₂ₜ with μ = t + 1 are exactly these t + 4 families up to isomorphism
(7 classes at t = 3, 8 at t = 4). At t = 2 there are 8 classes, two more
than the list, so the pattern starts at t = 3.

> **[CONJECTURE] F3.** For every t ≥ 3, a valid extension of M₂ₜ has
> μ = t + 1 if and only if it is isomorphic to I(t,j) (0 ≤ j ≤ t), II(t),
> B(2,…,2,3) or H_t.

I did not attempt a proof. It would be the equality analysis of F1 with one
unit of slack in (α) and (β), and the case tree is several times larger.
Confidence: about 80%. The enumeration at t = 5 (M₁₀, 37 members) is out of
reach for `proof/extensions.py` as written; it would need a search that
prunes on (α) and (β).

#### F.4 Statement (i): types of minimisers [FALSIFIED as posed]

"Every minimiser at k ≥ 4 is a hub-type, block-type or matching-type
family." With the three types read as H_t, B(…) and M_k, plus lifts of
minimisers:

| k | minimiser classes | of the three types or lifts | others |
|---|---|---|---|
| 4 | 8 | 2 | 6 |
| 5 | 51 | 10 | 41 |
| 6 | 1 | 1 | 0 |
| 7 | 7 | 3 | 4 |

The four others at k = 7 are I(3,1), I(3,2), I(3,3) and II(3). Adding the
families of F2 to the list:

- [PROVED-EXH, k = 7] every minimiser is one of I(3,0..3), II(3),
  B(2,2,3), H₃, i.e. an extremal extension of M₆.
- [FALSIFIED, k = 5] 38 of the 51 classes are still unnamed. Only 8 of the
  51 are extensions of M₄.
- [FALSIFIED, k = 4] 6 of the 8 classes are unnamed.

**What survives:** at k = 6 and k = 7 every minimiser is M_k or an extremal
one-element extension of M_{k−1}. At k = 4, 5 the minimisers are far more
varied. I cannot tell from this whether k = 4, 5 are small-case accidents
or whether k = 6, 7 are. [CONJECTURE, about 45%] For every t ≥ 3 the
minimisers at k = 2t are exactly M₂ₜ and at k = 2t + 1 exactly the t + 4
families of F3. This contains min μ(k) = ⌈k/2⌉, so it is at least as strong
as Frankl's conjecture. The k = 8 search would be the first real test.

#### F.5 Statement (ii): deletions [FALSIFIED, with three weakenings]

For a valid G and a point x, call the deletion *valid* if G − x is valid on
k − 1 points. All counts are over isomorphism classes of minimisers.

| k | classes | some valid deletion | a deletion is a k−1 minimiser | a one- or two-point deletion is a minimiser |
|---|---|---|---|---|
| 4 | 8 | 4 | 4 | n/a |
| 5 | 51 | 42 | 39 | 42 |
| 6 | 1 | 0 | 0 | 1 |
| 7 | 7 | 7 | 7 | 7 |

The third column reproduces the ledger's 4/8, 39/51, 0/1, 7/7. M₆ has no
valid one-point deletion at all: deleting a_i or b_i leaves the other as a
singleton member.

- **W1** "every minimiser at k ≥ 5 has a one- or two-point deletion that is
  a minimiser": [FALSIFIED at k = 5], 9 of 51 classes have none. It holds
  at k = 6 (M₆ ↦ M₄ by deleting a block) and k = 7.
- **W2** "a valid deletion never raises μ: μ(G − x) ≤ μ(G)":
  [OBSERVED for all valid G at k = 4 and k = 5, 256 and 314,640 pairs
  (G, x)], [FALSIFIED at k = 6]: G = {0, 6, 14, 24, 30, 38, 46, 49, 55, 57,
  59, 61, 62, 63} (bitmasks) has μ(G) = 4 and μ(G − 5) = 5, both valid.
- **W3** "a valid deletion lowers μ by at least 1": [FALSIFIED at k = 5],
  4,570 pairs (G, x) with μ(G − x) = μ(G). It holds for every pair at
  k = 4.
- On minimisers only: [OBSERVED, k = 4..7] whenever a minimiser has a valid
  deletion, some valid deletion has μ ≤ μ(G), and in 50 of the 53 such
  classes it is a minimiser one level down.

So no deletion statement of this kind holds for all valid families, and by
Lemma E the reason is concrete: μ(G) − μ(G − x) is governed by g_D on the
doubled members D, and D can be chosen to hurt exactly the elements that
are abundant in G − x. **What survives is the one-sided, family-specific
form: Theorem F1 for H = M₂ₜ.** A general statement "extensions never
lower μ" would give min μ(k) ≤ min μ(k+1) only on families that have valid
deletions, and W2 shows it is false anyway.

Note on scope. Any statement of the form "every minimiser at k has a valid
deletion with μ no larger" for all k would make min μ non-decreasing, hence
≥ 1, which is rung 1 (Poonen's conjecture, B2). So statement (ii), had it
been true, could not have been proved here.

#### F.6 Summary of Section F

| Claim | Tag |
|---|---|
| Lemma E, extension formulas | [PROVED], standard |
| F1: extensions of M₂ₜ have μ ≥ t + 1 | [PROVED]; also [PROVED-EXH] t = 2, 3, 4 |
| F2: I(t,j), II(t), B(2,…,2,3), H_t are extensions of M₂ₜ with μ = t + 1 | [PROVED] |
| k = 7 minimisers = extremal extensions of M₆ | [PROVED-EXH] |
| F3: the list in F2 is complete for t ≥ 3 | [CONJECTURE]; [PROVED-EXH] t = 3, 4 |
| (i) every minimiser is hub, block or matching type | [FALSIFIED] k = 4, 5, 7 |
| (ii) and W1, W3 | [FALSIFIED] k = 5 |
| W2 | [OBSERVED] k = 4, 5; [FALSIFIED] k = 6 |

### Section D. The valid-class case of Poonen's strict conjecture (rung 1)

**Short answer.** Not proved, as expected: by B2, rung 1 *is* Poonen's
conjecture. The deliverables are (1) the exact place where each induction
breaks, with a family that breaks it; (2) what Frankl's conjecture (FC)
does give, which decides rung 1 for about 70% of the valid families at
k = 5 and leaves a sharply described residual class; (3) one unconditional
bound, 3μ ≥ 4k − 4 − n for k ≤ 13, which proves rung 1 for all valid
families with n ≤ 4k − 5 on at most 13 points and is tight on the
minimisers at k = 3, 4, 5, 6, 7.

FC(m) means Frankl's conjecture for union-closed families whose universe
has at most m elements. FC(12) is a theorem (Živković–Vučković). Irr(G) is
the set of join-irreducible members of G, and
g_J(e) = #{A ∈ J : e ∈ A} − #{A ∈ J : e ∉ A}. Recall g_G(e) ≡ n (mod 2).

Certificate: `results/proof_poonen.txt`, the output of `proof/poonen.py`
(about 3 minutes).

#### D.1 The lift/peel induction and where it stops [PROVED]

**Proposition D1.** If every valid family on at most k − 1 points has
μ ≥ 1, then every degree-1 valid family on k points has μ ≥ 2. Since
min μ(3) = 1, a valid family with μ ≤ 0 on the smallest possible number of
points is a core (s ≥ 2).

*Proof.* `docs/THEORY.md` B.2–B.3: peel(G) is valid on k − 1 points and
μ(G) = μ(peel G) + 1. ∎

So the induction through `peel_compress` and `lift` closes the degree-1
sector completely and says nothing about cores: **a core has no peel.** The
two substitutes one might try both fail, with explicit families:

- *Delete a point.* For a core G, G − x need not be valid: M₆ has no valid
  one-point deletion (F.5). When it is valid, μ can go **up**: the
  14-member family of W2 (F.5) has μ(G) = 4 and μ(G − 5) = 5. So
  "μ(G) ≥ μ(G − x)" is false and cannot carry an induction.
- *Delete a member.* If B ∈ Irr(G) then G ∖ {B} is union-closed, and
  g_G(e) = g_{G∖B}(e) ± 1. From the hypothesis μ(G ∖ B) ≥ 1 one gets only
  μ(G) ≥ 0, unless the element that witnesses μ(G ∖ B) ≥ 1 lies in B.
  **This loss of exactly 1 is the step that breaks**, and it is the
  obstruction Bruhn and Schaudt describe for Frankl's conjecture itself
  (`PROOF_SURVEY.md` §4.2), one unit higher. It happens constantly: among
  the pairs (G, B) with G and G ∖ B both valid, μ(G) = μ(G ∖ B) − 1 for
  452 of 1,004 at k = 4 and 695,175 of 1,602,455 at k = 5, and 9,885 of the
  latter have G a minimiser. Smallest example: G = {∅, 01, 02, 12, 012},
  B = 01: μ(G) = 1 and μ(G ∖ B) = 2.

#### D.2 What Frankl's conjecture gives [PROVED, conditional on FC(k); unconditional for k ≤ 12]

**Lemma D2 (deletion).** Let G be valid on Z and J ⊆ Irr(G) with Z ∉ J.
Then G ∖ J is union-closed with universe Z. If Frankl's conjecture holds
for G ∖ J, there is e with g_G(e) ≥ g_J(e) + p_J, where p_J = 1 if n − |J|
is odd and 0 otherwise. Hence μ(G) ≥ min_e g_J(e) + p_J.

*Proof.* A union of two members outside J that lay in J would be
join-irreducible, hence equal to one of them. FC gives e with
g_{G∖J}(e) ≥ 0, hence ≥ p_J by parity, and g_G = g_{G∖J} + g_J. ∎

**Corollary D3.** Let G be valid on k points and assume FC(k). Then:

(a) if n is odd, μ(G) ≥ 1;

(b) μ(G) ≥ j − 2, where j is the number of join-irreducible co-singletons,
and μ(G) ≥ j − 1 if n − j is odd;

(c) if μ(G) = 0 then n is even, G is a core, E₀ = {e : g(e) = 0} has at
least two elements, no join-irreducible member contains E₀, and j ≤ 2.

*Proof.* (a) J = ∅. (b) Each e lies in every member of J except possibly
Z ∖ {e}, so g_J(e) ≥ j − 2. (c) n is even by (a). G is a core by D1's
argument with FC(k−1). If B ∈ Irr(G) and B = Z, then G has at most one
co-singleton (two would have union Z), hence exactly one by Lemma C, and G
is degree-1; excluded. Otherwise D2 with J = {B} gives e with
0 ≥ g_G(e) ≥ g_B(e) + 1, so e ∉ B and e ∈ E₀. For |E₀| ≥ 2 take e ∈ E₀
and B inclusion-minimal among the members containing e; B is
join-irreducible, so some e′ ∈ E₀ is outside B. Finally (b) gives
0 ≥ j − 2 + [j odd], so j ≤ 2. ∎

For k ≤ 12 these are unconditional. In particular: **[PROVED] every valid
family on at most 12 points with an odd number of members, or with at
least three join-irreducible co-singletons, has μ ≥ 1.**

**How far this goes.** Define β(G) = max_J (min_e g_J(e) + p_J) over all
J ⊆ Irr(G). FC implies μ ≥ β. Over all valid families (exact, labeled
counts):

| k | valid | β ≥ 1, n odd | β ≥ 1, n even | β ≤ 0 (all have n even) |
|---|---|---|---|---|
| 3 | 4 | 1 | 0 | 3 |
| 4 | 304 | 156 | 56 | 92 |
| 5 | 235,749 | 117,880 | 46,654 | 71,215 |

μ ≥ β and μ ≥ j − 2 hold with no exception, and μ − β is always even. So
at k = 5, **Frankl's conjecture together with deletion and parity decides
rung 1 for 69.8% of the valid families.** The residual class is

 𝓡 = {valid G : n even, β(G) ≤ 0}.

It contains minimisers: the family I(3,1) at k = 7 has β = 0 and μ = 4.
The other six minimiser classes at k = 7 have β = 2, and M₆ has β = 1.

> **The exact open step.** Rung 1 for all k is equivalent to FC together
> with: *no family in 𝓡 has μ = 0.* Whether FC implies this is open
> (`PROOF_SURVEY.md` §4.4: Carvalho–Machiavelo prove the implication in the
> other direction only). I have no argument for it and no family that
> suggests it is false.

**Best argument that rung 1 is false.** A counterexample would be a core
with n even, at least two elements at exactly half, every join-irreducible
member missing one of them, and at most two join-irreducible co-singletons.
Nothing in that list is contradictory on its face; it is the profile of a
"balanced" family such as a product of power sets, and power sets are
excluded from the valid class only by the no-singleton rule. If a
counterexample exists I would expect it to be a large family that is
locally Boolean. By D4 below it has n ≥ 4k − 4.

#### D.3 An unconditional bound for small families [PROVED given FC(k−1); unconditional for k ≤ 13]

**Lemma S (staircase; Hu, as in Tian Lemma 2.4).** Let G be valid on Z,
elements listed as u₁, …, u_k with c(u₁) ≤ … ≤ c(u_k). For i < k let Y_i be
the union of the members avoiding u_i, and S = {Z, Y₁, …, Y_{k−1}}. Then

- (S2) u_j ∈ Y_i whenever i < j;
- (S3) the k members of S are distinct and all contain u_k;
- (S5) if B ⊆ G consists of members avoiding u_k and φ = max_e c_B(e) > 0,
  some a ≠ u_k with c_B(a) = φ lies in exactly k − 1 members of S.

*Proof.* (S2) Otherwise every member containing u_j contains u_i, so
G_{u_j} ⊆ G_{u_i}, and c(u_j) ≥ c(u_i) forces equality, against separation.
(S3) u_j ∈ Y_i ∖ Y_j for i < j < k, Z ≠ Y_i, and u_k ∈ Y_i by (S2).
(S5) u_i lies in Z and in Y₁, …, Y_{i−1}, not in Y_i; so it lies in k − 1
members of S unless u_i ∉ Y_j for some i < j ≤ k − 1, in which case every
member containing u_i contains u_j and c_B(u_j) ≥ c_B(u_i). Start from any
u_i with c_B(u_i) = φ (i ≠ k since c_B(u_k) = 0) and move to such a j while
possible; the index increases and stays ≤ k − 1. ∎

**Proposition D4.** Let G be valid on k points with n members and assume
FC(k − 1). Then **3μ(G) ≥ 4k − 4 − n.**

*Proof.* c(u_k) = (n + μ)/2. Let B be the set of members avoiding u_k; it
is union-closed, contains ∅ and has (n − μ)/2 members. If B = {∅}, then
μ = n − 2 and n ≥ k + 1 by (S3), which gives the claim. Otherwise FC(k−1)
applies to B, so φ ≥ |B|/2. Take a from (S5). The k − 1 members of S
containing a contain u_k, so they are not in B, and c(a) ≥ φ + k − 1.
Therefore

 μ ≥ 2c(a) − n ≥ |B| + 2k − 2 − n = (n − μ)/2 + 2k − 2 − n,

which is 3μ ≥ 4k − 4 − n. ∎

At μ = −1 this is the Lo Faro / Roberts–Simpson bound n ≥ 4k − 1 for a
counterexample; D4 is that bound read as a function of the margin. It
improves the μ ≥ 2k − n of `PROOF_SURVEY.md` §2.4 whenever n > k + 2.

**Corollary D5 [PROVED, unconditional for k ≤ 13].** Every valid family on
k ≤ 13 points has μ at least the smallest integer of the parity of n that
is ≥ (4k − 4 − n)/3. In particular:

- **rung 1 holds for every valid family with n ≤ 4k − 5** (and for
  n = 4k − 3, by parity);
- μ ≥ ⌈k/2⌉ for every valid family with n ≤ 4k − 3⌈k/2⌉ − 2, and for one
  more value of n by parity (n ≤ 20 except n = 19 at k = 8).

Checks. [PROVED-EXH against data] 3μ ≥ 4k − 4 − n and the step
c(a) ≥ φ + k − 1 hold on all 4, 304 and 235,749 valid families at
k = 3, 4, 5. The bound is **attained**: ⌈(4k − 4 − n)/3⌉ = μ for 1 of 1,
44 of 48 and 1,906 of 2,484 labeled minimisers at k = 3, 4, 5, for M₆
(n = 11, bound 3), and for six of the seven minimiser classes at k = 7
(n = 12, bound 4; the exception is H₃ with n = 18). It is not attained by
M₈ (n = 20: the bound gives 3, and 4 after the parity correction).

**What D5 says about the table.** It is a second, independent proof that
no valid family with at most 13 members has μ ≤ 2 at k = 6, and none with
at most 14 members has μ ≤ 3 at k = 7. The exhaustive searches are still
needed for larger families. At k = 8 it gives something the repository did
not have: **any valid family on [8] with μ ≤ 3 has n = 19 or n ≥ 21**, and
any with μ ≤ 0 has n ≥ 28.

#### D.4 Summary of Section D

| Claim | Tag |
|---|---|
| D1: a smallest valid family with μ ≤ 0 is a core | [PROVED] |
| Deletion of a point or of a member cannot carry the induction | [FALSIFIED] by the families in D.1 |
| D2, D3: under FC(k), μ ≥ 1 if n is odd; μ ≥ j − 2; profile of a μ = 0 family | [PROVED] conditional; unconditional for k ≤ 12; known device |
| FC + deletion + parity decide rung 1 for 69.8% of valid families at k = 5 | [OBSERVED], exact count, k = 5 only |
| D4: 3μ ≥ 4k − 4 − n under FC(k−1) | [PROVED] conditional; partly known |
| D5: rung 1 for n ≤ 4k − 5, k ≤ 13 | [PROVED], unconditional |
| Rung 1 for all valid families | **Open.** Equivalent to Poonen's conjecture (B2). |

Confidence that rung 1 is true: about 85%, essentially my confidence in
Poonen's conjecture; the data here (k ≤ 7, and n ≤ 4k − 5 for k ≤ 13) do
not reach the families where it could fail.

### Section E. A growing lower bound (rungs 2 and 3)

**Short answer.** No unbounded lower bound for min μ(k) was proved, and
none can be without proving Frankl's conjecture (B.4). What was proved is
growth on a slice: **for every k, every valid family with n ≤ c·k members,
c < 1 + √5, has μ ≥ ((2 − 0.618c)k − 2)/1.382**, unconditionally. The
argument cannot be pushed past n ≈ 4k even assuming Frankl's conjecture,
and the families that attain ⌈k/2⌉ at large k have exponentially many
members, so rung 3 is out of its reach. The exact obstruction is stated in
E.3.

Certificates: `results/proof_growth.txt` (output of `proof/growth.py`) and
`results/proof_rung3_break.txt` (output of `proof/rung3_break.py`).

#### E.1 A growing bound on small families [PROVED, unconditional]

Let T_κ be the statement that every union-closed family with a non-empty
member has an element in at least κ|F| of its members. T_ψ with
ψ = (3 − √5)/2 is a theorem (Alweiss–Huang–Sellke, EJC 2024; Sawin;
`PROOF_SURVEY.md` §1.1). T_{1/2} is Frankl's conjecture.

**Proposition E1.** If T_κ holds for some κ ∈ (0, 1/2], then every valid
family G on k points with n members satisfies

 (1 + κ)·μ(G) ≥ 2k − 2 − (1 − κ)·n.

*Proof.* As for D4, with T_κ in place of FC(k−1). Let u_k be a most
frequent element, B the members avoiding it, |B| = (n − μ)/2. If B = {∅}
then μ = n − 2 and n ≥ k + 1 by Lemma S, and the claim is n ≥ k + κ.
Otherwise T_κ gives φ = max_e c_B(e) ≥ κ|B| > 0, Lemma S gives a with
c(a) ≥ φ + k − 1, and μ ≥ 2c(a) − n ≥ κ(n − μ) + 2k − 2 − n. ∎

**Corollary E2 [PROVED, every k, no hypothesis].** With κ = ψ, where
1 − ψ = (√5 − 1)/2:

- every valid family on k points with **n < (1 + √5)(k − 1)** members has
  μ ≥ 1;
- every valid family with n ≤ c·k members, c < 1 + √5, has
  μ ≥ ((2 − (1 − ψ)c)k − 2)/(1 + ψ), which tends to infinity with k.

The proof uses only "separating, union-closed, contains ∅", so the first
item says: **a separating union-closed family with fewer than
3.236(k − 1) members has an element in strictly more than half of them.**
For comparison, the published range is n ≤ 2k (Falgas-Ravry) and
n ≤ 2(k + k/(log₂k − log₂log₂k)) (Maßberg), which is below 3.236k once k is
in the hundreds. Hu's theorem (Bruhn–Schaudt Thm 24) says that a range
c·k with c > 2 for Frankl's conjecture would imply a constant fraction
(c − 2)/(2(c − 1)) for all families; E2 is the converse direction, from the
constant fraction to a range, and the two are consistent (c = 3.236 gives
0.276 < ψ).

**Corollary E3.** κ = 1/2 gives D4, 3μ ≥ 4k − 4 − n, a theorem for
k ≤ 13 and conditional on Frankl's conjecture beyond.

Checks. [PROVED-EXH against data] Both inequalities hold on all valid
families at k = 3, 4, 5. Ranges covered (largest n for which the bound
forces the stated μ for every smaller n):

| k | μ ≥ 1, κ = ψ | μ ≥ 1, κ = ½ | μ ≥ ⌈k/2⌉, κ = ψ | μ ≥ ⌈k/2⌉, κ = ½ | size of M_k or B(2,…,2,3) |
|---|---|---|---|---|---|
| 8 | 22 | 27 | 15 | 18 | 20 |
| 10 | 29 | 35 | 20 | 23 | 37 |
| 12 | 35 | 43 | 24 | 28 | 70 |
| 13 | 38 | 47 | 25 | 29 | 71 |
| 20 | 61 | (75) | 41 | (48) | 1,034 |
| 40 | 126 | (155) | 83 | (98) | 1,048,596 |

Entries in parentheses assume Frankl's conjecture.

#### E.2 Why this is not rung 2

Rung 2 asks for min μ(k) ≥ f(k) → ∞ over **all** valid families. E2 gives
it only for n = O(k).

1. [PROVED, B.4] Any f that is eventually ≥ 0 gives Frankl's conjecture.
   So an unconditional rung 2 is at least as hard as the conjecture.
2. Even assuming Frankl's conjecture, I have no proof of rung 2 or of
   rung 1. The three tools of this phase each stop for an identified
   reason:
   - *Averaging* (Section C): vacuous for k ≥ 11 even with all
     co-singletons present (C5).
   - *Staircase* (D4, E1): the gain is the k − 1 extra members of S, a
     quantity linear in k, set against |B| ≈ n/2. For n ≥ 4k the bound is
     ≤ 0 whatever κ ≤ 1/2 is. The extremal families at large k have
     n ≈ 2^{k/2}.
   - *Deletion with Frankl's conjecture* (D2, D3): gives μ ≥ j − 2, growth
     only for families with many join-irreducible co-singletons. M_k has
     j = k/2, so this is the one tool that sees the right order of
     magnitude on the extremal family (it gives k/2 − 2 against the true
     k/2), but a family can have j ≤ 2.
3. [CONJECTURE] min μ(k) → ∞. Confidence about 60%. Best argument
   against: nothing rules out a sequence of large, locally Boolean valid
   families with μ bounded; the valid class excludes power sets only
   through the no-singleton rule, and doubling every point of a power set
   and adding k/2 co-singletons (that is M_k) already costs only k/2. A
   cleverer way to separate the doubled points might cost O(1).

#### E.3 Rung 3: where ⌈k/2⌉ fails to be provable

What is proved toward min μ(k) = ⌈k/2⌉:

- **Upper bound, all k ≥ 4** [PROVED, `docs/THEORY.md` A.9].
- **Lower bound for small families** [PROVED]: μ ≥ ⌈k/2⌉ for every valid
  family with n ≤ 4k − 3⌈k/2⌉ − 2 members when k ≤ 13 (D5), and with
  n < 2.118k − 1.9 for every k (E2; column 4 of the table).
- **Lower bound one step above M₂ₜ** [PROVED]: Theorem F1.
- **Lower bound for k ≤ 7** [PROVED-EXH]: the table.

Where it fails: the lower bound for families with more than about 2.5k
members. At k = 8 that means n = 19 and n ≥ 21 (D.3), which includes
everything near M₈ except M₈'s own size. The staircase argument cannot
help there, and no argument in this phase distinguishes a family with
n ≈ 2^{k/2} from a power set closely enough to see a margin of k/2.

**Attempt to break rung 3.** A randomised search over valid families
(union-closures of generator lists, started from M_k, B(…), H_t, random
block families and random lists, with local moves; 150 s per k) found no
family with μ < ⌈k/2⌉ at k = 8, 9, 10, 11 and re-found the minimum at
k = 5, 6, 7. [OBSERVED]; the search caps families at 3,000 members and is
not tuned, so this is weak evidence.

[CONJECTURE] min μ(k) = ⌈k/2⌉ for all k ≥ 4. Confidence about 45% (it
contains Frankl's and Poonen's conjectures; conditional on both, about
60%). The k = 8 value, min μ(8) = 4, I put at about 85%.

#### E.4 Summary of Section E

| Claim | Tag |
|---|---|
| E1: (1+κ)μ ≥ 2k − 2 − (1−κ)n given T_κ | [PROVED] |
| E2: μ ≥ 1 for n < (1+√5)(k−1); linear growth of μ on slices n ≤ ck, c < 1+√5; every k | [PROVED], unconditional; novelty NOT FOUND, about 50% |
| Rung 2: min μ(k) → ∞ | **Not proved.** Implies Frankl's conjecture. |
| Rung 3: min μ(k) = ⌈k/2⌉ | **Not proved.** Lower bound known for k ≤ 7, for small families, and above M₂ₜ only. |
| No family below ⌈k/2⌉ found at k = 8..11 | [OBSERVED], randomised |

## 4. Report

Written 2026-11-12, after Sections A–F. Nothing in this phase proves or
verifies Frankl's conjecture. Every certificate named below was regenerated
at the end of the session and is byte-identical to the file in `results/`.

### 4.1 What was proved

Tags as in the ledgers. "Novelty" is the verdict of the log in §2; NOT FOUND
means only that I did not find it.

| # | Statement | Tag | Novelty |
|---|---|---|---|
| B1 | Frankl's conjecture ⇔ μ ≥ 0 on valid families | [PROVED] | KNOWN |
| B2 | Poonen's strict conjecture ⇔ μ ≥ 1 on valid families (rung 1) | [PROVED] | PARTLY KNOWN |
| C1 | Sum identity for the all-co-singleton sector, all k | [PROVED] | routine |
| D₅, D₆ | Sector at k = 5 has μ ≥ 3 (exact); at k = 6 the method gives 3, the truth is 4 | [PROVED-EXH] | NOT FOUND, routine |
| — | Sector minimum is k − 2 for k = 3..7 | [PROVED-EXH] | NOT FOUND |
| C4 | Frankl's conjecture ⇔ μ ≥ 0 on valid families containing all co-singletons | [PROVED] | PARTLY KNOWN (~50% folklore) |
| C5 | The sum method gives nothing for any top layer once k ≥ 11 | [PROVED] | NOT FOUND |
| F1 | Every valid one-point extension of M₂ₜ has μ ≥ t + 1, all t ≥ 2 | [PROVED] | NOT FOUND |
| F2 | Families I(t,j), II(t): μ = ⌈k/2⌉ at every odd k | [PROVED] | NOT FOUND |
| — | The 7 minimiser classes at k = 7 are exactly the extremal extensions of M₆ | [PROVED-EXH] | NOT FOUND |
| D1 | A smallest valid family with μ ≤ 0 is a core | [PROVED] | routine |
| D2, D3 | Under Frankl's conjecture: μ ≥ 1 if n is odd; μ ≥ j − 2; profile of a μ = 0 family. Unconditional for k ≤ 12 | [PROVED] | KNOWN device |
| D4, D5 | 3μ ≥ 4k − 4 − n for k ≤ 13; so μ ≥ 1 when n ≤ 4k − 5 | [PROVED] | PARTLY KNOWN (~35% in Hu 2023) |
| E1, E2 | (1+ψ)μ ≥ 2k − 2 − (1−ψ)n for every k; so μ ≥ 1 when n < (1+√5)(k−1) | [PROVED] | NOT FOUND (~50% exists) |

The two results I consider the substance of the phase:

1. **Theorem F1 with F2** (Section F). It is unconditional, it is about the
   repository's own extremal family, it explains half of the k = 7
   observation, and it names all seven k = 7 minimisers as members of
   infinite families.
2. **Proposition E1 / Corollary E2** (Sections D, E). It is unconditional
   for every k, it is attained by M₆ and six of the seven k = 7 minimisers
   in its κ = ½ form, and if it is new it extends the known range of
   Frankl's conjecture for separating families from about 2k to 3.236k
   members. Its novelty is the least certain item in the table: the proof is
   a short combination of two published arguments.

### 4.2 Which known approaches were tried, and what happened

| Approach (`PROOF_SURVEY.md`) | Tried on | Outcome |
|---|---|---|
| Weighted averaging / FC-families (§2.3, §3) | Section C, the all-co-singleton sector | Works at k = 5, loses 1 at k = 6, covers part of the sector at k = 7 (Lemma D). **Fails for k ≥ 11** for every top layer (C5): lower layers can cost 3·2^{k−3} against a cubic gain. |
| Reduction by cloning and co-singleton padding (Hu, §2.4) with amplification by powers | Section C | Turned into C4: the sector is as hard as the whole conjecture. A negative result about the target, not a bound. |
| Deletion of join-irreducible members (§4.2) | Sections D, F | Gives D2/D3 conditionally on Frankl's conjecture. As an induction it **loses exactly 1 per step** (D.1). |
| Lift / peel (repository) | Section D | Closes the degree-1 sector; **says nothing about cores**. |
| Element deletion / extension (A_x, A_x̄ splitting, §4.2) | Section F | Lemma E and Theorem F1 for H = M₂ₜ. As a general monotonicity statement it is **false** (W2, W3). |
| Staircase / minimal-counterexample bound (Lo Faro, Hu; §2.4) | Sections D, E | D4 and E1. **Stops at n ≈ 4k** by construction. |
| Entropy (§1) | Section E, as a black box | Supplies the constant in E1. On its own it gives μ ≥ −0.234n, nothing. |
| Lattice-class theorems (§2.1) | not tried | μ is not a lattice invariant (`LITERATURE.md` Prop. L). |
| Compression (§4.3) | not tried | Raises μ or leaves the valid class. |
| Reimer's theorem (§3.1) | not tried beyond the remark in §6 of the survey | Non-negative only for the power set. |

### 4.3 What was tried and failed, with the obstruction

1. **Rung 1 (μ ≥ 1 on valid families).** Not proved. It is Poonen's
   conjecture (B2) and implies Frankl's. Obstruction: for a core there is no
   smaller valid family whose margin controls μ(G). Point deletion can be
   invalid (M₆) or raise μ (the k = 6 family in F.5); member deletion loses
   1 (D.1). Under Frankl's conjecture the open part is exactly the class
   𝓡 = {n even, β ≤ 0} of D.2, 30.2% of the valid families at k = 5.
2. **Rung 2 (min μ(k) → ∞).** Not proved. Implies Frankl's conjecture.
   Proved only on slices n ≤ ck, c < 3.236 (E2). Obstruction: every tool
   gains a quantity polynomial in k, and the families that matter have
   about 2^{k/2} members.
3. **Rung 3 (min μ(k) = ⌈k/2⌉).** Not proved. The lower bound holds for
   k ≤ 7, for n up to about 2.5k when k ≤ 13, and for extensions of M₂ₜ.
   It fails to be provable for large families; at k = 8 the uncovered sizes
   are n = 19 and n ≥ 21.
4. **A Lemma-D-type bound for k ≥ 8 in the sector.** Not obtained. With
   weights −4, −2, 0, +2, +4 the forced sets of positive weight are too
   few, and G_W shows the size vector alone cannot suffice.
5. **A derivation of C6 (μ ≥ k − 2 in the sector) from Frankl's
   conjecture.** Not obtained. The lattice obtained by contracting the
   co-singletons satisfies Frankl's conjecture, but its meet-irreducibles
   do not correspond to elements when a co-singleton is a union of smaller
   members.
6. **The classification conjecture F3 for general t.** Not attempted;
   exhaustive at t = 3, 4 only.
7. **Opening Poonen (1992) and Abe (2002).** Failed again: the hosts are
   refused by this environment. Hu (2023) was also not opened, which
   matters for the novelty of D4 and E1.

### 4.4 What was falsified

| Statement | Where | Counterexample |
|---|---|---|
| (i) every minimiser is hub, block or matching type | k = 4, 5, 7 | 6 of 8, 41 of 51, 4 of 7 classes are none of these |
| (ii) every minimiser has a one-point deletion that is a minimiser | k = 4, 5, 6 | 4/8, 39/51, 0/1 (ledger counts reproduced) |
| W1: some one- or two-point deletion is a minimiser | k = 5 | 9 of 51 classes |
| W2: a valid deletion never raises μ | k = 6 | G = {0, 6, 14, 24, 30, 38, 46, 49, 55, 57, 59, 61, 62, 63}: μ(G) = 4, μ(G − 5) = 5 |
| W3: a valid deletion lowers μ by ≥ 1 | k = 5 | 4,570 pairs (G, x) with equality |
| "μ(G) ≥ μ(G∖B) for B join-irreducible" as an induction step | k = 3 | U2[3] and B = 01 |
| The sum method proves μ ≥ 1 on the sector at k = 7 | k = 7 | two top layers give a bound ≤ 0 |
| A sentence of `PROOF_SURVEY.md` §4.1 ("no weighted version is known to fail") | — | Wang 2026; corrected in §8 of the survey |

### 4.5 Open items, with confidence

| Item | Confidence it is true |
|---|---|
| Rung 1 = Poonen's strict conjecture | about 85% |
| C6: μ ≥ k − 2 on the all-co-singleton sector, all k | about 55% (65% given Frankl's conjecture) |
| F3: the t + 4 families are all the extremal extensions of M₂ₜ, t ≥ 3 | about 80% |
| min μ(8) = 4 | about 85% |
| min μ(k) → ∞ | about 60% |
| min μ(k) = ⌈k/2⌉ for all k ≥ 4 | about 45% |
| Minimisers for t ≥ 3 are M₂ₜ at k = 2t and the t + 4 families at k = 2t + 1 | about 45% |
| E2 is not already in the literature | about 50% |
| D4 (margin form of the Lo Faro bound) is not already in the literature | about 65% |
| C4 is not already in the literature | about 50% |

### 4.6 What would be worth doing next

1. Read Hu, *On the union-closed sets conjecture*, Discrete Math. 346
   (2023) 113430, and Poonen (1992), from a network that can reach them.
   That settles the novelty of D4, E1 and B2.
2. k = 8. By D5 a family with μ ≤ 3 has n = 19 or n ≥ 21. That is a size
   constraint the existing engines do not use. A prune "n ≤ 18 or n = 20 is
   impossible at cap 3" would cut the s = 2..8 searches.
3. Prove or refute F3 at t = 5 with an extension search that prunes on (α)
   and (β) of the F1 proof.
4. C6 at k = 8: `mu_search3 8 5 8 …` on the 12,346 top-layer orbits of the
   sector, a laptop job. Not started here.
