# ORIGINAL CODE — ledger run 8 (ember-spotting branch: grid with long-range jumps vs ODE)
# Provenance: chat-side Claude sandbox, 2026-11-10, verbatim as executed (co-authored, Kavik + Claude).
# Environment: Python 3 + numpy + scipy (brentq). RNG seed 4. Grid L=100, 10 reps, density 0.8,
#   spread p = 0.2 + 0.75*drought. Spotting: on each of 4 spread attempts, with prob `spot` the
#   target is a uniformly random cell anywhere on the grid instead of a neighbour.
# Logged output (mean/sd), columns spot = 0, 0.05, 0.2, 1.0:
#   drought 0.2 ODE 0.21 | 0.00/0.00 0.00/0.00 0.00/0.00 0.05/0.09
#   drought 0.4 ODE 0.64 | 0.00/0.01 0.02/0.06 0.33/0.27 0.45/0.30
#   drought 0.5 ODE 0.75 | 0.01/0.01 0.38/0.31 0.73/0.01 0.60/0.30
#   drought 0.6 ODE 0.82 | 0.20/0.15 0.81/0.01 0.84/0.01 0.74/0.25
#   drought 0.7 ODE 0.87 | 0.76/0.26 0.82/0.27 0.90/0.00 0.78/0.26
# "Convergence anchor" claim (spot 0.2, drought >= 0.5): 0.73 vs 0.75, 0.84 vs 0.82, 0.90 vs 0.87.
#   That was read by eye, with NO pre-declared tolerance and n = 10 reps — status CANDIDATE only.
import numpy as np
from collections import deque
from scipy.optimize import brentq
rng=np.random.default_rng(4);L=100
def burn(dens,p,spot,reps=10):
    res=[]
    for _ in range(reps):
        veg=rng.random((L,L))<dens;c=L//2;veg[c,c]=True
        b=np.zeros((L,L),bool);b[c,c]=True;q=deque([(c,c)])
        while q:
            i,j=q.popleft()
            for _k in range(4):
                if rng.random()<spot: a,bb=rng.integers(L),rng.integers(L)
                else:
                    di,dj=((1,0),(-1,0),(0,1),(0,-1))[_k];a,bb=i+di,j+dj
                if 0<=a<L and 0<=bb<L and veg[a,bb] and not b[a,bb] and rng.random()<p:
                    b[a,bb]=True;q.append((a,bb))
        res.append(b.sum()/veg.sum())
    return np.mean(res),np.std(res)
def ode(d,p):
    R=4*p*d;return 0 if R<=1 else brentq(lambda z:z-(1-np.exp(-R*z)),1e-9,1)
print("drought  ODE   | spot=0   0.05   0.2   1.0  (mean / sd)")
for dr in [0.2,0.4,0.5,0.6,0.7]:
    p=0.2+0.75*dr;row=[]
    for s in [0,0.05,0.2,1.0]:
        m,sd=burn(0.8,p,s);row.append(f"{m:.2f}/{sd:.2f}")
    print(f"{dr:4.1f}   {ode(0.8,p):.2f}  | "+"  ".join(row))
