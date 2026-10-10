#!/usr/bin/env node
'use strict';
// Pinned public-source QA only: no pain outcome values read or analyzed.
const https=require('node:https'),crypto=require('node:crypto');
const commit='6c419ffc8a5d242b00ff95106aacb250365d3715';
const api='https://api.github.com/repos/canlab/stimMAP_2025';
const get=url=>new Promise((ok,fail)=>https.get(url,{headers:{'User-Agent':'feeling-origin-audit','Accept':'application/vnd.github+json'}},r=>{let s='';r.on('data',x=>s+=x);r.on('end',()=>r.statusCode===200?ok(JSON.parse(s)):fail(new Error('HTTP '+r.statusCode+' '+s.slice(0,100))))}).on('error',fail));
const pad=x=>String(x).padStart(2,'0');
const pain=(s,phase,id,run)=>`Session ${s}/Pain ${phase} tDCS/Results/sub-${pad(id)}/sub-${pad(id)}_ses-${pad(s)}/sub-${pad(id)}_ses-${pad(s)}_run-${pad(run)}.csv`;
const sensation=(s,id)=>`Session ${s}/tDCS induced sensation${s===3?'':'s'}/Results/sub-${pad(id)}/sub-${pad(id)}_ses-${pad(s)}/sub-${pad(id)}_ses-${pad(s)}-total.csv`;
const cal=(id,type)=>`Session 0/Calibration/Results/sub-${pad(id)}/sub-${pad(id)}_${type}.csv`;
async function main(){
 const tree=await get(api+'/git/trees/'+commit+'?recursive=1');
 if(tree.truncated)throw Error('truncated tree');
 const files=tree.tree.filter(x=>x.type==='blob'),csv=files.filter(x=>x.path.endsWith('.csv'));
 const sha=new Map(csv.map(x=>[x.path,x.sha])),expected=new Set();
 for(let id=1;id<=50;id++)for(const t of ['Calibration','Calibration_output','Calibration_regions_order'])expected.add(cal(id,t));
 for(let s=1;s<=3;s++)for(let id=1;id<=50;id++){
  for(const phase of ['before','after'])for(let run=1;run<=3;run++)expected.add(pain(s,phase,id,run));
  expected.add(sensation(s,id));
 }
 const missing=[...expected].filter(p=>!sha.has(p)).sort();
 const noncanonical=[...sha.keys()].filter(p=>!expected.has(p)).sort();
 const samples=[];
 for(let s=1;s<=3;s++)for(const id of [1,2,3,17]){
  const path=pain(s,'after',id,1);
  const response=await get(api+'/contents/'+path.split('/').map(encodeURIComponent).join('/')+'?ref='+commit);
  const bytes=Buffer.from(response.content.replace(/\s/g,''),'base64');
  const hash=crypto.createHash('sha1').update(Buffer.from('blob '+bytes.length+'\0')).update(bytes).digest('hex');
  if(hash!==sha.get(path)||hash!==response.sha)throw Error('source hash mismatch: '+path);
  const rows=bytes.toString('utf8').trim().split(/\r?\n/),h=rows[0].split(',');
  const idx=h.indexOf('tDCS_Protocol');
  if(idx<0)throw Error('missing protocol field');
  samples.push({path,sha:hash,rows:rows.length-1,protocol_values:[...new Set(rows.slice(1).map(r=>r.split(',')[idx]))],allocation_fields:h.filter(x=>/anodal|cathodal|sham|allocation|polarity|treatment|randomi[sz]/i.test(x))});
 }
 console.log(JSON.stringify({source_commit:commit,tree_sha:tree.sha,tree_entries:tree.tree.length,csv_files:csv.length,mat_files:files.filter(x=>x.path.endsWith('.mat')).length,expected_csv:expected.size,missing,noncanonical,samples,conclusion:'No verified treatment allocation in inspected CSVs. MAT and external allocation key uninspected. No causal effect, no affect-specific S, no reasoning Q, no phenomenal P inference.'},null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1});
