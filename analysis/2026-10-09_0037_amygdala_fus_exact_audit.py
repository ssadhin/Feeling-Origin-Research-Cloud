#!/usr/bin/env python3
"""Post-hoc sensitivity check; not the authors' reported test."""
from math import comb
def mcnemar_exact(b, c):
    n=b+c
    return min(1.0, 2*sum(comb(n,i) for i in range(min(b,c)+1))/2**n)
def fisher_two_sided(a,b,c,d):
    n1=a+b; n2=c+d; m=a+c; n=n1+n2
    p=lambda x: comb(m,x)*comb(n-m,n1-x)/comb(n,n1)
    lo=max(0,n1-(n-m)); hi=min(n1,m); observed=p(a)
    return sum(p(x) for x in range(lo,hi+1) if p(x)<=observed+1e-14)
if __name__=="__main__":
    print("Fisher 7/10 vs 0/10:", fisher_two_sided(7,3,0,10))
    print("Fisher 7/10 vs 0/9:", fisher_two_sided(7,3,0,9))
    print("Paired exact 7 vs 0:",mcnemar_exact(7,0))
    print("Paired exact 6 vs 0:",mcnemar_exact(6,0))
