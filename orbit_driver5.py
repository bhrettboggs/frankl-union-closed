"""orbit_driver5.py k s [budget_s] [pw] [node_limit] [q] [cap] [lemma_file] — orbit_driver4.py plus an optional
lemma_d2 output file: reps marked covered there are logged as 'L idx T osz' (closed by Lemma D,
never searched, never added to node totals). Log orb3_k{k}_s{s}_c{cap}.log.
Like orbit_driver.py (same log file, same 'R idx T nodes found osz' lines, so it
resumes earlier progress), but each mu_search call gets node_limit; a shard that
hits NODELIMIT is split into 2^q sub-shards by forcing q further candidates
(P += q), recursively. Sub-shard completions are logged as
'SUB idx P bits nodes found' so a rep in progress also resumes.
A rep's R line reports the summed node count over its sub-shards.
"""
import sys, subprocess, time, os

k = int(sys.argv[1]); s = int(sys.argv[2])
budget = float(sys.argv[3]) if len(sys.argv) > 3 else 185.0
pw = sys.argv[4] if len(sys.argv) > 4 else "1"
limit = int(sys.argv[5]) if len(sys.argv) > 5 else 3_000_000_000
q = int(sys.argv[6]) if len(sys.argv) > 6 else 3
cap = int(sys.argv[7]) if len(sys.argv) > 7 else 3
lemfile = sys.argv[8] if len(sys.argv) > 8 else None
S_mask = (1 << s) - 1
log = f"orb3_k{k}_s{s}_c{cap}.log"

out = subprocess.run(["./orbits", str(k), str(S_mask)], capture_output=True, text=True).stdout
lines = out.splitlines()
NC5 = int(lines[0].split()[1])
NC = int(lines[0].split()[3])
reps = [(int(p[1]), int(p[2])) for p in (l.split() for l in lines) if p[0] == "REP"]
covered = set()
if lemfile:
    lem = [l.split() for l in open(lemfile)]
    assert len(lem) == len(reps)
    for i, p in enumerate(lem):
        assert int(p[1]) == reps[i][0]
        if p[7] == "1":
            covered.add(i)
done = set(); subdone = {}
if os.path.exists(log):
    for l in open(log):
        p = l.split()
        if p and p[0] in ("R", "L"):
            done.add(int(p[1]))
        elif p and p[0] == "SUB":
            subdone[(int(p[1]), int(p[2]), int(p[3]))] = (int(p[4]), int(p[5]))
t0 = time.time()
n_new = 0; stopped = False
f = open(log, "a")

class Budget(Exception):
    pass

def run(idx, P, bits, fams):
    """Run one shard; returns (nodes, found). Splits on NODELIMIT."""
    key = (idx, P, bits)
    if key in subdone:
        return subdone[key]
    if time.time() - t0 > budget:
        raise Budget()
    r = subprocess.run(["./mu_search2", str(k), str(cap), str(s), pw, str(limit),
                        str(S_mask), str(P), str(bits)],
                       capture_output=True, text=True)
    if r.returncode == 2:  # NODELIMIT -> split
        assert P + q <= NC, "cannot split further"
        tn = 0; tf = 0
        for sub in range(1 << q):
            n1, f1 = run(idx, P + q, bits | (sub << P), fams)
            tn += n1; tf += f1
        f.write(f"SUB {idx} {P} {bits} {tn} {tf}\n"); f.flush()
        subdone[key] = (tn, tf)
        return tn, tf
    assert r.returncode == 0, r.stdout
    sline = None
    for l in r.stdout.splitlines():
        p = l.split()
        if p[0] == "FAM":
            fams.append(l)
        elif p[0] == "S":
            sline = p
    nodes, found = int(sline[3]), int(sline[7])
    if P > NC5:
        f.write(f"SUB {idx} {P} {bits} {nodes} {found}\n"); f.flush()
        subdone[key] = (nodes, found)
    return nodes, found

try:
    for idx, (T, osz) in enumerate(reps):
        if idx in done:
            continue
        if idx in covered:
            f.write(f"L {idx} {T} {osz}\n"); f.flush(); n_new += 1
            continue
        fams = []
        nodes, found = run(idx, NC5, T, fams)
        for l in fams:
            f.write(l + "\n")
        f.write(f"R {idx} {T} {nodes} {found} {osz}\n"); f.flush()
        n_new += 1
except Budget:
    stopped = True
    print("STOPPED (budget)")
f.close()

tot_nodes = 0; tot_found = 0; ndone = 0; fams = []; nsub = 0; nlem = 0
for l in open(log):
    p = l.split()
    if p[0] == "R":
        ndone += 1; tot_nodes += int(p[3]); tot_found += int(p[4])
    elif p[0] == "FAM":
        fams.append(l.strip())
    elif p[0] == "SUB":
        nsub += 1
    elif p[0] == "L":
        ndone += 1; nlem += 1
status = "COMPLETE" if ndone == len(reps) else "PARTIAL"
print(f"k={k} s={s} S={S_mask} NC5={NC5} reps={len(reps)} done={ndone} {status} "
      f"searched={ndone-nlem} lemmaD={nlem} nodes={tot_nodes} found={tot_found} sublines={nsub} new_this_call={n_new} "
      f"elapsed={time.time()-t0:.1f}s")
for l in fams:
    print(l)
