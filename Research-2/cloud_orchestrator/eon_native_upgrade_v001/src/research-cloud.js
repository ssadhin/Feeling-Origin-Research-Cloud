/* Eon MCP Agent: integrated cloud-native, condition-driven research continuation.
 * Existing authenticated Eon workspace link; no new MCP installation.
 * v0.1 is smoke-only; independent prospective science is NOT self-certified.
 */
import { DurableObject, WorkflowEntrypoint } from 'cloudflare:workers';
import { advance, validRunId } from './cloud-decision.mjs';

const PROGRAM = 'Research-2-AES-v2';
const GOAL = 'Determine using independent, frozen prospective tests whether AES v2 is superior, equivalent, inferior or inconclusive against six strong research methodologies for the four-function virtual-organism research case.';
const ACTIONS = Object.freeze([
  {action:'research_capabilities',description:'Describe Eon cloud research continuity, no online PC needed',arguments_schema:{type:'object',properties:{}}},
  {action:'research_status',description:'Read the authenticated workspace persistent cloud run and current loop',arguments_schema:{type:'object',properties:{}}},
  {action:'research_history',description:'Read a bounded ledger of persisted, classified cloud loop events',arguments_schema:{type:'object',properties:{}}},
  {action:'research_start',description:'Start THREE event-driven smoke loops immediately chained by goal condition; NOT scientific research',arguments_schema:{type:'object',properties:{mode:{type:'string',enum:['smoke']}}}},
  {action:'research_pause',description:'Pause further cloud loops independent of PC connection',arguments_schema:{type:'object',properties:{}}}
]);
const respond=(data,status=200)=>Response.json(data,{status,headers:{'cache-control':'no-store'}});
function validWorkspace(s){return typeof s==='string' && /^[a-zA-Z0-9_-]{12,128}$/.test(s);}
function storageStub(env,workspaceId){return env.RESEARCH_CONTROL.get(env.RESEARCH_CONTROL.idFromName(PROGRAM+':'+workspaceId));}
async function control(env,workspaceId,path,body=null){
 const req={method:body===null?'GET':'POST'};
 if(body!==null){req.headers={'content-type':'application/json'};req.body=JSON.stringify(body);}
 const r=await storageStub(env,workspaceId).fetch('https://eon-cloud-internal'+path,req);
 let data;try{data=await r.json();}catch{data={error:'UNPARSEABLE_CONTROL_RESPONSE'};}
 return {status:r.status,body:data};
}
function details(env){return {
 engine:'cloud',name:'Eon Agent MCP native Cloud Research Continuation',
 delivery:'Same authenticated Eon MCP link and original tools eon_device, eon_catalog, eon_run',
 infrastructure:'Cloudflare Eon Worker + Durable Objects + Workflows; NOT bound to a laptop relay',
 operation:'Next loop triggered by prior workflow completion condition; never scheduled polling',
 requires_online_device:false,mode:env.RESEARCH_MODE||'disabled',
 autonomous_scientific_research_activated:false,
 actual_capability:'Three-loop cloud-only smoke test; NO scientific experiments or OpenAI prompting while cloud research executor is not authorized',
 goal:GOAL,
 status:'Official AES-v2 prospective methodology superiority UNTESTED; six rival fidelity 0/6 at canonical 17T; no positive claim authorized',
 actions:ACTIONS
};}
export function researchCatalogData(env,workspaceId,query=''){
 if(!validWorkspace(workspaceId))return {status:403,body:{error:'WORKSPACE_AUTH_REQUIRED'}};
 const description=details(env);const s=String(query||'').toLowerCase();
 if(s)description.actions=ACTIONS.filter(x=>x.action.includes(s)||x.description.toLowerCase().includes(s));
 return {status:200,body:description};
}
export async function researchToolData(env,args,workspaceId){
 if(!validWorkspace(workspaceId))return {status:403,body:{error:'WORKSPACE_AUTH_REQUIRED'}};
 if(!env.RESEARCH_CONTROL||!env.RESEARCH_FLOW)return {status:503,body:{error:'CLOUD_BINDINGS_MISSING'}};
 const action=String(args.action||'research_capabilities');
 if(action==='research_capabilities')return {status:200,body:details(env)};
 if(action==='research_status'){
  const r=await control(env,workspaceId,'/state');
  return {status:r.status,body:{...r.body,engine:'cloud',goal:GOAL}};
 }
 if(action==='research_history')return control(env,workspaceId,'/history');
 if(action==='research_pause')return control(env,workspaceId,'/pause',{});
 if(action==='research_start'){
  const mode=String(args.arguments?.mode||'smoke');
  if(mode!=='smoke'||env.RESEARCH_MODE!=='smoke')return {status:409,body:{error:'SCIENTIFIC_AUTOMATION_NOT_ARMED',mode:env.RESEARCH_MODE||'disabled'}};
  const runId=crypto.randomUUID();
  const init=await control(env,workspaceId,'/start',{runId,mode,maxLoops:3});
  if(init.status!==200)return init;
  const id='eon-r2-'+runId+'-loop-0000';
  try{
   const instance=await env.RESEARCH_FLOW.create({id,params:{workspaceId,runId,loop:0,mode}});
   return {status:200,body:{ok:true,runId,workflowInstance:instance.id,cloudOnly:true,clockSchedule:false,maxSmokeLoops:3,sciencePerformed:false}};
  }catch(e){
   await control(env,workspaceId,'/pause',{});
   return {status:503,body:{error:'WORKFLOW_CREATION_FAILED',detail:String(e).slice(0,170)}};
  }
 }
 return {status:400,body:{error:'UNKNOWN_CLOUD_ACTION',actions:ACTIONS.map(x=>x.action)}};
}
export class ResearchControl extends DurableObject {
 async fetch(request){
  const pathname=new URL(request.url).pathname;
  const state=await this.ctx.storage.get('state');
  if(pathname==='/state')return respond({state:state||null});
  if(pathname==='/history'){
   if(!state)return respond({state:null,events:[]});
   const e=await this.ctx.storage.list({prefix:'event-'+state.runId+'-',limit:40});
   return respond({state,events:[...e.values()].slice(-30)});
  }
  if(pathname==='/start'&&request.method==='POST'){
   if(state?.status==='RUNNING')return respond({error:'ACTIVE_RUN_EXISTS',state},409);
   const b=await request.json().catch(()=>({}));
   if(!validRunId(b.runId)||b.mode!=='smoke'||b.maxLoops!==3)return respond({error:'INVALID_SMOKE_CONFIGURATION'},400);
   const next={runId:b.runId,status:'RUNNING',mode:'smoke',nextLoop:0,maxLoops:3,
     startedAt:new Date().toISOString(),lastOutcome:null,auditedTargets:[],goalMet:false,scientificTrials:0};
   await this.ctx.storage.put('state',next);
   return respond({ok:true,state:next});
  }
  if(pathname==='/pause'&&request.method==='POST'){
   if(!state)return respond({error:'RUN_MISSING'},404);
   if(state.status!=='RUNNING')return respond({ok:true,state});
   const next={...state,status:'PAUSED',lastOutcome:'User paused. Scientific goal remains untested.'};
   await this.ctx.storage.put('state',next);
   return respond({ok:true,state:next});
  }
  if(pathname==='/claim'&&request.method==='POST'){
   const b=await request.json().catch(()=>({}));
   if(!state||state.runId!==b.runId||state.nextLoop!==b.loop||state.status!=='RUNNING')return respond({error:'OUT_OF_ORDER_OR_PAUSED',state:state||null},409);
   return respond({ok:true,state});
  }
  if(pathname==='/commit'&&request.method==='POST'){
   const b=await request.json().catch(()=>({}));
   if(!state)return respond({error:'NO_ACTIVE_LEDGER'},404);
   const key='event-'+b.runId+'-'+String(b.loop).padStart(4,'0');
   const prev=await this.ctx.storage.get(key);
   if(prev && prev.runId===b.runId && prev.loop===b.loop){
    return respond({ok:true,alreadyCommitted:true,state,continue:state.runId===b.runId&&state.status==='RUNNING'&&state.nextLoop===b.loop+1});
   }
   let next;try{next=advance(state,b);}catch(e){return respond({error:String(e.message||e)},409);}
   await this.ctx.storage.put(key,{...b,committedAt:new Date().toISOString()});
   await this.ctx.storage.put('state',next.state);
   return respond({ok:true,...next});
  }
  return respond({error:'UNSUPPORTED_CONTROL_ACTION'},404);
 }
}
export class ResearchLoopWorkflow extends WorkflowEntrypoint {
 async run(event,step){
  const {workspaceId,runId,loop,mode}=event.payload||{};
  if(!validWorkspace(workspaceId)||!validRunId(runId)||!Number.isInteger(loop)||loop<0||mode!=='smoke')return {stopped:true,error:'UNAUTHORIZED_OR_UNSUPPORTED_WORKFLOW_INPUT'};
  const claim=await step.do('claim-exact-workspace-loop',async()=>await control(this.env,workspaceId,'/claim',{runId,loop}));
  if(claim.status!==200||!claim.body.ok)return {stopped:true,reason:'NOT_CURRENT_OR_PAUSED'};
  let outcome;
  try{
   outcome=await step.do('cloud-event-only-no-LLM-no-research',async()=>({
    runId,loop,status:'CONTINUE',goalMet:false,scientificTrials:0,
    summary:'Eon cloud smoke loop '+loop+' completed; research goal remains scientifically untested',
    evidence:{cloudOnly:true,eventTriggered:true,noResearchClaim:true,deviceRelayNotUsed:true}
   }));
  }catch(e){outcome={runId,loop,status:'BLOCKED',summary:'Cloud smoke step failed',evidence:{type:String(e?.name||'Error')}};}
  const record=await step.do('commit-durable-evidence-and-state',async()=>await control(this.env,workspaceId,'/commit',outcome));
  if(record.status!==200||!record.body.ok)return {stopped:true,error:'COMMIT_REJECTED'};
  if(record.body.continue){
   const nxt=loop+1;
   const next=await step.do('trigger-next-unresolved-loop-now',async()=>{
    const id='eon-r2-'+runId+'-loop-'+String(nxt).padStart(4,'0');
    try{const instance=await this.env.RESEARCH_FLOW.create({id,params:{workspaceId,runId,loop:nxt,mode}});return {instanceId:instance.id};}
    catch(e){if(/duplicate|exist|conflict/i.test(String(e)))return {instanceId:id,alreadyExists:true};throw e;}
   });
   return {finishedLoop:loop,immediateSuccessor:next,goalMet:false};
  }
  return {finishedLoop:loop,finalStatus:record.body.state?.status,goalMet:false,noSuccessor:true};
 }
}