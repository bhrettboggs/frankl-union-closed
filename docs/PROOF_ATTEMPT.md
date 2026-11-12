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

## 4. Report

*(Written in Section G.)*
