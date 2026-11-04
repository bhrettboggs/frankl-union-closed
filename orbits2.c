/* orbits2.c — second-level quotient. Given S, a top-layer pattern T (bits over
 * candidates 0..NC5-1) and a contiguous candidate block [lo,hi), compute
 * H = {pi in Stab(S) : pi(T) = T}, verify the block is H-invariant, and print
 * orbit representatives U of subsets of the block under H as combined patterns
 * bits = T | (U << lo), to be run with P = hi.
 * Usage: ./orbits2 k S_mask T lo hi
 * Prints "H <order> NC5 <n> NC <n>" then "REP <bits> <orbitsize>" then DONE line.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int K, S_MASK, FULLMASK, NC, NC5;
static int cands[128];
static int perms[5040][8];
static int nperm;
static int cur[8]; static int used[8];

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
static int cand_index(int m) {
    for (int t = 0; t < NC; t++) if (cands[t] == m) return t;
    return -1;
}
static void gen(int pos) {
    if (pos == K) {
        if (apply_perm(cur, S_MASK) != S_MASK) return;
        memcpy(perms[nperm++], cur, sizeof cur);
        return;
    }
    for (int v = 0; v < K; v++) if (!used[v]) {
        used[v] = 1; cur[pos] = v; gen(pos + 1); used[v] = 0;
    }
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: %s k S_mask T lo hi\n", argv[0]); return 1; }
    K = atoi(argv[1]); S_MASK = atoi(argv[2]);
    uint64_t T = strtoull(argv[3], 0, 10);
    int lo = atoi(argv[4]), hi = atoi(argv[5]);
    FULLMASK = (1 << K) - 1;
    NC = 0;
    for (int m = 3; m < FULLMASK; m++) {
        int p = pc(m);
        if (p >= 2 && p <= K - 2 && (m & S_MASK) != S_MASK) cands[NC++] = m;
    }
    qsort(cands, NC, sizeof(int), cmp_cand);
    NC5 = 0;
    while (NC5 < NC && pc(cands[NC5]) == K - 2) NC5++;
    if (lo < NC5 || hi > NC || hi - lo > 40) { fprintf(stderr, "bad block\n"); return 2; }
    nperm = 0; gen(0);
    /* filter to stabilizer of T */
    int nh = 0;
    for (int q = 0; q < nperm; q++) {
        uint64_t T2 = 0;
        for (int i = 0; i < NC5; i++) if ((T >> i) & 1) {
            int j = cand_index(apply_perm(perms[q], cands[i]));
            if (j < 0 || j >= NC5) { fprintf(stderr, "top layer not invariant\n"); return 3; }
            T2 |= 1ULL << j;
        }
        if (T2 == T) { if (nh != q) memcpy(perms[nh], perms[q], sizeof perms[q]); nh++; }
    }
    nperm = nh;
    int W = hi - lo;
    static int idxmap[5040][40];
    for (int q = 0; q < nperm; q++)
        for (int i = 0; i < W; i++) {
            int j = cand_index(apply_perm(perms[q], cands[lo + i]));
            if (j < lo || j >= hi) { fprintf(stderr, "block not H-invariant\n"); return 4; }
            idxmap[q][i] = j - lo;
        }
    uint64_t total = 1ULL << W;
    unsigned char *mark = calloc((total + 7) / 8, 1);
    long long nreps = 0, sumorb = 0;
    printf("H %d NC5 %d NC %d W %d\n", nperm, NC5, NC, W);
    for (uint64_t U = 0; U < total; U++) {
        if (mark[U >> 3] & (1 << (U & 7))) continue;
        long long osz = 0;
        for (int q = 0; q < nperm; q++) {
            uint64_t U2 = 0;
            for (int i = 0; i < W; i++) if ((U >> i) & 1) U2 |= 1ULL << idxmap[q][i];
            if (!(mark[U2 >> 3] & (1 << (U2 & 7)))) { mark[U2 >> 3] |= (1 << (U2 & 7)); osz++; }
        }
        printf("REP %llu %lld\n", (unsigned long long)(T | (U << lo)), osz);
        nreps++; sumorb += osz;
    }
    printf("DONE reps %lld sumorb %lld expected %llu\n", nreps, sumorb, (unsigned long long)total);
    return 0;
}
