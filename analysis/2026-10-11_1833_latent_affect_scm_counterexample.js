// Synthetic exact SCM, Feeling Origin; frozen protocol Drive 1jbGxOtzPfawJEULTlNoijix2ihiNWCiikjysHgNJd3k
function calc(model,m,q){
let obs={},mass=0,S=0,R=0,N=0,Q=0;
for(let u=0;u<2;u++)for(let k=0;k<2;k++)for(let j=0;j<2;j++){
let w=(u?.2:.8)*(k?.35:.65)*(j?.7:.3),v=m^u,z=q===null?j:q,s=model==="A"?v:u;
let key=[m,v,v,v,k,z,z,z].join(",");
obs[key]=(obs[key]||0)+w;mass+=w;S+=w*s;R+=w*v;N+=w*k;Q+=w*z;
}
if(Math.abs(mass-1)>1e-12)throw Error("mass");
return {obs,S,R,N,Q};
}
let out=[];
for(let m of [0,1])for(let q of [0,1,null]){
let a=calc("A",m,q),b=calc("B",m,q);
let tv=Object.keys(a.obs).reduce((x,k)=>x+Math.abs(a.obs[k]-b.obs[k]),0)/2;
if(tv>1e-12)throw Error("TV");
out.push({m,q,tv,S_A:a.S,S_B:b.S,R:a.R,N:a.N,Q:a.Q});
}
console.log(JSON.stringify(out));
