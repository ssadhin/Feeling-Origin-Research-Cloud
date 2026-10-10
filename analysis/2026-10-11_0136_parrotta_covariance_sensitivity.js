// Published summary sensitivity only; not raw participant reanalysis.
const u=.16/4, i=3.27/100, su=.067/4, si=1.56/100;
const d=u-i;
const rho=(su*su+si*si-(d/1.96)**2)/(2*su*si);
for(const r of [-1,0,.9,.95,.975,.99,1]){
 const se=Math.sqrt(su*su+si*si-2*r*su*si);
 console.log(r,d,se,d-1.96*se,d+1.96*se);
}
console.log('critical_rho',rho);