# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 19:52:31 2025

@author: ssamp
"""

from statsmodels.formula.api import ols
from statsmodels.iolib.summary2 import summary_col
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('Working file.csv')

#variable column names need to be one word to work for ols
df['l_r'] = df['Placement on left right scale']
df['emotional_country'] = df['How emotionally attached to [country]']
df['emotional_europe'] = df['How emotionally attached to Europe']
df['log_news'] = df['News about politics and current affairs, watching, reading or listening, in minutes'].apply(lambda x: np.log(x+1))
df[['religion']]= df[['Religion or denomination belonging to at present, United Kingdom']].astype('category')

# model= ols('Placement on left right scale ~ log news mins + How emotionally attached to [country] + How emotionally attached to Europe + Feeling of safety of walking alone in local area after dark + C(Religion or denomination belonging to at present, United Kingdom)', data=df).fit() # fit the model
model= ols("l_r ~ log_news + emotional_country + emotional_europe + C(religion, Treatment(reference='Not applicable'))", data=df).fit()


table=summary_col( # create a regression table 
    model, # pass the models to the summary_col function
    stars=True, # add stars denoting the p-values of the coefficient to the table; * p<0.05, ** p<0.01, *** p<0.001
    float_format='%0.3f', # set the decimal places to 3
    model_names=['UK, 2023'], # set the name of the model
    info_dict = {"N":lambda x: "{0:d}".format(int(x.nobs))}) # add the number of observations to the table

print(table)
print(table.as_text())