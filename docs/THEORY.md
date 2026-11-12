# Theory behind the search

This file states every definition, lemma and conjecture that the code and the
`SESSION_*.md` ledgers rely on, so the repository can be read without the
earlier unpublished notes. Results are tagged as in the ledgers:

- **[PROVED]**: hand proof given here.
- **[PROVED-EXH]**: exhaustive computation with a certificate in `results/`.
- **[OBSERVED]**: checked only at the stated k.
- **[FALSIFIED]**: killed by a computed counterexample.
- **[UNPROVED-IN-REPO]**: used by the code or the README, but no proof or
  certificate is in this repository. Section E lists every such item.

Nothing here proves or verifies Frankl's conjecture. The project studies the
margin μ on small universes, where the conjecture itself is already known.

---

## A. Definitions and the search space

### A.1 Conventions

The universe is [k] = {0, …, k−1}, written Z. Sets are bitmasks, and bit e
stands for element e, so Z = `(1 << k) - 1`. A *family* G is a set of subsets
of Z. Throughout:

- n = |G| counts **all** members, including ∅ and Z.
- c(e) = c_G(e) = #{A ∈ G : e ∈ A} (`member_counts`, `frankl_core.py`).
- g(e) = 2c(e) − n. Equivalently, g(e) = Σ_{A∈G} (+1 if e ∈ A, else −1).
  The C engines keep this vector in `g[]` and add ±1 per member. They leave
  out ∅ and Z, which contribute −1 and +1 to every g(e) and so cancel.

### A.2 Margin μ and cap

**μ(G) = max_e g(e) = max_e 2c(e) − n** (`mu`, `frankl_core.py`). Frankl's
conjecture for G is the statement μ(G) ≥ 0. min μ(k) is the minimum of μ over
all valid families on [k] (A.3).

A **cap** is an integer argument to every search engine and to `lemma_d2`.
A search "at cap c" looks only for families with μ ≤ c. At its leaves it
enforces g(e) ≤ c for every e, because prune A runs before the leaf test
(`mu_search.py` lines 61–64, `mu_search2.c` lines 79–80). "Sector s is closed
at cap c" means that no valid family in that sector has μ ≤ c.

### A.3 Valid

G is **valid at level k** if all of the following hold (`is_valid`,
`frankl_core.py` line 91):

1. ∅ ∈ G and Z ∈ G;
2. G is union-closed: A, B ∈ G ⇒ A ∪ B ∈ G;
3. G has no singleton members;
4. G is *separating*: the k incidence patterns
   e ↦ {A ∈ G : e ∈ A} are pairwise distinct (`is_separating`). So for every
   e ≠ f, some member contains exactly one of them.

Condition 4 is what makes μ a property of the *k-element* problem. Without it,
two indistinguishable elements could be merged.

### A.4 Co-singleton, the co-singleton set S, and sector s

A **co-singleton** is a set of size k−1, Z∖{x}. For a family G, its
**co-singleton set** is

  S(G) = {x ∈ Z : Z∖{x} ∈ G},  s = |S(G)|.

The **sector** of G is s. The ledgers write "sector s" or "s = …". By
Proposition A.7, every valid G has s ≥ 1. Sector s = 1 is the degree-1 sector,
and sectors s = 2..k are the core sectors. The code does not compute S(G) in
one named function. It appears as `S_mask` in the engines, and `classify.py`
counts it as `s` (members of popcount k−1).

### A.5 Degree-1 family and core

- G is **degree-1** (deg-1) if min_e c(e) = 1. Because Z ∈ G, a degree-1
  element e lies in Z and nowhere else. If G is separating, it has at most one
  such element: two of them would have the same pattern {Z}. `peel_compress`
  asserts this.
- G is a **core** if min_e c(e) ≥ 2 (`min_degree`, `frankl_core.py` line 112;
  also asserted in `classify.py`).

### A.6 Lift and peel

- **lift** (`lift`, `frankl_core.py` line 280). For G on [k−1], lift(G) =
  G ∪ {[k]}, a family on [k]. The new element k−1 lies only in the new top set.
- **peel** (`peel_compress`, `frankl_core.py` line 284). For a degree-1 valid
  G on [k] with degree-1 element e, delete the member Z, delete e from every
  remaining member (all of them avoid e), and relabel the elements above e
  down by one. The result is a family on [k−1].

Up to relabeling, peel and lift are inverse to each other. Section B proves
that they are bijections between degree-1 valid families at level k and valid
families at level k−1, and that lift raises μ by exactly 1.

### A.7 Maximal members

