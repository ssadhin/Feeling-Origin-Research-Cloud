"""Nondecisive source-native EvoScientist ES-3/ES-4/ES-5 context sentinel.
No provider calls, no source changes, no final-policy or outcome claims.
"""
from types import SimpleNamespace
from langchain_core.messages import SystemMessage
from EvoScientist.memory.observations import (
    MemoryScope, MemorySourceType, MemoryType, record_observation_file
)
from EvoScientist.memory.project import resolve_project_id
from EvoScientist.middleware.memory import create_memory_middleware

MARKER = "FAILED_ROBOT_CALIBRATION_DIRECTION_20261009_X7"

def req():
    request = SimpleNamespace(
        state={}, runtime=object(), system_message=SystemMessage(content="base next task")
    )
    request.override = lambda **kw: SimpleNamespace(
        state=request.state, runtime=request.runtime,
        system_message=kw.get("system_message", request.system_message)
    )
    return request

def inject(memories, workspace, enabled):
    agent = create_memory_middleware(
        str(memories), workspace_dir=workspace,
        enable_profile_memory=False, enable_observation_memory=enabled,
        enable_observation_tool=False,
    )
    return str(agent.modify_request(req()).system_message.content)

def record_failed_direction(memories, workspace):
    return record_observation_file(
        memory_dir=memories,
        project_id=resolve_project_id(workspace),
        memory_type=MemoryType.PROCEDURAL,
        summary=MARKER + ": prior calibration strategy produced irreproducible estimates.",
        observation="Prior task failed: calibration artifact varied between repeated instrument trials.",
        why_it_matters="Later tasks should check calibration before repeating the same approach.",
        scope=MemoryScope.PROJECT,
        source_type=MemorySourceType.SUBAGENT,
        source_session_id="task-one",
        source_agent="research-agent"
    )

def test_prior_failed_direction_reaches_later_task_only_with_memory(tmp_path):
    workspace = tmp_path / "project_A"
    workspace.mkdir()
    memories = tmp_path / "memories"
    before = inject(memories, workspace, enabled=True)
    assert MARKER not in before
    saved = record_failed_direction(memories, workspace)
    assert saved is not None
    later_task_with_memory = inject(memories, workspace, enabled=True)
    later_task_ablated = inject(memories, workspace, enabled=False)
    assert MARKER in later_task_with_memory
    assert MARKER not in later_task_ablated
    assert "base next task" in later_task_with_memory

def test_project_scoped_failed_direction_not_in_other_workspace(tmp_path):
    workspace_a = tmp_path / "project_A"
    workspace_b = tmp_path / "project_B"
    workspace_a.mkdir()
    workspace_b.mkdir()
    memories = tmp_path / "memories"
    record_failed_direction(memories, workspace_a)
    assert MARKER in inject(memories, workspace_a, enabled=True)
    assert MARKER not in inject(memories, workspace_b, enabled=True)
