from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

FEATURES=Path("results_snapshots/o001_feature_rows_run-37214461250.jsonl")
PRIMARY=Path("results_snapshots/observational-multimodal-redundancy-o001-run-37214461250.json")
OUT=Path("results")
N_PERM=200
N_BOOT=5000
SEED_BASE=91000

def make_preprocessor(spec,target,eeg_cols,auto_cols):
    cat=["target_code","music_id"]
    prior=["prior_valence" if target=="valence" else "prior_arousal"]
    trs=[("cat",OneHotEncoder(handle_unknown="ignore",sparse_output=False),cat),
         ("prior",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),prior)]
    if spec in ("eeg","combined"):
        trs.append(("eeg",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler()),
                                   ("pca",PCA(n_components=20,svd_solver="auto"))]),eeg_cols))
    if spec in ("autonomic","combined"):
        trs.append(("auto",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),auto_cols))
    return ColumnTransformer(trs,remainder="drop",sparse_threshold=0.0)

def alpha_map(primary,target,spec):
    rows=primary["analysis"]["targets"][target]["chosen_alphas"][spec]
    return {r["heldout"]:float(r["alpha"]) for r in rows}

def permutation_maps(df):
    groups=[]
    for _,idx in df.groupby(["subject","target_code"],sort=True).groups.items():
        ids=list(idx)
        ids=sorted(ids,key=lambda i:(str(df.at[i,"run"]),float(df.at[i,"onset"]),int(df.at[i,"trial"])))
        if len(ids)<2:
            raise RuntimeError("Non-permutable subject×target_code group")
        groups.append(np.asarray(ids,dtype=int))
    maps=[]
    for p in range(N_PERM):
        rng=np.random.default_rng(SEED_BASE+p)
        m=np.arange(len(df),dtype=int)
        for ids in groups:
            k=int(rng.integers(1,len(ids)))
            m[ids]=np.roll(ids,k)
        maps.append(m)
    return maps

def boot(vals,seed):
    vals=np.asarray(vals,float)
    rng=np.random.default_rng(seed)
    z=np.asarray([np.mean(rng.choice(vals,size=len(vals),replace=True)) for _ in range(N_BOOT)])
    return {"mean":float(np.mean(vals)),"ci95":[float(np.percentile(z,2.5)),float(np.percentile(z,97.5))]}

