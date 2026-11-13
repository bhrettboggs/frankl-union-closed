"""Write the CNF for (k, cap) as DIMACS and refute it with CaDiCaL 1.9.5
(python-sat), saving the solver's DRAT proof.

  python3 proof.py K CAP OUTPREFIX [--sb-level 0|1|2] [--cosing]

writes OUTPREFIX.cnf and, if UNSAT, OUTPREFIX.drat (text DRAT).

Re-check (two independent steps):
  1. The CNF is the encoding of encode.py:
       python3 encode.py K CAP --sb | grep -v '^c' | md5sum
       grep -v '^c' OUTPREFIX.cnf | md5sum            (must agree)
  2. The proof refutes the CNF, with any DRAT checker, e.g. drat-trim
     (https://github.com/marijnheule/drat-trim):
       drat-trim OUTPREFIX.cnf OUTPREFIX.drat         (expect "s VERIFIED")
"""
import sys
import time

from pysat.solvers import Solver

from encode import Encoding

a = sys.argv[1:]
k, cap, pre = int(a[0]), int(a[1]), a[2]
sbl = int(a[a.index("--sb-level") + 1]) if "--sb-level" in a else 2
cos = "--cosing" in a
E = Encoding(k, cap, sb=sbl > 0, sb_level=max(sbl, 1), cosingletons=cos)
cnf = E.to_cnf("totalizer")
with open(pre + ".cnf", "w") as f:
    cnf.to_fp(f)
t = time.time()
with Solver(name="cadical195", bootstrap_with=cnf.clauses, with_proof=True) as s:
    r = s.solve()
    dt = time.time() - t
    print(f"k={k} cap={cap} sb_level={sbl} cosingletons={cos}: "
          f"{'SAT' if r else 'UNSAT'} in {dt:.1f}s; {cnf.nv} vars, "
          f"{len(cnf.clauses)} clauses", flush=True)
    if not r:
        n = 0
        with open(pre + ".drat", "w") as f:
            for line in s.get_proof():
                f.write(line + "\n")
                n += 1
        print(f"DRAT proof ({n} lines) written to {pre}.drat")
