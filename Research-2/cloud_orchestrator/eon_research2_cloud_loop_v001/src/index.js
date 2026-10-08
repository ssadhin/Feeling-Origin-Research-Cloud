import { DurableObject, WorkflowEntrypoint } from 'cloudflare:workers';
import { RIVALS, narrowDecision, advance, validRunId } from './decision.mjs';

const FOLDER='1PXwQlCDQfRLKvPQo3QuGX5-DiI7L4LbQ';
const GITHUB='ssadhin/Feeling-Origin-Research-Cloud';
const BRANCH='research2-provenance-v001';
const PREFIX='Research-2/cloud_orchestrator/loops';
const PENDING='AES methodology superiority NOT ESTABLISHED; 0 prospective Research #2 decisive trials in 17S';

function json(data,status=200){return Response.json(data,{status,headers:{'cache-control':'no-store'}})}
function ctl(env){return env.CONTROL.get(env.CONTROL.idFromName('Research-2-AES-v2'))}
async function control(env,path,body){const r=await ctl(env).fetch('https://internal'+path,{method:body?'POST':'GET',headers:{'content-type':'application/json'},body:body?JSON.stringify(body):undefined});return await r.json()}
function auth(req,env){const h=req.headers.get('authorization');return !!env.ADMIN_TOKEN && h===`Bearer ${env.ADMIN_TOKEN}`}
function limits(env){const n=Number(env.MAX_LOOPS||12);return Number.isSafeInteger(n)&&n>0?Math.min(n,100):12}

// Single globally consistent state and event ledger, persisted in Cloudflare Durable Object storage.
export class ResearchControl extends DurableObject{
 async fetch(request){
  const url=new URL(request.url); const path=url.pathname;
  const s=await this.ctx.storage.get('state');
  if(path==='/state')return json({state:s||null});
  if(path==='/history')return json({state:s||null,events:(await this.ctx.storage.list({prefix:'event-'})).size});
  if(path==='/start'&&request.method==='POST'){
   if(s&&s.status==='RUNNING')return json({error:'RUN_ALREADY_ACTIVE',state:s},409);
   const b=await request.json();
   if(!validRunId(b.runId)||!Number.isInteger(b.maxLoops)||b.maxLoops<1||b.maxLoops>100)return json({error:'INVALID_RUN'},400);
   const next={runId:b.runId,status:'RUNNING',nextLoop:0,maxLoops:b.maxLoops,mode:b.mode,startedAt:new Date().toISOString(),lastOutcome:null,auditedTargets:[]};
   await this.ctx.storage.put('state',next);
   return json({ok:true,state:next});
  }
  if(path==='/pause'&&request.method==='POST'){
   if(!s)return json({error:'RUN_MISSING'},404);
   const next={...s,status:'PAUSED',lastOutcome:'Paused by authorized user'};
   await this.ctx.storage.put('state',next);return json({ok:true,state:next});
  }
  if(path==='/claim'&&request.method==='POST'){
   const b=await request.json();
   if(!s||s.runId!==b.runId||s.status!=='RUNNING'||s.nextLoop!==b.loop)return json({error:'NOT_CURRENT',state:s||null},409);
   return json({ok:true,state:s});
  }
  if(path==='/commit'&&request.method==='POST'){
   const outcome=await request.json();
   if(!s)return json({error:'NO_RUN'},404);
   const previous=await this.ctx.storage.get('event-'+String(outcome.loop).padStart(4,'0'));
   if(previous&&previous.runId===outcome.runId&&previous.loop===outcome.loop){
    return json({ok:true,alreadyCommitted:true,state:s,continue:s.status==='RUNNING'&&s.nextLoop===outcome.loop+1});
   }
   let a;try{a=advance(s,outcome)}catch(e){return json({error:String(e.message||e)},409)}
   // Put evidence before transition; exact replays remain idempotent by step checkpointing.
   await this.ctx.storage.put('event-'+String(outcome.loop).padStart(4,'0'),{...outcome,committedAt:new Date().toISOString()});
   await this.ctx.storage.put('state',a.state);
   return json({ok:true,...a});
  }
  return json({error:'NOT_FOUND'},404);
 }
}

