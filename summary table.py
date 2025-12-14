# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 23:11:51 2025

@author: ssamp
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('Working file.csv')
variables = ['News about politics and current affairs, watching, reading or listening, in minutes',
    'How emotionally attached to [country]',
    'How emotionally attached to Europe',
    'Religion or denomination belonging to at present, United Kingdom',
    'Feeling of safety of walking alone in local area after dark',
    'Placement on left right scale'
    ]
df = df[variables]
df[['Religion or denomination belonging to at present, United Kingdom']]= df[['Religion or denomination belonging to at present, United Kingdom']].astype('category')

summary=df.describe().round(2)  # generate summary statistics, and round everything to 2 decimal degrees
summary=summary.T #.T transposes the table (rows become columns and vice versa)
summary.to_clipboard()