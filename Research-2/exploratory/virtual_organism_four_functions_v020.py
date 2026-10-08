#!/usr/bin/env python3
"""Research #2: v0.2 adversarial virtual organism, exploratory only.
Separates tuned development from held-out fixed-seed evaluation.
Never interprets report labels as phenomenal feeling or validates AES-v2.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import statistics
from dataclasses import dataclass, field
from pathlib import Path

VERSION = "0.2.0"
HORIZON = 120
DEV_N = 64
EVAL_N = 256
DEV_BASE = 10000
EVAL_BASE = 500000
SEEN = ("calm", "persistent", "volatile")
OOD = ("hazard_shift", "hazard_shift_reverse", "unreliable_signal", "scarce_food")
POLICIES = (
    "maintenance", "instinct_fixed", "instinct_tuned",
    "emotion_v01", "ema_clone", "emotion_report", "ema_tuned",
    "window_tuned", "bayes_fixed", "bayes_tuned", "memory_ablation",
)
COMPARATORS = (
    "instinct_fixed", "instinct_tuned", "ema_clone", "emotion_report",
    "ema_tuned", "window_tuned", "bayes_fixed", "bayes_tuned",
    "memory_ablation", "maintenance",
)

@dataclass(frozen=True)
class Exog:
    hazard: int
    cue: int
    food: float
    strike: float
    food_probability: float

@dataclass
class Body:
    energy: float = 52.0
    health: float = 100.0

@dataclass
class Memory:
    value: float = 0.0
    belief: float = 0.15
    cues: list[int] = field(default_factory=list)

def spec(regime: str, step: int):
    if regime == "calm":
        return .015, .30, .75, .18, .78
    if regime == "persistent":
        return .05, .94, .75, .18, .78
    if regime == "volatile":
        return .36, .45, .75, .18, .78
    if regime == "hazard_shift":
        return spec("persistent" if step < 60 else "volatile", step)
    if regime == "hazard_shift_reverse":
        return spec("volatile" if step < 60 else "persistent", step)
    if regime == "unreliable_signal":
        return .05, .94, .55, .45, .78
    if regime == "scarce_food":
        return .05, .94, .75, .18, .55
    raise ValueError(regime)

def world(seed: int, regime: str):
    rng = random.Random(seed)
    hazard = 0
    seq = []
    for t in range(HORIZON):
        onset, persistence, sens, false_pos, food_prob = spec(regime, t)
        hazard = int(rng.random() < (persistence if hazard else onset))
        cue = int(rng.random() < (sens if hazard else false_pos))
        strike = rng.random()
        food = rng.random()
        seq.append(Exog(hazard, cue, food, strike, food_prob))
    return seq

def choose(policy: str, energy: float, cue: int, memory: Memory, config: dict):
    # No scenario identifier or hidden hazard reaches the controller.
    # All controllers see only energy, health (not needed), and cue.
    report = None
    if policy == "maintenance":
        forage = energy < 48
    elif policy in ("instinct_fixed", "instinct_tuned"):
        urgent, target = (18, 80) if policy == "instinct_fixed" else config["instinct_tuned"]
        forage = energy < urgent or (cue == 0 and energy < target)
    elif policy in ("emotion_v01", "ema_clone", "emotion_report", "ema_tuned", "memory_ablation", "window_tuned"):
        if policy == "ema_tuned":
            alpha, threshold = config["ema_tuned"]
        elif policy == "window_tuned":
            window_size, threshold = config["window_tuned"]
        else:
            alpha, threshold = .22, .36
        if policy == "memory_ablation":
            risk = float(cue)
        elif policy == "window_tuned":
            memory.cues.append(cue)
            memory.cues = memory.cues[-int(window_size):]
            risk = sum(memory.cues) / len(memory.cues)
        else:
            memory.value = (1.0 - alpha) * memory.value + alpha * cue
            risk = memory.value
        forage = energy < 16 or (risk < threshold and energy < 78)
        if policy == "emotion_report":
            valence = 1.0 - 2.0 * abs(energy - 55.0) / 55.0 - risk
            report = "unpleasant" if valence < -0.2 else "neutral" if valence < 0.2 else "pleasant"
    elif policy in ("bayes_fixed", "bayes_tuned"):
        # One generic guessed model is used in every regime, including OOD.
        # Unlike v0.1, the real scenario's Markov rates are never provided.
        onset_guess, persist_guess = .15, .75
        prior = memory.belief * persist_guess + (1 - memory.belief) * onset_guess
        likelihood_h = .75 if cue else .25
        likelihood_no_h = .18 if cue else .82
        memory.belief = prior * likelihood_h / (prior * likelihood_h + (1 - prior) * likelihood_no_h)
        threshold = .29 if policy == "bayes_fixed" else config["bayes_tuned"][0]
        forage = energy < 14 or (memory.belief < threshold and energy < 80)
    else:
        raise ValueError(policy)
    return ("forage" if forage else "shelter"), report

def episode(policy, draws, config, trace=False):
    body, state = Body(), Memory()
    steps = hits = forages = reports = 0
    actions = []
    for exog in draws:
        if body.energy <= 0 or body.health <= 0:
            break
        action, report = choose(policy, body.energy, exog.cue, state, config)
        steps += 1
        reports += int(report is not None)
        forages += int(action == "forage")
        if action == "forage":
            body.energy += (8.0 if exog.food < exog.food_probability else 0) - 1.3
        else:
            body.energy -= 1.75
        hit = exog.hazard and exog.strike < (.31 if action == "forage" else .015)
        hits += int(hit)
        if hit:
            body.health -= 21.0
        body.energy = max(0.0, min(100.0, body.energy))
        body.health = max(0.0, min(100.0, body.health))
        if trace:
            actions.append(action)
    result = {"survived": int(body.energy > 0 and body.health > 0),
              "steps": steps, "hits": hits, "forages": forages,
              "energy": round(body.energy, 8), "health": round(body.health, 8),
              "reports": reports}
    if trace:
        result["actions"] = actions
    return result

def candidates(family):
    if family == "instinct_tuned":
        return [list(x) for x in itertools.product((10, 16, 18, 24), (60, 78, 80, 90))]
    if family == "ema_tuned":
        return [list(x) for x in itertools.product((.10, .22, .35, .55, .80), (.25, .36, .45, .55))]
    if family == "window_tuned":
        return [list(x) for x in itertools.product((2, 4, 8, 16), (.25, .36, .45, .55))]
    if family == "bayes_tuned":
        return [[x] for x in (.20, .29, .40, .50)]
    raise ValueError(family)

def self_tests():
    config = {"instinct_tuned": [18, 80], "ema_tuned": [.22, .36],
              "window_tuned": [4, .36], "bayes_tuned": [.29]}
    kinds = SEEN + OOD
    for kind in kinds:
        for seed in range(12):
            draws = world(seed, kind)
            assert draws == world(seed, kind)
            e = episode("emotion_v01", draws, config, trace=True)
            c = episode("ema_clone", draws, config, trace=True)
            f = episode("emotion_report", draws, config, trace=True)
            # Exact non-identifiability: relabelled EMA and report-only controller.
            assert e == c, (kind, seed, "clone")
            for k in e:
                if k != "reports":
                    assert e[k] == f[k], (kind, seed, k)
            assert f["reports"] == f["steps"] and e["reports"] == 0
            assert len(e["actions"]) == e["steps"]
            for policy in POLICIES:
                r = episode(policy, draws, config)
                assert 0 <= r["energy"] <= 100 and 0 <= r["health"] <= 100
                assert 0 <= r["steps"] <= HORIZON
    assert any(
        episode("emotion_v01", world(s, "persistent"), config, True)["actions"]
        != episode("memory_ablation", world(s, "persistent"), config, True)["actions"]
        for s in range(60)
    )
    # Independent regression against the prior v0.1 code when available.
    prior_path = Path(__file__).with_name("exploratory_four_functions_v010.py")
    if prior_path.exists():
        import importlib.util
        specfile = importlib.util.spec_from_file_location("r2_prior_v01", prior_path)
        m = importlib.util.module_from_spec(specfile)
        import sys
        sys.modules[specfile.name] = m
        specfile.loader.exec_module(m)
        for kind in SEEN:
            for seed in range(5):
                prev = m.episode("emotion", m.world(seed, kind), kind, trace=True)
                curr = episode("emotion_v01", world(seed, kind), config, trace=True)
                for key, alias in (("survived", "survived"), ("steps", "steps"),
                                   ("hits", "hits"), ("forages", "forages"),
                                   ("actions", "actions"), ("final_energy", "energy"),
                                   ("final_health", "health")):
                    a = prev[key]
                    b = curr[alias]
                    if isinstance(a,float):
                        assert abs(a - b) < .00011, (kind,seed,key,a,b)
                    else:
                        assert a == b, (kind,seed,key,a,b)
    return {"paired_worlds_deterministic": True,
            "literal_ema_emotion_equivalence": True,
            "report_only_actions_identical": True,
            "memory_removal_changes_behavior": True,
            "bounds_and_action_contract": True,
            "v01_regression_checked": prior_path.exists()}

def source_hash():
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

def train():
    self_tests()
    dev = [(regime, seed, world(seed, regime))
           for regime in SEEN for seed in range(DEV_BASE, DEV_BASE+DEV_N)]
    best = {}
    grid = {}
    for family in ("instinct_tuned", "ema_tuned", "window_tuned", "bayes_tuned"):
        rows = []
        for p in candidates(family):
            settings = {family: p}
            rr = [episode(family, draws, settings) for _,_,draws in dev]
            total_survival = sum(x["survived"] for x in rr)
            total_steps = sum(x["steps"] for x in rr)
            total_hits = sum(x["hits"] for x in rr)
            rows.append({"parameters": p, "survivals": total_survival,
                         "living_steps": total_steps, "hits": total_hits})
        # Stable tie break: maximize survival, then steps, minimize hits,
        # then prefer lexicographically smaller parameter tuple.
        winner = sorted(rows, key=lambda x: (
            -x["survivals"], -x["living_steps"], x["hits"], tuple(x["parameters"])
        ))[0]
        best[family] = winner["parameters"]
        grid[family] = rows
    return {
        "study": "Research2_four_function_exploratory_v020",
        "stage": "development_selection_pre_evaluation",
        "version": VERSION,
        "source_sha256": source_hash(),
        "dev_seed_base": DEV_BASE,
        "dev_n_per_seen_regime": DEV_N,
        "seen_regimes": SEEN,
        "development_priority": "max number survived, then steps, then min hits, then min lexicographic parameter tuple",
        "selected": best, "grid": grid, "software_checks": self_tests(),
    }

def paired_interval(left, right, rng, reps=700):
    assert len(left) == len(right)
    diffs = [a-b for a,b in zip(left,right)]
    point = round(sum(diffs)/len(diffs), 5)
    sims = []
    for _ in range(reps):
        sims.append(sum(diffs[rng.randrange(len(diffs))] for _ in diffs)/len(diffs))
    sims.sort()
    return {"difference":point,"bootstrap_95_interval":[round(sims[int(reps*.025)],5),round(sims[int(reps*.975)],5)]}

def evaluate(selected_config):
    self_tests()
    assert selected_config["source_sha256"] == source_hash(), "Code/source hash changed after development freeze"
    assert selected_config["stage"] == "development_selection_pre_evaluation"
    assert selected_config["dev_seed_base"] == DEV_BASE
    assert selected_config["dev_n_per_seen_regime"] == DEV_N
    config = selected_config["selected"]
    assert set(config) == {"instinct_tuned", "ema_tuned", "window_tuned", "bayes_tuned"}
    # Deterministically rerun all development tuning and validate selection
    # before reading any evaluation seeds; no silent config optimization.
    recalculated = train()
    assert recalculated["selected"] == config, "Frozen configuration fails dev reproducibility"
    records=[]
    difference={}
    rng = random.Random(920210)
    for regime in SEEN+OOD:
        draws_by_seed=[world(seed,regime) for seed in range(EVAL_BASE,EVAL_BASE+EVAL_N)]
        by_policy={p:[episode(p, draws, config) for draws in draws_by_seed] for p in POLICIES}
        for name,rr in by_policy.items():
            records.append({
                "regime":regime,"policy":name,"n":EVAL_N,
                "survived":sum(x["survived"] for x in rr),
                "survival_rate":round(statistics.mean(x["survived"] for x in rr),5),
                "mean_steps":round(statistics.mean(x["steps"] for x in rr),4),
                "mean_hits":round(statistics.mean(x["hits"] for x in rr),4),
                "mean_forages":round(statistics.mean(x["forages"] for x in rr),4),
                "mean_reports":round(statistics.mean(x["reports"] for x in rr),4),
            })
        assert all(
            (a["survived"],a["steps"],a["hits"],a["forages"],a["energy"],a["health"])
            == (b["survived"],b["steps"],b["hits"],b["forages"],b["energy"],b["health"])
            for a,b in zip(by_policy["emotion_v01"],by_policy["emotion_report"])
        )
        assert by_policy["emotion_v01"] == by_policy["ema_clone"]
        difference[regime]={}
        reference=[x["survived"] for x in by_policy["emotion_v01"]]
        for p in COMPARATORS:
            other=[x["survived"] for x in by_policy[p]]
            difference[regime][p]=paired_interval(reference,other,rng)
    return {
      "study": "Research2_four_function_exploratory_v020",
      "stage": "development_heldout_evaluation_not_Research2_methodology_trial",
      "version": VERSION,"source_sha256":source_hash(),
      "dev_parameters":config,"n_per_regime":EVAL_N,"eval_seed_base":EVAL_BASE,
      "regimes":list(SEEN+OOD),"policies":list(POLICIES),
      "report":records,"paired_emotion_minus_comparator":difference,
      "self_tests":self_tests(),
      "caveats":[
        "Constructed virtual world and hand-written controllers, no human emotion evidence.",
        "Identical EMA and emotion controllers refute uniqueness of name/function in this model.",
        "Predictive model uses guessed generic rates, not real scenario rates, but assumptions/compute still differ.",
        "This heldout split is in an open developer-authored synthetic family, not independently controlled or sealed.",
        "Bootstrap confidence intervals are exploratory and not multiple-comparison-adjusted.",
        "No real subjective feelings, no methodology AES-v2 competitor trials.",
      ]
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--train",action="store_true")
    ap.add_argument("--eval",action="store_true")
    ap.add_argument("--config")
    args=ap.parse_args()
    assert sum([args.self_test,args.train,args.eval]) == 1
    if args.self_test:
        obj={"version":VERSION,"source_sha256":source_hash(),"checks":self_tests()}
    elif args.train:
        obj=train()
    else:
        if not args.config:
            ap.error("--eval requires previously frozen --config")
        with open(args.config,encoding="utf-8-sig") as f:
            config=json.load(f)
        obj=evaluate(config)
    print(json.dumps(obj,sort_keys=True,indent=2))

if __name__=="__main__":
    main()
