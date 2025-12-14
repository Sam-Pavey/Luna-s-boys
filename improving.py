# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 14:42:41 2025

@author: ssamp
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('master dataset.csv')

#importing the keys given by the ess to make the dataset more readable
with open('location.txt', 'r') as file:
    location_codes = {key.strip(): value.strip() for key, value in (line.split(' ', 1) for line in file)}  
with open('keys.txt', 'r') as file:
    column_names = {key.strip(): value.strip() for key, value in (line.split('-', 1) for line in file)}
with open('religion labels (with other).txt', 'r') as file:
    religion_codes = {key.strip(): value.strip() for key, value in (line.split(' ', 1) for line in file)}  
    
    
#renaming columns with intelligible names instead of shortened codes
df = df.rename(columns=column_names)
    
#turning region codes into a text string for the region
for index, row in df.iterrows():
    df.loc[index, 'region'] = location_codes[row['region']] 
    df.loc[index, 'Religion or denomination belonging to at present, United Kingdom'] = religion_codes[str(row['Religion or denomination belonging to at present, United Kingdom'])] 
    
    
#changing codes for no response, refusal, not applicable, etc., into nan values
nan_codes = [66, 77, 88, 6666, 7777, 8888]
variables = ['News about politics and current affairs, watching, reading or listening, in minutes',
    'How emotionally attached to [country]',
    'How emotionally attached to Europe',
    'Feeling of safety of walking alone in local area after dark',
    'Placement on left right scale'
    ]

df = df[(~df[variables].isin(nan_codes).any(axis=1))]
df['Adjusted l/r placement'] = df['Placement on left right scale'].apply(lambda x: (x-5))

#creating distribution plot:
# plt.hist(df['Adjusted l/r placement'], color='blue')
# plt.title('Adjusted Distribution of placement on left right scale (UK, 2023)')
# plt.xticks(range(-5, 6))
# plt.show()

df.to_csv('Working file.csv', encoding='utf-8-sig', index=False)

    

