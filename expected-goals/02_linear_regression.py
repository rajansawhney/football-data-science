#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 17:15:13 2020

@author: rsawhney
"""

'''
An example of linear regression
'''

import pandas as pd
import numpy as np
import matplotlib as plt

# Some made up data
minutes_played=np.array([120,452,185,708,340,561])
goals_scored=np.array([1,6,3,7,3,5])

# Set up dataframe