`maximal_members(G, k)` (line 358) returns the members of G ∖ {∅, Z} that are
not strictly contained in another member of G ∖ {∅, Z}.
`lemma_c_holds(G, k)` (line 368) returns whether every such maximal member has
size k−1. Lemma C (Section B) says this is always true for valid G.

### A.8 Top layer T

Fix k and a co-singleton set S with |S| = s ≥ 2. The engines' **candidate
list** is

  C_S = {m ⊆ Z : 2 ≤ |m| ≤ k−2 and S ⊄ m},

sorted by popcount descending, then by mask ascending (`mu_search.py` lines
28–30, `mu_search2.c` lines 159–165, `cmp_cand`). Its first block is the
**top candidate layer**

  L_S = {m ∈ C_S : |m| = k−2},  NC5 := |L_S|

The name NC5 comes from k = 7, where the top layer has popcount 5.

The **top layer** of a family G in sector S is T(G) = {m ∈ G : |m| = k−2}.
By Lemma C, T(G) ⊆ L_S (Section B). The code encodes T as an NC5-bit integer:
bit i is set iff `cands[i]` ∈ T. This is the `REP <bits>` value printed by
`orbits.c` and the `bits` argument of `mu_search*` with P = NC5. A run of
`mu_search2 k cap s pw limit S P bits` forces the first P candidates: bit i
set means "in G", and bit i clear means "not in G" (`run_S`, lines 174–188).
Driver sub-shards extend P past NC5 in the same way.

`t = |T|` throughout Section C.

Implementation limit (found this session; see Section D.3): `PREF_BITS` is a
signed 64-bit `long long` read with `atoll` in `mu_search.c`, `mu_search2.c`
and `mu_search3.c`. Prefixes with P > 63 are therefore not passed correctly.
For P ≤ 63 they are.

### A.9 Block families B(…) and the matching family M_k

`block_family(blocks, k)` (line 301). Let the blocks b_1, …, b_r partition
[k], each with |b_j| ≥ 2. The **kept** element of a block is its minimum.
Then

  B(b_1, …, b_r) = {all unions of blocks} ∪ {Z∖{x} : x not kept}.

In the README and ledgers, B(2,2,3) means block sizes 2, 2, 3 on consecutive
elements. The isomorphism class depends only on the multiset of sizes.

**M_k = B(2, …, 2)** for even k, with blocks {2i, 2i+1} (`matching_family`,
line 330).

**Proposition A.9 [PROVED].** If k ≥ 3, r ≥ 1 and every |b_j| ≥ 2, then B is
valid, n = 2^r + k − r, and μ(B) = k − r. In particular
μ(M_{2t}) = t for t ≥ 2, and μ(B(2,…,2,3)) = (k+1)/2 for odd k ≥ 5. Hence
min μ(k) ≤ ⌈k/2⌉ for all k ≥ 4 (the "block-family bound").

*Proof.* Validity. ∅ (the empty union) and Z (all blocks) are members. A
union of two block-unions is a block-union. A co-singleton united with
anything is itself or Z. There are no singletons: block-unions are empty or
have size ≥ 2, and co-singletons have size k−1 ≥ 2. Separation: elements of
different blocks are split by either block. Inside a block, a non-kept x is
the only element missing from Z∖{x}, so x is split from every other element.

Count. The 2^r block-unions are distinct, because the blocks are disjoint and
nonempty. No co-singleton equals a block-union: Z∖{x} would then make {x} a
block-union, which would need a block of size 1. So n = 2^r + (k − r).

Degrees. Let x lie in block j. Then x lies in 2^{r−1} block-unions, and in
every co-singleton except Z∖{x} when x is non-kept. A kept x has
c = 2^{r−1} + (k−r), so g = 2^r + 2(k−r) − 2^r − (k−r) = k − r. A non-kept x
has g = k − r − 2. So μ = k − r. All blocks of size 2 (plus one block of size 3
if k is odd) give r = ⌊k/2⌋. ∎

Checked numerically for k = 3..10 this session. Calibration also checks
M_4, M_6, M_8, B(2,2,3) and B(3,4) (`run_A_verify.py`). At k = 3 the bound is
not sharp: B(3) has μ = 2, while U2[3] = {∅, 011, 101, 110, 111} has μ = 1.

### A.10 What `mu_search` searches

**Proposition A.10 (search space).** Fix k, a cap c, and S ⊆ [k] with
|S| = s ≥ 2. `search_S(k, S, c)` (`mu_search.py`), and the C engines
`mu_search`, `mu_search2` and `mu_search3` run with that S and no prefix,
output exactly the valid families G on [k] with S(G) = S and μ(G) ≤ c. Each
such family is output once.

