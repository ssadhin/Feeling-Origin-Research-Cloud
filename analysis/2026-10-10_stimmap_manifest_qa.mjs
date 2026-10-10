// Pinned manifest QA; metadata only; no participant outcomes.
// Run with Node 18+: node analysis/stimmap_manifest_qa.mjs
const sha='6c419ffc8a5d242b00ff95106aacb250365d3715';
const u='https://api.github.com/repos/canlab/stimMAP_2025/git/trees/'+sha+'?recursive=1';
const r=await fetch(u,{headers:{'User-Agent':'Feeling-Origin-Research'}});
if(!r.ok)throw Error('HTTP '+r.status);
const data=await r.json();if(data.truncated)throw Error('truncated tree');
const csv=new Set(data.tree.filter(x=>x.type==='blob'&&x.path.endsWith('.csv')).map(x=>x.path));
const expected=new Set();
for(let i=1;i<=50;i++){
 const sub='sub-'+String(i).padStart(2,'0');
 for(const s of ['Calibration','Calibration_output','Calibration_regions_order'])expected.add('Session 0/Calibration/Results/'+sub+'/'+sub+'_'+s+'.csv');
 for(let k=1;k<=3;k++){
  const ses='ses-'+String(k).padStart(2,'0');
  for(const phase of ['before','after'])for(let run=1;run<=3;run++)expected.add('Session '+k+'/Pain '+phase+' tDCS/Results/'+sub+'/'+sub+'_'+ses+'/'+sub+'_'+ses+'_run-'+String(run).padStart(2,'0')+'.csv');
  expected.add('Session '+k+'/tDCS induced sensation'+(k===3?'':'s')+'/Results/'+sub+'/'+sub+'_'+ses+'/'+sub+'_'+ses+'-total.csv');
 }
}
const missing=[...expected].filter(x=>!csv.has(x)).sort();
const extra=[...csv].filter(x=>!expected.has(x)).sort();
console.log(JSON.stringify({source_sha:sha,expected:expected.size,observed:csv.size,missing_count:missing.length,extra_count:extra.length,missing,extra},null,2));
