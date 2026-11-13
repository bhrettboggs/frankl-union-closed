"""Explicit families, built from their written definitions
(docs/PROOF_ATTEMPT.md, Section F notation), not from frankl_core.

M_2t on Z = [2t]: blocks P_i = {a_i, b_i} with a_i = 2i, b_i = 2i+1,
members U_J = union of P_i over i in J (all J subset of [t], so U_empty =
empty set and U_[t] = Z) and C_i = Z - {b_i}.  |M_2t| = 2^t + t."""
from itertools import combinations


def matching_family(t):
    k = 2 * t
    Z = (1 << k) - 1
    P = [(1 << (2 * i)) | (1 << (2 * i + 1)) for i in range(t)]
    fam = set()
    for r in range(t + 1):
        for J in combinations(range(t), r):
            U = 0
            for i in J:
                U |= P[i]
            fam.add(U)
    for i in range(t):
        fam.add(Z ^ (1 << (2 * i + 1)))
    return tuple(sorted(fam))


def extension_constraints(H, k):
    """Constraints on families G on [k+1] (new point x = k) with
    G - x = H, where G - x = {A - {x} : A in G}.
    For S subset of [k]:  S notin H  =>  S, S+x not in G;
                          S in H     =>  S in G or S+x in G.
    Returns (fix, clauses) in the format of encode.Encoding."""
    X = 1 << k
    Hs = set(H)
    fix, clauses = {}, []
    for S in range(1 << k):
        if S in Hs:
            clauses.append([(S, True), (S | X, True)])
        else:
            fix[S] = False
            fix[S | X] = False
    return fix, clauses


def delete_point(G, x):
    """G - x, re-indexed to [k-1] (elements above x shift down by one)."""
    out = set()
    lo = (1 << x) - 1
    for A in G:
        out.add((A & lo) | ((A >> (x + 1)) << x))
    return tuple(sorted(out))


def named_extensions(t):
    """The t+4 families of PROOF_ATTEMPT.md Prop. F2, built from the (B, D, E)
    table:  G = (B u D) u {A + x : A in D u E}, x = 2t, on [2t+1].
    Returns {name: family}."""
    k = 2 * t
    Z = (1 << k) - 1
    X = 1 << k
    P = [(1 << (2 * i)) | (1 << (2 * i + 1)) for i in range(t)]

    def U(J):
        u = 0
        for i in J:
            u |= P[i]
        return u

    C = [Z ^ (1 << (2 * i + 1)) for i in range(t)]
    Js = [J for r in range(t + 1) for J in combinations(range(t), r)]
    H = set(matching_family(t))
    rows = {}
    for j in range(t + 1):
        D = {Z}
        E = set(C[:j])
        rows[f"I({t},{j})"] = (H - D - E, D, E)
    E = {U(J) for J in Js if t - 1 in J and len(J) < t} | set(C[:t - 1])
    rows[f"II({t})"] = ({U(J) for J in Js if t - 1 not in J} | {C[t - 1]}, {Z}, E)
    E = {U(J) for J in Js if t - 1 in J and len(J) < t} | set(C)
    rows[f"B(2..2,3) t={t}"] = ({U(J) for J in Js if t - 1 not in J}, {Z}, E)
    rows[f"H_{t}"] = ({0}, {U(J) for J in Js if J}, set(C))
    out = {}
    for name, (B, D, E) in rows.items():
        assert B | D | E == H and not (B & D) and not (B & E) and not (D & E), name
        out[name] = tuple(sorted((B | D) | {A | X for A in D | E}))
    return out
