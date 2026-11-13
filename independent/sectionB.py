"""Section B: k <= 6.  Decisions at (3,0),(4,1),(5,2),(6,2) [expect UNSAT]
and (3,1),(4,2),(5,3),(6,3) [expect SAT], each with both solvers and with
and without symmetry breaking; then full labelled enumeration (no symmetry
breaking) at the feasible caps, with both solvers.
Repo values: labelled attainers 1, 48, 2484, 120 and classes 1, 8, 51, 1
(docs/THEORY.md rows k = 3..6; SESSION_2026-11-09.md)."""
import time
from common import (cpsat_solve, sat_solve, cpsat_enumerate, sat_enumerate,
                    check_family, orbit_classes)
from encode import Encoding

REPO = {3: (1, 1), 4: (48, 8), 5: (2484, 51), 6: (120, 1)}
CASES = [(3, 0), (4, 1), (5, 2), (6, 2), (3, 1), (4, 2), (5, 3), (6, 3)]
findings = []

for k, cap in CASES:
    expect = "UNSAT" if (k, cap) in [(3, 0), (4, 1), (5, 2), (6, 2)] else "SAT"
    for sb in (True, False):
        E = Encoding(k, cap, sb=sb)
        for name, fn in (("cpsat", cpsat_solve), ("cadical", sat_solve)):
            st, fam, dt = fn(E)
            st = {"INFEASIBLE": "UNSAT", "OPTIMAL": "SAT", "FEASIBLE": "SAT"}.get(st, st)
            line = f"k={k} cap={cap} sb={sb!s:5} {name:7}: {st:5} {dt:7.2f}s"
            if fam:
                ok, mu = check_family(fam, k)
                line += f"  witness: direct check valid={ok}, mu={mu}, n={len(fam)}"
                if not ok or mu > cap:
                    findings.append(line)
            if st != expect:
                findings.append(line + f"  EXPECTED {expect}")
            print(line, flush=True)

print()
for k, cap in [(3, 1), (4, 2), (5, 3), (6, 3)]:
    res = {}
    for name, fn in (("cpsat", cpsat_enumerate), ("cadical", sat_enumerate)):
        t = time.time()
        fams = fn(Encoding(k, cap))
        res[name] = set(fams)
        chk = [check_family(f, k) for f in fams]
        bad = sum(1 for ok, mu in chk if not ok or mu > cap)
        mus = sorted(set(mu for _, mu in chk))
        print(f"k={k} cap={cap} {name:7}: {len(fams)} labelled solutions in "
              f"{time.time() - t:.1f}s, mu values {mus}, direct re-check failures {bad}")
    same = res["cpsat"] == res["cadical"]
    fams = res["cpsat"]
    cls = orbit_classes(fams, k)
    closed = all(o == m for _, o, m in cls)
    rl, rc = REPO[k]
    verdict = "MATCH" if (len(fams), len(cls)) == (rl, rc) and same and closed else "MISMATCH"
    print(f"  solvers agree: {same}; {len(cls)} classes, union of full orbits: {closed}; "
          f"orbit sizes {sorted(o for _, o, _ in cls)}; repo {rl} labelled / {rc} classes: {verdict}")
    if verdict != "MATCH":
        findings.append(f"k={k} cap={cap}: {len(fams)} labelled / {len(cls)} classes vs repo {rl}/{rc}")
print()
print("SECTION B RESULT:", "ALL AS EXPECTED, ALL COUNTS MATCH" if not findings else "FINDINGS:\n" + "\n".join(findings))
