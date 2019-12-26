# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 11:58:03 2019

@author: ag
"""

import pandas as pd
import numpy as np
import scipy.sparse.linalg


#TODO: make singleton...
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
harmonicsfile = os.path.join(dir_path,'tidalconstants/harmonics.xlsx')
constituents = pd.read_excel(harmonicsfile,index_col='sname',usecols=['sname', 'speed'])
constituents.index = constituents.index.str.upper()


NOAA = ['M2', 'S2', 'N2', 'K1', 'M4', 'O1', 'M6', 'MK3', 'S4', 'MN4', 'NU2', 
        'S6', 'MU2', '2N2', 'OO1', 'LAM2', 'S1', 'M1', 'J1', 'MM', 'SSA', 'SA', 
        'MSF', 'MF', 'RHO1', 'Q1', 'T2', 'R2', '2Q1', 'P1', '2SM2', 'M3', 'L2', 
        '2MK3', 'K2', 'M8', 'MS4']


class TidalModel:
    
    
    def __init__(self, constituentlist = NOAA):
        C = constituents.loc[NOAA].copy() #TODO: case sensitive!!!
        C.insert(1,'amplitude',0.0)
        C.insert(2,'phase',0.0)
        self.constituents = C

    def _predictors(self,t):
        t0 = pd.datetime.fromisoformat("2000-01-01T12:00:00")
        t = (t-t0)/np.timedelta64(1,'h')
        phi = np.outer(t,np.pi*self.constituents.speed/180.0)
        C = np.cos(phi)
        S = np.sin(phi)
        return (C,S)
    
    def predict(self,t):
        (C,S) = self._predictors(t)
        pC = self.constituents.amplitude * np.cos(self.constituents.phase)
        pS = self.constituents.amplitude * np.sin(self.constituents.phase)
        return np.dot(C,pC) + np.dot(S,pS)

    def fit(self,t,z):
        
        t = t[~np.isnan(z)]
        z = z[~np.isnan(z)]

        A = np.hstack(self._predictors(t))
        N = self.constituents.shape[0]
        
        (p,istop,itn,r1norm,r2norm,anorm,acond,arnorm,xnorm,var) = scipy.sparse.linalg.lsqr(A,z-np.nanmean(z))

        self.constituents.amplitude = np.sqrt(p[0:N]**2+p[N:2*N]**2)
        self.constituents.phase = np.arctan2(p[N:2*N],p[0:N])


        
    
    
if __name__ == '__main__':
    import pickle
    with open('tests/testsl.pickle', 'rb') as file:
        sl = pickle.load(file)
        
    T = TidalModel()
    T.fit(sl.index,sl.sl)
    import matplotlib.pyplot as plt
    plt.style.use('seaborn')

    plt.figure(figsize=[12, 6])
    sl=sl.loc[sl.index>pd.datetime.fromisoformat("2009-12-05")]
    plt.plot(sl.index,sl.sl-np.nanmean(sl.sl),linewidth=4)
    plt.plot(sl.index,T.predict(sl.index),'k',linewidth=1)
    
    