# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 19:05:25 2025

@author: ssamp
"""
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('Working file.csv')
df['log news mins'] = df['News about politics and current affairs, watching, reading or listening, in minutes'].apply(lambda x: np.log(x+1))
df['log safety'] = df['Feeling of safety of walking alone in local area after dark'].apply(lambda x: np.log(x))
#to do different plots just change the x variable and the lable



sns.jointplot(data=df, # plot a scatterplot with a regression line and two histograms
                x='log safety', # set the x axis to be the years of schooling
                y='Placement on left right scale', # set the y axis to be the hourly wage
                kind="reg",  # set the kind of plot to be a regression plot
                scatter_kws=dict(alpha=0.1), # set the transparency of the points to be 0.1 (10%)
                line_kws=dict(color='red'), # set the color of the regression line to red
                height=8) # set the height of the plot to be 10 inches 

plt.xlabel('log(Feeling of safety of walking alone in local area after dark)') # add a label to the x axis
plt.ylabel('Placement on left right scale') # add a label to the y axis