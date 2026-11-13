"""Decide "is there a valid family on [k] with mu <= cap?" with CP-SAT.
  python3 decide.py K CAP [--workers W] [--limit SECONDS] [--sb-level 0|1|2]
                          [--cosing] [--log FILE]
sb-level 0 = no symmetry breaking.  Prints one RESULT line; with --log the
full CP-SAT search log is written to FILE."""
import sys, time, platform
from common import cpsat_solve, check_family
from encode import Encoding
import ortools

a = sys.argv[1:]
k, cap = int(a[0]), int(a[1])
opt = lambda name, d: type(d)(a[a.index(name) + 1]) if name in a else d
workers, limit, sbl = opt("--workers", 4), opt("--limit", 0.0), opt("--sb-level", 2)
logname = opt("--log", "")
cos = "--cosing" in a
E = Encoding(k, cap, sb=sbl > 0, sb_level=max(sbl, 1), cosingletons=cos)
hdr = (f"k={k} cap={cap} cosingletons={cos} sb_level={sbl} workers={workers} "
       f"limit={f'{limit}s' if limit else 'none'} ortools={ortools.__version__} python={platform.python_version()}")
print(hdr, flush=True)
lf = open(logname, "w") if logname else None
if lf:
    lf.write(hdr + "\n")
t = time.time()
st, fam, wall = cpsat_solve(E, workers=workers, limit=limit or None, logfile=lf)
line = f"RESULT k={k} cap={cap} cosingletons={cos}: {st} wall={wall:.1f}s"
if fam:
    ok, mu = check_family(fam, k)
    line += f" witness n={len(fam)} direct-check valid={ok} mu={mu} members={list(fam)}"
print(line, flush=True)
if lf:
    lf.write(line + "\n"); lf.close()