*Soundness [PROVED].* Every output has the form

  G = {∅, Z} ∪ {Z∖{x} : x ∈ S} ∪ M,  M ⊆ C_S.

- Union-closure. The engine adds candidates in list order. When it adds m, it
  rejects m if m ∪ x is not m, x, Z, a chosen candidate, or a co-singleton in
  S, for some earlier chosen x (lines 86–91). Every pair of chosen candidates
  is tested once, when the later one is added. Unions involving ∅, Z or a
  co-singleton are always members.
- No singletons: candidates have size ≥ 2, and co-singletons have size
  k−1 ≥ 2 once k ≥ 3.
- S(G) = S exactly: co-singletons outside S are never candidates, because
  candidates have size ≤ k−2.
- Separation. Each x ∈ S is the unique element missing from Z∖{x}. Elements
  outside S are tested pairwise at the leaf (lines 70–80).
- μ ≤ c: prune A at the leaf, as in A.2.

*Completeness.* Take a valid G with S(G) = S and μ(G) ≤ c. Every member other
than ∅, Z and the co-singletons has size 2..k−2. By Lemma C it lies below a
maximal member, which is a co-singleton Z∖{x} with x ∈ S, so it misses x.
Hence it lies in C_S. The branch that includes exactly M = G ∖ {∅, Z,
co-singletons} passes every closure test, because G is union-closed and
every union lies in G. It also passes the leaf tests. It remains to check that
no prune cuts that branch:

- Prune A (line 62): g(e) − #(remaining candidates avoiding e) > c. Each
  remaining candidate changes g(e) by +1 if it contains e and by −1 if not. So
  the final g(e) is at least the current g(e) minus that count. If the bound
  already exceeds c, the final g(e) does too. The prune is admissible.
- Prune B (line 65): Σ_e g(e) + Σ_remaining min(0, 2|m| − k) > kc. A
  candidate adds 2|m| − k to Σ_e g(e), and μ ≤ c forces Σ_e g(e) ≤ kc. The
  prune is admissible.
- `mu_search2/3` only. Pairwise prune P (lines 82–88), applied to
  g(e) + g(f). It uses the same argument with candidates avoiding both e and
  f, and is admissible. Dead candidates (lines 59–72): if x is chosen and a
  later m has u = m ∪ x ∉ {m, x, Z} ∪ chosen ∪ co-singletons, then u ⊋ x, so u
  comes earlier in the list and was already decided against. Or u is not a
  candidate at all (u ⊇ S, or |u| = k−1 with u ∉ S), and then u ∉ G by
  Lemma C. Either way m can never be added in this branch. Removing m from
  the counts behind prunes A, B and P keeps them admissible.

So completeness holds **given Lemma C** (proved in Section B). Uniqueness:
each family corresponds to one include/exclude path.

*Computational cross-checks (this session, not new certificates).* At k = 5,
cap 3, `mu_search.py` and `./mu_search` (pw 0) visit the same 226,410 nodes
and find the same 2,244 families. That equals the number of μ ≤ 3 cores among
all 235,749 valid families from brute force (`enum_uc_leaves`), and
`mu_search2` (pw 1) finds the identical set. At k = 6, `mu_search2` finds 0
cores at cap 2 and 120 at cap 3, all in the orbit of M_6.

### A.11 Orbit reduction

Every S of size s is the image of S_s = {0, …, s−1} under some permutation of
[k], and permutations preserve validity, μ and sector size. So the drivers
search only S_mask = (1 << s) − 1.

`orbits.c` lists one representative T for each orbit of subsets of L_S under
Stab(S) = Sym(S) × Sym([k]∖S). The function `gen` keeps exactly the
permutations that fix S_mask. It also checks that the orbit sizes sum to
2^NC5. A σ ∈ Stab(S) maps a valid family with co-singleton set S and top
layer T to a valid family with co-singleton set S, top layer σT, and the same
μ. So if the search over all families with top layer T finds nothing, the
same holds for every T′ in T's orbit. Searching one T per orbit with P = NC5
therefore closes the whole sector. This argument is **[PROVED]**.

FAM lines from orbit runs are one labeled family per hit, not per isomorphism
class. `classify.py` canonicalizes them under S_k and recovers labeled counts
as k!/|Aut|.

### A.12 Why sectors s = 2..k plus the degree-1 sector exhaust all valid families

