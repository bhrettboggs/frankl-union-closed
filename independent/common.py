"""Helpers for the scripts in independent/: solving, enumeration and a
direct (non-SAT) re-check of each solution against the written definition.
Nothing here imports frankl_core or any other repo module."""
import time
from itertools import combinations, permutations


def check_family(fam, k):
    """(valid, mu), computed directly from the definition, without SAT."""
    full = (1 << k) - 1
    fs = set(fam)
    ok = 0 in fs and full in fs
    ok = ok and all(bin(S).count("1") != 1 for S in fs)
    ok = ok and all((A | B) in fs for A in fs for B in fs)
    for e, f in combinations(range(k), 2):
        if not any(((S >> e) & 1) != ((S >> f) & 1) for S in fs):
            ok = False
    n = len(fs)
    mu = max(2 * sum(1 for S in fs if S >> e & 1) - n for e in range(k))
    return ok, mu


# ---------------------------------------------------------------- CP-SAT
def cpsat_solve(enc, workers=4, limit=None, log=False, logfile=None):
    from ortools.sat.python import cp_model
    m, x = enc.to_cpsat()
    s = cp_model.CpSolver()
    s.parameters.num_workers = workers
    if limit:
        s.parameters.max_time_in_seconds = limit
    if log or logfile:
        s.parameters.log_search_progress = True
        s.parameters.log_to_stdout = logfile is None
        if logfile is not None:
            s.log_callback = lambda line: (logfile.write(line + "\n"), logfile.flush())
    st = s.Solve(m)
    fam = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        fam = tuple(S for S in range(enc.N) if s.Value(x[enc.var(S)]))
    return s.StatusName(st), fam, s.WallTime()


def cpsat_enumerate(enc):
    """All solutions (enc must have no auxiliary variables, i.e. sb=False)."""
    from ortools.sat.python import cp_model
    assert enc.nextvar == enc.N + 1 and not enc.condcards
    m, x = enc.to_cpsat()
    out = []

    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            out.append(tuple(S for S in range(enc.N) if self.Value(x[enc.var(S)])))

    s = cp_model.CpSolver()
    s.parameters.enumerate_all_solutions = True
    s.parameters.num_workers = 1
    st = s.Solve(m, CB())
    assert s.StatusName(st) in ("OPTIMAL", "INFEASIBLE"), s.StatusName(st)
    assert len(set(out)) == len(out)
    return out


# ---------------------------------------------------------- python-sat
def sat_solve(enc, solver="cadical195", cardenc="totalizer"):
    from pysat.solvers import Solver
    t = time.time()
    with Solver(name=solver, bootstrap_with=enc.to_cnf(cardenc).clauses) as s:
        r = s.solve()
        fam = enc.decode(set(l for l in s.get_model() if l > 0)) if r else None
    return ("SAT" if r else "UNSAT"), fam, time.time() - t


def sat_enumerate(enc, solver="cadical195", cardenc="totalizer"):
    from pysat.solvers import Solver
    out = []
    with Solver(name=solver, bootstrap_with=enc.to_cnf(cardenc).clauses) as s:
        while s.solve():
            fam = enc.decode(set(l for l in s.get_model() if l > 0))
            out.append(fam)
            s.add_clause(enc.block(fam))
    return out


# ------------------------------------------------------------ symmetry
def relabel(fam, perm):
    out = []
    for S in fam:
        T = 0
        for e, p in enumerate(perm):
            if S >> e & 1:
                T |= 1 << p
        out.append(T)
    return tuple(sorted(out))


def orbit_classes(fams, k):
    """Partition labelled families into S_k-orbits by generating each orbit
    explicitly.  Returns [(representative, orbit size, #inputs in orbit)]."""
    remaining = set(tuple(sorted(f)) for f in fams)
    perms = list(permutations(range(k)))
    classes = []
    while remaining:
        rep = min(remaining)
        orb = {relabel(rep, p) for p in perms}
        inside = orb & remaining
        remaining -= orb
        classes.append((rep, len(orb), len(inside)))
    return classes
