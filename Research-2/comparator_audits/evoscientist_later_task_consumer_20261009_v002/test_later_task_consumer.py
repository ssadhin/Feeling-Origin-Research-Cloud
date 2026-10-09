"""Bounded predeclared ES-3/4/5 source-native retrieval -> scripted consumer sentinel.
Read ./pre_execution_protocol.md. No AI API calls; never modify upstream.
"""
import json
from pathlib import Path
import pytest

from EvoScientist.memory.observations import (
    MemoryScope, MemorySourceType, MemoryType, record_observation_file
)
from EvoScientist.memory.project import resolve_project_id
from EvoScientist.memory.observations.tools import (
    create_search_observations_tool, create_read_memory_tool
)

def write(memory_dir,workspace,kind):
    relevant=(kind=="relevant")
    return record_observation_file(
        memory_dir=memory_dir,project_id=resolve_project_id(workspace),
        memory_type=MemoryType.PROCEDURAL,
        summary=("Failed calibration strategy produced irreproducible measurements"
                  if relevant else "Failed habitat mapping produced unstable location estimates"),
        observation=("Earlier calibration strategy produced irreproducible estimates on a sensor."
                     if relevant else "Earlier habitat mapping took inconsistent coordinate fixes."),
        why_it_matters=("Check calibration before any direct measurement."
                        if relevant else "Check map landmarks before route selection."),
        scope=MemoryScope.PROJECT,source_type=MemorySourceType.SUBAGENT,
        source_session_id="task-one",source_agent="researcher")

def make_tools(memory_dir,workspace):
    project=resolve_project_id(workspace)
    return (
        create_search_observations_tool(memory_dir=memory_dir,project_id=project),
        create_read_memory_tool(memory_dir=memory_dir,project_id=project)
    )

def consumer(search_tool,read_tool,allow_read=True):
    """Predeclared script. ONLY returned native tool text can affect decision."""
    result=json.loads(search_tool.invoke({
        "query":"calibration","mode":"regex","scope":"project","limit":8
    }))
    hits=result.get("results",[])
    read_text=""
    read_calls=0
    if hits and allow_read:
        observation_id=hits[0].get("observation_id") or hits[0].get("id")
        assert observation_id, "official search result ID absent"
        payload=json.loads(read_tool.invoke({"observation_id":observation_id}))
        assert "error" not in payload,payload
        read_text=payload.get("text","")
        read_calls+=1
    decision=("CALIBRATE_FIRST" if
            "calibration strategy produced irreproducible" in read_text.lower()
            and "check calibration" in read_text.lower()
            else "DIRECT_MEASUREMENT")
    return {"search_hits":len(hits),"read_calls":read_calls,"action":decision}

def test_later_task_consumer_controls(tmp_path):
    a=tmp_path/"project_A";b=tmp_path/"project_B"
    a.mkdir();b.mkdir()
    relevant=tmp_path/"relevant_memories"
    empty=tmp_path/"empty_memories"
    irrelevant=tmp_path/"irrelevant_memories"
    saved=write(relevant,a,"relevant")
    assert saved is not None
    write(irrelevant,a,"irrelevant")
    search_relevant,read_relevant=make_tools(relevant,a)
    result_a=consumer(search_relevant,read_relevant)
    result_b=consumer(*make_tools(empty,a))
    result_c=consumer(*make_tools(irrelevant,a))
    result_d=consumer(*make_tools(relevant,b))
    result_e=consumer(search_relevant,read_relevant,allow_read=False)
    assert result_a["search_hits"]>=1 and result_a["read_calls"]==1
    assert result_a["action"]=="CALIBRATE_FIRST"
    assert result_b=={"search_hits":0,"read_calls":0,"action":"DIRECT_MEASUREMENT"}
    assert result_c=={"search_hits":0,"read_calls":0,"action":"DIRECT_MEASUREMENT"}
    assert result_d=={"search_hits":0,"read_calls":0,"action":"DIRECT_MEASUREMENT"}
    assert result_e["read_calls"]==0 and result_e["action"]=="DIRECT_MEASUREMENT"
    print("SENTINEL_RESULTS "+json.dumps({"A_memory_on":result_a,
        "B_memory_empty":result_b,"C_irrelevant_negative":result_c,
        "D_other_project":result_d,"E_no_read":result_e},sort_keys=True))