**Proposition A.12 [PROVED, using Lemma C].** Let k ≥ 2 and let G be valid on
[k]. Then exactly one of the following holds:

- s = 1: then G is degree-1, and its degree-1 element is the unique x ∈ S(G);
- s ≥ 2: then G is a core.

Also, s ≥ 1 always.

*Proof.* G ∖ {∅, Z} is nonempty. Otherwise all k ≥ 2 elements would have
the same pattern {Z}, and G would not be separating. So G has a maximal
member, and by Lemma C it is a co-singleton: s ≥ 1.

If s = 1 with S(G) = {x}, then every proper member lies below the unique
maximal member Z∖{x}, so x lies only in Z, and c(x) = 1.

If s ≥ 2, then every e lies in Z and in at least s − 1 ≥ 1 co-singletons, so
c(e) ≥ 2.

Conversely, if c(e) = 1, then every co-singleton Z∖{y} with y ≠ e contains e,
so S(G) ⊆ {e}, and s = 1. ∎

Exhaustive computation agrees at k = 4 (`run_A_verify.py`, "trichotomy") and,
this session, at k = 3, 4, 5 over all valid families.

So the valid families on [k] are the disjoint union of:

- the degree-1 sector, which Section B reduces to level k−1; and
- the core sectors s = 2..k, each searched exhaustively by A.10 and A.11.

That is why a table "s = 2..k closed at cap c, plus degree-1 sector μ > c"
establishes min μ(k) > c.

---

## B. Lemma C and the degree-1 reduction

### B.1 Lemma C

**Lemma C [PROVED].** Let k ≥ 2 and let G be a union-closed, separating
family on [k] with Z ∈ G. Then every maximal member of G ∖ {∅, Z} has size
k − 1. Equivalently, every member of G other than Z lies below some
co-singleton of G.

This is the statement that `lemma_c_holds(G, k)` tests (`frankl_core.py`
line 368). It is also what `mu_search.py` uses (docstring, lines 3–8): a
member of size 2..k−2 must miss some x ∈ S(G), so the candidate list can
be restricted to C_S (A.8).

*Proof.* Let m be a maximal member of G ∖ {∅, Z}. Suppose for contradiction
that |Z ∖ m| ≥ 2, and pick y ≠ z, both outside m.

Let A ∈ G contain y. Then A ⊄ m, so A ∪ m strictly contains m. By
union-closure A ∪ m ∈ G. By maximality of m, A ∪ m cannot be a member of
G ∖ {∅, Z}, so A ∪ m = Z. Since z ∉ m, this forces z ∈ A.

So every member containing y also contains z. By symmetry, every member
containing z also contains y. Then y and z have the same incidence pattern,
which contradicts separation. Hence |Z ∖ m| ≤ 1, and |Z ∖ m| = 1 because
m ≠ Z.

For the second form: every A ∈ G ∖ {Z} lies below a maximal member of
G ∖ {∅, Z}, provided that set is nonempty, and that maximal member is a
co-singleton. If the set is empty, then G = {∅, Z}, which is not
separating when k ≥ 2. ∎

The proof uses neither "∅ ∈ G" nor "no singletons", so Lemma C holds for
every valid family.

*Checks.* `run_A_verify.py` checks Lemma C on all valid families at k = 3
and k = 4. This session it also held on all 235,749 valid families at
k = 5 (brute force with `enum_uc_leaves`, no certificate file).

*Where it is used.*

- Completeness of `mu_search` (A.10). A member m ⊇ S with |m| ≤ k−2 would
  lie below no co-singleton of G, so it cannot exist.
- The dead-candidate prune in `mu_search2/3` (A.10).
- The sector trichotomy (A.12).
- The assertion "compressed top missing (Lemma C violated?)" in
  `peel_compress`.

### B.2 The degree-1 sector is the set of lifts

**Proposition B.2 [PROVED].** Let k ≥ 3.

(a) If H is valid on [k−1], then lift(H) is valid on [k] and degree-1, and
its degree-1 element is k−1.

(b) If G is valid and degree-1 on [k], with degree-1 element e, then
peel(G) is valid on [k−1]. Inserting e back as a new element gives
lift(peel(G)), which is G up to the relabeling that moves e to position k−1.

(c) Consequently, G ↦ (e, peel(G)) is a bijection between labeled degree-1
valid families on [k] and pairs (e ∈ [k], H valid on [k−1]). So the
degree-1 sector at level k consists, up to isomorphism, of exactly the
lifts of the valid families at level k−1. There are k · #valid(k−1) labeled
degree-1 families.

*Proof.*

