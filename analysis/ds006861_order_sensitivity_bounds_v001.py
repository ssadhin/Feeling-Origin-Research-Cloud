"""Feeling Origin: frozen two-period crossover sensitivity identity (NO participant data).
Model: Y_ip = alpha_i + tau*T_ip + pi*I(p=2) + kappa*T_i1*I(p=2) + e_ip.
q = sham-first fraction, D = active-minus-sham condition-coded paired contrast.
E[D] = tau + (2q-1)*pi - (1-q)*kappa.
Given |pi| <= P, |kappa| <= K and q in [qlo,qhi], the sharp symmetric
worst-case bias radius for this additive model is max_q |2q-1|P+(1-q)K.
These are algebraic bounds, not estimates or dataset results.
"""
from fractions import Fraction as F

def bias(q, pi, kappa):
    return (2*q-F(1))*pi - (F(1)-q)*kappa

def bias_radius(qlo, qhi, P, K):
    assert F(0) <= qlo <= qhi <= F(1) and P >= 0 and K >= 0
    candidates = [qlo, qhi]
    if qlo <= F(1,2) <= qhi:
        candidates.append(F(1,2))
    return max(abs(2*q-F(1))*P+(F(1)-q)*K for q in candidates)

def test():
    assert bias_radius(F(0), F(1), F(1), F(1)) == F(2)
    assert bias_radius(F(1,2), F(1,2), F(1), F(1)) == F(1,2)
    assert bias_radius(F(2,5), F(3,5), F(1), F(1)) == F(4,5)
    assert bias_radius(F(1,2), F(1,2), F(1), F(0)) == F(0)
    for q in [F(0), F(1,4), F(1,2), F(3,4), F(1)]:
        radius = bias_radius(q,q,F(1),F(1))
        for pi in [F(-1),F(0),F(1)]:
            for kappa in [F(-1),F(0),F(1)]:
                assert abs(bias(q,pi,kappa)) <= radius
    print('PASS: exact rational sensitivity identities; no human outcomes')
    print('Unrestricted q, P=K=1 -> radius',bias_radius(F(0),F(1),F(1),F(1)))
    print('q=.5, P=K=1 -> radius',bias_radius(F(1,2),F(1,2),F(1),F(1)))
    print('q in [.4,.6], P=K=1 -> radius',bias_radius(F(2,5),F(3,5),F(1),F(1)))

if __name__=='__main__':
    test()
