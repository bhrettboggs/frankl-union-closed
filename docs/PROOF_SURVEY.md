# Survey of proof techniques for Frankl's conjecture, and what they give for the margin μ

Survey date: 2026-11-12. This file is Section A of Phase 8. It surveys
**proof techniques and their barriers**, and asks of each one whether it can
say anything about the margin

  μ(G) = max_e 2c(e) − |G|

on valid families (union-closed on [k], contains ∅ and [k], no singleton
members, separating; `docs/THEORY.md` A.3). It does not repeat the
small-universe literature check in `docs/LITERATURE.md`.

Nothing here proves or verifies Frankl's conjecture.

## 0. How to read this file

### 0.1 Read status of each source

Every statement below carries one of these labels.

- **[read]**: I opened the paper and read the cited statement myself.
- **[helper]**: a delegated reader opened the paper in full and reported the
  statement; I did not re-open it. Treat as one step less reliable.
- **[via X]**: the original was not opened by anyone this session; the
  statement is taken from source X, which quotes it.
- **[not opened]**: nobody could open it. Nothing is stated from memory.

Evidence tags for this repository's own claims are as in the ledgers:
[PROVED], [PROVED-EXH], [OBSERVED], [FALSIFIED], plus [CONJECTURE] for
unproved claims.

### 0.2 The rungs

The task refers to "rungs 1 to 3" without listing them. I read them as the
three lower-bound targets of Phase 8, in increasing strength:

- **Rung 1.** μ(G) ≥ 1 for every valid G on [k], k ≥ 3 (Section D of the task).
- **Rung 2.** min μ(k) ≥ f(k) for some unbounded f (Section E).
- **Rung 3.** min μ(k) = ⌈k/2⌉ for k ≥ 4 (Section E, second part).

If a different list was intended, the per-approach verdicts in Section 6
need re-reading against it.

### 0.3 Two sources that are still unread

