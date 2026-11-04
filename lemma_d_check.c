/* lemma_d_check.c — verify: for every graph F on 7 vertices,
 * u(F) - 3|F| <= 2, where u(F) = number of 4-subsets Q of [7] such that F
 * meets all three perfect matchings of Q (equivalently F[Q] contains a
 * triangle or a claw).  Also print the maximum and its attainers' edge counts. */
#include <stdio.h>
int main(void){
    int eid[7][7], ne=0;
    for(int a=0;a<7;a++)for(int b=a+1;b<7;b++){eid[a][b]=eid[b][a]=ne++;}
    /* 35 four-sets, each with 3 matchings, each matching = mask of 2 edges */
    int nq=0; unsigned mt[35][3];
    for(int q=0;q<128;q++){ if(__builtin_popcount(q)!=4) continue;
        int v[4],c=0; for(int i=0;i<7;i++) if(q>>i&1) v[c++]=i;
        mt[nq][0]=(1u<<eid[v[0]][v[1]])|(1u<<eid[v[2]][v[3]]);
        mt[nq][1]=(1u<<eid[v[0]][v[2]])|(1u<<eid[v[1]][v[3]]);
        mt[nq][2]=(1u<<eid[v[0]][v[3]])|(1u<<eid[v[1]][v[2]]);
        nq++; }
    int best=-100; long long cnt_best=0; int hist[80]={0};
    for(unsigned F=0;F<(1u<<21);F++){
        int u=0;
        for(int i=0;i<35;i++) if((F&mt[i][0])&&(F&mt[i][1])&&(F&mt[i][2])) u++;
        int val=u-3*__builtin_popcount(F);
        if(val>best){best=val;cnt_best=0;}
        if(val==best) cnt_best++;
        if(val>=0) hist[__builtin_popcount(F)]++;
    }
    printf("max over F of u(F)-3|F| = %d (attained by %lld labeled graphs)\n",best,cnt_best);
    printf("|F| values with u(F)-3|F|>=0: "); for(int i=0;i<22;i++) if(hist[i]) printf("%d:%d ",i,hist[i]); printf("\n");
    /* coverage: t covered iff 3t-50 >= best */
    for(int t=14;t<=21;t++) printf("t=%d threshold 3t-50=%d %s\n",t,3*t-50,(3*t-50>=best)?"COVERED":"not covered");
    return 0;
}
