# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 09:15:48 2020

@author: ag
"""

#acajutla-b:
#LATITUDE                                   13.5833
#LONGITUDE                                 -89.8333

import pandas as pd
import tidalfit

TICON = pd.read_csv('TICON/TICON.txt',names=('lat','lon','constituent','amplitude','phase'), sep=r'\s+', header=None, usecols=[0,1,2,3,4])

acaticon = TICON.loc[(TICON.lat==13.5833) & (TICON.lon==-89.8333)]
 
constituents = acaticon.constituent.values
amplitude = acaticon.amplitude.values
phase = acaticon.phase.values


T = tidalfit.TidalModel(constituentlist=constituents,amplitude=amplitude,phase=phase)
