# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 09:15:48 2020

@author: ag
"""

#acajutla-b:
#LATITUDE                                   13.5833
#LONGITUDE                                 -89.8333

import pandas as pd
import numpy as np
import tidalfit

TICON = pd.read_csv('TICON/TICON.txt',names=('lat','lon','constituent','amplitude','phase'), sep=r'\s+', header=None, usecols=[0,1,2,3,4])

acaticon = TICON.loc[(TICON.lat==13.5833) & (TICON.lon==-89.8333)]
 
constituents = acaticon.constituent.values
amplitude = acaticon.amplitude.values /100
phase = acaticon.phase.values


T = tidalfit.TidalModel(constituentlist=constituents,amplitude=amplitude,phase=phase)


import pickle
with open('Acajutla-B.pickle', 'rb') as file:
    sl = pickle.load(file)

import matplotlib.pyplot as plt
plt.style.use('seaborn')

plt.figure(figsize=[12, 6])

sl=sl.loc[sl.index>pd.datetime.fromisoformat("2009-12-05")]
plt.plot(sl.index,sl.sl-np.nanmean(sl.sl),linewidth=4)
plt.plot(sl.index,T.predict(sl.index),'k',linewidth=1)

phase = T.constituents.phase.copy()
T.fit(sl.index,sl.sl)
print(phase-T.constituents.phase.copy())