async function oauthGoogle(env){
 const params=new URLSearchParams({client_id:env.GOOGLE_CLIENT_ID,client_secret:env.GOOGLE_CLIENT_SECRET,refresh_token:env.GOOGLE_REFRESH_TOKEN,grant_type:'refresh_token'});
 const response=await fetch('https://oauth2.googleapis.com/token',{method:'POST',headers:{'content-type':'application/x-www-form-urlencoded'},body:params});
 if(!response.ok)throw Error('GOOGLE_OAUTH_REFRESH_FAILED:'+response.status);
 const t=await response.json();if(!t.access_token)throw Error('GOOGLE_OAUTH_ACCESS_TOKEN_EMPTY');return t.access_token;
}
async function googleJSON(url,access){const r=await fetch(url,{headers:{authorization:'Bearer '+access}});if(!r.ok)throw Error('GOOGLE_API_'+r.status);return await r.json()}
function docText(doc){
 const chunks=[];
 function traverse(x){if(!x||typeof x!=='object')return; if(x.textRun?.content)chunks.push(x.textRun.content);
  if(Array.isArray(x))for(const p of x)traverse(p);
  else for(const [k,v]of Object.entries(x))if(k!=='textRun'&&k!=='suggestedInsertionIds')traverse(v);
 }
 traverse(doc.tabs||doc.body||doc);return chunks.join('').slice(0,24000);
}
async function readLatestStatus(env){
 const a=await oauthGoogle(env);
 const q=`'${FOLDER}' in parents and name contains '17' and trashed = false`;
 const uri='https://www.googleapis.com/drive/v3/files?'+new URLSearchParams({q,fields:'nextPageToken,files(id,name,modifiedTime,mimeType)',page_size:'100',pageSize:'100',orderBy:'modifiedTime desc'});
 const files=(await googleJSON(uri,a)).files||[];
 const statuses=files.filter(f=>/^17[A-Z]?_RESEARCH_2_CURRENT_STATUS/.test(f.name)).sort((x,y)=>y.modifiedTime.localeCompare(x.modifiedTime));
 if(!statuses.length)throw Error('NO_CANONICAL_17_STATUS_IN_DRIVE');
 const f=statuses[0]; const doc=await googleJSON(`https://docs.googleapis.com/v1/documents/${encodeURIComponent(f.id)}?includeTabsContent=true`,a);
 const text=docText(doc);
 if(!text.includes('RESEARCH #2')||text.length<200)throw Error('CANONICAL_DRIVE_STATUS_EMPTY_OR_UNREADABLE');
 return {id:f.id,name:f.name,modified:f.modifiedTime,text};
}
async function githubAPI(env,path,method='GET',body){
 const headers={authorization:`Bearer ${env.GITHUB_TOKEN}`,accept:'application/vnd.github+json','x-github-api-version':'2022-11-28','user-agent':'eon-research2-cloud-loop'};
 if(body)headers['content-type']='application/json';
 const r=await fetch('https://api.github.com/'+path,{method,headers,body:body?JSON.stringify(body):undefined});
 const text=await r.text();return {ok:r.ok,status:r.status,data:text?JSON.parse(text):null};
}
async function decideNext(env,statusText,loop,auditedTargets){
 const pinned=Object.fromEntries(Object.entries(RIVALS).map(([k,v])=>[k,{repo:v[0]+'/'+v[1],sha:v[2]}]));
 const input=`Verify Research #2 Phase-3 next *legitimate* source acquisition/fidelity task. You are NOT authorized to freeze a scientific verdict. Any independent review not actually supplied remains BLOCKED. Read this latest canonical status:\n${statusText.slice(0,18000)}\n\nLoop index: ${loop}. Already audited in this chain: ${JSON.stringify(auditedTargets)}. DO NOT repeat these. Immutable pinned repositories: ${JSON.stringify(pinned)}. Choose one source boundary audit if permissible; if status shows that a needed safety gate blocks such an audit, choose BLOCKED. No code execution by text, no provider/tool advantage, no AES favoritism.`;
 const schema={type:'object',properties:{action:{type:'string',enum:['AUDIT_SOURCE','BLOCKED']},target:{type:'string',enum:[...Object.keys(RIVALS),'none']},reason:{type:'string'}},required:['action','target','reason'],additionalProperties:false};
 const r=await fetch('https://api.openai.com/v1/responses',{method:'POST',headers:{authorization:`Bearer ${env.OPENAI_API_KEY}`,'content-type':'application/json'},body:JSON.stringify({model:env.OPENAI_MODEL||'gpt-5',store:false,input:[{role:'system',content:'You are a hostile-to-all-sides independent research auditor; never fabricate progress. Execute one narrowly allowable evidence task, or mark BLOCKED. You cannot certify methods or mark the goal resolved.'},{role:'user',content:input}],text:{format:{type:'json_schema',name:'bounded_next_action',strict:true,schema}}})});
 if(!r.ok)throw Error('OPENAI_RESPONSE_HTTP_'+r.status);const answer=await r.json();
 const output=(answer.output||[]).filter(x=>x.type==='message').flatMap(x=>x.content||[]).filter(x=>x.type==='output_text').map(x=>x.text).join('');
 if(!output)throw Error('OPENAI_MODEL_OUTPUT_MISSING');
 const d=narrowDecision(JSON.parse(output));return {decision:d,responseId:answer.id||null,model:env.OPENAI_MODEL||'gpt-5'};
}
async function auditPinnedSource(env,target){
 const [owner,repo,sha]=RIVALS[target];const tr=await githubAPI(env,`repos/${owner}/${repo}/git/trees/${sha}?recursive=1`);
 if(!tr.ok)throw Error('PINNED_TREE_READ_FAILED:'+target+':'+tr.status);
 const entries=tr.data.tree||[];
 const names=entries.filter(x=>x.type==='blob').map(x=>x.path);
 const result={target,officialRepo:`${owner}/${repo}`,pinnedSha:sha,treeTruncated:tr.data.truncated===true,files:names.length,
  licenseFiles:names.filter(x=>/(^|\/)(license|copying)(\.[^/]*)?$/i.test(x)).slice(0,20),
  testCandidates:names.filter(x=>/(^|\/)(tests?|specs?)\//i.test(x)||/(^|\/)test_[^/]+\.py$/i.test(x)).slice(0,20),
  dependencyManifests:names.filter(x=>/(^|\/)(pyproject\.toml|uv\.lock|poetry\.lock|requirements[^/]*\.txt|package-lock\.json|package\.json|environment[^/]*\.ya?ml)$/i.test(x)).slice(0,25),
  note:'Original source inventory only; not executable behavior, license adjudication, native-test pass, independent defender, resource parity, or methodology win.'};
 if(tr.data.truncated)result.note+=' Tree truncated; completeness BLOCKED.';
 return result;
}
async function archiveGithub(env,runId,loop,payload){
 const path=`${PREFIX}/${runId}/loop_${String(loop).padStart(4,'0')}_audit.json`;
 const raw=JSON.stringify(payload,null,2)+'\n';
 const utf8=new TextEncoder().encode(raw); let binary='';for(const byte of utf8)binary+=String.fromCharCode(byte);
 const put=await githubAPI(env,`repos/${GITHUB}/contents/${path}`,'PUT',{message:`research2: archive cloud loop ${loop} evidence`,content:btoa(binary),branch:BRANCH});
 if(!put.ok){if(put.status===422){const existing=await githubAPI(env,`repos/${GITHUB}/contents/${path}?ref=${BRANCH}`);if(existing.ok)return {path,commit:'already-exists',duplicate:true}}throw Error('GITHUB_CREATE_ONLY_FAILED:'+put.status)}
 return {path,commit:put.data.commit?.sha||null,duplicate:false};
}
async function executeCloudLoop(env,runId,loop,mode){
 if(mode==='smoke')return {runId,loop,status:'CONTINUE',summary:`Cloud-only event continuation smoke loop ${loop}; not science`,evidence:{smoke:true,cloud_runtime:true,offline_device_test_not_performed:true}};
 for(const k of ['OPENAI_API_KEY','GITHUB_TOKEN','GOOGLE_CLIENT_ID','GOOGLE_CLIENT_SECRET','GOOGLE_REFRESH_TOKEN'])if(!env[k])return {runId,loop,status:'BLOCKED',summary:'Missing required cloud secret '+k+'; no research performed',evidence:{missing:k}};
 // Fail closed if canonical Drive cannot be read. No chat-derived or stale snapshot substitutions.
 const newest=await readLatestStatus(env);
 const plan=await decideNext(env,newest.text,loop);
 if(plan.decision.action==='BLOCKED'){
  const obj={runId,loop,status:'BLOCKED',summary:'Cloud science reviewer found gating blocker',decision:plan.decision,checkpoint:{name:newest.name,id:newest.id},evidence:{}};
  const archive=await archiveGithub(env,runId,loop,obj);
  return {...obj,evidence:{archive,checkpointId:newest.id}};
 }
 if(auditedTargets.includes(plan.decision.target)){
  const obj={runId,loop,status:'BLOCKED',summary:'Repeated already-audited source rejected; scientific next executor capability is missing',decision:plan.decision,checkpoint:{name:newest.name,id:newest.id}};
  const archive=await archiveGithub(env,runId,loop,obj);return {...obj,evidence:{archive,repeated:true}};
 }
 const audit=await auditPinnedSource(env,plan.decision.target);
 const obj={runId,loop,status:'CONTINUE',summary:`Source-tree manifest verified for ${plan.decision.target}; full fidelity still uncertified`,decision:plan.decision,checkpoint:{name:newest.name,id:newest.id,modified:newest.modified},audit,
  claimCeiling:PENDING,completion:false,requiresIndependentReview:true};
 const archive=await archiveGithub(env,runId,loop,obj);
 return {...obj,evidence:{archive,sourceSha:audit.pinnedSha,treeTruncated:audit.treeTruncated,canonicalStatusId:newest.id}};
}
export class ResearchLoopWorkflow extends WorkflowEntrypoint{
 async run(event,step){
  const {runId,loop,mode}=event.payload;
  const claimed=await step.do('claim-sequential-loop',async()=>await control(this.env,'/claim',{runId,loop}));
  if(!claimed.ok)return {stopped:true,reason:claimed.error||'not-current'};
  let result;
  try{result=await step.do('execute-one-evidence-bounded-loop',{retries:{limit:1,delay:'15 seconds',backoff:'constant'}},async()=>await executeCloudLoop(this.env,runId,loop,mode));}
  catch(e){result={runId,loop,status:'BLOCKED',summary:'Research tool failure: '+String(e.message||e).slice(0,400),evidence:{toolError:true}}}
  const committed=await step.do('commit-audit-ledger',async()=>await control(this.env,'/commit',result));
  if(!committed.ok)return {stopped:true,reason:committed.error};
  if(committed.continue){
   // Event-driven immediate successor, with a deterministic idempotent instance id. NO CRON.
   const next=loop+1;
   const spawned=await step.do('immediate-next-loop-on-unresolved-condition',async()=>{
    const id=`r2-${runId}-loop-${String(next).padStart(4,'0')}`;
    try{const instance=await this.env.RESEARCH_FLOW.create({id,params:{runId,loop:next,mode}});return {id:instance.id,alreadyExisted:false}}
    catch(e){if(/exist|duplicate|conflict/i.test(String(e)))return {id,alreadyExisted:true};throw e}
   });
   return {finishedLoop:loop,outcome:result.status,next:spawned};
  }
  return {finishedLoop:loop,outcome:result.status,state:committed.state?.status||'unknown',noAutomaticNext:true};
 }
}
export default {
 async fetch(request,env){
  const url=new URL(request.url);
  if(url.pathname==='/health'&&request.method==='GET')return json({service:'eon-research2-cloud-loop',cloudOnly:true,mode:env.RESEARCH_MODE||'disabled',cron:false,autonomousResearchActivated:false});
  if(!url.pathname.startsWith('/admin/'))return json({error:'NOT_FOUND'},404);
  if(!auth(request,env))return json({error:'UNAUTHORIZED'},401);
  if(url.pathname==='/admin/status'&&request.method==='GET')return json(await control(env,'/state'));
  if(url.pathname==='/admin/pause'&&request.method==='POST')return json(await control(env,'/pause',{}));
  if(url.pathname==='/admin/start'&&request.method==='POST'){
   const mode=env.RESEARCH_MODE||'disabled';
   if(mode!=='smoke'&&mode!=='live')return json({error:'NOT_ARMED'},409);
   if(mode==='live'&&(!env.OPENAI_API_KEY||!env.GITHUB_TOKEN||!env.GOOGLE_CLIENT_ID||!env.GOOGLE_CLIENT_SECRET||!env.GOOGLE_REFRESH_TOKEN))return json({error:'CLOUD_CREDENTIALS_MISSING_FAIL_CLOSED'},409);
   const n=mode==='smoke'?3:limits(env);
   const runId=crypto.randomUUID();
   const init=await control(env,'/start',{runId,maxLoops:n,mode});
   if(!init.ok)return json(init,409);
   try{const instance=await env.RESEARCH_FLOW.create({id:`r2-${runId}-loop-0000`,params:{runId,loop:0,mode}});return json({runId,instanceId:instance.id,started:true,mode,maxLoops:n,note:'No hourly schedule. Each unfinished loop immediately triggers the next in cloud; budget pause is not goal satisfaction.'})}
   catch(e){await control(env,'/pause',{});return json({error:'WORKFLOW_CREATE_FAILED',message:String(e).slice(0,200)},503)}
  }
  return json({error:'NOT_FOUND'},404);
 }
};