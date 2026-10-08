// Pure, auditable state machine. No I/O, cloud services or hidden globals.
export const RIVALS = Object.freeze({
  'ai-scientist-v2': ['SakanaAI','AI-Scientist-v2','96bd51617cfdbb494a9fc283af00fe090edfae48'],
  'internagent': ['InternScience','InternAgent','fa8c3eedfa9751d3752ea6eb49220b303ac2397d'],
  'omniscientist-v2': ['tsinghua-fib-lab','OmniScientist-V2','1cbb9f6f6d793290326ca29df4d389fb64832f91'],
  'evoscientist': ['EvoScientist','EvoScientist','3b382b92b8fdad6e1f13467c382dcdd91d9b19d2'],
  'researchloop': ['plan-lab-szu','ResearchLoop','7e0a4fbe0cf646f4c859b6d20e46870d73abb11a'],
  'evomaster': ['sjtu-sai-agents','EvoMaster','36a52bc6c42a6b9fd710a41c52f3c3bb948b9ac9']
});
export function validRunId(s) { return typeof s === 'string' && /^[a-f0-9-]{36}$/.test(s); }
export function narrowDecision(o) {
  if (!o || typeof o !== 'object') throw Error('Model decision missing');
  if (!['AUDIT_SOURCE','BLOCKED'].includes(o.action)) throw Error('Unsupported action');
  if (o.action === 'AUDIT_SOURCE' && !Object.hasOwn(RIVALS,o.target)) throw Error('Unpinned source');
  if (typeof o.reason !== 'string' || o.reason.length < 10 || o.reason.length > 2000) throw Error('Invalid rationale');
  return {action:o.action, target:o.action === 'AUDIT_SOURCE'?o.target:null, reason:o.reason};
}
export function advance(s, outcome) {
  if (!s || s.status !== 'RUNNING' || !Number.isInteger(s.nextLoop)) throw Error('State not running');
  if (outcome.runId !== s.runId || outcome.loop !== s.nextLoop) throw Error('Out of sequence outcome');
  if (!['CONTINUE','BLOCKED','PAUSED'].includes(outcome.status)) throw Error('Non-evidence terminal claim rejected');
  const newState = {...s, nextLoop:s.nextLoop + 1, lastOutcome:outcome.summary};
  if (outcome.status === 'CONTINUE' && outcome.decision?.action === 'AUDIT_SOURCE') {
    const prev=Array.isArray(s.auditedTargets)?s.auditedTargets:[];
    if(prev.includes(outcome.decision.target))throw Error('Audit already performed for pinned source');
    newState.auditedTargets=[...prev,outcome.decision.target];
  }
  if (outcome.status === 'BLOCKED') newState.status = 'BLOCKED';
  else if (outcome.status === 'PAUSED') newState.status = 'PAUSED';
  else if (newState.nextLoop >= s.maxLoops) newState.status = 'PAUSED_BUDGET';
  return {state:newState, continue:newState.status === 'RUNNING'};
}