- **Poonen, *Union-closed families*, JCTA 59 (1992) 253–268**
  ([doi](https://doi.org/10.1016/0097-3165(92)90068-6)). **[not opened]**.
  Tried: the author's page at math.mit.edu, the ScienceDirect article and
  PDF pages, and the DOI resolver. All three hosts are refused by this
  session's network policy. Everything attributed to Poonen below is
  [via Bruhn–Schaudt], [via Kabela–Polák–Teska] or
  [via Carvalho–Machiavelo].
- **Abe, *Excess of a lattice*, Graphs Combin. 18 (2002) 395–402**
  ([doi](https://doi.org/10.1007/s003730200029)). **[not opened]**. The
  Springer host and the DOI resolver are refused as well. Not even the
  abstract was retrieved this session, so `docs/LITERATURE.md` B.1 remains
  the only account of it in this repository.

Both gaps recorded in `docs/LITERATURE.md` are therefore **still open**.

---

## 1. The entropy method

### 1.1 What it proves

| Paper | Read | Statement |
|---|---|---|
| Gilmer, [arXiv:2211.09055](https://arxiv.org/abs/2211.09055) | [helper], full text | Thm 2: every union-closed F ≠ {∅} has an element in at least 0.01·\|F\| sets. Thm 1: if A, B are independent samples from a distribution on subsets of [n] with Pr[i ∈ A] ≤ 0.01 for all i, then H(A∪B) ≥ 1.26·H(A). Union-closure is used only at the end: for A, B uniform on F, A∪B is supported on F, so H(A∪B) ≤ log\|F\| = H(A). |
| Chase, Lovett, [arXiv:2211.11689](https://arxiv.org/abs/2211.11689) | [read], full text | Claim 4.1: for independent A, B with Pr[A_i = 0], Pr[B_i = 0] ≥ p, H(A∪B) ≥ (p/2φ)(H(A)+H(B)), φ = (√5−1)/2. Thm 1.3: a (1−ε)-approximate union-closed family has an element in a ψ − δ fraction of sets, ψ = (3−√5)/2, δ = 2ε(1 + log(1/ε)/log\|F\|). |
| Sawin, [arXiv:2211.11504](https://arxiv.org/abs/2211.11504) | [read], full text | Thm 1: fraction ≥ ψ. Thm 2: for independent A, B with all marginals ≤ u, H(A∪B) ≥ λ(u)·H(A), with λ(u) = H(2u−u²)/H(u) for u ≤ ψ and λ(u) = (1−u)·2/(√5−1) for u ≥ ψ. Examples 4–5: **sharp for every u**. |
| Alweiss, Huang, Sellke, [arXiv:2211.11731](https://arxiv.org/abs/2211.11731) (EJC 31(3) 2024) | [helper], full text | Same constant ψ; the one-variable inequality φH(x²) ≥ xH(x) is checked with interval arithmetic. |
| Pebody, [arXiv:2211.13139](https://arxiv.org/abs/2211.13139) | [helper], v1 | Same constant; two lemmas are marked "to be proven" in v1. |
| Sawin, §2 of the same paper | [read] | Proof **sketch** of ψ + δ for some inexplicit δ > 0, using a second, correlated sample C. |
| Yu, [arXiv:2212.00658](https://arxiv.org/abs/2212.00658); Cambie, [arXiv:2212.12500](https://arxiv.org/abs/2212.12500) | [helper] | ≈ 0.38234 (Cambie: 0.3823455…, final verification partly numerical by the author's own description). |
| Liu, [arXiv:2306.08824](https://arxiv.org/abs/2306.08824) | [helper] | A constant strictly above 0.3823455 (Thm 6); ≈ 0.382709 conditional on two numerically checked hypotheses (Thm 13). |
| Jiang, [arXiv:2609.08291](https://arxiv.org/abs/2609.08291) | [read], pp. 1–4, 6–7, 11, 14, 16–17, 20–23 | Thm 1.1: fraction ≥ 1531541/4000000 = 0.38288525. Computer-assisted (interval arithmetic), single-author preprint, unrefereed; I did not re-run its program. |

### 1.2 Why it stops near 0.38

There are two separate facts, and they are often blurred.

**(a) The independent-sample inequality is sharp at ψ [read: Sawin Thm 2,
Examples 4–5].** The method needs H(A∪B) > H(A) whenever all marginals are
below the target constant. Take the coordinates of A independent, each
present with probability u. Then H(A) = nH(u) and H(A∪B) = nH(2u−u²). The
ratio H(2u−u²)/H(u) exceeds 1 exactly when u < ψ, because ψ is the root of
2u − u² = 1 − u. So for u ∈ (ψ, 1/2) there are product distributions with all
marginals below 1/2 for which the union of two independent samples has
**less** entropy than one sample. No inequality of the form "independent
samples, marginals ≤ u ⇒ H(A∪B) > H(A)" can hold past ψ.

**(b) The conclusion itself fails past ψ for approximately union-closed
families [read: Chase–Lovett Example 1.4].** Let F₁ = {x ∈ {0,1}ⁿ : |x| =
ψn + n^{2/3}} and F₂ = {x : |x| ≥ (1−ψ)n}, F = F₁ ∪ F₂. Then F is
(1−o(1))-approximate union-closed, |F₂| = o(|F₁|), and every element lies in
at most a ψ + o(1) fraction of sets. The independent-sample argument uses
union-closure only through "A∪B ∈ F for almost all pairs", so it proves
Thm 1.3 for such families too. That theorem is optimal, so the argument
cannot be pushed past ψ **without using union-closure in a stronger way**.

**(c) Beyond ψ.** The later improvements use dependent pairs (A, C), which
escape (a). Each scheme then has its own proved ceiling:

- Sawin's scheme as posed: 0.3823455… [helper: Cambie].
- Jiang's "pointwise product" reduction: C* ≈ 0.38288526 [read: Jiang
  Prop. 4.1]. Jiang states that this is "a limit of the proof method, not an
  upper bound on the frequency in Frankl's conjecture" and that it "does not
  exclude stronger estimates from other entropy arguments or from global
  couplings".

**No source read proves that entropy arguments in general cannot reach 1/2.**
Sawin's Question 9 [read] asks whether, for every distribution with all
marginals below 1/2, some coupling of two copies has H(A∪B) > H(A); a
positive answer would imply the conjecture. It is stated as open. So "the
barrier near 0.38" is a barrier for the known schemes, not a theorem about
the method. The README's phrase "nudged it slightly higher" is accurate.

Related refuted statement: Gilmer's Conjecture 1 (adding a KL-divergence
term) is false [read: Sawin Prop. 6; helper: Ellis,
[arXiv:2211.12401](https://arxiv.org/abs/2211.12401), an explicit n = 2
counterexample].

### 1.3 Does it apply to μ or to valid families?

- It gives c(e) ≥ 0.38288525·n for some e, i.e. **μ ≥ −0.2342295·n**. This
  is negative for every family, so it gives nothing toward rung 1.
- None of these papers uses or mentions separation, singleton-freeness,
  strict majority, or an excess over half [helper, all nine papers;
  consistent with the parts I read]. The method treats the family as a
  uniform distribution and never sees the universe size.
- Jiang's Prop. 10.3 [read] adds a correction of order
  ln²(2N−1)/(N² ln² N) in the family size N. It tends to 0 and is far too
  small to matter here.

**Route to the rungs: none.** A method that is tight at ψ on product
measures cannot detect a margin of a few sets out of n.

---

## 2. The lattice formulation and structural special cases

### 2.1 The lattice form

[read: Bruhn–Schaudt, [arXiv:1309.3297](https://arxiv.org/abs/1309.3297),
§3.1, Conjecture 1.] Every finite lattice L with at least two elements has a
join-irreducible a with |[a)| ≤ |L|/2. This is equivalent to the
union-closed conjecture. The order dual reads: some meet-irreducible m has
|↓m| ≤ |L|/2. `docs/LITERATURE.md` Proposition L relates this to μ: for a
valid G, μ(G) ≥ λ(L(G)) = |L| − 2·min_m |↓m|.

Lattice classes for which it is proved:

| Class | Source | Read | Argument |
|---|---|---|---|
| Lower semimodular | Reinhold, Graphs Combin. 16 (2000) | [read via Bruhn–Schaudt Thm 3, proof reproduced there] | Pick a coatom b and a join-irreducible a ≰ b. The map [a) → L∖[a), x ↦ x∧b is injective. |
| Modular (hence distributive) | Abe–Nakano, Graphs Combin. 14 (1998) | [via Bruhn–Schaudt §3.2] | Not given in any text opened. |
| Distributive, geometric, complemented | Poonen 1992 | [via Bruhn–Schaudt §3.2] | Not given in any text opened. |
| Strong upper semimodular | Abe, Algebra Univers. 44 (2000) | [via Bruhn–Schaudt §3.2] | — |
| Upper semimodular with \|L\| > (5/8)·2^m, and planar upper semimodular | Czédli–Schmidt (2008) | [via Bruhn–Schaudt §3.2]; original host refused | — |
| L or its dual | folklore | [read: Bruhn–Schaudt §3.2] | Immediate from the formulation. |

The task also names relatively complemented, sectionally complemented and
dismantlable lattices. **No source for these was found or opened**, so no
claim is made about them.

**Why it stops.** Each proof builds an injection or a count that depends on
the covering structure of the class (Reinhold's needs "b a coatom ⇒ x∧b is a
lower cover of x"). General lattices have no such regularity, and upper
semimodular lattices are already open in general [read: Bruhn–Schaudt §3.2,
"this class seems to be much harder"].

**Margin.** All of these conclude "≤ half" with no excess [helper; matches
the Reinhold proof I read]. More fundamentally, Proposition L shows μ is not
a lattice invariant: min λ = 0 at every k [OBSERVED, k = 3..5,
`docs/LITERATURE.md` B.1], because a valid family can have a Boolean
lattice. So **no purely lattice-theoretic argument can prove rung 1**, let
alone rungs 2–3. An argument has to use the set representation: the
universe is exactly [k] and there are no singleton members.

### 2.2 Injections

[read: Bruhn–Schaudt §4.] If {x} ∈ A then A ↦ A + x injects the sets
avoiding x into those containing x, so x is abundant. One element of any
2-set member is abundant (Sarvate–Renaud [via Bruhn–Schaudt]). "The main
problem with the injection method is that we need to first identify an
element that is likely to be abundant."

The pattern breaks at 3-sets. Poonen's family A_k [read: Bruhn–Schaudt §4,
construction reproduced there] has 1 + 6k + 2^k sets, [k] is its unique
smallest set, and each i ∈ [k] lies in 1 + (2k+2) + 2^{k−1} sets, fewer than
half. Ellis–Ivan–Leader ([arXiv:2201.11484](https://arxiv.org/abs/2201.11484))
strengthen this: for every k there is a family whose unique smallest set has
size k and whose elements all have frequency (1+o(1))·log₂k/(2k) [helper].

**Valid families.** Valid families have no singletons, and a valid family
with a 2-set member already satisfies μ ≥ 0 by the 2-set result. Neither
gives strictness in the convention with ∅ ∈ G.

### 2.3 FC-families (local configurations)

[read: Bruhn–Schaudt Thm 16, attributed to Poonen.] For a union-closed L
with universe [k], the following are equivalent: (i) every union-closed
family containing L has an abundant element in [k]; (ii) there are reals
c₁..c_k ≥ 0 summing to 1 such that Σ c_i |K_i| ≥ |K|/2 for every
union-closed K ⊆ 2^[k] with K = L ⊎ K. Such an L is FC.

How it is used [helper: Pulaj–Wood,
[arXiv:2301.01331](https://arxiv.org/abs/2301.01331) §5]: split a family
F ⊇ L by the trace of its members outside [k]; each fibre satisfies (ii);
sum. This is a weighted averaging over the elements of L only.

Known FC-families and counts [helper: Morris,
[arXiv:math/0702348](https://arxiv.org/abs/math/0702348), Thms 1, 2, 12;
Pulaj–Wood Thms 2.2–2.5]: all FC-families on 5 elements are classified;
FC(3,5) = 3, FC(3,6) = 4, FC(4,6) = 7, FC(3,n) = ⌊n/2⌋ + 1, FC(4,7) = 10,
FC(4,8) = 12. Three 3-sets with a common element are FC (Vaughan
[via Bruhn–Schaudt]). All families containing four 3-subsets of a 7-set are
FC (Marić–Živković–Vučković [via Bruhn–Schaudt]).

Small universes [read: Bruhn–Schaudt §5.1; `docs/LITERATURE.md` A.2]:
m ≤ 7 (Poonen), ≤ 9 (Lo Faro; Morris), ≤ 10 (Marković), ≤ 11
(Bošnjak–Marković), ≤ 12 (Živković–Vučković). All use FC-families and
element weights plus case analysis.

**Why it stops.** A single 3-set is not FC (the family A_k above). Bruhn and
Schaudt [read, §4]: "it seems doubtful that we will be able to show that any
union-closed family always contains such a local configuration." The case
analysis also grows too fast with the universe.

**Margin.** Condition (ii) is a non-strict inequality, and the method
concludes "at least half". It is the only technique here that works with a
quantity of the same kind as μ: Morris tests (ii) through Σ_A (2|A∩[k]| − k)
with unit weights. That is the sum identity of `docs/THEORY.md` C.2
restricted to a sub-universe. **Lemma D is, in this sense, an FC-style
weighted averaging argument run over the whole universe with a cap in place
of 0.**

### 2.4 Small and large families

| Result | Source | Read |
|---|---|---|
| A counterexample has at least 4m − 1 sets, m the least universe size of any counterexample | Lo Faro (1994); Roberts–Simpson (2010) | [read: Bruhn–Schaudt Lemma 18]; re-derived in height-bounded form in Tian, [arXiv:2608.25147](https://arxiv.org/abs/2608.25147), Prop. 2.5 [read] |
| A smallest counterexample has at least three elements of frequency exactly (n₀−1)/2 | Norton–Sarvate (1993) | [read: Bruhn–Schaudt §7]; proof in the ∅-free convention in Tian Lemma 2.2 [read] |
| Separating, n ≤ 2m ⇒ Frankl | Falgas-Ravry, via Bruhn–Schaudt Thm 23 | [read] |
| Separating, n ≤ 2(m + m/(log₂m − log₂log₂m)) ⇒ Frankl | Maßberg, [arXiv:1508.05718](https://arxiv.org/abs/1508.05718) | [helper] |
| If "separating, n ≤ c·m ⇒ Frankl" held for some c > 2, every family would have an element of frequency ≥ (c−2)/(2(c−1))·n | Hu | [read: Bruhn–Schaudt Thm 24] |
| n ≥ ⌈(2/3)·2^m⌉ ⇒ Frankl (average frequency ≥ n/2) | Balla–Bollobás–Eccles (2013) | [read: Bruhn–Schaudt Thm 30]; original not opened |
| n ≥ (2/3 − 1/104)·2^m; n ≥ 2^{m−1}; n ≥ (1/2 − c)·2^m | Eccles [arXiv:1311.2298](https://arxiv.org/abs/1311.2298); Karpas [arXiv:1708.01434](https://arxiv.org/abs/1708.01434) | [helper] |
| Height ≤ 4 (∅-free convention, strict), hence height ≤ 5 with ∅ | Tian Thm 1.1, Cor. 1.2 | [read] |

A note on direction: the remark after Bruhn–Schaudt Thm 23 prints
"n ≤ 4m − 1". Lemma 18, Corollary 19 (4·13 − 1 = 51) and Tian's Remark 2.6
all give "at least", which is the direction used here.

Hu's theorem explains the cloning-plus-co-singleton device that
`docs/LITERATURE.md` B.6 connected to M_k: one clones elements and adds sets
U′ − x to separate the clones.

**The one unconditional margin bound for separating families.** The proof of
Bruhn–Schaudt Thm 23 [read] shows more than its statement. Order the
elements by frequency, x_m the most frequent. It constructs m distinct
members X₀, …, X_{m−1}, each containing x_m. So c(x_m) ≥ m and

> **μ(G) ≥ 2k − n for every separating union-closed family G on k elements
> with n members.**

This is my reading of a published proof, not a new result. It is the only
bound found that gives rung 1 on a non-trivial range: **μ ≥ 1 whenever
n ≤ 2k − 1.** [OBSERVED: no violation among all 4, 304 and 235,749 valid
families at k = 3, 4, 5; equality in 4, 81 and 1,951 of them. Brute force
with `enum_uc_leaves`, run this session, no certificate file.] It is far
from the table: M₆ has n = 11, so it gives μ ≥ 1 against the true 3, and
H₃ has n = 18 > 2k, so it gives nothing.

---

## 3. Average-set-size results

### 3.1 Reimer

[read: Bruhn–Schaudt Thm 21 and §6.4, Lemmas 27–29 as reported there;
Reimer's paper (Combin. Probab. Comput. 12 (2003) 89–93) itself not opened.]
For a union-closed family A with n sets,

  (1/n)·Σ_{A∈A} |A| ≥ (log₂ n)/2.

Technique: up-compression u_i (replace A by A + i when A + i ∉ A) preserves
union-closure, and iterating over all i gives an up-set. For an up-set the
total size is controlled by an edge-boundary count in the hypercube, and the
compression raises the total size by at most n(m − log₂ n).

What it gives: max_e c(e) ≥ n·log₂n/(2m). In the notation of this
repository, with Σ_e g(e) = 2Σ|A| − kn (`docs/THEORY.md` C.2),

  Σ_e g(e) ≥ n(log₂ n − k),  so  μ ≥ n(log₂ n − k)/k.

This is non-negative only when n = 2^k, i.e. for the power set. Bruhn and
Schaudt: "too weak for Frankl's conjecture as usually log₂(n) < m."

### 3.2 Separating families

[read: Bruhn–Schaudt Thm 22.] For a separating union-closed family on m
elements, the average frequency is at least (m+1)/2. Falgas-Ravry
([arXiv:1101.2589](https://arxiv.org/abs/1101.2589)) [helper]: ordered
frequencies satisfy d(i) ≥ i − 1, total weight ≥ C(m,2), with equality only
for the staircase.

As pure averaging this gives μ ≥ (k+1) − n, weaker than the 2k − n of 2.4.

### 3.3 Where averaging fails

[read: Bruhn–Schaudt Thm 26 and its proof.] The Hungarian family H^(n) is
the initial segment of length n of the finite subsets of ℕ, ordered by
largest element and then reverse colex. For every m > 1 and n = ⌊(2/3)·2^m⌋
its average frequency is strictly below n/2 (the sum of frequencies is
(m/2)·n − 1 for even m). With Balla–Bollobás–Eccles this makes (2/3)·2^m the
exact threshold for averaging.

[read: Bruhn–Schaudt §6.3.] Duffus–Sands: A = 2^V ∪ {V ∪ {w₁..w_i}} with
|V| = 2t and 2^t extra elements is separating, and its average relative
frequency tends to 0. So averaging over all elements cannot even give a
constant fraction.

Open, not refuted [read: Bruhn–Schaudt §6.5]: the Duffus–Sands question
whether (1/|U|)·Σ_u c^{|A_u|} ≥ c^{|A|/2} for some c > 1.

### 3.4 Averaging with a large smallest set

[read: Kabela–Polák–Teska,
[arXiv:2212.09279](https://arxiv.org/abs/2212.09279), Thm 5(3) and its
proof.] Let k and n be the sizes of the smallest and largest set of a
union-closed family without ∅, and f the number of elements in **more than**
half the sets. Then f ≥ min{n, 2k − n + 1}. The proof is two lines of
averaging: the total size exceeds k·|F|, while f elements contribute at most
|F| each and the rest at most |F|/2.

This is a proved strict statement, but only when the smallest set has more
than half the universe. Valid families contain ∅, and their smallest
non-empty member is usually small (2-sets in M_k).

### 3.5 Applies to μ? Route to the rungs?

- Averaging bounds Σ_e g(e), and μ ≥ (1/k)·Σ_e g(e). This is exactly the
  mechanism of Lemma D (`docs/THEORY.md` C.2, (∗)).
- It cannot prove rung 1 in general, for a structural reason visible in the
  attainers: in M_k the non-kept elements have g = k/2 − 2 while the kept
  ones have g = k/2, and in hub-like families the gap is larger. Whenever
  the family has rare elements, the average sits below the maximum, and the
  Duffus–Sands example shows the gap is unbounded.
- **It does suggest the right scope for Section C**: averaging can work on
  sub-classes where no element is rare. The all-co-singleton sector is such
  a class, since there every element lies in k − 1 of the k co-singletons.

---

## 4. Strengthenings known to be false, and why naive arguments fail

### 4.1 False strengthenings

| Statement | Status | Counterexample and source |
|---|---|---|
| Some element of a smallest set is abundant | False for size 3 | Poonen's A_k; Sarvate–Renaud [read: Bruhn–Schaudt §4]. Quantitatively, frequency (1+o(1))·log₂k/(2k): Ellis–Ivan–Leader [helper]. |
| The average frequency is at least n/2 | False | Hungarian family at n = ⌊(2/3)·2^m⌋ [read: Bruhn–Schaudt Thm 26]. |
| The average frequency is at least c·n for some c > 0 | False | Duffus–Sands [read: Bruhn–Schaudt §6.3]. |
| Smallest non-empty set of size k ⇒ at least k abundant elements (Cui–Hu S1) | False | An 11-set family on 9 elements due to a referee, in Cui–Hu, [arXiv:1711.04276](https://arxiv.org/abs/1711.04276) §4.1 [helper]; (k−1, k, n)-constructions for n − 4 ≥ k ≥ 3, n ≥ 9 in Kabela–Polák–Teska Thm 6(4) [read]. |
| Independent samples with marginals < 1/2 have H(A∪B) > H(A) | False for marginals in (ψ, 1/2) | Product measures [read: Sawin Example 4]. |
| Gilmer's Conjecture 1 (KL-divergence refinement) | False | Sawin Prop. 6 [read]; Ellis [helper]. |
| The conclusion with 1/2 for approximately union-closed families | False | Chase–Lovett Example 1.4 [read]. |
| Morris's conjecture on which generating families are FC | Disproved by Pulaj | [via Pulaj–Wood, helper] |

Not refuted, still open: Cui–Hu's k = 2 case (two abundant elements when the
smallest non-empty set has size ≥ 2), which Kabela–Polák–Teska Prop. 7
[read] place between Frankl's conjecture and Poonen's unique-abundant-element
conjecture; the Duffus–Sands generalised mean; the
Pulaj–Raymond–Theis f- and g-conjectures [helper].

No source read contains a refuted *monotone-injection* strengthening, and
none discusses a weighted or fractional version that is known to fail. I
make no claim about either.

### 4.2 Why induction fails

[read: Bruhn–Schaudt §4.] "The obvious first approach is to try an
induction, for instance on the number of member-sets. If, given a
union-closed family, we could delete one (or two) basis sets so that the
maximum frequency drops then, by induction, the original family would
satisfy the conjecture, too. Unfortunately, this is not always possible: in
a power set of sufficient size, deleting one or two basis sets will never
reduce the maximum frequency." They add that an induction would need a
strengthened hypothesis and "structural insight on those families with low
maximum frequencies", and that "so far, there are not even any good
candidates" for the extremal families (§4, §8).

The survey says nothing specific about restricting to A_x and its
complement, or about deleting an element, so I state no published
obstruction for those.

What *is* available as an inductive tool, and is used in every
minimal-counterexample paper:

- [read: Bruhn–Schaudt §2.] A ∖ {B} is union-closed exactly when B is a
  basis set (join-irreducible) or ∅.
- [read: Tian §7.] "Deleting any collection of join-irreducible members
  leaves a union-closed family."
- [read: Tian Lemma 2.2, after Norton–Sarvate.] Deleting an
  inclusion-minimal member, or a member minimal among those containing a
  given element, keeps union-closure; this is how three elements of
  frequency exactly half are forced in a smallest counterexample.

These deletions change every g(e) by ±1 per deleted set, so they move μ in a
controlled way. They are the natural device for comparing μ(G) with μ of a
sub-family, and Sections D and F will use them. **They are known; any
statement built on them needs its own novelty check.**

### 4.3 Why compression fails

[read: Bruhn–Schaudt §6.4.] Up-compression with respect to i preserves
union-closure, but "the up-compressed family u_i(A) is much too simple with
respect to the union-closed sets conjecture: the family satisfies it for
trivial reasons. Indeed, the element i always appears in at least half of
the member-sets of u_i(A)." Lo Faro's restricted variant compresses y only
inside A_x when y is dominated by x; it keeps union-closure and does not
raise any frequency above that of x, and it yields the 4m − 1 bound, but "it
is not clear whether it or a variant may be used to a more far-reaching
effect."

No source read discusses down-compression in this context, apart from its
use by Eccles for the total-size problem [helper]. I make no claim about it.

**For μ.** Up-compression moves frequencies up, so it can only raise μ and
cannot bound it from below. Lo Faro's variant preserves the maximum
frequency and the number of sets, hence preserves μ when x is the most
frequent element, but it destroys separation (it tends to make y a twin of
x), so it leaves the valid class.

### 4.4 Poonen's strict conjectures: what exactly is open

- **Conjecture 14** [read: Bruhn–Schaudt §4]: a separating union-closed
  family that is not a power set has an element in strictly more than half
  of its members. Rung 1 is its restriction to valid families.
- **Conjecture 15** [read: Bruhn–Schaudt §4]: a separating family with a
  unique abundant element a is {∅} ∪ {B + a : B ⊆ U − a}.
- Kabela–Polák–Teska [read, §1]: their Conjectures 2 and 3 (the
  unique-abundant-element conjectures, with and without twins) "are still
  open and little is known in terms of partial results."
- Carvalho–Machiavelo, [arXiv:2408.11213](https://arxiv.org/abs/2408.11213),
  Thm 5.3 [read, with proof]: "exactly half ⇒ power set" (their Conj. 5.2)
  is equivalent to the strict conjecture (their Conj. 5.1). The non-trivial
  direction is that Conj. 5.2 **implies Frankl's conjecture**. This is a
  reformulation, not a proved case. Their statement of Conj. 5.1 omits
  "separating"; as printed it fails for a power set with a cloned element,
  so I follow Bruhn–Schaudt's wording. Without Poonen's paper I cannot say
  which wording is his.
- Tian Thm 1.1 [read] is strict only in the ∅-free convention, where strict
  majority is the ordinary conjecture for F ∪ {∅}. It is not a case of
  Conjecture 14.

**No proved case of Conjecture 14 was found** beyond the range n ≤ 2k − 1
implicit in 2.4. Whether Poonen checked small universes for the strict
version remains unknown (0.3).

**Is any rung already a published theorem?** No.

- Rung 1 is a case of an open conjecture. Because μ ≥ 1 implies μ ≥ 0, and
  the standard reductions (Section B of this phase will check them) reduce
  Frankl's conjecture to valid families, **rung 1 for all k is at least as
  strong as Frankl's conjecture itself.** The same holds for rungs 2 and 3.
  This is the main thing the survey says about Sections D and E: a complete
  proof of any rung would settle a conjecture that has been open since 1979.
- Rungs 2 and 3 were not found in any form. No source minimises the excess
  over half at fixed universe size (`docs/LITERATURE.md` A.5), so there is
  nothing to cite and skip.

---

## 5. Summary table

| Approach | What it proves | Why it stops | Applies to μ / valid families? | Route to the rungs |
|---|---|---|---|---|
| Entropy (§1) | c(e) ≥ 0.38288525·n | Independent samples are sharp at ψ; approximate union-closed families attain ψ; each dependent scheme has its own ceiling. No proof that entropy cannot reach 1/2. | μ ≥ −0.234·n only. Blind to the universe, separation and singletons. | None. |
| Lattice classes (§2.1) | λ(L) ≥ 0 for lower semimodular, modular, geometric, … | Needs covering regularity. | No: min λ = 0 on valid families, so μ is not a lattice invariant. | None for rungs as stated. Lattice arguments must be combined with the set representation. |
| Injections (§2.2) | Abundant element given a 1- or 2-set | One must know where the abundant element is; fails for 3-sets. | Valid families have no 1-sets. Non-strict. | Only inside a class where the abundant element is identifiable (e.g. kept elements of block families). |
| FC-families, weights (§2.3) | Frankl for families containing an FC configuration; universes ≤ 12 | Not every family contains one; case explosion. | Same type of quantity as μ (weighted Σ of 2\|A∩[k]\| − k). Non-strict. | **Yes, for Section C**: Lemma D is this argument over the whole universe. Not for rungs 1–3 in general. |
| Small families (§2.4) | Frankl for separating families with n ≤ 2k (+ lower-order term) | Any factor c > 2 would give a constant fraction for all families (Hu). | **μ ≥ 2k − n** for separating families. | Rung 1 for n ≤ 2k − 1 only. |
| Large families (§2.4) | Frankl for n ≥ (1/2 − c)·2^k | Averaging is exact at (2/3)·2^k; Boolean-analytic methods need density. | Non-strict; valid families of that size exist but are not the minimisers. | None. |
| Reimer (§3.1) | Average size ≥ ½log₂n | log₂n < k. | μ ≥ n(log₂n − k)/k, negative unless n = 2^k. | None alone. |
| Averaging on separating families (§3.2–3.4) | Average frequency ≥ (k+1)/2; strict abundance when the smallest set is large | Rare elements pull the average below the maximum, without bound. | μ ≥ k + 1 − n; Kabela–Polák–Teska needs a large smallest set. | **Section C**: works where no element is rare. |
| Minimal counterexample (§2.4, §4.2) | n₀ ≥ 4m − 1; three elements at exactly half; height ≤ 5 with ∅ | Structure is only forced at the threshold. | The deletion lemmas compare μ of a family with μ of a sub-family. | **Sections D and F**: the natural tool for the lift/peel induction and for one-element deletions. Each use needs a novelty check. |
| Compression (§4.3) | Reimer's theorem; the 4m − 1 bound | Up-compression makes the conjecture trivial for the compressed family. | Raises μ or leaves the valid class. | None. |

---

## 6. What this means for the plan

1. **Rungs 1–3 are each at least as strong as Frankl's conjecture** (§4.4),
   subject to the scope check in Section B. Sections D and E should
   therefore be read as searches for the exact obstruction, for conditional
   statements ("if Frankl's conjecture holds, then …"), and for statements
   on universes of size ≤ 12, where the conjecture is a theorem
   (Živković–Vučković). They should not be expected to end in a proof.
2. **Section C has a real method.** Lemma D is weighted averaging in the
   style of Poonen's theorem and Morris. Averaging fails in general because
   of rare elements, and the all-co-singleton sector has none. The right
   question is what Σ_e g(e) can be shown to satisfy there at general k.
3. **Section F has real tools**: deletion of join-irreducible members and
   the degree-1 reduction. Both are standard devices, so the novelty of
   anything proved with them lies in the statement about μ, not in the
   device.
4. Unconditional bounds available today for a valid G on [k] with n members:

   μ(G) ≥ max( 2k − n,  n(log₂n − k)/k,  −0.2342295·n ).

   None of these is non-negative on the range 2k < n < 2^k, which contains
   every attainer at k = 7 except through the first term (the 12-member
   classes have 2k − n = 2).

## 7. Limits of this survey

- Poonen (1992) and Abe (2002) are unread (0.3). Poonen is the origin of
  rung 1 and of Theorem 16; a small-universe check of the strict conjecture
  in that paper would change the novelty picture for rung 1 at small k.
- Originals not opened, used only through a survey or a later paper:
  Reimer, Reinhold, Abe–Nakano, Czédli–Schmidt, Czédli–Maróti–Schmidt,
  Balla–Bollobás–Eccles, Lo Faro, Roberts–Simpson, Norton–Sarvate,
  Sarvate–Renaud, Vaughan, Marić–Živković–Vučković, Duffus–Sands, Hu.
- Opened only by a delegated reader, not re-opened by me: Gilmer,
  Alweiss–Huang–Sellke, Pebody, Yu, Cambie, Liu, Ellis, Morris, Pulaj–Wood,
  Falgas-Ravry, Maßberg, Eccles, Karpas, Cui–Hu, Ellis–Ivan–Leader.
- Jiang's preprint is unrefereed and its computation was not re-run.
- Two arXiv identifiers in my delegation briefs were wrong and were
  corrected by the reader: 1106.0369 is Balla's *Minimum density of
  union-closed families*, and Ellis–Ivan–Leader is 2201.11484.
- No citation-graph search was possible (as in `docs/LITERATURE.md`), so
  recent work that proves a strict or quantitative statement for a class of
  separating families may be missing. Three 2025–2026 items surfaced only
  as references inside Tian's preprint and were not opened: Bouchard,
  arXiv:2509.12537 (an averaging result for separating height-four
  families), Colbert (Order 43, 2026), and Hu (Discrete Math. 346, 2023).

## 8. Additions after Section A

Found during the novelty checks of Section C (2026-11-12). They were missed
by the survey above.

- **A weighted strengthening is false.** Wang,
  [arXiv:2609.25101](https://arxiv.org/abs/2609.25101) [read, full text;
  single-author preprint, September 2026, unrefereed]: there are weights
  w ≥ 0 on subsets of a finite set with w(∅) = 0 and
  w(A∪B) ≥ min{w(A), w(B)} such that every element carries less than ε of
  the total weight (Thm 1.3; quantitatively ≤ 1/m + (m−1)/(mr), Thm 1.4).
  The paper attributes the question to the Polymath11 discussion and says
  that Kahn's course notes already disprove the weighted statement with
  constant 1/2 [via Wang; neither source opened]. This contradicts the
  sentence in §4.1 that no weighted version is known to fail: **that
  sentence is wrong and is superseded by this entry.**
- **Minimal counterexamples in the lattice form.** Bouchard,
  [arXiv:2503.00277](https://arxiv.org/abs/2503.00277) [read, full text]:
  deleting any set of join-irreducible (or any set of meet-irreducible)
  elements of a finite lattice leaves a lattice (Thm 1.4), and a
  minimum-size counterexample has at most one doubly irreducible element
  (Thm 2.6), among other conditions. Relevant to §4.2 and to Sections D
  and F. The paper also cites a proof of the conjecture for dismantlable
  lattices (Joshi–Waphare–Kavishwar, Algebra Universalis 76 (2016)
  [via Bouchard]), which answers part of the gap noted in §2.1.
- **A stronger conjecture that is still open.** Marigo–Schipani,
  [arXiv:1603.01215](https://arxiv.org/abs/1603.01215) [read]: for a
  reduced union-closed family, Σ_{(A,B)} |A∩B| ≥ Σ_{(A,B)} |A∖B|
  (their Conjecture 4.2), which implies Frankl's conjecture. They also
  restate Poonen's strict conjecture for reduced families.
- **Not opened at all:** the Polymath11 threads on Gowers's blog (FUNC1 to
  FUNC4), which discuss strengthenings, variants and potential
  counterexamples at length.

**What this says about completeness.** The survey was built from the
Bruhn–Schaudt survey (2013) and from papers reachable by keyword. Three
relevant items surfaced only when a specific claim was searched for, and
one of them falsified a sentence of the survey. So the survey is reliable
for the pre-2015 literature and for the entropy line, and **incomplete for
2016–2026 work outside the entropy line**, in particular for the Polymath11
material and for recent preprints. A statement here of the form "no source
does X" should be read as "none of the sources listed does X".
