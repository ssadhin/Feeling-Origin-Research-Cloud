from itertools import product
def world(h,z,w,u):
    P=1
    S=z if h=="affect" else 0
    R=S if h=="affect" else z
    return (z,w,u,u,1-w,0,0,1,1,R),(P,S)
cells=list(product((0,1),repeat=3))
for z,w,u in cells:
    assert world("affect",z,w,u)[0]==world("criterion",z,w,u)[0]
    if z: assert world("affect",z,w,u)[1][1]!=world("criterion",z,w,u)[1][1]
for h in ("affect","criterion"):
    for w,u in product((0,1),repeat=2):
        assert world(h,1,w,u)[0][-1]-world(h,0,w,u)[0][-1]==1
    for z,u in product((0,1),repeat=2):
        a,b=world(h,z,0,u)[0],world(h,z,1,u)[0]
        assert a[4]-b[4]==1 and a[-1]==b[-1]
print("PASS: 8/8 identical observable cells; latent affect differs; apparent double dissociation in both")
