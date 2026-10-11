#!/usr/bin/env python3
"""Research #2 nondecisive, isolated original-source GitHub compute sentinel."""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import logging
import os
import pathlib
import platform
import subprocess
import sys
import time
import types
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

ROOT = pathlib.Path(__file__).resolve().parents[2]
WORK = ROOT / "research2" / "qualification" / "workspace"
OUT = ROOT / "research2" / "qualification" / "output"
PIN = "96bd51617cfdbb494a9fc283af00fe090edfae48"
ORIGIN = "https://github.com/SakanaAI/AI-Scientist-v2.git"
OUT.mkdir(parents=True, exist_ok=True)
start = time.monotonic()
results = []
def run(cmd, cwd=None):
    completed = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=180)
    if completed.returncode:
        raise RuntimeError(f"{cmd[0]} code={completed.returncode}: {completed.stderr[-1200:]}")
    return completed.stdout.strip()
def check(label, action):
    try:
        result = action()
        results.append({"label": label, "verdict": "PASS", "evidence": result})
    except Exception as e:
        results.append({"label": label, "verdict": "FAIL", "error": type(e).__name__ + ": " + str(e)})
source_hash = None
commit = None
def checkout():
    global source_hash, commit
    WORK.mkdir(parents=True, exist_ok=False)
    run(["git", "init", "-q"], WORK)
    run(["git", "remote", "add", "origin", ORIGIN], WORK)
    run(["git", "-c", "protocol.version=2", "fetch", "--quiet", "--no-tags", "--depth=1", "origin", PIN], WORK)
    run(["git", "checkout", "-q", "--detach", "FETCH_HEAD"], WORK)
    commit = run(["git", "rev-parse", "HEAD"], WORK)
    assert commit == PIN, "pinned-commit mismatch"
    assert not run(["git", "status", "--porcelain", "--untracked-files=all"], WORK)
    path = WORK / "ai_scientist" / "treesearch" / "journal.py"
    source_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    assert source_hash
    return "original git checkout exact pinned commit and clean worktree"
check("AIS_ORIGINAL_GIT_PIN", checkout)
def sentinel():
    assert commit == PIN, "cannot execute without pinned source"
    path = WORK / "ai_scientist" / "treesearch" / "journal.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name in {"Node", "Journal"}]
    assert [n.name for n in classes] == ["Node", "Journal"], "original classes absent"
    program = ast.Module(
        body=[ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0)] + classes,
        type_ignores=[])
    ast.fix_missing_locations(program)
    class DataClassJsonMixin:
        pass
    env = {
        "__name__": "research2_ais_original_ast", "DataClassJsonMixin": DataClassJsonMixin,
        "dataclass": dataclass, "field": field, "uuid": uuid, "time": time, "copy": copy,
        "json": json, "logging": logging, "logger": logging.getLogger("r2_q1"), "pathlib": pathlib,
        "Path": pathlib.Path, "Any": Any, "Dict": Dict, "List": List,
        "Literal": Literal, "Optional": Optional, "MetricValue": float, "WorstMetricValue": float,
        "ExecutionResult": object,
    }
    mod = types.ModuleType(env["__name__"])
    mod.__dict__.update(env)
    sys.modules[mod.__name__] = mod
    exec(compile(program, filename=str(path), mode="exec"), mod.__dict__, mod.__dict__)
    Node, Journal = mod.Node, mod.Journal
    root = Node(id="r", metric=1, is_buggy=False, is_buggy_plots=False)
    candidate = Node(id="valid", parent=root, metric=5, is_buggy=False, is_buggy_plots=False)
    mutant = Node(id="excluded", parent=root, metric=100, is_buggy=True, is_buggy_plots=False)
    assert root.children == {candidate, mutant}
    j = Journal()
    for node in (root, candidate, mutant):
        j.append(node)
    assert len(j) == 3
    assert [x.step for x in j.nodes] == [0, 1, 2]
    assert j.draft_nodes == [root]
    assert j.buggy_nodes == [mutant]
    assert j.good_nodes == [root, candidate]
    assert j.get_best_node(only_good=True, use_val_metric_only=True) is candidate
    mutant.is_buggy = False
    assert j.buggy_nodes == []
    assert len(j.good_nodes) == 3
    assert j.get_best_node(only_good=True, use_val_metric_only=True) is mutant
    assert j.get_node_by_id("valid") is candidate
    return "original Node tree, Journal filters, metric-only best selection and negative flag mutation"
check("AIS_ORIGINAL_NODE_JOURNAL_BEHAVIOR", sentinel)
def final_clean():
    assert run(["git", "rev-parse", "HEAD"], WORK) == PIN
    assert not run(["git", "status", "--porcelain", "--untracked-files=all"], WORK)
    return "source unchanged at pinned HEAD"
check("AIS_SOURCE_CLEAN_POST", final_clean)
receipt = {
    "program": "Research2", "stage": "Q1_NOT_DECISIVE",
    "full_19C_method_certified": False, "head_to_head_trials": 0,
    "origin": ORIGIN, "pinned_sha": PIN, "actual_sha": commit,
    "original_source_sha256": source_hash,
    "platform": platform.platform(), "python": sys.version.split()[0],
    "cpu_count": os.cpu_count(), "elapsed_seconds": round(time.monotonic() - start, 3),
    "checks": results, "pass": sum(r["verdict"] == "PASS" for r in results),
    "fail": sum(r["verdict"] == "FAIL" for r in results)
}
p = OUT / "cloud_source_qualification_receipt.json"
p.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(receipt, sort_keys=True))
sys.exit(1 if receipt["fail"] else 0)
