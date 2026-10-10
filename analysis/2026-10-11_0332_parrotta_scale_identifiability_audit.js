/* Feeling Origin — 2026-10-11 03:32 +06 post-primary calibration audit.
 * Input: committed 2026-10-11_0237_parrotta_raw_matched_v2_negative.json.
 * NO raw XLSX replay; no new causal/phenomenal evidence.
 * Run: node analysis/2026-10-11_0332_parrotta_scale_identifiability_audit.js results/2026-10-11_0237_parrotta_raw_matched_v2_negative.json
 */
function audit(doc){
  if(doc.sourceGitBlob!=="447fff57c91fb5ff761449d98d93737e26b1236c")throw Error("unexpected source");
  const p=doc.results.primary,A=p.Intero,B=p.Extero;
  if(A.n!==34||B.n!==29)throw Error("unexpected sample");
  const uA=A.meanUnpleasantness,iA=A.meanIntensity,uB=B.meanUnpleasantness,iB=B.meanIntensity;
  const D=(u,i,c)=>u-c*i;
  const calibration=[0.7,0.8,0.9,1,1.1,1.2].map(c=>({relativeIntensityCalibration:c,interoD:D(uA,iA,c),exteroD:D(uB,iB,c),betweenD:D(uA-uB,iA-iB,c)}));
  const thresholds={intero:uA/iA,extero:uB/iB,between:(uA-uB)/(iA-iB)};
  const original=p.InteroMinusExtero;
  if(Math.abs(D(uA-uB,iA-iB,1)-original)>1e-12)throw Error("baseline mismatch");
  return {status:"POST-PRIMARY, NONBLIND ANALYTIC SENSITIVITY; NO PROOF",sourceGitBlob:doc.sourceGitBlob,sourceResultPath:"results/2026-10-11_0237_parrotta_raw_matched_v2_negative.json",sample:{Intero:A.n,Extero:B.n},formula:"D(c) = meanDeltaLIK/4 - c*(meanDeltaVAS/100); c=1 is original range-normalized comparison",zeroCrossingCalibration:thresholds,calibration,limitations:["No validated cross-scale psychometric mapping c","Crossings of point estimates do not imply significant effects","No confidence intervals for c != 1 without paired participant data and covariance","No objective sensory discrimination or reasoning/access reverse arm","No direct phenomenality measure or isolated mechanism M","Not an independent dataset; no manuscript-worthy proof"]};
}
if(typeof module!=="undefined"){module.exports={audit};if(require.main===module){const fs=require("fs");console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2));}}
