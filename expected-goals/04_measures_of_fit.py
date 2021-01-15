#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 15:59:49 2021

@author: rsawhney
"""

"""
Measuring the fit of the xG model

Need to run 01_xG_model to load data
and then 03_xG_model_fit to fit the model
"""

# The basics
import pandas as pd
import numpy as np
import json

# Plotting
import matplotlib
import matplotlib.pyplot as plt

import FCPython

# Statistical fitting of models
import statsmodels.api as sm
import statsmodels.formula.api as smf

# LaTex math usage
matplotlib.rcParams['text.usetex'] = True

# Mcfaddens Rsq for Logistic regression
'''
0.131, Answer b/w 0 and 1
Perfectly predicted goals = 1
No predictive power = 0

'''
null_model = smf.glm(formula="Goal ~ 1 ", data=shots_model,
                     family=sm.families.Binomial()).fit()
1-log_ang_model.llf/null_model.llf
1-log_dist_model.llf/null_model.llf


# ROC curve
num_obs=100
TP=np.zeros(num_obs)
FP=np.zeros(num_obs)
TN=np.zeros(num_obs)
FN=np.zeros(num_obs)

'''
TP - xG says it's a goal, and it's a goal in reality
FP - xG says its a goal, but not a goal in reality

TN - xG says it's not a goal, and not a goal in reality
FN - xG says it's not a goal, and it is a goal in reality

Area under the curve tells you the accuracy
'''

for i, threshold in enumerate(np.arange(0,1,1/num_obs)):
    for j, shot in shots_model.iterrows():
        if(shot['Goal']==1):
            if(shot['xG']>threshold):
                TP[i] = TP[i] + 1
            else:
                FN[i] = FN[i] + 1
        if(shot['Goal']==0):
            if(shot['xG']>threshold):
                FP[i] = FP[i] + 1
            else:
                TN[i] = TN[i] + 1
                

fig,ax = plt.subplots(num=1)
# fp-rate/tp-rate
ax.plot(FP/(FP+TN), TP/(TP+FN), color='black') 
ax.plot([0,1], [0,1], linestyle='dotted', color='black')
ax.set_ylabel('Predicted to score and did [ TP/(TP+FN) ]')
ax.set_xlabel('Predicted to score and did not [ FP/(FP+TN) ]')
plt.ylim((0.00, 1.00))
plt.xlim((0.00, 1.00))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.savefig('output/ROC_' + model + '.pdf', dpi=None, bbox='tight')




               