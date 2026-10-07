import itertools, collections
import networkx as nx

NODES = ["M","I","E","F"]
EDGES = [(a,b) for a in NODES for b in NODES if a != b]

def is_dag(es):
    g = nx.DiGraph()
    g.add_nodes_from(NODES)
    g.add_edges_from(es)
    return nx.is_directed_acyclic_graph(g)

def skeleton(es):
    return frozenset(tuple(sorted((a,b))) for a,b in es)

def vstructures(es):
    es = set(es)
    out = set()
    for b in NODES:
        parents = [a for a in NODES if (a,b) in es]
        for a,c in itertools.combinations(parents,2):
            if (a,c) not in es and (c,a) not in es:
                out.add((min(a,c),b,max(a,c)))
    return frozenset(out)

all_graphs = []
dags = []
for mask in range(1 << len(EDGES)):
    es = frozenset(EDGES[i] for i in range(len(EDGES)) if (mask >> i) & 1)
    all_graphs.append(es)
    if is_dag(es):
        dags.append(es)

mecs = collections.defaultdict(list)
for es in dags:
    mecs[(skeleton(es), vstructures(es))].append(es)

orders = list(itertools.permutations(NODES))
m_first = [o for o in orders if o[0] == "M"]
m_first_e_before_f = [o for o in m_first if o.index("E") < o.index("F")]

chain_edges = {("M","I"),("I","E"),("E","F")}
chain = nx.DiGraph()
chain.add_nodes_from(NODES)
chain.add_edges_from(chain_edges)

tests = [
    ("M","E",{"I"}),
    ("M","F",{"E"}),
    ("I","F",{"E"}),
]

print("All directed graphs without self loops:", len(all_graphs))
print("DAGs:", len(dags))
print("Markov equivalence classes among DAGs:", len(mecs))
print("Total linear orders:", len(orders))
print("Linear orders with M first:", len(m_first))
print("Linear orders with M first and E before F:", len(m_first_e_before_f))
print("\nStrict-chain d-separation predictions:")
for a,b,z in tests:
    print(f"{a} _||_ {b} | {sorted(z)}:", nx.is_d_separator(chain,{a},{b},z))

branch = chain.copy()
branch.add_edge("M","F")
print("\nAfter adding a homeostatic M->F bypass:")
for a,b,z in tests:
    print(f"{a} _||_ {b} | {sorted(z)}:", nx.is_d_separator(branch,{a},{b},z))
