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

No proof step, novelty verdict or choice of claim was delegated.

## 2. Novelty-check log

One entry per specific claim, made before any proof attempt. Verdicts:
KNOWN (cited), PARTLY KNOWN (which part), NOT FOUND (which means only that
I did not find it).

| # | Claim | Queries and sources | Verdict |
|---|---|---|---|
| N1 | B1: Frankl's conjecture is equivalent to μ ≥ 0 on valid families. | Bruhn–Schaudt §2 (separating; ∅) and §4 (singleton), re-read; Tian Lemma 2.1 (twin deletion); Kabela–Polák–Teska Prop. 10(3)–(4). | **KNOWN.** Each step is a standard reduction. Only the packaging as "valid" is this repository's. |
| N2 | B2: Poonen's strict conjecture for all separating families is equivalent to μ ≥ 1 on valid families. | Web search "Poonen conjecture union-closed strictly more than half separating reduce to families without singletons equivalent"; Bruhn–Schaudt §4; Carvalho–Machiavelo §5 (Thm 5.3 is a different equivalence, via normalized families); Kabela–Polák–Teska Props 7, 9, 10 (the ∅-free step is their Prop. 10(4) pattern). | **PARTLY KNOWN.** The ∅-free case and the singleton injection are standard. The induction that peels a singleton in the bijective case, and the resulting equivalence, were NOT FOUND. It is elementary and could well be folklore or in Poonen (1992), which is unread. |

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

## 4. Report

*(Written in Section G.)*
