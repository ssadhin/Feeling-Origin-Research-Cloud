import test from 'node:test';
import assert from 'node:assert/strict';
import { RIVALS,narrowDecision,advance,validRunId } from '../src/cloud-decision.mjs';
test('all six rivals pinned with 40-character immutable hashes',()=>{assert.equal(Object.keys(RIVALS).length,6);for(const v of Object.values(RIVALS))assert.match(v[2],/^[a-f0-9]{40}$/)});
test('reject unsupported and unpinned AI actions',()=>{
 assert.throws(()=>narrowDecision({action:'EXECUTE_SHELL',reason:'Try dangerous command'}));
 assert.throws(()=>narrowDecision({action:'AUDIT_SOURCE',target:'other',reason:'Some valid rationale'}));
 assert.deepEqual(narrowDecision({action:'AUDIT_SOURCE',target:'evomaster',reason:'Audit native source boundary'}),{action:'AUDIT_SOURCE',target:'evomaster',reason:'Audit native source boundary'});
});
test('continue instantly until explicit budget pause; not mistaken for success',()=>{
 let s={runId:'aaaa',status:'RUNNING',nextLoop:8,maxLoops:10};
 let r=advance(s,{runId:'aaaa',loop:8,status:'CONTINUE',summary:'More fidelity required'});
 assert.equal(r.continue,true);assert.equal(r.state.nextLoop,9);
 r=advance(r.state,{runId:'aaaa',loop:9,status:'CONTINUE',summary:'Further work required'});
 assert.equal(r.continue,false);assert.equal(r.state.status,'PAUSED_BUDGET');
});
test('cannot certify AES victory or skip a loop through model output',()=>{
 const s={runId:'aaaa',status:'RUNNING',nextLoop:1,maxLoops:10};
 assert.throws(()=>advance(s,{runId:'aaaa',loop:1,status:'GOAL_MET',summary:'Claimed best'}));
 assert.throws(()=>advance(s,{runId:'aaaa',loop:2,status:'CONTINUE',summary:'Skipped loop'}));
});
test('blockers stop without inventing progress',()=>{
 const r=advance({runId:'aaaa',status:'RUNNING',nextLoop:8,maxLoops:10},{runId:'aaaa',loop:8,status:'BLOCKED',summary:'Missing credentials'});
 assert.equal(r.continue,false);assert.equal(r.state.status,'BLOCKED');
});
test('strict run identifiers',()=>{assert.ok(validRunId('11111111-1111-4111-a111-111111111111'));assert.equal(validRunId('../../etc'),false)});