def main():
    OUT.mkdir(exist_ok=True)
    df=pd.read_json(FEATURES,lines=True)
    df=df.reset_index(drop=True)
    primary=json.loads(PRIMARY.read_text(encoding="utf-8"))
    subjects=sorted(df.subject.unique())
    eeg_cols=sorted(c for c in df.columns if c.startswith("eeg_"))
    auto_cols=sorted(c for c in df.columns if c.startswith("auto_"))
    if len(subjects)!=19 or len(eeg_cols)!=160 or len(auto_cols)!=9:
        raise RuntimeError(f"Frozen O001 shape mismatch subjects={len(subjects)} eeg={len(eeg_cols)} auto={len(auto_cols)}")
    pmaps=permutation_maps(df)
    result={
      "status":"O001_P1_TRIAL_ALIGNMENT_PERMUTATION",
      "protocol":"protocols/o001_p1_trial_alignment_permutation.json",
      "parent_primary_run":37214461250,
      "n_permutations":N_PERM,
      "targets":{},
      "control_limitation":"Permutation preserves subject and coarse target_code but cannot preserve music_id because music_id is unique within participant in the frozen O001 table.",
      "firewall":"Observational predictive replication only; alignment may include stimulus-specific physiology; no causal or phenomenal inference."
    }
    any_neg=False
    for ti,target in enumerate(("valence","arousal")):
        result["targets"][target]={}
        for si,spec in enumerate(("autonomic","eeg","combined")):
            amap=alpha_map(primary,target,spec)
            real_mae={}
            shifted_mae={s:[] for s in subjects}
            frozen_subject=primary["analysis"]["targets"][target]["subject_mae"]
            for oi,sub in enumerate(subjects,1):
                print(f"{target} {spec} {oi}/{len(subjects)} {sub}",flush=True)
                tr_ids=np.flatnonzero(df.subject.to_numpy()!=sub)
                te_ids=np.flatnonzero(df.subject.to_numpy()==sub)
                train=df.iloc[tr_ids]
                ytr=train["y_"+target].to_numpy(float)
                yte=df.iloc[te_ids]["y_"+target].to_numpy(float)
                pp=make_preprocessor(spec,target,eeg_cols,auto_cols)
                pp.fit(train)
                Xall=np.asarray(pp.transform(df),float)
                alpha=amap[sub]
                mdl=Ridge(alpha=alpha).fit(Xall[tr_ids],ytr)
                rmae=float(mean_absolute_error(yte,mdl.predict(Xall[te_ids])))
                real_mae[sub]=rmae
                # record but do not fail on PCA stochastic drift for EEG-containing specs
                frozen=float(frozen_subject[sub][spec])
                if spec=="autonomic" and abs(rmae-frozen)>1e-8:
                    raise RuntimeError(f"Autonomic reproduction mismatch {target} {sub}: {rmae} vs {frozen}")
                slices=[]
                if spec in ("eeg","combined"): slices.append(pp.output_indices_["eeg"])
                if spec in ("autonomic","combined"): slices.append(pp.output_indices_["auto"])
                base_tr=Xall[tr_ids]
                base_te=Xall[te_ids]
                for p,m in enumerate(pmaps):
                    xtr=base_tr.copy(); xte=base_te.copy()
                    for sl in slices:
                        xtr[:,sl]=Xall[m[tr_ids],sl]
                        xte[:,sl]=Xall[m[te_ids],sl]
                    sp=Ridge(alpha=alpha).fit(xtr,ytr).predict(xte)
                    shifted_mae[sub].append(float(mean_absolute_error(yte,sp)))
            subj_delta=[]; subj={}
            for sub in subjects:
                arr=np.asarray(shifted_mae[sub],float)
                d=float(np.mean(arr)-real_mae[sub])
                subj_delta.append(d)
                subj[sub]={
                  "real_mae":real_mae[sub],
                  "frozen_primary_mae":float(frozen_subject[sub][spec]),
                  "mean_shifted_mae":float(np.mean(arr)),
                  "delta_shifted_minus_real":d
                }
            stat=boot(subj_delta,92000+100*ti+si)
            perm_means=[
              float(np.mean([shifted_mae[sub][p]-real_mae[sub] for sub in subjects]))
              for p in range(N_PERM)
            ]
            lo,hi=stat["ci95"]
            if lo>0: align="ALIGNED_REAL_BETTER_THAN_SHIFTED"
            elif hi<0:
                align="SHIFTED_BETTER_ANOMALY"; any_neg=True
            else: align="NO_ALIGNMENT_EVIDENCE"
            result["targets"][target][spec]={
              "alignment_verdict":align,
              "primary_shifted_minus_real":stat,
              "fraction_permutations_real_better":float(np.mean(np.asarray(perm_means)>0)),
              "permutation_mean_deltas":perm_means,
              "subject_results":subj
            }
    both_autonomic=all(result["targets"][t]["autonomic"]["alignment_verdict"]=="ALIGNED_REAL_BETTER_THAN_SHIFTED" for t in ("valence","arousal"))
    both_combined=all(result["targets"][t]["combined"]["alignment_verdict"]=="ALIGNED_REAL_BETTER_THAN_SHIFTED" for t in ("valence","arousal"))
    any_pos=any(result["targets"][t][s]["alignment_verdict"]=="ALIGNED_REAL_BETTER_THAN_SHIFTED" for t in ("valence","arousal") for s in ("autonomic","eeg","combined"))
    if any_neg:
        verdict="SHIFTED_BETTER_ANOMALY"
    elif both_autonomic or both_combined:
        verdict="EXTERNAL_REAL_SIGNAL_REPLICATION"
    elif any_pos:
        verdict="PARTIAL_ALIGNMENT_REPLICATION"
    else:
        verdict="NO_ALIGNMENT_REPLICATION"
    result["verdict"]=verdict
    (OUT/"o001_p1_trial_alignment_permutation.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps({
      "verdict":verdict,
      "summary":{t:{s:{
        "alignment":result["targets"][t][s]["alignment_verdict"],
        "primary":result["targets"][t][s]["primary_shifted_minus_real"],
        "fraction":result["targets"][t][s]["fraction_permutations_real_better"]
      } for s in ("autonomic","eeg","combined")} for t in ("valence","arousal")}
    },indent=2))

if __name__=="__main__":
    main()
