# Research2 Relay5 compact source-branch reproducer, post-run GitHub publication.
# Upstream exact P14/P15 branch from ssadhin/Feeling-Origin-Research-Cloud
# commit 633fc711e34e9bf1be37f5760147a5918276d31a
# meta_methodology/benchmark_v002.py blob 47fc8c9f2d85646ade45b846d49efbd2db8d93c4
# The local full runner additionally executes exact residual-flag source and 13 checks.
import json
COST={"generate":8,"observe":8,"compare":10,"residual":6,"negative_control":8,"ancestor":8,"equivalence":10,"ood":14,"mist":10}
SOURCE='''    if pid=="P14":
        for a in ("generate","observe","compare","residual","generate","negative_control","ancestor","equivalence","ood"):
            if env.can(a): act(a)

    elif pid=="P15":
        for a in ("generate","observe","mist","compare","residual","generate","negative_control","ancestor","equivalence","ood"):
            if env.can(a): act(a)

'''
def run(pid,observation,budget=100,branch=SOURCE):
    class Env:
        def __init__(self):
            self.budget=budget
            self.spent=0
            self.history=[]
            self.residual_seen=False
            self.observation=observation
        def can(self,a):return self.budget>=COST[a]
        def act(self,a):
            if not self.can(a):return False
            self.budget-=COST[a]
            self.spent+=COST[a]
            self.history.append(a)
            if a=="residual":self.residual_seen=True
            return True
    env=Env()
    def act(a):return env.act(a)
    ns={}
    exec("def original_branch(env,pid,act):\n"+branch+"    else:\n        raise KeyError(pid)\n",ns)
    ns["original_branch"](env,pid,act)
    return {"history":env.history,"spent":env.spent,"remaining":env.budget,"residual_seen":env.residual_seen}
if __name__=="__main__":
    p14a=run("P14","healthy");p14b=run("P14","failing")
    p15a=run("P15","healthy");p15b=run("P15","failing")
    assert p14a==p14b and p15a==p15b
    assert p14a["spent"]==80 and p15a["spent"]==90
    assert p14a["history"][3:5]==["residual","generate"]
    assert p15a["history"][4:6]==["residual","generate"]
    assert run("P15","healthy",0)["history"]==[]
    mutant=SOURCE.replace('"residual","generate","negative_control"','"residual","negative_control"',1)
    assert run("P14","healthy",100,mutant)["history"]!=p14a["history"]
    print(json.dumps({"P14_healthy":p14a,"P14_failing":p14b,"P15_healthy":p15a,"P15_failing":p15b},sort_keys=True))
