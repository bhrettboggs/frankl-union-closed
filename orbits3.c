/* orbits3.c — orbits.c with perm tables sized for k <= 8 (40320 perms). Logic unchanged.
 * (popcount k-2) under the stabilizer Stab(S) = Sym(S) x Sym([k]\S).
 * Candidate order is identical to mu_search.c (pc desc, mask asc), so the
 * first NC5 candidates are exactly the pc-(k-2) masks missing >=1 element of S.
 * A subset T of that layer is encoded as a bit pattern over indices 0..NC5-1,
 * i.e. exactly the `bits` argument mu_search expects with P = NC5.
 * Usage: ./orbits k S_mask   -> prints "NC5 <n>" then lines "REP <bits> <orbitsize>"
 * Sanity: sum of orbit sizes must equal 2^NC5.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int K, S_MASK, FULLMASK, NC, NC5;
static int cands[256];
static int perms[40320][8];
static int nperm;
static int idxmap[40320][32];

static int pc(int x) { return __builtin_popcount(x); }
static int cmp_cand(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    if (pc(x) != pc(y)) return pc(y) - pc(x);
    return x - y;
}
static int apply_perm(const int *p, int m) {
    int t = 0;
    for (int e = 0; e < K; e++) if ((m >> e) & 1) t |= 1 << p[e];
    return t;
}
static int cur[8]; static int used[8];
static void gen(int pos) {
    if (pos == K) {
        int sm = apply_perm(cur, S_MASK);
        if (sm != S_MASK) return;
        memcpy(perms[nperm++], cur, sizeof cur);
        return;
    }
    for (int v = 0; v < K; v++) if (!used[v]) {
        used[v] = 1; cur[pos] = v; gen(pos + 1); used[v] = 0;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s k S_mask\n", argv[0]); return 1; }
    K = atoi(argv[1]); S_MASK = atoi(argv[2]); FULLMASK = (1 << K) - 1;
    NC = 0;
    for (int m = 3; m < FULLMASK; m++) {
        int p = pc(m);
        if (p >= 2 && p <= K - 2 && (m & S_MASK) != S_MASK) cands[NC++] = m;
    }
    qsort(cands, NC, sizeof(int), cmp_cand);
    NC5 = 0;
    while (NC5 < NC && pc(cands[NC5]) == K - 2) NC5++;
    nperm = 0; gen(0);
    for (int q = 0; q < nperm; q++)
        for (int i = 0; i < NC5; i++) {
            int img = apply_perm(perms[q], cands[i]);
            int j = -1;
            for (int t = 0; t < NC5; t++) if (cands[t] == img) { j = t; break; }
            if (j < 0) { fprintf(stderr, "layer not perm-invariant!\n"); return 2; }
            idxmap[q][i] = j;
        }
    uint64_t total = 1ULL << NC5;
    unsigned char *mark = calloc((total + 7) / 8, 1);
    long long nreps = 0, sumorb = 0;
    printf("NC5 %d NC %d nperm %d\n", NC5, NC, nperm);
    for (uint64_t T = 0; T < total; T++) {
        if (mark[T >> 3] & (1 << (T & 7))) continue;
        long long osz = 0;
        for (int q = 0; q < nperm; q++) {
            uint64_t T2 = 0;
            for (int i = 0; i < NC5; i++) if ((T >> i) & 1) T2 |= 1ULL << idxmap[q][i];
            if (!(mark[T2 >> 3] & (1 << (T2 & 7)))) {
                mark[T2 >> 3] |= (1 << (T2 & 7)); osz++;
            }
        }
        printf("REP %llu %lld\n", (unsigned long long)T, osz);
        nreps++; sumorb += osz;
    }
    printf("DONE reps %lld sumorb %lld expected %llu\n", nreps, sumorb,
           (unsigned long long)total);
    return 0;
}
