"""Independent encoding of "valid family on [k] with margin <= cap".

This file shares no code with frankl_core.py, mu_search*.c or orbits*.c.
Validity is re-implemented from the written definition:

  A family G of subsets of [k] = {0, ..., k-1} is VALID if
    (V1) the empty set and [k] are members,
    (V2) no member is a singleton,
    (V3) G is union-closed: A, B in G  =>  A | B in G,
    (V4) G is separating: for every pair e != f some member contains
         exactly one of e, f.
  The margin is mu(G) = max_e (2 c(e) - |G|), c(e) = #{A in G : e in A}.

Sets are bitmasks: bit e of S is set iff e is in S.

One 0/1 variable per subset: x_S = S + 1 for S = 0 .. 2^k - 1 ("S is a
member").  The constraints are generated once, as clauses plus cardinality
constraints, and handed to one of two pip-installable solvers:

  * CP-SAT from OR-Tools (pip "ortools", tested 9.15.6755): clauses become
    BoolOr, cardinality constraints become linear constraints.  Fast; used
    for the k = 7, 8 decisions and most enumerations.  No proof output.
  * CaDiCaL 1.9.5 via python-sat (pip "python-sat", tested 1.9.dev22):
    cardinality constraints compiled to CNF with pysat.card (totalizer by
    default).  Slower; used to cross-check, and to produce DRAT proofs
    (the DIMACS file is written by to_dimacs()).

Constraints
-----------
(V1)  units x_0, x_[k].
(V2)  units -x_{e} for every singleton {e}.
(V3)  for every pair S, T of sets of size >= 2, neither containing the
      other, with S|T != [k]:  (-x_S | -x_T | x_{S|T}).  (Pairs where one
      contains the other have union in {S, T}; pairs involving the empty
      set or a singleton are covered by (V1)/(V2); unions equal to [k] are
      true by (V1).)
(V4)  for every e < f: OR of x_S over S containing exactly one of e, f.
(CAP) for every e:  2c(e) - n <= cap, i.e.
      sum_{S ni e} x_S - sum_{S not ni e} x_S <= cap.

Symmetry breaking (sb=True), two parts
--------------------------------------
(SB1) c(0) >= c(1) >= ... >= c(k-1).
(SB2) for each i < j:  c(i) = c(j)  =>  x >=_lex tau(x), where tau is the
      transposition (i j) acting on families, and >=_lex compares the 0/1
      vectors (x_0, x_1, ..., x_{2^k-1}) at the smallest index first.
      (With sb_level=1 only adjacent j = i+1 are used.)  tau swaps x_S and
      x_{S'} for S containing i but not j, S' = S - {i} + {j} > S, and fixes
      all other coordinates.  So the first coordinate where x and tau(x)
      differ is the smallest such S with x_S != x_{S'}, and
      x >=_lex tau(x) says x_S = 1, x_{S'} = 0 there.  Encoded with chain
      variables q_0, q_1, ... ("all earlier pairs equal"):
      q_0 <- tie_i & ... & tie_{j-1};  q_t -> (x_S | -x_S');
      q_t & (x_S <-> x_S') -> q_{t+1}.
      tie_i is a fresh variable with  (not tie_i) -> c(i) - c(i+1) >= 1, so
      under (SB1) c(i) = c(j) forces tie_i = ... = tie_{j-1} = true.

  WHY THIS IS SOUND.  The symmetric group on [k] acts on families by
  relabelling elements.  (V1)-(V4) and (CAP) are invariant: relabelling
  maps the empty set, [k], singletons, unions and separated pairs to
  objects of the same kind, keeps n and permutes the degrees c(e), so
  max_e 2c(e) - n is unchanged.  (The co-singleton option and the
  "contains all of a given list" constraints used below are also invariant
  or are only used with sb=False.)  Take any solution G.  Among all
  relabellings pi(G) whose degree sequence is non-increasing (there is at
  least one: sort the elements by degree), let R be the one whose vector
  x(R) is lexicographically largest.  R satisfies (SB1) by choice.  If
  c_R(i) = c_R(j), then tau(R) has the same, non-increasing, degree
  sequence, so x(R) >=_lex x(tau(R)) by maximality: (SB2) holds.  Setting
  tie_t true exactly when c_R(t) = c_R(t+1) and the chain variables to
  their intended meaning satisfies every auxiliary clause.  So
  every orbit of solutions contains a solution satisfying (SB1)+(SB2), and
  the formula with symmetry breaking is satisfiable iff it is without.
  Symmetry breaking must NOT be used when counting labelled solutions, and
  must not be combined with constraints that are not invariant under S_k
  (e.g. "G - x = M_6"); the scripts here never do either.

Other options:
  cosingletons=True  adds units x_{[k]-{e}} for every e (the all-co-singleton
                     sector of docs/PROOF_ATTEMPT.md, Section C).
  cap=None           omits (CAP).
  fix={S: bool}      extra unit constraints (used for one-point extensions).
  clauses=[[...]]    extra clauses over set variables, as lists of
                     (S, polarity) pairs.

Usage as a script:
  python3 encode.py K CAP [--sb] [--cosing] [--enc totalizer] > out.cnf
writes DIMACS CNF (for any DIMACS SAT solver / DRAT-producing solver).
"""
import sys
from itertools import combinations


