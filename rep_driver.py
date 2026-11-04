"""rep_driver.py k s T lo hi [budget] [pw] [limit] [q]
Runs the second-level orbit sub-shards of top-layer pattern T (from ./orbits2)
with P = hi, splitting on NODELIMIT like orbit_driver2. Log: rep_k{k}_s{s}_T{T}.log
with lines 'SUB P bits nodes found' and a final 'TOTAL nodes found' line.
"""
import sys, subprocess, time, os

k = int(sys.argv[1]); s = int(sys.argv[2]); T = int(sys.argv[3])
lo = int(sys.argv[4]); hi = int(sys.argv[5])
budget = float(sys.argv[6]) if len(sys.argv) > 6 else 185.0
pw = sys.argv[7] if len(sys.argv) > 7 else "1"
limit = int(sys.argv[8]) if len(sys.argv) > 8 else 1_000_000_000
q = int(sys.argv[9]) if len(sys.argv) > 9 else 3
S_mask = (1 << s) - 1
log = f"rep_k{k}_s{s}_T{T}.log"

out = subprocess.run(["./orbits2", str(k), str(S_mask), str(T), str(lo), str(hi)],
                     capture_output=True, text=True)
assert out.returncode == 0, out.stderr
lines = out.stdout.splitlines()
hdr = lines[0].split(); H = int(hdr[1]); NC = int(hdr[5])
reps = [(int(p[1]), int(p[2])) for p in (l.split() for l in lines) if p[0] == "REP"]
done = {}
if os.path.exists(log):
    for l in open(log):
        p = l.split()
        if p and p[0] == "SUB":
            done[(int(p[1]), int(p[2]))] = (int(p[3]), int(p[4]))
t0 = time.time(); f = open(log, "a"); fams = []

class Budget(Exception):
    pass

def run(P, bits):
    key = (P, bits)
    if key in done:
        return done[key]
    if time.time() - t0 > budget:
        raise Budget()
    r = subprocess.run(["./mu_search", str(k), "3", str(s), pw, str(limit),
                        str(S_mask), str(P), str(bits)], capture_output=True, text=True)
    if r.returncode == 2:
        assert P + q <= NC
        tn = tf = 0
        for sub in range(1 << q):
            n1, f1 = run(P + q, bits | (sub << P)); tn += n1; tf += f1
        f.write(f"SUB {P} {bits} {tn} {tf}\n"); f.flush(); done[key] = (tn, tf)
        return tn, tf
    assert r.returncode == 0, r.stdout
    sline = None
    for l in r.stdout.splitlines():
        p = l.split()
        if p[0] == "FAM":
            fams.append(l); f.write(l + "\n")
        elif p[0] == "S":
            sline = p
    nodes, found = int(sline[3]), int(sline[7])
    f.write(f"SUB {P} {bits} {nodes} {found}\n"); f.flush(); done[key] = (nodes, found)
    return nodes, found

stopped = False
try:
    for bits, osz in reps:
        run(hi, bits)
except Budget:
    stopped = True
ndone = sum(1 for bits, _ in reps if (hi, bits) in done)
tn = sum(done[(hi, b)][0] for b, _ in reps if (hi, b) in done)
tf = sum(done[(hi, b)][1] for b, _ in reps if (hi, b) in done)
status = "COMPLETE" if ndone == len(reps) else "PARTIAL"
if status == "COMPLETE":
    f.write(f"TOTAL {tn} {tf}\n")
f.close()
print(f"rep T={T} |H|={H} block=[{lo},{hi}) reps={len(reps)} done={ndone} {status} "
      f"nodes={tn} found={tf} elapsed={time.time()-t0:.1f}s")
for l in fams:
    print(l)
