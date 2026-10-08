#!/usr/bin/env node
// Feeling Origin: TMS discomfort nuisance robustness replication.
// Inputs are the two CSVs from JingJiangLab/Brain_Distress at pinned commit
// 36497488d66f5806e8b0a29ce9396fb725f306da.
// Expected blob SHA (GitHub): Healthy dce52ce24f6d0d77d5fb0d89f73a490a8aa51ea2,
// Symptomatic 980dade38115cfdda0ed2bb57c66df5c42882514.
// Usage: node tms_discomfort_robustness.js Healthy_TMS_SUDS.csv Symptomatic_TMS_SUDS.csv
// No external dependencies; no claim about phenomenality, no causal neural inference.
"use strict";
const fs = require("fs");
if (process.argv.length !== 4) {
  console.error("Usage: node tms_discomfort_robustness.js Healthy_TMS_SUDS.csv Symptomatic_TMS_SUDS.csv");
  process.exit(2);
}
const mean = xs => xs.reduce((s,x) => s+x,0)/xs.length;
function parse(path,g) {
  return fs.readFileSync(path,"utf8").trim().split(/\r?\n/).slice(1)
    .map(line => {const [p,site,v]=line.split(",",3);return {g,p:g+"|"+p,site,y:Number(v),raw:v};})
    .filter(x => x.p && x.site && x.raw!=="" && Number.isFinite(x.y));
}
const all=[...parse(process.argv[2],"H"),...parse(process.argv[3],"S")];
function score(rows) {
  const persons=new Map();
  for(const x of rows) {if(!persons.has(x.p)) persons.set(x.p,[]); persons.get(x.p).push(x);}
  const valid=new Set([...persons].filter(([p,a])=>new Set(a.map(x=>x.site)).size>=8).map(([p])=>p));
  const kept=rows.filter(x=>valid.has(x.p));
  const per=new Map();
  for(const x of kept){if(!per.has(x.p))per.set(x.p,[]);per.get(x.p).push(x);}
  const centered=kept.map(x=>({...x,c:x.y-mean(per.get(x.p).map(z=>z.y))}));
  const maps=[new Map(),new Map()];
  for(const x of centered) for(const [m,k] of [[maps[0],x.g+"|"+x.site],[maps[1],x.site]]) {
    if(!m.has(k))m.set(k,[]);m.get(k).push(x);
  }
  const errs=[],personErrs=new Map();
  for(const x of kept){
    const other=per.get(x.p).filter(z=>z.site!==x.site);
    const offset=(pooled,site)=>{
      const a=(maps[pooled?1:0].get(pooled?site:x.g+"|"+site)||[]).filter(z=>z.p!==x.p);
      return a.length?mean(a.map(z=>z.c)):0;
    };
    const baseline=mean(other.map(z=>z.y));
    const group=mean(other.map(z=>z.y-offset(false,z.site)))+offset(false,x.site);
    const pooled=mean(other.map(z=>z.y-offset(true,z.site)))+offset(true,x.site);
    const e={p:x.p,g:x.g,b:Math.abs(x.y-baseline),group:Math.abs(x.y-group),pooled:Math.abs(x.y-pooled)};
    errs.push(e);
    if(!personErrs.has(x.p))personErrs.set(x.p,[]);
    personErrs.get(x.p).push(e);
  }
  const pg=[...personErrs].map(([p,a])=>({
    p,delta:mean(a.map(z=>z.b-z.group)),
    pooledDelta:mean(a.map(z=>z.b-z.pooled)),
    groupMinusPooled:mean(a.map(z=>z.group-z.pooled))
  }));
  return {
    n:errs.length,persons:pg.length,
    maeBaseline:mean(errs.map(x=>x.b)),maeGroup:mean(errs.map(x=>x.group)),maePooled:mean(errs.map(x=>x.pooled)),
    gain:mean(errs.map(x=>x.b-x.group)),pooledGain:mean(errs.map(x=>x.b-x.pooled)),
    personMeanGain:mean(pg.map(x=>x.delta)),
    personPositive:pg.filter(x=>x.delta>0).length,personNegative:pg.filter(x=>x.delta<0).length,
    personTies:pg.filter(x=>x.delta===0).length,
    personPooledBetter:pg.filter(x=>x.groupMinusPooled>0).length,
    personGroupBetter:pg.filter(x=>x.groupMinusPooled<0).length
  };
}
const sites=[...new Set(all.map(x=>x.site))].sort();
const result={
  sourceRows:{healthy:all.filter(x=>x.g==="H").length,symptomatic:all.filter(x=>x.g==="S").length},
  primary:score(all),
  siteExclusion:sites.map(site=>({excludedSite:site,...score(all.filter(x=>x.site!==site))})),
  interiorOnly:score(all.filter(x=>x.y>0&&x.y<100))
};
console.log(JSON.stringify(result,null,2));
