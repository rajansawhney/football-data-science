#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 17:15:13 2020

@author: rsawhney
"""

'''
An example of linear regression

Find relation b/w minutes played and goals scored
'''


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Some made up data
minutes_played = np.array([120, 452, 185, 708, 340, 561])
goals_scored = np.array([1, 6, 3, 7, 3, 5])

# Set up dataframe
minutes_model = pd.DataFrame()
minutes_model = minutes_model.assign(minutes=minutes_played)
minutes_model = minutes_model.assign(goals=goals_scored)

fig, ax = plt.subplots(num=1)
ax.plot(minutes_played, goals_scored, linestyle='none',
        marker='.', markerSize=12, color='black')
ax.set_ylabel('Goals scored')
ax.set_xlabel('Minutes played')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlim((0, 750))
plt.ylim((0, 8))

# slope of one goal per 90 mins played
b = 1/90
# intercept
a = 0

# Slope determined by linear regression
model_fit = smf.ols(formula='goals_scored ~ minutes_played - 1',
                    data=minutes_model).fit()
print(model_fit.summary())
[b] = model_fit.params

x = np.arange(800, step=0.1)
y = a + b*x

ax.plot(minutes_played, goals_scored, linestyle='none',
        marker='.', markerSize=12, color='black')
ax.plot(x, y, color='black')

# Show distances to line
for i, mp in enumerate(minutes_played):
    ax.plot([mp, mp], [goals_scored[i], a+b*mp], color='red')

plt.show()

# Objective -- fit curve to reduce the distance from line
# let model figure out slope (b) and intercept (a)
fig, ax = plt.subplots(num=1)
ax.plot(minutes_played, goals_scored, linestyle='none',
        marker='.', markerSize=12, color='black')
ax.set_ylabel('Goals scored')
ax.set_xlabel('Minutes played')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlim((0, 750))
plt.ylim((0, 8))

model_fit = smf.ols(formula='goals_scored ~ minutes_played',
                    data=minutes_model).fit()
print(model_fit.summary())
[a, b] = model_fit.params

x = np.arange(800, step=0.1)
y = a + b*x

ax.plot(minutes_played, goals_scored, linestyle='none',
        marker='.', markerSize=12, color='black')
ax.plot(x, y, color='black')

# Show distances to line
for i, mp in enumerate(minutes_played):
    ax.plot([mp, mp], [goals_scored[i], a+b*mp], color='red')

plt.show()

# ^ problem with the above is that at minute 0, player has chance of scoring 0.7 goals - not correct
# hence add -1 to fit, and model will not return a anymore. Set a=0 manually
fig, ax = plt.subplots(num=1)
ax.plot(minutes_played, goals_scored, linestyle='none',
        marker='.', markerSize=12, color='black')
ax.set_ylabel('Goals scored')
ax.set_xlabel('Minutes played')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlim((0, 750))
plt.ylim((0, 8))

model_fit = smf.ols(formula='goals_scored ~ minutes_played -1',
                    data=minutes_model).fit()
print(model_fit.summary())
[b] = model_fit.params
a = 0

x = np.arange(800, step=0.1)
y = a + b*x

ax.plot(minutes_played, goals_scored, linestyle='none',
        marker='.', markersize=12, color='black')
ax.plot(x, y, color='black')

# Show distances to line
for i, mp in enumerate(minutes_played):
    ax.plot([mp, mp], [goals_scored[i], a+b*mp], color='red')

plt.show()

'''
What we see is 1/b = 97.3444 - best model is that player score on avg every 97mins
'''

'''
Since a straight goes on for infinity, linear model is not the best model for xG
we want the value to be b/w 0 and 1, hence logistic regression is a better option
'''

