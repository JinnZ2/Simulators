# ORIGINAL CODE — ledger run 6 (mass-conserving N rebuild + old-model leak audit)
# Provenance: chat-side Claude sandbox, 2026-11-10, verbatim as executed (co-authored, Kavik + Claude).
# Environment: Python 3 + numpy (numpy RNG; seed 2 for structure, seed 0 for fire draws).
# Logged result: OLD misclosure -2.0e-02 -> -24.18 by end; CONSERVED max |misclosure| ~1.27e-09;
#   47 fires at fire_thr=0.6; late biomass mean 0.359, swing 0.466, tree share 1.0 (grasses extinct);
#   thr sweep 0.3/0.5/0.8/1.2 -> fires 56/48/45/38.
import numpy as np
r0=np.random.default_rng(2)
nP,nF=8,4
trait=r0.uniform(0,1,(nP,nP));trait=(trait+trait.T)/2;np.fill_diagonal(trait,0)
aff=r0.uniform(0,1,(nP,nF))*(r0.random((nP,nF))<0.7)
niche=r0.uniform(0,1,nF);tree=np.arange(nP)<5
dt=0.05;T=3000;steps=int(T/dt)

def old(seed=0):  # run-4 equations, audited as N budget
    N=np.full(nP,0.3);F=np.full(nF,0.2);Bac=WR=0.2;Lf=Ls=0.3;R=0.5
    comp=0.1;a=-comp*np.exp(-2*trait)-0.1*comp;np.fill_diagonal(a,-1)
    nd=np.abs(niche[:,None]-niche[None,:]);d=np.where(nd>0.4,0.5,-0.3*(1-nd));np.fill_diagonal(d,-1)
    mort=np.where(tree,0.03,0.12);ext_in=ext_out=0;tot0=N.sum()+F.sum()+Bac+WR+Lf+Ls+R;mis=[]
    for k in range(steps):
        up=R/(0.5+R);ben=aff@(F/(1+F));gN=0.6*up+ben*up
        dN=N*(gN+a@N-mort);cF=(aff*0.4).T@N/(1+N.sum());dF=F*(cF+d@F-0.05)+0.001
        decf=0.8*Bac*Lf/(0.5+Lf);decs=0.08*WR*Ls/(1+Ls)
        dBac=Bac*(0.4*Lf/(0.5+Lf)-0.15)+0.001;dWR=WR*(0.3*Ls/(1+Ls)-0.03-0.02*F.sum())+0.001
        lit=mort*N;dLf=lit[~tree].sum()+0.05*F.sum()-decf;dLs=lit[tree].sum()-decs
        dR=0.02+decf+decs-0.3*gN@N-0.05*R
        ext_in+=0.02*dt;ext_out+=0.05*R*dt
        N=N+dt*dN;F=F+dt*dF;Bac+=dt*dBac;WR+=dt*dWR;Lf+=dt*dLf;Ls+=dt*dLs;R+=dt*dR
        if k%2000==0:
            tot=N.sum()+F.sum()+Bac+WR+Lf+Ls+R;mis.append(tot-(tot0+ext_in-ext_out))
    return np.array(mis)

def conserved(fire_thr=0.6,seed=0,return_series=False):
    rng=np.random.default_rng(seed)
    comp=0.1;a=-comp*np.exp(-2*trait)-0.1*comp;np.fill_diagonal(a,0)
    N=np.full(nP,0.3);F=np.full(nF,0.2);Bac=WR=0.2;Lf=Ls=0.3;R=0.5
    mort=np.where(tree,0.03,0.12);tot0=N.sum()+F.sum()+Bac+WR+Lf+Ls+R
    dep=fix=leach=volat=0.0;mis=[];fires=0;B=[]
    for k in range(steps):
        upR=R/(0.5+R)
        u_direct=0.3*upR*N                                  # plant uptake R->N
        fung_up=0.3*upR*F                                   # fungal uptake R->F
        deliv=(aff*(F/(1+F))).T                             # fungi pass N to partners
        share=(aff*N[:,None]);share=share/(share.sum(0)+1e-9)
        f_to_p=(0.4*F*(N@aff>0))                            # flux F->plants
        to_plants=share@f_to_p
        crowd=-(a@N)*N*0.5 + 0.5*N**2                       # crowding mortality -> litter
        mN=mort*N+crowd
        mF=0.05*F+0.3*F**2
        decf=0.8*Bac*Lf/(0.5+Lf);decs=0.08*WR*Ls/(1+Ls)
        gB=0.3*decf;gW=0.3*decs                             # microbe immobilization
        mB=0.15*Bac;mW=0.03*WR
        dN=u_direct+to_plants-mN
        dF=fung_up-f_to_p-mF
        dBac=gB-mB;dWR=gW-mW
        dLf=mN[~tree].sum()+mF.sum()+mB+mW-decf
        dLs=mN[tree].sum()-decs
        dR=(decf-gB)+(decs-gW)-u_direct.sum()-fung_up.sum()+0.02+0.01-0.05*R
        dep+=0.02*dt;fix+=0.01*dt;leach+=0.05*R*dt
        N+=dt*dN;F+=dt*dF;Bac+=dt*dBac;WR+=dt*dWR;Lf+=dt*dLf;Ls+=dt*dLs;R+=dt*dR
        h=0.02*max(Ls+0.5*Lf-fire_thr,0)**2
        if rng.random()<h*dt:
            fires+=1
            burn=0.9*Ls+0.9*Lf+0.7*N[tree].sum()+0.3*N[~tree].sum()+0.4*F.sum()
            volat+=0.5*burn;R+=0.5*burn
            Ls*=0.1;Lf*=0.1;N=np.where(tree,N*0.3,N*0.7);F*=0.6
        if k%2000==0:
            tot=N.sum()+F.sum()+Bac+WR+Lf+Ls+R
            mis.append(tot-(tot0+dep+fix-leach-volat))
        if k%200==0:B.append((k*dt,N.sum(),N[tree].sum(),Ls,R))
    return np.array(mis),fires,np.array(B)

mo=old();print("OLD misclosure (N units) at checkpoints:",np.round(mo[[0,1,5,10,-1]],3),"final |mis|/total ~",round(abs(mo[-1]),2))
mc,fires,B=conserved();print("CONSERVED misclosure max:",np.abs(mc).max())
late=B[B[:,0]>1000]
print("fires",fires,"biomass late mean",late[:,1].mean().round(3),"swing",(late[:,1].max()-late[:,1].min()).round(3),"tree share",(late[:,2]/late[:,1]).mean().round(2),"Ls range",late[:,3].min().round(2),late[:,3].max().round(2))
for thr in [0.3,0.5,0.8,1.2]:
    _,f,Bb=conserved(fire_thr=thr);l=Bb[Bb[:,0]>1000]
    print("thr",thr,"fires",f,"B mean",l[:,1].mean().round(3),"swing",(l[:,1].max()-l[:,1].min()).round(3),"Ls max",l[:,3].max().round(2))
