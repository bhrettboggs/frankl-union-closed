/* mu_search2.c — mu_search.c plus a closure-aware admissible prune (v7).
 * Identical candidate order, branch order, leaf test and output format to
 * mu_search.c; same CLI. Difference: "dead" candidates.
 *   When x is included, every later candidate m with u = m|x, u != m, u != x,
 *   u != Z, u not chosen, u not a co-singleton, is DEAD for the rest of this
 *   branch: pc(u) > pc(x) so u precedes x in candidate order and was already
 *   decided (excluded); m in G would force u in G. Dead candidates are removed
 *   from the counts that feed prunes A (per element), B (sum) and P (pairwise),
 *   which therefore become tighter but remain admissible: g_final(e) >= g(e) -
 *   #(alive remaining candidates avoiding e), etc.
 * Node counts differ from mu_search.c; found sets must be identical.
 * Extra stats field 'kills' appended to the S line.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int K, CAP, FULLMASK, NC, PAIRWISE;
static long long NODE_LIMIT = -1;
static int cands[128];
static int g[8];
static int chosen[128], n_chosen;
static unsigned char in_chosen[256], in_cos[256];
static unsigned char dead[128];
static int killstack[128 * 128], ks_top;
static int an[8];          /* alive candidates at index >= frontier avoiding e */
static int ann[8][8];      /* ... avoiding both e and f */
static int adec;           /* sum over alive remaining of min(0, 2pc-K) */
static int cos_arr[8], n_cos;
static int out_elems[8], n_out;
static long long nodes, leaves, pruneA, pruneB, pruneP, closure_rej, sep_fail, kills;
static long long found_cnt;

static int pc(int x) { return __builtin_popcount(x); }

static void add_contrib(int m, int sign) {
    for (int e = 0; e < K; e++) {
        if ((m >> e) & 1) continue;
        an[e] += sign;
        if (PAIRWISE)
            for (int f = e + 1; f < K; f++)
                if (!((m >> f) & 1)) ann[e][f] += sign;
    }
    int d = 2 * pc(m) - K;
    if (d < 0) adec += sign * d;
}

static void emit_family(void) {
    int mu = g[0];
    for (int e = 1; e < K; e++) if (g[e] > mu) mu = g[e];
    printf("FAM %d 0,%d", mu, FULLMASK);
    for (int i = 0; i < n_cos; i++) printf(",%d", cos_arr[i]);
    for (int i = 0; i < n_chosen; i++) printf(",%d", chosen[i]);
    printf("\n");
    found_cnt++;
}

/* kill later candidates incompatible with newly included x = cands[i] */
static void propagate(int i, int x) {
    for (int j = i + 1; j < NC; j++) {
        if (dead[j]) continue;
        int m = cands[j];
        int u = m | x;
        if (u != m && u != x && u != FULLMASK && !in_chosen[u] && !in_cos[u]) {
            dead[j] = 1;
            killstack[ks_top++] = j;
            add_contrib(m, -1);
            kills++;
        }
    }
}

static void rec(int i, int sum_g) {
    nodes++;
    if (NODE_LIMIT > 0 && nodes > NODE_LIMIT) {
        printf("NODELIMIT\n"); fflush(stdout); exit(2);
    }
    for (int e = 0; e < K; e++)
        if (g[e] - an[e] > CAP) { pruneA++; return; }
    if (sum_g + adec > K * CAP) { pruneB++; return; }
    if (PAIRWISE) {
        for (int e = 0; e < K; e++)
            for (int f = e + 1; f < K; f++)
                if (g[e] + g[f] - 2 * ann[e][f] > 2 * CAP) {
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
    int m = cands[i];
    int alive = !dead[i];
    if (alive) add_contrib(m, -1);           /* frontier moves past i */
    rec(i + 1, sum_g);
    if (alive) {
        int bad = 0;
        for (int j = 0; j < n_chosen; j++) {
            int x = chosen[j];
            int u = m | x;
            if (u != m && u != x && u != FULLMASK && !in_chosen[u] && !in_cos[u]) {
                bad = 1; break;
            }
        }
        if (!bad) {
            int mark = ks_top;
            chosen[n_chosen++] = m;
            in_chosen[m] = 1;
            for (int e = 0; e < K; e++) g[e] += ((m >> e) & 1) ? 1 : -1;
            propagate(i, m);
            rec(i + 1, sum_g + 2 * pc(m) - K);
            while (ks_top > mark) {
                int j = killstack[--ks_top];
                dead[j] = 0;
                add_contrib(cands[j], +1);
            }
            for (int e = 0; e < K; e++) g[e] -= ((m >> e) & 1) ? 1 : -1;
            in_chosen[m] = 0;
            n_chosen--;
        } else closure_rej++;
        add_contrib(m, +1);
    }
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
    memset(dead, 0, sizeof dead);
    ks_top = 0;
    n_chosen = 0; n_cos = 0; n_out = 0;
    nodes = leaves = pruneA = pruneB = pruneP = closure_rej = sep_fail = kills = 0;
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
    int sum_g = 0;
    for (int e = 0; e < K; e++) g[e] = 0;
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
        propagate(i, m);
    }
    if (feasible) {
        int s0 = PREF_LEN < NC ? PREF_LEN : NC;
        /* alive counts over candidates at index >= s0 */
        for (int e = 0; e < K; e++) { an[e] = 0; for (int f = 0; f < K; f++) ann[e][f] = 0; }
        adec = 0;
        for (int j = s0; j < NC; j++) if (!dead[j]) add_contrib(cands[j], +1);
        rec(s0, sum_g);
    }
    printf("S %d nodes %lld leaves %lld found %lld pruneA %lld pruneB %lld "
           "pruneP %lld closure %lld sepfail %lld kills %lld\n",
           S_mask, nodes, leaves, found_cnt, pruneA, pruneB, pruneP,
           closure_rej, sep_fail, kills);
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
