# ORIGINAL CODE — ledger run 7 (mean-field ODE vs nearest-neighbour percolation, drought sweep)
# Provenance: chat-side Claude sandbox, 2026-11-10, verbatim as executed (co-authored, Kavik + Claude).
# Environment: Python 3 + numpy + scipy (brentq). RNG seed 3. Grid L=120, 12 reps, density 0.8,
#   spread p = 0.2 + 0.75*drought, single ignition at centre, BFS spread.
# Logged output (drought, p, R0, ODE_frac, GRID_frac, grid_sd):
#   0.0 0.20 0.64 0.000 0.000 0.000 | 0.1 0.28 0.88 0.000 0.000 0.000 | 0.2 0.35 1.12 0.206 0.000 0.000
#   0.3 0.43 1.36 0.478 0.001 0.001 | 0.4 0.50 1.60 0.642 0.002 0.002 | 0.5 0.57 1.84 0.747 0.012 0.014
#   0.6 0.65 2.08 0.817 0.164 0.123 | 0.7 0.73 2.32 0.866 0.719 0.322 | 0.8 0.80 2.56 0.900 0.954 0.005
#   0.9 0.88 2.80 0.925 0.983 0.003 | 1.0 0.95 3.04 0.943 0.994 0.001
# NOTE on "~60x": ODE/GRID at drought 0.5 = 0.747/0.012 ≈ 62x; at 0.4 = 0.642/0.002 ≈ 321x and
#   at 0.3 ≈ 478x. "Up to ~60x" in the ledger UNDERSTATES the raw ratio; ratios at very small
#   grid means are noise-dominated (few-cell burns). Flag, do not reinterpret.
import numpy as np
from scipy.optimize import brentq
from collections import deque
rng=np.random.default_rng(3)
L=120
def grid_burn(dens,p,reps=12):
    out=[]
    for _ in range(reps):
        veg=rng.random((L,L))<dens
        burned=np.zeros((L,L),bool);c=L//2;veg[c,c]=True;burned[c,c]=True
        q=deque([(c,c)])
        while q:
            i,j=q.popleft()
            for di,dj in((1,0),(-1,0),(0,1),(0,-1)):
                a,b=i+di,j+dj
                if 0<=a<L and 0<=b<L and veg[a,b] and not burned[a,b] and rng.random()<p:
                    burned[a,b]=True;q.append((a,b))
        out.append(burned.sum()/max(veg.sum(),1))
    return np.mean(out),np.std(out)
def ode_burn(dens,p):
    R0=4*p*dens
    if R0<=1:return 0.0
    return brentq(lambda z:z-(1-np.exp(-R0*z)),1e-9,1)
print("drought -> spread prob p ; vegetation density 0.8 (moist forest drying)")
print("drought   p    R0   ODE_frac  GRID_frac  grid_sd")
for dr in np.linspace(0,1,11):
    p=0.2+0.75*dr;dens=0.8
    g,s=grid_burn(dens,p);o=ode_burn(dens,p)
    print(f"{dr:5.1f}  {p:4.2f}  {4*p*dens:4.2f}   {o:6.3f}    {g:6.3f}    {s:5.3f}")
