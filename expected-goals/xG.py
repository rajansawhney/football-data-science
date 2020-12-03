#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 19:47:16 2020

@author: rsawhney
"""

# The basics
import pandas as pd
import numpy as np
import json

# Plotting
import matplotlib.pyplot as plt
import FCPython

# Statistical fitting of models
import statsmodels.api as sm
import statsmodels.formula.api as smf

## Decide which league to load
# Wyscout data from https://figshare.com/collections/Soccer_match_event_dataset/4415000/2
with open(data/matches/matches_England.json) as f:
    data = json.load(f)
    
# Create a data set of shots
train = pd.DataFrame(data)
pd.unique(train['subEventName'])
shots = train[train['subEventName']=='Shot']
shots_model = pd.DataFrame(columns=['Goal', 'X', 'Y'])

## Go through the dataframe and calculate X, Y coordinates
# Distance from a line in the centre
# Shot angle
# Details of tags can be found here: https://apidocs.wyscout.com/matches-wyid-events
for i, shot in shot.iterrows():
    header=0
    for shottags['id']==403