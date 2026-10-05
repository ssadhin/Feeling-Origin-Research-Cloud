"""Layered Regulatory-Access (LRA) synthetic consistency simulation.
Purpose: test internal coherence and intervention signatures only.
This is NOT evidence of phenomenality or biological truth.
Frozen model: v0.1
"""
import numpy as np

SEED = 123
N = 100_000
rng = np.random.default_rng(SEED)

H0 = rng.normal(size=N)
Mimp0 = rng.normal(size=N)
Mexp0 = rng.normal(size=N)
X0 = rng.normal(size=N)
epsV = rng.normal(scale=.5, size=N)
epsE = rng.normal(scale=.45, size=N)
epsP = rng.normal(scale=.45, size=N)
epsR = rng.normal(scale=.5, size=N)
epsE2 = rng.normal(scale=.45, size=N)
epsF = rng.normal(scale=.4, size=N)

def simulate(do=None):
    do = do or {}
    H = do.get("H", H0)
    Mimp = do.get("Mimp", Mimp0)
    Mexp = do.get("Mexp", Mexp0)
    X = do.get("X", X0)

    V = np.tanh(.70*H + .55*X + .35*Mimp + epsV)
    if "V" in do: V = np.full(N, do["V"])

    E = np.tanh(.70*V + .35*H + .15*Mexp + epsE)
    if "E" in do: E = np.full(N, do["E"])

    P = np.tanh(.65*E + .45*H + .25*X + .15*Mexp + epsP)
    if "P" in do: P = np.full(N, do["P"])

    R = np.tanh(.75*Mexp + .55*X + .25*P + epsR)
    if "R" in do: R = np.full(N, do["R"])

    E2 = np.tanh(.65*V + .25*H + .25*R + epsE2)
    F = np.tanh(.50*P + .40*E2 + .25*R + epsF)

    return {
        "sd_F": float(np.std(F)),
        "sd_R": float(np.std(R)),
        "corr_FR": float(np.corrcoef(F, R)[0,1]),
    }

for name, intervention in [
    ("baseline", {}),
    ("suppress_valuation", {"V":0}),
    ("suppress_organism_state_representation", {"P":0}),
    ("suppress_reasoning", {"R":0}),
    ("suppress_homeostatic_input", {"H":np.zeros(N)}),
]:
    print(name, simulate(intervention))
