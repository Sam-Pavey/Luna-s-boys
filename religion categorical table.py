# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 23:51:58 2025

@author: ssamp
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('Working file.csv')
df[['Religion or denomination belonging to at present, United Kingdom']]= df[['Religion or denomination belonging to at present, United Kingdom']].astype('category') 



counts = df['Religion or denomination belonging to at present, United Kingdom'].value_counts().reset_index()
counts.columns = ["category", "n_mentions"]

counts.to_clipboard()