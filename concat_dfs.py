#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:35:27 2023

@author: thomastesselaar
"""

import pandas as pd

n = 12

for i in range(n):
    df1 = pd.read_csv("/Users/thomastesselaar/Projects/QMIND2022/keyword_checking/multiTimeline-"+str(i+1)+".csv", header=1)
    df2 = pd.read_csv("/Users/thomastesselaar/Downloads/multiTimeline-"+str(i+1)+".csv", header=1)
    df1 = pd.concat([df2, df1], ignore_index=True)
    df1.to_csv("/Users/thomastesselaar/Projects/QMIND2022/keyword_checking/Term"+str(i+1)+".csv", index=False)

# print(df1)
# df1.to_csv("/Users/thomastesselaar/Desktop/multiTimeline-1.csv", index=False)