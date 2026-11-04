"""orbit_driver.py k s [budget_s] [pw]
Runs ./mu_search k 3 s pw 0 S_mask NC5 T for every orbit representative T of the
top (pc k-2) layer under Stab(S), S = {0..s-1}. Resumable via log file
orb_k{k}_s{s}.log (one 'R idx T nodes found' line per completed rep, FAM lines
verbatim). Budget guard stops cleanly; rerun to continue.
"""
import sys, subprocess, time, os

k = int(sys.argv[1]); s = int(sys.argv[2])
budget = float(sys.argv[3]) if len(sys.argv) > 3 else 185.0
pw = sys.argv[4] if len(sys.argv) > 4 else "1"
S_mask = (1 << s) - 1
log = f"orb_k{k}_s{s}.log"

out = subprocess.run(["./orbits", str(k), str(S_mask)], capture_output=True, text=True).stdout
lines = out.splitlines()
NC5 = int(lines[0].split()[1])
reps = [(int(p[1]), int(p[2])) for p in (l.split() for l in lines) if p[0] == "REP"]
done = set()
if os.path.exists(log):
    for l in open(log):
        p = l.split()
        if p and p[0] == "R":
            done.add(int(p[1]))
t0 = time.time()
n_new = 0
with open(log, "a") as f:
    for idx, (T, osz) in enumerate(reps):
        if idx in done:
            continue
        if time.time() - t0 > budget:
            print(f"STOPPED at rep {idx}/{len(reps)} (budget)")
            break
        r = subprocess.run(["./mu_search", str(k), "3", str(s), pw, "0",
                            str(S_mask), str(NC5), str(T)],
                           capture_output=True, text=True)
        sline = None
        for l in r.stdout.splitlines():
            p = l.split()
            if p[0] == "FAM":
                f.write(l + "\n")
            elif p[0] == "S":
                sline = p
            elif p[0] == "NODELIMIT":
                raise SystemExit("NODELIMIT?!")
        assert sline is not None and r.returncode == 0
        f.write(f"R {idx} {T} {sline[3]} {sline[7]} {osz}\n")
        f.flush()
        n_new += 1
# summary
tot_nodes = 0; tot_found = 0; ndone = 0; fams = []
for l in open(log):
    p = l.split()
    if p[0] == "R":
        ndone += 1; tot_nodes += int(p[3]); tot_found += int(p[4])
    elif p[0] == "FAM":
        fams.append(l.strip())
status = "COMPLETE" if ndone == len(reps) else "PARTIAL"
print(f"k={k} s={s} S={S_mask} NC5={NC5} reps={len(reps)} done={ndone} {status} "
      f"nodes={tot_nodes} found={tot_found} new_this_call={n_new} "
      f"elapsed={time.time()-t0:.1f}s")
for l in fams:
    print(l)
