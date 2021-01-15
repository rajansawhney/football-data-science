#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 17:12:04 2020

@author: rsawhney
"""

"""
Fitting the xG model
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

# Plot logistic curve
b = [-3, 3]
x = np.arange(5, step=0.1)
y = 1/(1 + np.exp(-b[0]-b[1]*x))
fig, ax = plt.subplots(num=1)
plt.ylim((-0.05, 1.05))
plt.xlim((0,5))
ax.set_ylabel('y')
ax.set_xlabel('x')
ax.plot(x, y, linestyle='solid', color='black')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()


'''
For logitic regression, we maximize the product of distances
b/w outcome and prediction

Equivalently maximize sum of log of distance between points
and line (logliklihood)
'''

# Get first 200 shots
shots_200 = shots_model.iloc[:200]

# Plot first 200 shots
fig, ax = plt.subplots(num=1)
ax.plot(shots_200['Angle']*180/np.pi, shots_200['Goal'],
        linestyle='none', marker='.', markerSize=12, color='black')
ax.set_ylabel('Goal Scored')
ax.set_xlabel('Shot angle (degrees')
plt.ylim((-0.05, 1.05))
ax.set_yticks([0,1])
ax.set_yticklabels(['No', 'Yes'])
plt.show()


# Show empirically how angle predicts prob. of scoring
shotcount_dist = np.histogram(shots_model['Angle']*180/np.pi, 
                              bins=40,
                              range=[0, 150])
goalcount_dist = np.histogram(goals_only['Angle']*180/np.pi,
                              bins=40,
                              range=[0, 150])
prob_goal = np.divide(goalcount_dist[0], shotcount_dist[0])
angle = shotcount_dist[1]
midangle = (angle[:-1] + angle[1:])/2
fig, ax = plt.subplots(num=2)
ax.plot(midangle, prob_goal, linestyle='none', marker='.',
        markerSize=12, color='black')
ax.set_ylabel('Prob. chance scored')
ax.set_xlabel('Shot angle (degrees)')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)


# First try a linear model
# This is NOT a good model because a probability can't be less than zero or more than one
# Intercept and Slope
b = [-0.05, 1/125]
x = np.arange(150, step=0.1)
y = b[0] + b[1]*x 
ax.plot(x, y, linestyle='solid', color='black')


# Let's try sigmoid model
# This is good model but NOT a good way of fitting
# because each point contains lots of data points
fig, ax = plt.subplots(num=2)
ax.plot(midangle, prob_goal, linestyle='none', marker='.',
        markerSize=12, color='black')
ax.set_ylabel('Prob. chance scored')
ax.set_xlabel('Shot angle (degrees)')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

b = [3, -3]
x = np.arange(150, step=0.1)
y = 1/(1 + np.exp(b[0] + b[1] *x*np.pi/180))
ax.plot(x, y, linestyle='solid', color='black')
plt.show()


# Likelihood of model given data
xG = 1/(1+np.exp(b[0]+b[1]*shots_model['Angle']))
shots_model = shots_model.assign(xG=xG)
shots_40 = shots_model[:40]
fig, ax = plt.subplots(num=1)
ax.plot(shots_40['Angle']*180/np.pi, shots_40['Goal'],
        linestyle='none', marker='.', markerSize=12,
        color='black')
ax.plot(x, y, linestyle='solid', color='black')
ax.plot(x, 1-y, linestyle='solid', color='black')
logliklihood=0
for item, shot in shots_40.iterrows():
    ang = shot['Angle']*180/np.pi
    if shot['Goal']==1:
        logliklihood = logliklihood + np.log(shot['xG'])
        ax.plot([ang, ang], [shot['Goal'], shot['xG']], color='red')
    else:
        logliklihood = logliklihood + np.log(1 - shot['xG'])
        ax.plot([ang, ang], [shot['Goal'], 1-shot['xG']], color='blue')
        
ax.set_ylabel('Goal scored')
ax.set_xlabel('Shot angle (degrees)')
plt.ylim((-0.05, 1.05))
plt.xlim((0, 80))
plt.text(45, 0.2, 'Log-likelihood:')
plt.text(45, 0.1, str(logliklihood))
ax.set_yticks([0, 1])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()


'''
Make single variable model of angle
- using logistic regression we find the optimal values of b
NOTE: This process minimizes the loglikelihood
'''
log_ang_model = smf.glm(formula='Goal ~ Angle', 
                    data=shots_model,
                    family=sm.families.Binomial()).fit()
print(log_ang_model.summary())
b = log_ang_model.params

xGprob=1/(1 + np.exp(b[0] + b[1]*midangle*np.pi/180))


fig, ax = plt.subplots(num=1)
ax.plot(midangle, prob_goal, linestyle='none', 
        marker='.', markerSize=12, color='black')
ax.plot(midangle, xGprob, linestyle='solid', color='black')
ax.set_ylabel('Prob. chance scored')
ax.set_xlabel('Shot angle (degrees)')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_title(r'$\displaystyle P(goal) = '
              r'\frac{1}{1+exp(3.71-3.45 \theta)}$', fontsize=16, color='b')
