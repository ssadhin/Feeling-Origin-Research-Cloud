from __future__ import annotations
import json
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

from popane_r1_independent_valence_replication import (
    ZIP, OUT, HORIZONS, GAPS, extract_rows, subject_folds,
    ridge_pipe, hgb_pipe, tune_ridge, bootstrap_subject
)

FAMILIES={
 "ECG_ONLY":["ecg_mean","ecg_std","ecg_rms","ecg_range","ecg_diff_std","rpeak_count","hr_mean","sdnn","rmssd"],
 "EDA_ONLY":["eda_mean","eda_std","eda_range","eda_slope","eda_diff_std","eda_posdiff_area"],
 "ICG_HEMODYNAMIC_ONLY":[
   "dzdt_mean","dzdt_std","dzdt_rms","dzdt_range","dzdt_diff_std",
   "dz_mean","dz_std","dz_rms","dz_range","dz_diff_std",
   "z0_mean","z0_std","z0_rms","z0_range","z0_diff_std",
   "sbp_mean","sbp_std","sbp_slope","dbp_mean","dbp_std","dbp_slope",
   "co_mean","co_std","co_slope","tpr_mean","tpr_std","tpr_slope"
 ]
}

def main():
    if not ZIP.exists():
        raise FileNotFoundError(ZIP)
    feat,qc=extract_rows()
    if len(feat)<500 or feat.subject.nunique()<20 or feat.segment.nunique()<2:
        out={"status":"POPANE_R5_FAMILY_ABLATION","verdict":"FAIL_TECHNICAL_QC","qc":qc}
        (OUT/"popane_r5_family_ablation.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
        print(json.dumps(out,indent=2)); return

    missing={fam:[c for c in cols if c not in feat.columns] for fam,cols in FAMILIES.items()}
    if any(missing.values()):
        raise RuntimeError(f"Frozen family columns missing: {missing}")

    folds=subject_folds(feat.subject.unique())
    feat=feat.copy(); feat["fold"]=feat.subject.map(folds)
    results={}
    robust_rescues=[]
    any_model_specific=False

    for hi,(h,gap) in enumerate(zip(HORIZONS,GAPS)):
        target=f"y_h{h}"
        # prediction rows separately by learner+family
        store={(learner,fam):[] for learner in ("ridge","hgb") for fam in FAMILIES}
        for f in range(10):
            for seg in sorted(feat.segment.unique()):
                te=feat[(feat["fold"]==f)&(feat.segment==seg)]
                if te.empty: continue
                tr=feat[(feat["fold"]!=f)&(feat.segment!=seg)]
                if tr.subject.nunique()<10 or len(tr)<100: continue

                ytr=tr[target].to_numpy(float)
                yte=te[target].to_numpy(float)
                ctx=["prior_affect","time_norm"]

                # fit context once for each learner/cell
                ac=tune_ridge(tr,ctx,target)
                ridge_ctx=ridge_pipe(ac).fit(tr[ctx],ytr).predict(te[ctx])
                hgb_ctx=hgb_pipe().fit(tr[ctx],ytr).predict(te[ctx])
                naive=te["prior_affect"].to_numpy(float)

                for fam,cols in FAMILIES.items():
                    ff=ctx+cols
                    ar=tune_ridge(tr,ff,target)
                    ridge_family=ridge_pipe(ar).fit(tr[ff],ytr).predict(te[ff])
                    hgb_family=hgb_pipe().fit(tr[ff],ytr).predict(te[ff])
                    for learner,ctxpred,fampred in (
                        ("ridge",ridge_ctx,ridge_family),
                        ("hgb",hgb_ctx,hgb_family)
                    ):
                        for idx,yy,nv,cv,pv in zip(te.index,yte,naive,ctxpred,fampred):
                            store[(learner,fam)].append((
                                int(te.loc[idx,"subject"]),float(yy),float(nv),float(cv),float(pv)
                            ))

        hz={}
        for fam in FAMILIES:
            famres={}
            positive={}
            for li,learner in enumerate(("ridge","hgb")):
                pr=pd.DataFrame(store[(learner,fam)],columns=["subject","y","naive","context","family"])
                if pr.empty:
                    raise RuntimeError(f"No predictions {gap}s {fam} {learner}")
                subj={}
                for s,q in pr.groupby("subject"):
                    subj[int(s)]={
                      "naive":float(mean_absolute_error(q.y,q.naive)),
                      "context":float(mean_absolute_error(q.y,q.context)),
                      "family":float(mean_absolute_error(q.y,q.family))
                    }
                dn={s:v["naive"]-v["family"] for s,v in subj.items()}
                dc={s:v["context"]-v["family"] for s,v in subj.items()}
                bn=bootstrap_subject(dn,91000+hi*1000+list(FAMILIES).index(fam)*100+li*10)
                bc=bootstrap_subject(dc,92000+hi*1000+list(FAMILIES).index(fam)*100+li*10)
                pos=bool(bc["ci95"][0]>0)
                positive[learner]=pos
                any_model_specific=any_model_specific or pos
                famres[learner]={
                  "n_rows":int(len(pr)),"n_subjects":int(pr.subject.nunique()),
                  "naive_mae":float(mean_absolute_error(pr.y,pr.naive)),
                  "context_mae":float(mean_absolute_error(pr.y,pr.context)),
                  "family_mae":float(mean_absolute_error(pr.y,pr.family)),
                  "delta_naive_family":bn,
                  "delta_context_family":bc,
                  "positive_vs_context":pos
                }
            both=positive["ridge"] and positive["hgb"]
            famres["both_learners_positive_vs_context"]=both
            if both:
                robust_rescues.append({"gap_sec":gap,"family":fam})
            hz[fam]=famres
        results[f"gap_{gap}s"]=hz

    if robust_rescues:
        verdict="MODEL_ROBUST_FAMILY_RESCUE"
    elif any_model_specific:
        verdict="FAMILY_SCREEN_MIXED"
    else:
        verdict="NO_FAMILY_RESCUE"

    out={
      "status":"POPANE_R5_PREAUTHORIZED_PHYSIOLOGY_FAMILY_ABLATION",
      "protocol":"protocols/popane_r5_family_ablation.json",
      "classification":"EXPLORATORY_POST_PRIMARY",
      "qc":qc,
      "results":results,
      "robust_rescues":robust_rescues,
      "verdict":verdict,
      "firewall":"Exploratory pre-authorized family screen; no causal, universal, or phenomenal inference."
    }
    (OUT/"popane_r5_family_ablation.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps({"verdict":verdict,"robust_rescues":robust_rescues},indent=2))

if __name__=="__main__":
    main()
