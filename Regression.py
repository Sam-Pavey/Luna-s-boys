# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 19:52:31 2025

@author: ssamp
"""


# this file can be altered easily to include different years in the regression (only 2026, 2018, 2023 work as they have the relevant variables. For our regression we used only 2023. 

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
# d2010 = df[df['Year']==2010]
# m2010= ols("l_r ~ log_news + emotional_country + emotional_europe + C(religion, Treatment(reference='Not applicable'))", data=d2010).fit()
# m2012= ols("l_r ~ log_news + emotional_country + emotional_europe + C(religion, Treatment(reference='Not applicable'))", data=df[df['Year']==2012]).fit()
# m2014= ols("l_r ~ log_news + emotional_country + emotional_europe + C(religion, Treatment(reference='Not applicable'))", data=df[df['Year']==2014]).fit()
# m2016= ols("l_r ~ log_news + emotional_country + emotional_europe + C(religion, Treatment(reference='Not applicable'))", data=df[df['Year']==2016]).fit()
# m2018= ols("l_r ~ log_news + emotional_country + emotional_europe + C(religion, Treatment(reference='Not applicable'))", data=df[df['Year']==2018]).fit()
m2023= ols("l_r ~ log_news + emotional_country + emotional_europe + C(religion, Treatment(reference='Not applicable'))", data=df[df['Year']==2023]).fit()




table=summary_col( # create a regression table 
    [m2023], # pass the models to the summary_col function
    stars=True, # add stars denoting the p-values of the coefficient to the table; * p<0.05, ** p<0.01, *** p<0.001
    float_format='%0.3f', # set the decimal places to 3
    model_names=['2023'], # set the name of the model
    info_dict = {"N":lambda x: "{0:d}".format(int(x.nobs))}) # add the number of observations to the table

# print(table.as_csv())
# print(table)

print(table.as_latex())
