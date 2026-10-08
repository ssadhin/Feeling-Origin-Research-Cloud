#!/usr/bin/env python3
"""Research #2 exploratory four-function virtual organism (development v0.1).
This is NOT a model of phenomenal consciousness or a decisive AES v2 trial.
Standard library only; no human or animal data; predeclared synthetic rules.
"""
from __future__ import annotations
import argparse, hashlib, json, random, statistics
from dataclasses import dataclass
from typing import NamedTuple

VERSION = "0.1.0"
HORIZON = 120
SEEDS = 160
POLICIES = ("maintenance", "instinct", "emotion", "emotion_report", "predictive", "emotion_no_memory")
REGIMES = {
    "calm": (0.015, 0.30),
    "persistent": (0.05, 0.94),
    "volatile": (0.36, 0.45),
}

class Exogenous(NamedTuple):
    hazard: int
    cue: int
    attack_draw: float
    food_draw: float

@dataclass
class Body:
    energy: float = 52.0
    health: float = 100.0
    alive: bool = True

@dataclass
class Controller:
    arousal: float = 0.0
    hazard_belief: float = 0.15
    report: str = ""

def world(seed, regime):
    rng = random.Random(seed)
    onset, persist = REGIMES[regime]
    hazard = 0
    seq = []
    for _ in range(HORIZON):
        hazard = int(rng.random() < (persist if hazard else onset))
        cue = int(rng.random() < (0.75 if hazard else 0.18))
        seq.append(Exogenous(hazard, cue, rng.random(), rng.random()))
    return seq

def choose(policy, body, state, cue, regime):
    """Same bodily input, cue and binary action set for every policy.
    The HMM policy has a specified model assumption, not additional observations.
    """
    if policy == "maintenance":
        forage = body.energy < 48
    elif policy == "instinct":
        forage = body.energy < 18 or (cue == 0 and body.energy < 80)
    elif policy in ("emotion", "emotion_report", "emotion_no_memory"):
        state.arousal = (0.78 * state.arousal + 0.22 * cue) if policy != "emotion_no_memory" else float(cue)
        forage = body.energy < 16 or (state.arousal < 0.36 and body.energy < 78)
        if policy == "emotion_report":
            # Explicit access/report proxy. This is NOT proof of subjective feeling.
            valence = 1.0 - 2.0 * abs(body.energy - 55.0) / 55.0 - state.arousal
            state.report = ("unpleasant" if valence < -0.2 else "neutral" if valence < 0.2 else "pleasant")
    elif policy == "predictive":
        onset, persist = REGIMES[regime]
        # Transparent model-privilege flag: assumes access to the regime parameters.
        prior = state.hazard_belief * persist + (1-state.hazard_belief) * onset
        positive = 0.75 if cue else 0.25
        negative = 0.18 if cue else 0.82
        state.hazard_belief = (prior * positive) / (prior * positive + (1-prior) * negative)
        forage = body.energy < 14 or (state.hazard_belief < 0.29 and body.energy < 80)
    else:
        raise ValueError(policy)
    return "forage" if forage else "shelter"

def transition(body, action, exog):
    b = Body(body.energy, body.health, body.alive)
    if not b.alive:
        return b, False
    if action == "forage":
        b.energy += (8.0 if exog.food_draw < 0.78 else 0.0) - 1.3
    else:
        b.energy -= 1.75
    hit = bool(exog.hazard and exog.attack_draw < (0.31 if action == "forage" else 0.015))
    if hit:
        b.health -= 21.0
    b.energy = max(0.0, min(100.0, b.energy))
    b.health = max(0.0, min(100.0, b.health))
    b.alive = b.energy > 0 and b.health > 0
    return b, hit

def episode(policy, exogenous, regime, trace=False):
    body, controller = Body(), Controller()
    steps = hits = forages = reports = 0
    actions = []
    for exog in exogenous:
        if not body.alive:
            break
        action = choose(policy, body, controller, exog.cue, regime)
        body, hit = transition(body, action, exog)
        steps += 1
        hits += int(hit)
        forages += int(action == "forage")
        reports += int(bool(controller.report))
        if trace:
            actions.append(action)
    out = {"survived": int(body.alive), "steps": steps, "hits": hits,
           "forages": forages, "final_energy": round(body.energy,4),
           "final_health": round(body.health,4), "reports": reports}
    if trace:
        out["actions"] = actions
    return out

def validate():
    # Identical report-enabled vs report-disabled agent behavior is a key
    # non-consciousness and non-behavioral-control negative control.
    for regime in REGIMES:
        for seed in range(4):
            w = world(seed, regime)
            assert w == world(seed, regime)
            a = episode("emotion",w,regime,True)
            b = episode("emotion_report",w,regime,True)
            for key in ("survived", "steps", "hits", "forages", "final_energy", "final_health", "actions"):
                assert a[key] == b[key],(regime, seed, key)
            assert b["reports"] == b["steps"]
            assert a["reports"] == 0
    mutated=False
    for regime in REGIMES:
        for seed in range(25):
            w=world(seed,regime)
            if episode("emotion",w,regime,True)["actions"] != episode("emotion_no_memory",w,regime,True)["actions"]:
                mutated=True
                break
    assert mutated,"Negative-control removal of persistent state was not detectable"
    for e in (Exogenous(1,1,0.0,0.0),Exogenous(0,0,0.99,0.99)):
        for action in ("forage","shelter"):
            b,hit=transition(Body(),action,e)
            assert 0<=b.energy<=100 and 0<=b.health<=100
            assert hit == bool(e.hazard and e.attack_draw < (0.31 if action=="forage" else 0.015))
    return {"deterministic_world":True,"report_only_noncausal":True,"memory_ablation_detected":True,
            "physiological_bounds":True,"action_equivalence":True}

def run():
    checks=validate()
    rows=[]
    for regime in REGIMES:
        for seed in range(SEEDS):
            w = world(seed+42173,regime)  # paired exogenous world across controllers
            for policy in POLICIES:
                result = episode(policy,w,regime)
                rows.append({"regime":regime,"seed":seed+42173,"policy":policy,**result})
    out=[]
    for regime in REGIMES:
        for policy in POLICIES:
            match=[r for r in rows if r["regime"]==regime and r["policy"]==policy]
            out.append({"regime":regime,"policy":policy,"n":len(match),
                        "survival_rate":round(statistics.mean(r["survived"] for r in match),4),
                        "mean_steps":round(statistics.mean(r["steps"] for r in match),2),
                        "mean_hits":round(statistics.mean(r["hits"] for r in match),2),
                        "mean_forages":round(statistics.mean(r["forages"] for r in match),2)})
    return {"label":"EXPLORATORY SYNTHETIC DEVELOPMENT ONLY", "version":VERSION,
            "worlds_per_regime":SEEDS, "steps_per_world":HORIZON,
            "policies":list(POLICIES),"regimes":REGIMES,
            "warnings":["No proof of human emotions or feelings.",
                        "Feeling layer is only an accessible report variable.",
                        "Predictive comparator uses true regime transition parameters (model privilege); comparison is not fair for ranking.",
                        "Fixed hand-designed controllers with unequal algorithmic capabilities.",
                        "No AES-v2 methodology ranking; benchmark remains unsealed and unfrozen."],
            "software_checks":checks,"results":out}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        print(json.dumps({"self_tests":validate(),"version":VERSION},sort_keys=True))
    else:
        print(json.dumps(run(),indent=2,sort_keys=True))

if __name__=="__main__":
    main()
