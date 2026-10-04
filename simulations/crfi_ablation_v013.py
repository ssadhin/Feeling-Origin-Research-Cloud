from __future__ import annotations
import math, time, itertools
import numpy as np

# V013: large-sweep necessity/sufficiency test for the CRFI functional architecture.
# We do NOT define "feeling" by the model output. Instead we test independent observable
# constraints: unconscious reaction, conscious-content selectivity, persistence,
# history dependence, prediction sensitivity, and context-dependent qualitative state.

RNG=np.random.default_rng(20261004)
NTRIALS=2500
T=40

# Architecture switches:
# M = memory/history state available
# P = prediction signal available
# C = conscious-capable recurrent domain available
# L = content admitted bidirectionally into that domain
ARCHS=list(itertools.product([0,1], repeat=4))

def simulate(params, arch, scenario):
    M,P,C,L=arch
    a_e,a_m,a_s,a_b = params["ae"],params["am"],params["as"],params["ab"]
    w_in,w_mem,w_pred,w_re,w_body = params["win"],params["wmem"],params["wpred"],params["wre"],params["wbody"]
    e=m=s=b=r=0.0
    hist=[]
    # scenario fields:
    # cue at t0, delayed outcome at t8, context sign, prediction sign
    cue=scenario["cue"]; context=scenario["context"]; pred=scenario["pred"]
    outcome=scenario["outcome"]

    for t in range(T):
        ext=cue if t==0 else (outcome if t==8 else 0.0)

        # History/memory integrates past content when enabled.
        m_next=a_m*m + (0.55*e if M else 0.0)

        # Prediction contributes prospectively when enabled.
        pterm=(pred if P else 0.0)

        # Local evaluative/emotional computation exists regardless of C/L.
        # Same instantaneous cue can be changed by memory/prediction/context.
        e_next=a_e*e + w_in*ext + w_mem*m + w_pred*pterm + w_body*b
        if C and L:
            e_next += w_re*s

        # Body and automatic reaction can be driven without conscious admission.
        b_next=a_b*b + 0.25*max(e,0.0)
        r_next=0.45*r + 0.55*abs(e)

        # Re-entrant conscious-capable domain.
        if C:
            if L:
                s_next=np.tanh(a_s*s + 0.48*e + 0.18*m + 0.14*pterm + 0.10*context)
            else:
                s_next=np.tanh(a_s*s)  # domain exists, this content not admitted
        else:
            s_next=0.0

        e,m,s,b,r=e_next,m_next,s_next,b_next,r_next
        hist.append((e,m,s,b,r))
    return np.asarray(hist)

def metrics(params, arch):
    # independent scenarios
    neutral={"cue":1.0,"context":0.0,"pred":0.0,"outcome":0.0}
    threat_pred={"cue":0.7,"context":0.0,"pred":-0.8,"outcome":0.0}
    safe_pred={"cue":0.7,"context":0.0,"pred":0.8,"outcome":0.0}
    samecue_ctxA={"cue":0.8,"context":-1.0,"pred":0.0,"outcome":0.0}
    samecue_ctxB={"cue":0.8,"context":1.0,"pred":0.0,"outcome":0.0}

    H0=simulate(params,arch,neutral)
    Ht=simulate(params,arch,threat_pred)
    Hs=simulate(params,arch,safe_pred)
    Ha=simulate(params,arch,samecue_ctxA)
    Hb=simulate(params,arch,samecue_ctxB)

    e0,m0,s0,b0,r0=H0.T

    # Observable constraints (not "feeling" labels):
    automatic_reaction = float(r0[:6].sum()) > 0.20

    # persistence after stimulus is gone
    persistence = float(np.sum(np.abs(e0[6:])>0.08)) >= 8

    # history dependence: delayed state contains memory contribution
    history = abs(float(m0[7])) > 0.05

    # prediction sensitivity: before delayed outcome, threat-vs-safe diverge
    prediction = abs(float(Ht[5,0]-Hs[5,0])) > 0.20

    # content-specific recurrent participation / admission:
    domain_participation = float(np.sum(np.abs(s0))) > 0.20

    # context changes the ongoing state for same immediate cue
    context_sensitivity = abs(float(Ha[6,0]-Hb[6,0])) > 0.15

    # recurrent amplification relative to same parameters with L=0
    M,P,C,L=arch
    if C and L:
        Habl=simulate(params,(M,P,C,0),neutral)
        amplification = (np.abs(e0).sum() > 1.35*np.abs(Habl[:,0]).sum())
    else:
        amplification=False

    return np.array([
        automatic_reaction,
        persistence,
        history,
        prediction,
        domain_participation,
        context_sensitivity,
        amplification
    ],dtype=bool)

def rand_params():
    return {
      "ae":RNG.uniform(0.35,0.70),
      "am":RNG.uniform(0.45,0.85),
      "as":RNG.uniform(0.40,0.80),
      "ab":RNG.uniform(0.50,0.82),
      "win":RNG.uniform(0.65,1.25),
      "wmem":RNG.uniform(0.05,0.30),
      "wpred":RNG.uniform(0.08,0.35),
      "wre":RNG.uniform(0.12,0.42),
      "wbody":RNG.uniform(0.01,0.10)
    }

def main():
    t0=time.perf_counter()
    names=["reaction","persistence","history","prediction","domain_participation","context","reentrant_amplification"]
    counts={a:np.zeros(len(names),dtype=int) for a in ARCHS}
    full={a:0 for a in ARCHS}

    for _ in range(NTRIALS):
        p=rand_params()
        for a in ARCHS:
            m=metrics(p,a)
            counts[a]+=m.astype(int)
            if m.all(): full[a]+=1

    print("=== V013 LARGE-SWEEP NECESSITY / SUFFICIENCY TEST ===")
    print("random parameter sets:",NTRIALS)
    print("constraints:",",".join(names))
    print()
    for a in ARCHS:
        rates=counts[a]/NTRIALS
        print(f"M={a[0]} P={a[1]} C={a[2]} L={a[3]} full={full[a]:5d}/{NTRIALS} " +
              " ".join(f"{names[i]}={rates[i]:.3f}" for i in range(len(names))))
    winners=[a for a in ARCHS if full[a]>0]
    print("\nArchitectures with ANY full successes:",winners)

    # Necessity test: among full successes, inspect whether all four switches are always on.
    if winners:
        common=[all(a[i]==1 for a in winners) for i in range(4)]
        print("Variables present in every winning architecture [M,P,C,L]:",common)

    # The architecture of interest
    target=(1,1,1,1)
    print("\nTarget M=P=C=L=1 success rate:",full[target]/NTRIALS)

    print("\nINTERPRETATION")
    print("This sweep tests whether memory, prediction, conscious-domain recurrence, and content admission")
    print("are jointly needed to reproduce the full functional signature under broad parameter variation.")
    print("A full success does not prove subjective phenomenality; it proves model-level functional sufficiency.")
    print(f"runtime_seconds={time.perf_counter()-t0:.3f}")

if __name__=="__main__":
    main()


