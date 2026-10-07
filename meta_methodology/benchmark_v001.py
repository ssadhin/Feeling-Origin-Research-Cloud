#!/usr/bin/env python3
"""
Adaptive Epistemic Search — Meta-Research Benchmark v001

Purpose
-------
Compare research policies under equal budgets in hidden-ground-truth synthetic
research worlds. Policies never receive the answer key. This benchmark can
falsify or separate policies within its declared world generator; it cannot
establish a universally best scientific method.

Important firewall
------------------
The CLI exposes TRAIN and VALIDATION only. Locked TEST and OOD meta-test are
implemented internally but intentionally blocked from normal CLI use until a
later frozen workflow is created after policy development is complete.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


BUDGET = 100

WORLD_CLASSES: Tuple[str, ...] = (
    "SIMPLE_TRUE",
    "MISSING_TRUE_HYPOTHESIS",
    "DIVERSITY_COLLAPSE",
    "CONFOUND_TRAP",
    "BEHAVIORAL_MIMIC",
    "NONIDENTIFIABLE",
    "INTERVENTION_ONLY",
    "PARAMETER_FRAGILITY",
    "ANALYSIS_FLEXIBILITY",
    "NEGATIVE_CONTROL_TRAP",
    "WEAK_NULL_EQUIVALENCE",
    "OOD_FAILURE",
    "MEASUREMENT_CIRCULARITY",
    "SOFTWARE_BUG",
    "HYBRID_TRUTH",
    "OVERCOMPLEXITY",
    "REEVALUATION_DRIFT",
    "REJECTED_ANCESTOR_RECOVERY",
    "SURPRISE_DISTRACTOR",
    "EXPENSIVE_PERFECT_TEST",
    "MYOPIC_INFORMATION_GAIN",
    "SHARED_ANALYST_BIAS",
)

META_COMPOSITIONS: Tuple[Tuple[str, str], ...] = (
    ("MISSING_TRUE_HYPOTHESIS", "CONFOUND_TRAP"),
    ("HYBRID_TRUTH", "OOD_FAILURE"),
    ("REJECTED_ANCESTOR_RECOVERY", "ANALYSIS_FLEXIBILITY"),
    ("SURPRISE_DISTRACTOR", "SOFTWARE_BUG"),
    ("MYOPIC_INFORMATION_GAIN", "SHARED_ANALYST_BIAS"),
    ("DIVERSITY_COLLAPSE", "PARAMETER_FRAGILITY"),
)

ACTIONS: Dict[str, int] = {
    "generate": 8,
    "parallel_generate": 14,
    "observe": 8,
    "compare": 10,
    "residual": 6,
    "preregister": 3,
    "intervene": 20,
    "negative_control": 8,
    "positive_control": 6,
    "mist": 10,
    "software_test": 8,
    "sensitivity": 10,
    "multiverse": 12,
    "equivalence": 10,
    "ood": 14,
    "replicate": 12,
    "ancestor": 8,
    "independent_analysis": 12,
    "simplify": 8,
    "hybridize": 10,
}

POLICIES: Tuple[str, ...] = (
    "P0",  # one pass
    "P1",  # prereg confirm
    "P2",  # Bayesian-workflow analogue
    "P3",  # strong inference
    "P5",  # recursive tournament
    "P6",  # tournament + MIST
    "P7",  # full fixed stack
    "P8",  # adaptive epistemic search
    "P9",  # minimal adaptive
    "P10", # diversity/hierarchical
    "P11", # surprise/MCTS analogue
    "P12", # parallel independent
)

SPLIT_BASE = {
    "train": 100_000,
    "validation": 2_000_000,
    "locked_test": 5_000_000,
    "ood": 9_000_000,
}


@dataclass(frozen=True)
class World:
    """Hidden answer-key state. A policy must never inspect this object directly."""
    world_id: str
    components: Tuple[str, ...]
    seed: int
    truth: str
    initial: Tuple[str, ...]
    equivalent: Tuple[str, ...] = ()
    ancestor: Optional[str] = None
    requires_generation: bool = False
    traps: Tuple[str, ...] = ()


@dataclass
class PublicState:
    """Only information exposed to policy logic."""
    candidates: Set[str]
    scores: Dict[str, float]
    budget: int = BUDGET
    spent: int = 0
    detected: Set[str] = field(default_factory=set)
    history: List[str] = field(default_factory=list)
    residual_seen: bool = False
    preregistered: bool = False
    # These markers are written by the environment for scoring/debugging only.
    # Policy functions below do not read them.
    generated_true_marker: bool = False
    surprise_added: bool = False


def _trap_names(components: Sequence[str]) -> Tuple[str, ...]:
    mapping = {
        "DIVERSITY_COLLAPSE": "early_bias",
        "CONFOUND_TRAP": "confound",
        "BEHAVIORAL_MIMIC": "mimic",
        "NONIDENTIFIABLE": "nonidentifiable",
        "INTERVENTION_ONLY": "intervention_only",
        "PARAMETER_FRAGILITY": "fragility",
        "ANALYSIS_FLEXIBILITY": "analysis_flex",
        "NEGATIVE_CONTROL_TRAP": "negative_control",
        "WEAK_NULL_EQUIVALENCE": "weak_null",
        "OOD_FAILURE": "ood",
        "MEASUREMENT_CIRCULARITY": "circularity",
        "SOFTWARE_BUG": "software_bug",
        "HYBRID_TRUTH": "hybrid",
        "OVERCOMPLEXITY": "overcomplex",
        "REEVALUATION_DRIFT": "drift",
        "REJECTED_ANCESTOR_RECOVERY": "ancestor",
        "SURPRISE_DISTRACTOR": "surprise",
        "EXPENSIVE_PERFECT_TEST": "expensive",
        "MYOPIC_INFORMATION_GAIN": "myopic",
        "SHARED_ANALYST_BIAS": "shared_bias",
    }
    return tuple(mapping[c] for c in components if c in mapping)


def make_world(label: str | Sequence[str], seed: int) -> World:
    components = (label,) if isinstance(label, str) else tuple(label)
    truth = "H0"
    initial = {"H0", "H1", "H2"}
    equivalent: Tuple[str, ...] = ()
    ancestor: Optional[str] = None
    requires_generation = False

    # Structural/search-space rules have explicit priority.
    if "HYBRID_TRUTH" in components:
        truth = "H4"
        requires_generation = True
    elif "MISSING_TRUE_HYPOTHESIS" in components or "MYOPIC_INFORMATION_GAIN" in components:
        truth = "H3"
        requires_generation = True
    elif "REJECTED_ANCESTOR_RECOVERY" in components:
        truth = "H0"
        initial = {"H1", "H2", "H3"}
        ancestor = "H0"
        requires_generation = True
    elif "DIVERSITY_COLLAPSE" in components:
        truth = "H2"

    if "NONIDENTIFIABLE" in components:
        truth = "H0"
        equivalent = ("H0", "H1")

    if "REEVALUATION_DRIFT" in components and ancestor is None:
        ancestor = "H0"

    world_id = "+".join(components) + f":{seed}"
    return World(
        world_id=world_id,
        components=components,
        seed=seed,
        truth=truth,
        initial=tuple(sorted(initial)),
        equivalent=equivalent,
        ancestor=ancestor,
        requires_generation=requires_generation,
        traps=_trap_names(components),
    )


class Environment:
    """Mediates all contact between a policy and hidden world state."""

    def __init__(self, world: World, policy_id: str):
        self._world = world
        stable = int(
            hashlib.sha256(f"{world.world_id}|{policy_id}".encode("utf-8")).hexdigest()[:16],
            16,
        )
        self._rng = random.Random(stable)
        self.state = PublicState(
            candidates=set(world.initial),
            scores={h: 0.0 for h in world.initial},
        )

    def can(self, action: str) -> bool:
        return self.state.budget >= ACTIONS[action]

    def act(self, action: str, *, surprise_mode: bool = False) -> bool:
        if action not in ACTIONS:
            raise KeyError(f"unknown action: {action}")
        st = self.state
        if not self.can(action):
            return False

        st.budget -= ACTIONS[action]
        st.spent += ACTIONS[action]
        st.history.append(action)

        if action == "preregister":
            st.preregistered = True
            return True

        if action == "residual":
            st.residual_seen = True
            return True

        if action in ("generate", "parallel_generate", "hybridize"):
            p = {"generate": 0.20, "parallel_generate": 0.45, "hybridize": 0.18}[action]
            if st.residual_seen:
                p += 0.45
            if action == "hybridize" and "HYBRID_TRUTH" in self._world.components:
                p = 0.90
            if "MYOPIC_INFORMATION_GAIN" in self._world.components and st.residual_seen:
                p = max(p, 0.85)
            if "REJECTED_ANCESTOR_RECOVERY" in self._world.components:
                p = min(p, 0.05)

            if self._world.truth not in st.candidates and self._rng.random() < min(p, 0.95):
                st.candidates.add(self._world.truth)
                st.scores.setdefault(self._world.truth, 0.0)
                st.generated_true_marker = True

            if surprise_mode and "H5" not in st.candidates and self._rng.random() < 0.75:
                st.candidates.add("H5")
                st.scores.setdefault("H5", 0.0)
                st.surprise_added = True
            return True

        if action == "ancestor" and self._world.ancestor and self._world.ancestor not in st.candidates:
            st.candidates.add(self._world.ancestor)
            st.scores.setdefault(self._world.ancestor, 0.0)
            if self._world.ancestor == self._world.truth:
                st.generated_true_marker = True

        self._detect(action)

        if action in {
            "observe",
            "compare",
            "intervene",
            "negative_control",
            "positive_control",
            "mist",
            "software_test",
            "sensitivity",
            "multiverse",
            "equivalence",
            "ood",
            "replicate",
            "ancestor",
            "independent_analysis",
            "simplify",
        }:
            self._apply_evidence(action)
        return True

    def _detect(self, action: str) -> None:
        detect_map = {
            "negative_control": {
                "CONFOUND_TRAP": "confound",
                "NEGATIVE_CONTROL_TRAP": "negative_control",
                "MEASUREMENT_CIRCULARITY": "circularity",
            },
            "software_test": {
                "SOFTWARE_BUG": "software_bug",
                "MEASUREMENT_CIRCULARITY": "circularity",
            },
            "sensitivity": {"PARAMETER_FRAGILITY": "fragility"},
            "multiverse": {
                "ANALYSIS_FLEXIBILITY": "analysis_flex",
                "MEASUREMENT_CIRCULARITY": "circularity",
            },
            "ood": {
                "OOD_FAILURE": "ood",
                "OVERCOMPLEXITY": "overcomplex",
                "SURPRISE_DISTRACTOR": "surprise",
            },
            "replicate": {
                "OOD_FAILURE": "ood",
                "SURPRISE_DISTRACTOR": "surprise",
                "SHARED_ANALYST_BIAS": "shared_bias",
            },
            "independent_analysis": {
                "SHARED_ANALYST_BIAS": "shared_bias",
                "ANALYSIS_FLEXIBILITY": "analysis_flex",
            },
            "simplify": {
                "OVERCOMPLEXITY": "overcomplex",
                "REEVALUATION_DRIFT": "drift",
            },
            "ancestor": {
                "REJECTED_ANCESTOR_RECOVERY": "ancestor",
                "REEVALUATION_DRIFT": "drift",
            },
            "equivalence": {
                "WEAK_NULL_EQUIVALENCE": "weak_null",
                "NONIDENTIFIABLE": "nonidentifiable",
                "BEHAVIORAL_MIMIC": "mimic",
            },
            "intervene": {
                "INTERVENTION_ONLY": "intervention_only",
                "BEHAVIORAL_MIMIC": "mimic",
                "CONFOUND_TRAP": "confound",
            },
            "mist": {
                "MEASUREMENT_CIRCULARITY": "circularity",
                "OVERCOMPLEXITY": "overcomplex",
            },
        }
        for component in self._world.components:
            marker = detect_map.get(action, {}).get(component)
            if marker:
                self.state.detected.add(marker)

    def _base_mean(self, hypothesis: str) -> float:
        if hypothesis == self._world.truth or hypothesis in self._world.equivalent:
            return 1.0
        return 0.0

    def _apply_evidence(self, action: str) -> None:
        st = self.state
        sd = {"observe": 0.55, "compare": 0.35, "intervene": 0.25}.get(action, 0.30)
        components = set(self._world.components)

        for h in list(st.candidates):
            mu = self._base_mean(h)

            if action == "observe":
                if components & {
                    "CONFOUND_TRAP",
                    "OOD_FAILURE",
                    "MEASUREMENT_CIRCULARITY",
                    "SOFTWARE_BUG",
                    "OVERCOMPLEXITY",
                    "SHARED_ANALYST_BIAS",
                }:
                    if h == "H1":
                        mu = max(mu, 1.25)
                    if h == self._world.truth:
                        mu = min(mu, 0.80)

                if components & {"BEHAVIORAL_MIMIC", "INTERVENTION_ONLY", "NONIDENTIFIABLE"}:
                    if h in {"H0", "H1"}:
                        mu = max(mu, 0.90)

                if "DIVERSITY_COLLAPSE" in components:
                    if h == "H1":
                        mu = max(mu, 1.15)
                    if h == "H2":
                        mu = min(mu, 0.80)

                if "ANALYSIS_FLEXIBILITY" in components and h == "H1":
                    mu = max(mu, 0.50 if st.preregistered else 1.10)

                if "NEGATIVE_CONTROL_TRAP" in components and h == "H1":
                    mu = max(mu, 1.15)

                if "WEAK_NULL_EQUIVALENCE" in components and h in {"H0", "H1"}:
                    mu = 0.50

                if "SURPRISE_DISTRACTOR" in components and h == "H5":
                    mu = max(mu, 1.25)
                if "SURPRISE_DISTRACTOR" in components and h == self._world.truth:
                    mu = min(mu, 0.85)

                if "REEVALUATION_DRIFT" in components and h == "H1":
                    mu = max(mu, 0.95)

            elif action == "compare":
                if components & {"BEHAVIORAL_MIMIC", "INTERVENTION_ONLY", "NONIDENTIFIABLE"}:
                    if h in {"H0", "H1"}:
                        mu = 0.90

                if "MYOPIC_INFORMATION_GAIN" in components:
                    if h == "H1":
                        mu = max(mu, 1.00)
                    if h == self._world.truth:
                        mu = min(mu, 0.40)

            elif action == "intervene":
                if "NONIDENTIFIABLE" in components:
                    mu = 1.0 if h in {"H0", "H1"} else -0.20
                else:
                    mu = 1.60 if h == self._world.truth else -0.20

            else:
                matched = {
                    "negative_control": {"CONFOUND_TRAP", "NEGATIVE_CONTROL_TRAP", "MEASUREMENT_CIRCULARITY"},
                    "software_test": {"SOFTWARE_BUG", "MEASUREMENT_CIRCULARITY"},
                    "sensitivity": {"PARAMETER_FRAGILITY"},
                    "multiverse": {"ANALYSIS_FLEXIBILITY", "MEASUREMENT_CIRCULARITY"},
                    "ood": {"OOD_FAILURE", "OVERCOMPLEXITY", "SURPRISE_DISTRACTOR"},
                    "replicate": {"OOD_FAILURE", "SURPRISE_DISTRACTOR", "SHARED_ANALYST_BIAS"},
                    "independent_analysis": {"SHARED_ANALYST_BIAS", "ANALYSIS_FLEXIBILITY"},
                    "simplify": {"OVERCOMPLEXITY", "REEVALUATION_DRIFT"},
                    "ancestor": {"REJECTED_ANCESTOR_RECOVERY", "REEVALUATION_DRIFT"},
                    "equivalence": {"WEAK_NULL_EQUIVALENCE", "NONIDENTIFIABLE", "BEHAVIORAL_MIMIC"},
                    "mist": {"MEASUREMENT_CIRCULARITY", "OVERCOMPLEXITY"},
                    "positive_control": set(),
                }

                if components & matched.get(action, set()):
                    if "NONIDENTIFIABLE" in components and action == "equivalence":
                        mu = 1.20 if h in {"H0", "H1"} else -0.30
                    else:
                        mu = 1.60 if h == self._world.truth else -0.40
                else:
                    mu = 0.70 if h == self._world.truth else 0.10

            st.scores[h] = st.scores.get(h, 0.0) + self._rng.gauss(mu, sd)


def public_decision(state: PublicState) -> Tuple[str, float]:
    """Terminal decision using only public state."""
    if "nonidentifiable" in state.detected:
        return "UNDERDETERMINED", 0.90

    if not state.candidates:
        return "UNDERDETERMINED", 0.10

    ranked = sorted(
        state.candidates,
        key=lambda h: (state.scores.get(h, 0.0), h),
        reverse=True,
    )
    best = ranked[0]
    second_score = (
        state.scores.get(ranked[1], 0.0)
        if len(ranked) > 1
        else state.scores.get(best, 0.0) - 1.0
    )
    gap = state.scores.get(best, 0.0) - second_score
    confidence = 1.0 / (1.0 + math.exp(-max(-5.0, min(5.0, gap))))
    return best, confidence


def _run_public_policy(env: Environment, policy_id: str) -> None:
    """Policy logic. This function has access to Environment methods + PublicState only."""
    s = env.state

    def act(name: str, **kwargs) -> bool:
        return env.act(name, **kwargs)

    if policy_id == "P0":
        act("generate")
        for _ in range(4):
            act("observe")

    elif policy_id == "P1":
        act("generate")
        act("preregister")
        for _ in range(4):
            act("observe")

    elif policy_id == "P2":
        act("generate")
        act("observe")
        act("observe")
        vals = sorted(s.scores.values(), reverse=True)
        gap = vals[0] - vals[1] if len(vals) > 1 else 99.0
        if vals and (vals[0] < 1.20 or gap < 0.80):
            act("residual")
            act("generate")
        act("compare")
        act("replicate")
        if env.can("observe"):
            act("observe")

    elif policy_id == "P3":
        for action in ("generate", "observe", "compare", "intervene", "compare", "ood"):
            if env.can(action):
                act(action)

    elif policy_id == "P5":
        for action in (
            "generate", "observe", "compare", "residual", "generate",
            "negative_control", "ancestor", "ood", "observe",
        ):
            if env.can(action):
                act(action)

    elif policy_id == "P6":
        for action in (
            "generate", "observe", "mist", "compare", "residual", "generate",
            "negative_control", "ancestor", "ood",
        ):
            if env.can(action):
                act(action)

    elif policy_id == "P7":
        for action in (
            "generate", "observe", "software_test", "mist", "compare",
            "negative_control", "intervene", "sensitivity", "multiverse",
            "equivalence", "ood", "ancestor",
        ):
            if env.can(action):
                act(action)

    elif policy_id == "P8":
        act("generate")
        act("observe")
        while s.budget >= 6:
            vals = sorted(s.scores.values(), reverse=True)
            best_score = vals[0] if vals else 0.0
            gap = vals[0] - vals[1] if len(vals) > 1 else 99.0

            if best_score < 1.20 and not s.residual_seen and env.can("residual"):
                act("residual")
                continue
            if s.residual_seen and s.history.count("generate") < 3 and env.can("generate"):
                act("generate")
                continue
            if gap < 0.70 and "intervene" not in s.history and env.can("intervene"):
                act("intervene")
                continue
            if "software_test" not in s.history and env.can("software_test"):
                act("software_test")
                continue
            if "negative_control" not in s.history and env.can("negative_control"):
                act("negative_control")
                continue
            if "sensitivity" not in s.history and env.can("sensitivity"):
                act("sensitivity")
                continue
            if "multiverse" not in s.history and env.can("multiverse"):
                act("multiverse")
                continue
            if gap < 1.0 and "equivalence" not in s.history and env.can("equivalence"):
                act("equivalence")
                continue
            if "ancestor" not in s.history and env.can("ancestor"):
                act("ancestor")
                continue
            if "ood" not in s.history and env.can("ood"):
                act("ood")
                continue
            if env.can("observe"):
                act("observe")
            else:
                break

    elif policy_id == "P9":
        act("generate")
        act("observe")
        vals = sorted(s.scores.values(), reverse=True)
        gap = vals[0] - vals[1] if len(vals) > 1 else 99.0
        if vals and vals[0] < 1.0:
            act("residual")
            act("generate")
        elif gap < 0.70 and env.can("compare"):
            act("compare")
        for action in ("negative_control", "ood", "ancestor", "observe"):
            if env.can(action):
                act(action)

    elif policy_id == "P10":
        for action in (
            "parallel_generate", "observe", "residual", "parallel_generate",
            "compare", "hybridize", "ood", "observe",
        ):
            if env.can(action):
                act(action)

    elif policy_id == "P11":
        act("parallel_generate", surprise_mode=True)
        act("observe")
        act("compare")
        if env.can("parallel_generate"):
            act("parallel_generate", surprise_mode=True)
        for action in ("replicate", "ood", "observe"):
            if env.can(action):
                act(action)

    elif policy_id == "P12":
        for action in (
            "parallel_generate", "observe", "independent_analysis", "compare",
            "negative_control", "intervene", "ood", "observe",
        ):
            if env.can(action):
                act(action)

    else:
        raise KeyError(f"unknown policy: {policy_id}")


def score_episode(world: World, policy_id: str) -> Dict[str, object]:
    env = Environment(world, policy_id)
    _run_public_policy(env, policy_id)
    s = env.state
    selected, confidence = public_decision(s)

    if "NONIDENTIFIABLE" in world.components:
        correct = selected == "UNDERDETERMINED"
    else:
        correct = selected == world.truth or selected in world.equivalent

    false_positive = (not correct) and confidence >= 0.80
    missing_recovery = world.requires_generation and selected == world.truth
    trapset = set(world.traps)
    failure_detected = True if not trapset else bool(trapset & s.detected)
    brier = (confidence - (1.0 if correct else 0.0)) ** 2

    return {
        "policy": policy_id,
        "world_id": world.world_id,
        "components": "+".join(world.components),
        "correct": int(correct),
        "false_positive": int(false_positive),
        "missing_recovery": int(missing_recovery),
        "confidence": round(confidence, 12),
        "brier": round(brier, 12),
        "failure_detected": int(failure_detected),
        "spent": s.spent,
        "budget_remaining": s.budget,
        "selected": selected,
        "truth": world.truth,
        "history": "|".join(s.history),
    }


def iter_worlds(split: str, n_per_class: int) -> Iterable[World]:
    if split == "ood":
        labels: Sequence[str | Sequence[str]] = META_COMPOSITIONS
    else:
        labels = WORLD_CLASSES

    base = SPLIT_BASE[split]
    for label_index, label in enumerate(labels):
        for i in range(n_per_class):
            yield make_world(label, base + label_index * 10_000 + i)


def run_benchmark(split: str, n_per_class: int) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for world in iter_worlds(split, n_per_class):
        for policy_id in POLICIES:
            rows.append(score_episode(world, policy_id))
    return rows


def summarize(rows: Sequence[Dict[str, object]]) -> Dict[str, object]:
    by_policy: Dict[str, List[Dict[str, object]]] = {p: [] for p in POLICIES}
    for row in rows:
        by_policy[str(row["policy"])].append(row)

    summaries = {}
    for policy, rws in by_policy.items():
        if not rws:
            continue
        summaries[policy] = {
            "episodes": len(rws),
            "accuracy": statistics.fmean(float(r["correct"]) for r in rws),
            "false_positive_rate": statistics.fmean(float(r["false_positive"]) for r in rws),
            "mean_brier": statistics.fmean(float(r["brier"]) for r in rws),
            "failure_detection_rate": statistics.fmean(float(r["failure_detected"]) for r in rws),
            "mean_cost": statistics.fmean(float(r["spent"]) for r in rws),
            "missing_recovery_rate_unconditional": statistics.fmean(float(r["missing_recovery"]) for r in rws),
        }

    # Pareto front over higher accuracy, lower FP, lower Brier, lower cost.
    front = []
    for p, a in summaries.items():
        dominated = False
        for q, b in summaries.items():
            if p == q:
                continue
            no_worse = (
                b["accuracy"] >= a["accuracy"]
                and b["false_positive_rate"] <= a["false_positive_rate"]
                and b["mean_brier"] <= a["mean_brier"]
                and b["mean_cost"] <= a["mean_cost"]
            )
            strictly_better = (
                b["accuracy"] > a["accuracy"]
                or b["false_positive_rate"] < a["false_positive_rate"]
                or b["mean_brier"] < a["mean_brier"]
                or b["mean_cost"] < a["mean_cost"]
            )
            if no_worse and strictly_better:
                dominated = True
                break
        if not dominated:
            front.append(p)

    return {"policies": summaries, "pareto_front": sorted(front)}


def write_csv(rows: Sequence[Dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("no rows")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def self_test() -> None:
    # Split/seed firewall
    assert SPLIT_BASE["train"] != SPLIT_BASE["validation"] != SPLIT_BASE["locked_test"]
    assert set(WORLD_CLASSES)
    assert all(cost > 0 for cost in ACTIONS.values())

    # Determinism across repeated execution.
    w = make_world("CONFOUND_TRAP", 12345)
    a = score_episode(w, "P8")
    b = score_episode(w, "P8")
    assert a == b, "benchmark must be exactly deterministic for same world/policy"

    # Budget invariant for every policy.
    for p in POLICIES:
        row = score_episode(make_world("SIMPLE_TRUE", 77), p)
        assert 0 <= int(row["spent"]) <= BUDGET

    # Answer-key isolation check: the public decision API accepts PublicState only.
    # It must be able to decide without a World argument.
    s = PublicState({"H0", "H1"}, {"H0": 1.0, "H1": 0.0})
    sel, conf = public_decision(s)
    assert sel == "H0" and 0.5 < conf < 1.0

    # Nonidentifiability is only declared after an allowed diagnostic reveals it.
    ni = make_world("NONIDENTIFIABLE", 90)
    env = Environment(ni, "TEST")
    sel0, _ = public_decision(env.state)
    assert sel0 != "UNDERDETERMINED"
    env.act("equivalence")
    sel1, _ = public_decision(env.state)
    assert sel1 == "UNDERDETERMINED"

    # Seed sets are disjoint for the first few worlds.
    tr = {w.seed for _, w in zip(range(50), iter_worlds("train", 5))}
    va = {w.seed for _, w in zip(range(50), iter_worlds("validation", 5))}
    te = {w.seed for _, w in zip(range(50), iter_worlds("locked_test", 5))}
    assert tr.isdisjoint(va) and tr.isdisjoint(te) and va.isdisjoint(te)

    print("SELF_TEST_PASS")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--split", choices=("train", "validation"), default="validation",
                   help="Locked test is intentionally not exposed by v001 development CLI.")
    p.add_argument("--n-per-class", type=int, default=250)
    p.add_argument("--output", type=Path, default=Path("results/methodology_v001.csv"))
    p.add_argument("--summary", type=Path, default=Path("results/methodology_v001_summary.json"))
    p.add_argument("--self-test", action="store_true")
    return p.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    if args.n_per_class < 1:
        raise SystemExit("--n-per-class must be >= 1")

    rows = run_benchmark(args.split, args.n_per_class)
    write_csv(rows, args.output)
    summary = summarize(rows)
    summary["split"] = args.split
    summary["n_per_class"] = args.n_per_class
    summary["world_classes"] = list(WORLD_CLASSES)
    summary["claim_ceiling"] = (
        "Development evidence only. TRAIN/VALIDATION cannot establish a benchmark winner; "
        "locked TEST + OOD meta-test + external real-case validation are still required."
    )
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
