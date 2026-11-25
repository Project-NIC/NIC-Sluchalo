"""NIC-Sluchalo (Netopýr): the propeller — 8 arms x 16 places (128), 32 or 64 fitted; each arm four groups of
four places, a group one data line of its converter, two of a group fitted for 64, one for 32.
    python3 propeller.py <diameter_m> <out.npz>   (25 Nov 2026)"""
import sys, importlib.util as u, numpy as np
s=u.spec_from_file_location('L','layout.py');L=u.module_from_spec(s);s.loader.exec_module(L)
D=float(sys.argv[1]); out=sys.argv[2]
ARMS,PL=8,16; r0,R=0.015,D/2-0.004; twist=np.pi/2   # r0: a ~3 cm middle for the Pi camera
rr=np.linspace(r0,R,4000); th_=twist*np.log(rr/r0)/np.log(R/r0)
x_,y_=rr*np.cos(th_),rr*np.sin(th_); sarc=np.r_[0,np.cumsum(np.hypot(np.diff(x_),np.diff(y_)))]
r=np.interp(np.linspace(0,sarc[-1],PL),sarc,rr)          # places evenly along the arm
places=[]
for a in range(ARMS):
    th=2*np.pi*a/ARMS+twist*np.log(r/r0)/np.log(R/r0)
    places.append(np.c_[r*np.cos(th),r*np.sin(th)])
P=np.array(places)                     # arm, place, xy ; groups = places 0-3, 4-7, 8-11, 12-15
pitch=np.linalg.norm(np.diff(P[0],axis=0),axis=1)
def pick(sel): return P[sel]
def search(per_group,seed,steps):
    rng=np.random.default_rng(seed); sel=np.zeros((ARMS,PL),bool)
    for a in range(ARMS):
        for g in range(4): sel[a,g*4+rng.choice(4,per_group,replace=False)]=True
    best=L.judge(P[sel])[2]
    for i in range(steps):
        a=rng.integers(ARMS); g=rng.integers(4); idx=np.arange(g*4,g*4+4)
        on=idx[sel[a,idx]]; off=idx[~sel[a,idx]]
        if len(off)==0: continue
        i1=rng.choice(on); i0=rng.choice(off); sel[a,i1]=False; sel[a,i0]=True
        c=L.judge(P[sel])[2]
        if c<=best: best=c
        else: sel[a,i1]=True; sel[a,i0]=False
    return best,sel
res={}
for n,pg in ((32,1),(64,2)):
    best=min((search(pg,sd,1500) for sd in (1,2)),key=lambda t:t[0])
    sel=best[1]; xy=P[sel]; wx,wy,g=L.judge(xy,201)
    d=np.linalg.norm(xy[:,None]-xy[None],axis=-1); d[d==0]=9
    print(f'D={D*100:.0f} cm  {n} of 128: spot {wx*1000:.0f} x {wy*1000:.0f} cm ghost {g:.1f} dB  nearest {d.min()*1000:.1f} mm  (place pitch {pitch.min()*1000:.1f}-{pitch.max()*1000:.1f} mm)',flush=True)
    res[n]=sel
# free sunflower in the same circle for comparison
for n in (32,64):
    xy=L_s=None
    k2=np.arange(n)+0.5; rr=np.sqrt(r0**2+(R**2-r0**2)*k2/n); aa=k2*np.pi*(3-np.sqrt(5))
    xy=np.c_[rr*np.cos(aa),rr*np.sin(aa)]; wx,wy,g=L.judge(xy,201)
    print(f'D={D*100:.0f} cm  sunflower {n}: spot {wx*1000:.0f} x {wy*1000:.0f} cm ghost {g:.1f} dB',flush=True)
np.savez(out,places=P,sel32=res[32],sel64=res[64])
