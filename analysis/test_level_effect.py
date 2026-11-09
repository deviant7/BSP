"""Audit check: the level-effect matching and event-path code (level_effect.py) recovers known in-ban shifts (+10 and -6 bp)
on synthetic random-walk data. Run: python3 -I analysis/test_level_effect.py"""
import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import level_effect as le
rng=np.random.default_rng(1)
nS,nT=60,400
days=pd.bdate_range('2018-01-01',periods=nT)
m=np.cumsum(rng.normal(0,3,(nS,nT)),axis=1)*0.3/1e4   # in units (pre-BP)
OM=rng.uniform(0.85,0.95,(nS,nT))
D=dict(days=days,M={'m':m*1e4},OM=OM,BAN=np.zeros((nS,nT),bool))
ev=[];true=[]
for e in range(150):
    j=rng.integers(0,30); i0=rng.integers(30,nT-30); L=rng.integers(1,8)
    eff=10.0 if e%2 else -6.0
    D['M']['m'][j,i0:i0+L]+=eff; true.append(eff)
    ev.append(dict(symbol=str(j),j=j,i0=i0,L=L,date=days[i0],C=1.0 if e%2 else -1.0,x=np.r_[OM[j,i0-4:i0+1][::-1],D['M']['m'][j,i0-1]],imputed=False))
E=pd.DataFrame(ev)
rows=[dict(j=j,s=s,date=days[s],x=np.r_[OM[j,s-4:s+1][::-1],D['M']['m'][j,s-1]]) for j in range(30,60) for s in range(30,nT-30)]
Cd=pd.DataFrame(rows); Cd['wk']=Cd.date.dt.to_period('W')
Mi=le.match(E,Cd)
ks,P=le.paths(D,E,Cd,Mi,'m')
E['D']=le.main_stat(E,ks,P)
print(E.groupby('C').D.agg(['mean','std','size']))
print('pre-period k=-10..-2 mean', np.nanmean(P[:,10:19]).round(3), ' post-spell k=10..20', np.nanmean(P[:,30:]).round(2))
