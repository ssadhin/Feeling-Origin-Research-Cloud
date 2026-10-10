#!/usr/bin/env node
// Paingen expectation-selectivity family audit, frozen 2026-10-10 07:34 +06.
// node audit.js merged_firstlvl_stim_betas_to_share.csv expectation_data.csv
const fs=require('fs'),crypto=require('crypto');
const PINS=['539a7bdeb9a324afc20d064a458979b43594c456','4ea9caf233d4e8f1cf8b975dd5e7c5bf1417998b'];
const blob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
function load(file,pin){const b=fs.readFileSync(file);if(blob(b)!==pin)throw Error('source SHA mismatch '+file);const lines=b.toString('utf8').replace(/^\uFEFF/,'').trim().split(/\r?\n/);const h=lines.shift().split(',');return lines.map(l=>{const v=l.split(',');if(v.length!==h.length)throw Error('CSV column mismatch');return Object.fromEntries(h.map((k,i)=>[k,v[i]]))});}
const [pain,expect]=[load(process.argv[2],PINS[0]),load(process.argv[3],PINS[1])];
const ex=new Map();for(const r of expect){if(ex.has(r.participant_ID))throw Error('duplicate expectation');const x=Number(r.expect);if(!Number.isFinite(x)||x<0||x>100)throw Error('invalid expectation');ex.set(r.participant_ID,x);}
const grp=new Map();for(const r of pain){const k=[r.participant_ID,r.heat,r.stimLvl].join('|');if(!grp.has(k))grp.set(k,{});const v=grp.get(k);if(v[r.prodicaine])throw Error('duplicate pain key');v[r.prodicaine]=r;}
const fam=new Map(),exc={unmatched:0,nonfinite:0,familyMismatch:0,missingExpectation:0};let pairs=0;
for(const v of grp.values()){if(!v['0']||!v['1']){exc.unmatched++;continue;}const a=v['0'],b=v['1'];if(a.family_ID!==b.family_ID){exc.familyMismatch++;continue;}const [i0,u0,i1,u1]=[a.Yint,a.Yunp,b.Yint,b.Yunp].map(Number);if(![i0,u0,i1,u1].every(Number.isFinite)){exc.nonfinite++;continue;}if(!ex.has(a.participant_ID)){exc.missingExpectation++;continue;}if(!fam.has(a.family_ID))fam.set(a.family_ID,{D:[],U:[],I:[],E:new Map()});const z=fam.get(a.family_ID);z.D.push((u0-u1)-(i0-i1));z.U.push(u0-u1);z.I.push(i0-i1);z.E.set(a.participant_ID,ex.get(a.participant_ID));pairs++;}
const mean=a=>a.reduce((s,v)=>s+v,0)/a.length;
const rows=[...fam].sort((a,b)=>a[0].localeCompare(b[0])).map(([id,z])=>({id,D:mean(z.D),U:mean(z.U),I:mean(z.I),X:(mean([...z.E.values()])-50)/50}));
function slope(a,y){const xm=mean(a.map(z=>z.X)),ym=mean(a.map(z=>z[y]));const den=a.reduce((s,z)=>s+(z.X-xm)**2,0);return a.reduce((s,z)=>s+(z.X-xm)*(z[y]-ym),0)/den;}
class RNG{constructor(seed){this.s=seed>>>0;}rand(){let x=this.s;x^=(x<<13)>>>0;x^=x>>>17;x^=(x<<5)>>>0;this.s=x>>>0;return this.s/4294967296;}}
const obs=slope(rows,'D'),N=10000;let rng=new RNG(20261012),extreme=0;const xs=rows.map(z=>z.X),ds=rows.map(z=>z.D),dm=mean(ds),xm=mean(xs),den=xs.reduce((s,x)=>s+(x-xm)**2,0);
for(let b=0;b<N;b++){const a=xs.slice();for(let j=a.length-1;j>0;j--){const k=Math.floor(rng.rand()*(j+1));[a[j],a[k]]=[a[k],a[j]];}let s=0;for(let j=0;j<a.length;j++)s+=(a[j]-xm)*(ds[j]-dm);if(s/den>=obs-1e-15)extreme++;}
rng=new RNG(20261013);const bs=[];for(let b=0;b<N;b++){const sample=Array.from({length:rows.length},()=>rows[Math.floor(rng.rand()*rows.length)]);const s=slope(sample,'D');if(Number.isFinite(s))bs.push(s);}bs.sort((a,b)=>a-b);
let mse=0,base=0;const folds=[];for(let f=0;f<5;f++){const train=rows.filter((_,i)=>i%5!==f),test=rows.filter((_,i)=>i%5===f),s=slope(train,'D'),tx=mean(train.map(z=>z.X)),ty=mean(train.map(z=>z.D));let m=0,n=0;for(const z of test){m+=(z.D-(ty+s*(z.X-tx)))**2;n+=(z.D-ty)**2;}mse+=m;base+=n;folds.push({fold:f,n:test.length,trainSlope:s});}
const result={sourceBlobs:PINS,rows:pain.length,expectationRows:expect.length,groups:grp.size,exclusions:exc,pairs,families:rows.length,meanD:mean(rows.map(z=>z.D)),meanU:mean(rows.map(z=>z.U)),meanI:mean(rows.map(z=>z.I)),slopeD:obs,slopeU:slope(rows,'U'),slopeI:slope(rows,'I'),oneSidedPermutationP:(extreme+1)/(N+1),bootstrapCI95:[bs[Math.floor(.025*bs.length)],bs[Math.floor(.975*bs.length)]],folds,heldoutMSE:mse/rows.length,interceptMSE:base/rows.length,heldoutSkill:1-mse/base,interpretation:'Negative affect-specific evidence; no causal M or phenomenal proof'};
console.log(JSON.stringify(result,null,2));