# plt.text(20, 1.2, r'$\displaystyle P(goal) = '
#              r'\frac{1}{1+exp(3.71-3.45 \theta)}$', color='black')
# plt.text(160, 1.5, r'P(goal) = \frac{1}{1+exp(3.71-3.45\theta)}')
plt.show()
fig.savefig('plots/fitted-prob-of-scoring-vs-angle.png', dpi=None, bbox='tight')



'''
Let's look at distance from goal
'''
shotcount_dist = np.histogram(shots_model['Distance'], bins=40, range=[0, 70])
goalcount_dist = np.histogram(goals_only['Distance'], bins=40, range=[0, 70])
prob_goal = np.divide(goalcount_dist[0], shotcount_dist[0])
distance = shotcount_dist[1]
middistance = (distance[:-1] + distance[1:])/2
fig, ax = plt.subplots(num=1)
ax.plot(middistance, prob_goal, linestyle='none',
        marker='.', color='black')
ax.set_ylabel('Prob. chance scored')
ax.set_xlabel('Distance from goal (metres)')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)


# Make single variable model of distance
log_dist_model = smf.glm(formula='Goal ~ Distance', 
                         data=shots_model,
                         family=sm.families.Binomial()).fit()
print(log_dist_model.summary())
b = log_dist_model.params

xGprob = 1/(1 + np.exp(b[0]+b[1]*middistance))
ax.plot(middistance, xGprob, linestyle='solid', color='black')
ax.set_title(r'$\displaystyle P(goal) = '
              r'\frac{1}{1+exp(-0.53+0.17d)}$', fontsize=16, color='b')
plt.show()
fig.savefig('plots/fitted-prob-of-scoring-vs-dist.png', dpi=None, bbox='tight')
                

# Adding distance_sq
squaredD = shots_model['Distance']**2
shots_model = shots_model.assign(D2=squaredD)
test_model = smf.glm(formula="Goal ~ Distance + D2",
                     data=shots_model, 
                     family=sm.families.Binomial()).fit()
print(test_model.summary())        
b=test_model.params

xGprob=1/(1+np.exp(b[0]+b[1]*middistance+b[2]*pow(middistance,2))) 
fig,ax=plt.subplots(num=1)
ax.plot(middistance, prob_goal, linestyle='none', marker= '.', color='black')
ax.set_ylabel('Probability chance scored')
ax.set_xlabel("Distance from goal (metres)")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.plot(middistance, xGprob, linestyle='solid', color='black')
ax.set_title(r'$\displaystyle P(goal) = '
              r'\frac{1}{1+exp(-1.38+0.29d-0.0038d^2)}$', fontsize=16, color='b')
plt.show()
fig.savefig('plots/fitted-prob-of-scoring-vs-distsq.png', dpi=None, bbox='tight')


'''
Adding even more variables to the model
'''
squaredX = shots_model['X']**2
shots_model = shots_model.assign(X2=squaredX)
squaredC = shots_model['C']**2
shots_model = shots_model.assign(C2=squaredC)
AX = shots_model['Angle']*shots_model['X']
shots_model = shots_model.assign(AX=AX)


# A general model for fitting goal probability
# list the model variables you want here
#model_variables = ['Angle', 'Distance']
model_variables = ['Angle', 'Distance', 'C']
model = ''
for v in model_variables[:-1]:
    model = model + v + ' + '
model = model + model_variables[-1]


# Fit the model
test_model = smf.glm(formula='Goal ~ ' + model, data=shots_model,
                     family=sm.families.Binomial()).fit()
print(test_model.summary())
b = test_model.params


#Return xG value for more general model
def calculate_xG(sh):    
   bsum=b[0]
   for i,v in enumerate(model_variables):
       bsum=bsum+b[i+1]*sh[v]
   xG = 1/(1+np.exp(bsum)) 
   return xG   

#Add an xG to my dataframe
xG=shots_model.apply(calculate_xG, axis=1) 
shots_model = shots_model.assign(xG=xG)

#Create a 2D map of xG
pgoal_2d=np.zeros((65,65))
for x in range(65):
    for y in range(65):
        sh=dict()
        a = np.arctan(7.32 *x /(x**2 + abs(y-65/2)**2 - (7.32/2)**2))
        if a<0:
            a = np.pi + a
        sh['X'] = x
        sh['Angle'] = a
        sh['Distance'] = np.sqrt(x**2 + abs(y-65/2)**2)
        sh['D2'] = x**2 + abs(y-65/2)**2
        sh['AX'] = x*a
        sh['X2'] = x**2
        sh['C'] = abs(y-65/2)
        sh['C2'] = (y-65/2)**2
        
        pgoal_2d[x,y] =  calculate_xG(sh)

(fig,ax) = FCPython.createGoalMouth()
pos=ax.imshow(pgoal_2d, extent=[-1,65,65,-1], aspect='auto',cmap=plt.cm.Reds,vmin=0, vmax=0.3)
fig.colorbar(pos, ax=ax)
ax.set_title('Probability of goal')
plt.xlim((0,66))
plt.ylim((-3,35))
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
fig.savefig('plots/goalprobfor_' + model  + '.png', dpi=None, bbox_inches="tight")   
        
        
        













    













































