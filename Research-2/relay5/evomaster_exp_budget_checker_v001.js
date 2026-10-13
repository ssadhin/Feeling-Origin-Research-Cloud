// Research2 Relay5 2026-10-13. Re-run with: node checker.js path/to/pinned/playground.py
// Pinned source blob f0de9bba97f6caa18178117ee364919e5e91c334 at EvoMaster 36a52bc6c42a6b9fd710a41c52f3c3bb948b9ac9.
const fs=require('fs'), assert=require('assert');
const source=fs.readFileSync(process.argv[2],'utf8');
function part(name){let i=source.indexOf('    def '+name+'(');assert(i>=0,name);let j=source.indexOf('\n    def ',i+8);return source.slice(i,j<0?source.length:j)}
const cfg=part('_load_workflow_config'), p=part('_run_with_parallel'),s=part('_run_with_serial');
const count=(s,x)=>s.split(x).length-1;
for(const stage of ['solve','critique','rewrite','select']){assert.equal(count(p,'exp_name="'+stage+'"'),1);assert.equal(count(s,'exp_name="'+stage+'"'),1)}
for(const [field,v] of [['agent_num','1'],['max_workers','1'],['parallel','True'],['max_retries','3']])assert(cfg.includes("self."+field+" = xmaster_config.get('"+field+"', "+v+")"));
assert.equal(count(p,'max_workers=self.max_workers'),3);
assert.equal(count(p,'while retry < self.max_retries'),4);
assert.equal(count(s,'while retry < self.max_retries'),4);
assert.equal(count(p,'for idx in pending_indices:'),3);
assert.equal(count(s,'for i in range(self.agent_num):'),3);
for(const N of [1,4,8])console.log({N,healthy:3*N+1,max_successful:3*(3*N+1)});
console.log('SOURCE_STRUCTURAL_CHECKS_PASS; NOT_NATIVE_RUNTIME');