def popcount(x):
    return bin(x).count("1")


class Encoding:
    def __init__(self, k, cap, sb=False, cosingletons=False, fix=None,
                 clauses=None, sb_level=2):
        self.k, self.cap = k, cap
        self.sb_level = sb_level
        self.N, self.full = 1 << k, (1 << k) - 1
        self.nextvar = self.N + 1
        self.fixed = {}          # S -> bool
        self.clauses = []        # lists of DIMACS literals
        self.cards = []          # (lits, bound, kind): sum(lits) kind bound
        self.condcards = []      # (lits, bound, guard): guard false -> sum(lits) >= bound
        self._build(sb, cosingletons, fix or {}, clauses or [])

    # ---- variables ----------------------------------------------------
    def var(self, S):
        return S + 1

    def newvar(self):
        v = self.nextvar
        self.nextvar += 1
        return v

    def _fix(self, S, val):
        if self.fixed.get(S, val) != val:
            raise ValueError(f"contradictory fixing of {S}")
        self.fixed[S] = val
        self.clauses.append([self.var(S) if val else -self.var(S)])

    def lit(self, S, pol=True):
        return self.var(S) if pol else -self.var(S)

    # ---- construction ---------------------------------------------------
    def _build(self, sb, cosingletons, fix, extra):
        k, N, full = self.k, self.N, self.full
        self._fix(0, True)                                   # (V1)
        self._fix(full, True)
        for e in range(k):                                   # (V2)
            self._fix(1 << e, False)
        if cosingletons:
            for e in range(k):
                self._fix(full ^ (1 << e), True)
        for S, v in sorted(fix.items()):
            self._fix(S, v)
        mids = [S for S in range(N) if popcount(S) >= 2 and S != full]
        for S, T in combinations(mids, 2):                   # (V3)
            U = S | T
            if U in (S, T) or U == full:
                continue
            self.clauses.append([-self.var(S), -self.var(T), self.var(U)])
        for e, f in combinations(range(k), 2):               # (V4)
            m = (1 << e) | (1 << f)
            self.clauses.append([self.var(S) for S in range(N)
                                 if popcount(S & m) == 1])
        if self.cap is not None:                             # (CAP)
            for e in range(k):
                lits = [self.var(S) if S >> e & 1 else -self.var(S)
                        for S in range(N)]
                # sum_{S ni e} x_S + sum_{S not ni e} (1 - x_S) <= cap + 2^(k-1)
                self.cards.append((lits, self.cap + N // 2, "<="))
        for cl in extra:
            self.clauses.append([self.lit(S, p) for S, p in cl])
        if sb:
            assert not fix and not extra, "sb needs an S_k-invariant formula"
            self._sb()

    def _sb(self):
        k, N = self.k, self.N
        deg_lits = {}
        for i in range(k - 1):
            a, b = 1 << i, 1 << (i + 1)
            P = [S for S in range(N) if S & a and not S & b]
            # (SB1)  c(i) - c(i+1) = sum_P x_S - sum_P x_{S'} >= 0
            lits = [self.var(S) for S in P] + [-self.var(S ^ a ^ b) for S in P]
            self.cards.append((lits, len(P), ">="))
            # tie_i false -> c(i) - c(i+1) >= 1
            tie = self.newvar()
            self.condcards.append((lits, len(P) + 1, tie))
            deg_lits[i] = tie
        # (SB2) for every i < j: if c(i) = ... = c(j) then x >=_lex (i j) x.
        # (c(i) = c(j) under (SB1) means tie_i = ... = tie_{j-1} hold.)
        for i in range(k - 1):
            for j in range(i + 1, k):
                if self.sb_level < 2 and j != i + 1:
                    continue
                a, b = 1 << i, 1 << j
                P = [S for S in range(N) if S & a and not S & b]
                q = self.newvar()   # q_0 <- tie_i & ... & tie_{j-1}
                self.clauses.append([q] + [-deg_lits[t] for t in range(i, j)])
                for t, S in enumerate(P):
                    xs, xt = self.var(S), self.var(S ^ a ^ b)
                    self.clauses.append([-q, xs, -xt])
                    if t + 1 < len(P):
                        q2 = self.newvar()
                        self.clauses.append([-q, xs, xt, q2])
                        self.clauses.append([-q, -xs, -xt, q2])
                        q = q2

    # ---- decoding / blocking -------------------------------------------
    def decode(self, true_vars):
        return tuple(S for S in range(self.N) if self.var(S) in true_vars)

    def block(self, fam):
        """Clause excluding exactly this family on the set variables."""
        fs = set(fam)
        return [(-self.var(S) if S in fs else self.var(S))
                for S in range(self.N) if S not in self.fixed]

    # ---- backend: CNF (python-sat) -------------------------------------
    def to_cnf(self, enc="totalizer"):
        from pysat.card import CardEnc, EncType
        from pysat.formula import CNF, IDPool
        et = getattr(EncType, enc)
        pool = IDPool(start_from=self.nextvar)
        cnf = CNF(from_clauses=[list(c) for c in self.clauses])
        fixedlit = {}
        for S, v in self.fixed.items():
            fixedlit[self.var(S)] = v
            fixedlit[-self.var(S)] = not v

        def fold(lits, bound):
            free = []
            for l in lits:
                if l in fixedlit:
                    bound -= 1 if fixedlit[l] else 0
                else:
                    free.append(l)
            return free, bound

        def false():
            v = pool.id(("false",))
            cnf.extend([[v], [-v]])

        for lits, bound, kind in self.cards:
            free, bd = fold(lits, bound)
            if kind == "<=":
                if bd < 0:
                    false(); continue
                if bd >= len(free):
                    continue
                cnf.extend(CardEnc.atmost(free, bound=bd, vpool=pool, encoding=et).clauses)
            else:
                if bd <= 0:
                    continue
                if bd > len(free):
                    false(); continue
                cnf.extend(CardEnc.atleast(free, bound=bd, vpool=pool, encoding=et).clauses)
        for lits, bound, guard in self.condcards:
            # guard OR (sum >= bound): add the literal guard to every clause
            # of the CNF encoding of sum >= bound.
            free, bd = fold(lits, bound)
            if bd <= 0:
                continue
            if bd > len(free):
                cnf.append([guard]); continue
            c = CardEnc.atleast(free, bound=bd, vpool=pool, encoding=et)
            cnf.extend([cl + [guard] for cl in c.clauses])
        return cnf

    def to_dimacs(self, fp, enc="totalizer", comments=()):
        self.to_cnf(enc).to_fp(fp, comments=list(comments))

    # ---- backend: CP-SAT -------------------------------------------------
    def to_cpsat(self):
        from ortools.sat.python import cp_model
        m = cp_model.CpModel()
        nv = self.nextvar
        x = [None] + [m.NewBoolVar(f"v{i}") for i in range(1, nv)]

        def L(l):
            return x[l] if l > 0 else x[-l].Not()

        for cl in self.clauses:
            m.AddBoolOr([L(l) for l in cl])
        for lits, bound, kind in self.cards:
            expr = sum(x[l] if l > 0 else 1 - x[-l] for l in lits)
            m.Add(expr <= bound) if kind == "<=" else m.Add(expr >= bound)
        for lits, bound, guard in self.condcards:
            expr = sum(x[l] if l > 0 else 1 - x[-l] for l in lits)
            m.Add(expr >= bound).OnlyEnforceIf(x[guard].Not())
        return m, x


if __name__ == "__main__":
    args = sys.argv[1:]
    k, cap = int(args[0]), args[1]
    cap = None if cap == "none" else int(cap)
    enc = args[args.index("--enc") + 1] if "--enc" in args else "totalizer"
    E = Encoding(k, cap, sb="--sb" in args, cosingletons="--cosing" in args)
    E.to_dimacs(sys.stdout, enc=enc, comments=[
        f"c valid families on [{k}], cap {cap}, sb={'--sb' in args}, "
        f"cosingletons={'--cosing' in args}, cardinality encoding {enc}",
        "c variable S+1 <-> subset S (bitmask) is a member"])