(a) Write Z_k = [k]. Then lift(H) contains ∅ and Z_k. It is union-closed:
unions inside H stay in H, and anything ∪ Z_k = Z_k. It has no singletons,
because the only new member Z_k has size k ≥ 2. For separation, the new
element k−1 has pattern {Z_k}. Every old element also lies in [k−1] ∈ H,
whose pattern differs from that. Two old elements are separated by a
member of H. Finally c(k−1) = 1.

(b) Since c(e) = 1, e lies only in Z. By A.12, S(G) = {e}, so Z∖{e} ∈ G.
Let G′ = G ∖ {Z}. Every member of G′ avoids e, so G′ is a family on
Z′ = Z∖{e}, and peel(G) is G′ relabeled.

- G′ contains ∅ and Z′.
- Union-closure: for A, B ∈ G′, A ∪ B ∈ G and A ∪ B ⊆ Z′ ≠ Z, so
  A ∪ B ∈ G′.
- No singletons: inherited from G.
- Separation: for y ≠ z in Z′, some member of G contains exactly one of
  them. That member is not Z, which contains both, so it lies in G′.

Re-adding Z and the element e gives back G.

(c) By (a) and (b), the two maps are inverse to each other. A separating
family has at most one degree-1 element (A.5), so e is determined by G. ∎

*Checks.* `run_A_verify.py` checks "peel image = all 4 valid k=3" at k = 4.
This session, exhaustively at k = 4 and 5: there are 16 = 4·4 and
1,520 = 5·304 degree-1 families, every peel lands in valid(k−1), and the
peel image is all of valid(k−1).

### B.3 Lifting raises μ by exactly 1

**Proposition B.3 [PROVED].** If H is valid on [k−1] with n = |H|, then
μ(lift(H)) = μ(H) + 1.

*Proof.* lift(H) has n + 1 members.

- Every old element e gains one member, Z_k, so its new value is
  2(c(e) + 1) − (n + 1) = g_H(e) + 1.
- The new element has c = 1, so its value is 2 − (n + 1) = 1 − n.

Every old e lies in [k−1] ∈ H, so c(e) ≥ 1 and g_H(e) ≥ 2 − n. Hence
μ(H) + 1 ≥ 3 − n > 1 − n, and the maximum is attained at an old element.
So μ(lift(H)) = μ(H) + 1. ∎

*Checks.* Exhaustively at k = 4 and 5 this session, for every valid H at
level k−1. Calibration also checks single cases: T4 = lift U2[3] and T5
have μ = 2 and 3.

### B.4 Consequences used in the README and the ledgers

**Corollary B.4 [PROVED].** For k ≥ 3,

  min{μ(G) : G degree-1 valid on [k]} = min μ(k−1) + 1,

and the degree-1 attainers are exactly the lifts of the min μ(k−1)
attainers.

*Proof.* Combine B.2(c) and B.3. ∎

It follows that:

1. **min μ(k) = min(min μ(k−1) + 1, min over the core sectors).** So
   min μ(k) ≤ min μ(k−1) + 1 always holds, and only the core sectors
   s = 2..k need searching at caps up to min μ(k−1).

2. **"The degree-1 sector at k = 8 has μ ≥ 5."** By B.4 this equals
   min μ(7) + 1. So it holds exactly when min μ(7) = 4, which is the k = 7
   row of the results table ([PROVED-EXH], Section D). The tag is therefore
   **[PROVED], conditional on the k = 7 row**, and it holds with equality.
   The degree-1 families at k = 8 with μ = 5 are exactly the lifts of the
   7 attainer classes at k = 7, one of which is lift(lift(M_6)).
   So minμ(8) ≥ 4 needs only the core sectors s = 2..8 at cap 3. That is
   what the 2026-11-09 ledger states.

3. **The k = 7 degree-1 attainers.** min μ(6) = 3 is attained only by the
   M_6 orbit (120 labeled; Section D, row k = 6). So the degree-1 sector at
   k = 7 attains μ = 4 only at lift(M_6), with 7 · 120 = 840 labeled
   families. This matches the 2026-11-09 classification (7 classes in
   total, 10,500 + 840 = 11,340 labeled).

4. **Small k, this session.** At k = 5, brute force finds 240 degree-1
   attainers, which is 5 × 48 = 5 × (# μ = 2 families at k = 4). At k = 6,
   the degree-1 sector has μ ≥ min μ(5) + 1 = 4 > 3. So all 120 k = 6
   attainers are cores, which agrees with the `mu_search2` count of 120.

Section B uses no [UNPROVED-IN-REPO] step.
