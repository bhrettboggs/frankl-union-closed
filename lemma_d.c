/* lemma_d.c — Lemma D test for k=7, S=[7], mu<=3.
 * For each top-layer pattern T (bits over the 21 pc-5 candidates in mu_search
 * order), compute t=|T| and alpha(T) = max independent set in the graph on the
 * 35 triples where tau1~tau2 iff |tau1&tau2|==1 and (tau1|tau2) not in T.
 * Necessary condition for a core: 3a2+a3-a4 >= 14+3t; with 3a2-a4 <= 30
 * (lemma_d_check.c) and a3 <= alpha(T): need alpha(T) >= 3t-16.
 * Prints for each T: t alpha covered(1/0). Usage: ./lemma_d < list_of_T */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int K=7;
static int pc(uint64_t x){return __builtin_popcountll(x);}
static int cmp(const void*a,const void*b){int x=*(int*)a,y=*(int*)b;if(pc(x)!=pc(y))return pc(y)-pc(x);return x-y;}
static uint64_t adj[35]; static int best;
static void mis(uint64_t rem,int cur){
    if(cur+pc(rem)<=best) return;
    if(!rem){best=cur;return;}
    /* pick vertex of max degree within rem */
    int v=-1,dv=-1; uint64_t r=rem;
    while(r){int u=__builtin_ctzll(r); r&=r-1; int d=pc(adj[u]&rem); if(d>dv){dv=d;v=u;}}
    if(dv==0){ if(cur+pc(rem)>best) best=cur+pc(rem); return; }
    mis(rem&~(adj[v]|(1ULL<<v)),cur+1);   /* include v */
    mis(rem&~(1ULL<<v),cur);              /* exclude v */
}
int main(void){
    int cands[128],nc=0; int FULL=127;
    for(int m=3;m<FULL;m++){int p=pc(m); if(p>=2&&p<=5) cands[nc++]=m;}
    qsort(cands,nc,sizeof(int),cmp);
    int tri[35],nt=0; for(int m=0;m<128;m++) if(pc(m)==3) tri[nt++]=m;
    unsigned long long T;
    while(scanf("%llu",&T)==1){
        unsigned char inT[128]={0}; int t=0;
        for(int i=0;i<21;i++) if(T>>i&1){inT[cands[i]]=1;t++;}
        for(int i=0;i<35;i++){adj[i]=0; for(int j=0;j<35;j++) if(i!=j && pc(tri[i]&tri[j])==1 && !inT[tri[i]|tri[j]]) adj[i]|=1ULL<<j;}
        best=0; mis((1ULL<<35)-1,0);
        printf("T %llu t %d alpha %d covered %d\n",T,t,best,(best<=3*t-17));
    }
    return 0;
}
