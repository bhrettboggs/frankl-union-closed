"""Section D, part 2: cap 4 is feasible at k = 8, witnessed by the matching
family M_8 (built in families.py from its written definition).
Checked twice: directly from the definition, and by the encoding (all 256
set variables fixed to M_8's membership; the solver must report SAT).
Part 1 (cap 3 at k = 8) is the time-boxed run:
  python3 decide.py 8 3 --workers 4 --limit 43200 --log results/k8_cap3_cpsat.log"""
from common import check_family, cpsat_solve, sat_solve
from encode import Encoding
from families import matching_family

M8 = matching_family(4)
v, mu = check_family(M8, 8)
print(f"M_8: n={len(M8)} members={list(M8)}")
print(f"direct check: valid={v} mu={mu}")
fix = {S: (S in set(M8)) for S in range(256) if S not in (0, 255) and bin(S).count('1') != 1}
E = Encoding(8, 4, fix=fix)
st1, fam1, _ = cpsat_solve(E)
st2, fam2, _ = sat_solve(E)
print(f"encoding with all variables fixed to M_8, cap 4: cpsat {st1}, cadical {st2}; "
      f"models equal M_8: {fam1 == M8 and fam2 == M8}")
E3 = Encoding(8, 3, fix=fix)
print(f"same at cap 3 (expect infeasible, mu(M_8) = 4): cpsat {cpsat_solve(E3)[0]}")
ok = v and mu == 4 and st1 == "OPTIMAL" and st2 == "SAT" and fam1 == M8 == fam2
print("SECTION D (cap 4 feasible at k=8):", "VERIFIED" if ok else "FAILED")
