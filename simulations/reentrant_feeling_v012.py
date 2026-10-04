from __future__ import annotations
import time, numpy as np

T=80

def run(C,L,stim=1.0):
    # e: evaluative/emotion state
    # s: conscious-domain re-entrant state
    # b: bodily sensitization/arousal
    # r: overt/automatic reaction drive
    e=s=b=r=0.0
    hist=[]
    for t in range(T):
        u=stim if t==0 else 0.0

        # local emotion computation can exist regardless of feeling
        e_next=0.58*e + u + (0.34*s if (C and L) else 0.0) + 0.10*b

        # automatic body/reaction path does not require conscious admission
        b_next=0.72*b + 0.28*e
        r_next=0.45*r + 0.55*max(e,0.0)

        # conscious domain exists only when C is on; content enters it only when L is on
        if C:
            s_next=0.64*s + (0.42*e if L else 0.0)
            # bounded nonlinear domain to avoid runaway
            s_next=np.tanh(s_next)
        else:
            s_next=0.0

        e,s,b,r=e_next,s_next,b_next,r_next
        hist.append((e,s,b,r))
    return np.asarray(hist)

def summarize(H):
    e,s,b,r=H.T
    return {
        "peak_emotion":float(e.max()),
        "emotion_auc":float(e.sum()),
        "body_auc":float(b.sum()),
        "reaction_auc":float(r.sum()),
        "domain_auc":float(np.abs(s).sum()),
        "emotion_duration":int(np.sum(e>0.10))
    }

def main():
    t0=time.perf_counter()
    cases={
      "automatic_only_C0L1":run(0,1),
      "awake_unseen_C1L0":run(1,0),
      "felt_reentrant_C1L1":run(1,1),
    }
    print("=== V012 RE-ENTRANT FEELING / AMPLIFICATION TEST ===")
    for name,H in cases.items():
        s=summarize(H)
        print(name)
        for k,v in s.items():
            print(f"  {k:18s} {v}")
    base=summarize(cases["awake_unseen_C1L0"])
    felt=summarize(cases["felt_reentrant_C1L1"])
    print("\nFELT / UNSEEN RATIOS")
    for k in ["peak_emotion","emotion_auc","body_auc","reaction_auc","emotion_duration"]:
        print(f"{k:18s} {felt[k]/(base[k]+1e-12):.3f}")

    print("\nInterpretation:")
    print("The initial local emotion and automatic reaction path are present without feeling.")
    print("When the same content is admitted into a recurrent domain, re-entry prolongs emotion,")
    print("increases bodily sensitization, and increases total reaction drive.")
    print("No extra post-hoc 'feeling force' is needed: the re-entrant trajectory itself is the candidate felt state.")
    print("This is a functional simulation, not independent proof of subjectivity.")
    print(f"runtime_seconds={time.perf_counter()-t0:.6f}")

if __name__=="__main__":
    main()
