"""Minimal source-derived offline reproduction, NOT native Typer or full OmniScientist.
Pinned upstream commit 1cbb9f6f6d793290326ca29df4d389fb64832f91
eval_cmd.py Git blob f3a3934243fdd82623004eddb8c9dffb6535cee0.
The complete 12-case raw test and independent verifier are in the local ZIP.
"""
import asyncio

async def render_eval(research_quality=False, quality_input=None, gate=False, record=False):
    events = []
    if research_quality or quality_input is not None:
        events.append("research_quality_renderer")
        return events
    events.append("capability_benchmark")
    if record or gate:
        events.append("trend_gate")
    return events

if __name__ == "__main__":
    assert asyncio.run(render_eval(research_quality=True, gate=True)) == ["research_quality_renderer"]
    assert asyncio.run(render_eval(quality_input="failing.json", gate=True, record=True)) == ["research_quality_renderer"]
    assert asyncio.run(render_eval(gate=True)) == ["capability_benchmark", "trend_gate"]
    print("3/3 bounded dispatch controls PASS; quality failure is not itself an exit gate.")
