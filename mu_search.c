/* mu_search.c — Lemma-C-structured targeted search for low-mu cores (C port).
 * Mirrors mu_search.py exactly when PAIRWISE is off (same candidate ordering,
 * prune order, branch order) so node counts match Python for cross-validation.
 * Usage: ./mu_search k mu_cap s [pairwise] [node_limit] [S_mask] [P] [bits]
 * Without S_mask: loops all S of size s. With S_mask: single-S (sharded) mode,
 * forcing the first P candidates' include/exclude per bits. Exits 2 on limit.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int K, CAP, FULLMASK, NC, PAIRWISE;
static long long NODE_LIMIT = -1;
static int cands[128];
static int cnt_not[130][8];
static int cnt_nn[130][8][8];
static int suf_dec[130];
static int g[8];
static int chosen[128], n_chosen;
static unsigned char in_chosen[256], in_cos[256];
static int cos_arr[8], n_cos;
static int out_elems[8], n_out;
static long long nodes, leaves, pruneA, pruneB, pruneP, closure_rej, sep_fail;
static long long found_cnt;

static int pc(int x) { return __builtin_popcount(x); }

static void emit_family(void) {
    int mu = g[0];
    for (int e = 1; e < K; e++) if (g[e] > mu) mu = g[e];
    printf("FAM %d 0,%d", mu, FULLMASK);
    for (int i = 0; i < n_cos; i++) printf(",%d", cos_arr[i]);
    for (int i = 0; i < n_chosen; i++) printf(",%d", chosen[i]);
    printf("\n");
    found_cnt++;
}

static void rec(int i, int sum_g) {
    nodes++;
    if (NODE_LIMIT > 0 && nodes > NODE_LIMIT) {
        printf("NODELIMIT\n"); fflush(stdout); exit(2);
    }
    const int *cn = cnt_not[i];
    for (int e = 0; e < K; e++)
        if (g[e] - cn[e] > CAP) { pruneA++; return; }
    if (sum_g + suf_dec[i] > K * CAP) { pruneB++; return; }
    if (PAIRWISE) {
        for (int e = 0; e < K; e++)
            for (int f = e + 1; f < K; f++)
                if (g[e] + g[f] - 2 * cnt_nn[i][e][f] > 2 * CAP) {
                    pruneP++; return;
                }
    }
    if (i == NC) {
        leaves++;
        for (int a = 0; a < n_out; a++)
            for (int b = a + 1; b < n_out; b++) {
                int ea = out_elems[a], eb = out_elems[b], sep = 0;
                for (int j = 0; j < n_chosen; j++) {
                    int m = chosen[j];
                    if ((((m >> ea) ^ (m >> eb)) & 1)) { sep = 1; break; }
                }
                if (!sep) { sep_fail++; return; }
            }
        emit_family();
        return;
    }
    rec(i + 1, sum_g);
    int m = cands[i];
    for (int j = 0; j < n_chosen; j++) {
        int x = chosen[j];
        int u = m | x;
        if (u != m && u != x && u != FULLMASK && !in_chosen[u] && !in_cos[u]) {
            closure_rej++; return;
        }
    }
    chosen[n_chosen++] = m;
    in_chosen[m] = 1;
    for (int e = 0; e < K; e++) g[e] += ((m >> e) & 1) ? 1 : -1;
    rec(i + 1, sum_g + 2 * pc(m) - K);
    for (int e = 0; e < K; e++) g[e] -= ((m >> e) & 1) ? 1 : -1;
    in_chosen[m] = 0;
    n_chosen--;
}

static int cmp_cand(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    if (pc(x) != pc(y)) return pc(y) - pc(x);
    return x - y;
}

static int PREF_LEN = 0; static long long PREF_BITS = 0;

static void run_S(int S_mask) {
    memset(in_chosen, 0, sizeof in_chosen);
    memset(in_cos, 0, sizeof in_cos);
    n_chosen = 0; n_cos = 0; n_out = 0;
    nodes = leaves = pruneA = pruneB = pruneP = closure_rej = sep_fail = 0;
    found_cnt = 0;
    for (int x = 0; x < K; x++) {
        if ((S_mask >> x) & 1) {
            int c = FULLMASK ^ (1 << x);
            cos_arr[n_cos++] = c;
            in_cos[c] = 1;
        } else out_elems[n_out++] = x;
    }
    NC = 0;
    for (int m = 3; m < FULLMASK; m++) {
        int p = pc(m);
        if (p >= 2 && p <= K - 2 && (m & S_mask) != S_mask)
            cands[NC++] = m;
    }
    qsort(cands, NC, sizeof(int), cmp_cand);
    for (int e = 0; e < K; e++) cnt_not[NC][e] = 0;
    if (PAIRWISE)
        for (int e = 0; e < K; e++)
            for (int f = 0; f < K; f++) cnt_nn[NC][e][f] = 0;
    suf_dec[NC] = 0;
    for (int i = NC - 1; i >= 0; i--) {
        int m = cands[i];
        for (int e = 0; e < K; e++)
            cnt_not[i][e] = cnt_not[i + 1][e] + (((m >> e) & 1) ? 0 : 1);
        if (PAIRWISE)
            for (int e = 0; e < K; e++)
                for (int f = 0; f < K; f++)
                    cnt_nn[i][e][f] = cnt_nn[i + 1][e][f]
                        + ((((m >> e) & 1) || ((m >> f) & 1)) ? 0 : 1);
        int d = 2 * pc(m) - K;
        suf_dec[i] = suf_dec[i + 1] + (d < 0 ? d : 0);
    }
    int sum_g = 0;
    for (int e = 0; e < K; e++) g[e] = 0;
    for (int e = 0; e < K; e++) g[e] += -1 + 1;
    for (int i = 0; i < n_cos; i++) {
        int c = cos_arr[i];
        for (int e = 0; e < K; e++) g[e] += ((c >> e) & 1) ? 1 : -1;
    }
    for (int e = 0; e < K; e++) sum_g += g[e];
    int feasible = 1;
    for (int i = 0; i < PREF_LEN && i < NC; i++) {
        if (!((PREF_BITS >> i) & 1)) continue;
        int m = cands[i], bad = 0;
        for (int j = 0; j < n_chosen; j++) {
            int u = m | chosen[j];
            if (u != m && u != chosen[j] && u != FULLMASK
                && !in_chosen[u] && !in_cos[u]) { bad = 1; break; }
        }
        if (bad) { feasible = 0; break; }
        chosen[n_chosen++] = m;
        in_chosen[m] = 1;
        for (int e = 0; e < K; e++) g[e] += ((m >> e) & 1) ? 1 : -1;
        sum_g += 2 * pc(m) - K;
    }
    if (feasible) { int s0 = PREF_LEN < NC ? PREF_LEN : NC; rec(s0, sum_g); }
    printf("S %d nodes %lld leaves %lld found %lld pruneA %lld pruneB %lld "
           "pruneP %lld closure %lld sepfail %lld\n",
           S_mask, nodes, leaves, found_cnt, pruneA, pruneB, pruneP,
           closure_rej, sep_fail);
    fflush(stdout);
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s k cap s [pairwise] [limit] [S] [P] [bits]\n",
                            argv[0]); return 1; }
    K = atoi(argv[1]); CAP = atoi(argv[2]);
    int s = atoi(argv[3]);
    PAIRWISE = (argc > 4) ? atoi(argv[4]) : 0;
    if (argc > 5) NODE_LIMIT = atoll(argv[5]);
    FULLMASK = (1 << K) - 1;
    if (argc > 6) {
        int Sm = atoi(argv[6]);
        if (argc > 7) PREF_LEN = atoi(argv[7]);
        if (argc > 8) PREF_BITS = atoll(argv[8]);
        run_S(Sm);
        return 0;
    }
    for (int S = 0; S <= FULLMASK; S++)
        if (pc(S) == s) run_S(S);
    return 0;
}
