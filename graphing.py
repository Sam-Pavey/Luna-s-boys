# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 18:10:55 2025

@author: ssamp
"""


# This file is an initial attempt at graphing regional results, before utilising ONS maps as these aligned with the regions used in the ESS survey. 
# Because of this, please ignore this file as it was not used in the final project. 




import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd

#https://www.ukpostcode.net/shapefile-of-uk-administrative-counties-wiki-16.html

df = pd.read_csv('Working file.csv')
with open('location.txt', 'r') as file:
    location_codes = {key.strip(): value.strip() for key, value in (line.split(' ', 1) for line in file)}  
counties = gpd.read_file(r"C:\Users\ssamp\OneDrive - University College London\modules\QM2\ess cleaning pipeline (longitudinal)\uk_admin_map_shapefile\Map_UK.shp", crs='epsg:32630')


regions = {}
for index, row in df.iterrows():
    if row['Region'] not in regions:
        regions[row['Region']] = 1
    else:
        regions[row['Region']] += 1



all_regions = {}

def add_regions(code, region):
    for key, value in location_codes.items():
        if code in key:
            all_regions[value] = regions[region]
        
add_regions('UKC', 'North East (England)')
add_regions('UKD', 'North West (England)')
add_regions('UKE', 'Yorkshire and the Humber')
add_regions('UKF', 'East Midlands (England)')
add_regions('UKG', 'West Midlands (England)')
add_regions('UKH', 'East of England')
add_regions('UKI', 'London')
add_regions('UKJ', 'South East (England)')
add_regions('UKK', 'South West (England)')
add_regions('UKL', 'Wales')
add_regions('UKM', 'Scotland')
add_regions('UKN', 'Northern Ireland')


counties['frequency'] = 0
for i in all_regions:
    try:
        print( counties[counties['NAME_2']==i].index[0])
        index = counties[counties['NAME_2']==i].index[0]
        counties.loc[index, 'frequency'] = all_regions[i]
    except:
        continue
    
    
fig = counties.plot(column='frequency', cmap='viridis', legend=True)

fig.set_xticks([])
fig.set_yticks([])

# set the plot title
plt.title("Heatmap of frequency in the dataset ")
plt.show()

# base = counties.plot(figsize=(9,9), color='whitesmoke', edgecolor='gainsboro')
# base.axis('off')


# london.plot(ax=base, column='NAME_2', cmap='Paired', alpha=0.4, zorder=1)

# base.axis('off')

# plt.annotate(text='London',
#              xy=(7.15e5, 5.71e6),
#              xytext=(8.6e5, 5.72e6),
#              horizontalalignment='left',
#              verticalalignment='top',
#              fontsize=11,
#              arrowprops={'arrowstyle': '->',
#                          'color': 'red'},

#              color='black')
