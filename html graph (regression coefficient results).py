# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 16:24:24 2026

html map for the website

@author: ssamp
"""



### this file generates the final html graph of coefficient results by region. 
# it is quite long but DOES work (this project was one of my first attempts at visualising geospatial data)



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd

import folium
import branca.colormap as cm
import numpy as np
from IPython.display import display

# variable = "emotional_country"

results = pd.read_csv("ols_regions_no_stars.csv")
results.columns = results.columns.str.replace(r"\s*\(.*?\)", "", regex=True)
results = results.rename(columns={"Yorkshire and the Humber": "Yorkshire and The Humber"})

uk_file = r"C:\Users\ssamp\OneDrive - University College London\modules\QM2\ess cleaning pipeline (longitudinal)\ONS Dec 2023 Countries uk\CTRY_DEC_2023_UK_BGC.shp"
en_file = r"C:\Users\ssamp\OneDrive - University College London\modules\QM2\ess cleaning pipeline (longitudinal)\ONS Dec 2023 regions en\RGN_DEC_2023_EN_BGC.shp"

uk = gpd.read_file(uk_file)
en = gpd.read_file(en_file)

non_england = uk[uk['CTRY23NM'] != 'England']
non_england['RGN23NM'] = non_england['CTRY23NM']

uk_full = gpd.GeoDataFrame(
    pd.concat([en, non_england], ignore_index=True),
    crs=en.crs
)

pop_density = pd.read_csv("ONS 2021 population density.csv")

def add_column(variable, uk_full):

    emotional_country = results[results['Unnamed: 0'] == variable]
    row = emotional_country.iloc[0]
    
    uk_full[variable] = 0
    
    for col, value in row[1:].items():
        try:
            index = uk_full[uk_full['RGN23NM'] == col].index
            # print(index)
            uk_full.loc[index, variable] = value
        except:
            continue
    
    uk_full[variable] = pd.to_numeric(uk_full[variable], errors="coerce")
    return uk_full


uk_full['pop_density'] = 0  
for index, row in pop_density.iterrows():
    # print(index, row)
    try: 
        index = uk_full[uk_full['RGN23NM'] == row['region']].index
        uk_full.loc[index, 'pop_density'] = row['density']
    except:
        continue    
uk_full['pop_density'] = pd.to_numeric(uk_full['pop_density'], errors="coerce")


add_column("emotional_country", uk_full)
add_column("emotional_europe", uk_full)
add_column("log_news", uk_full)
add_column("C(religion, Treatment(reference='Not applicable'))[T.Church of England / Anglican]", uk_full)
add_column("C(religion, Treatment(reference='Not applicable'))[T.Islam / Muslim]", uk_full)
add_column("C(religion, Treatment(reference='Not applicable'))[T.Other]", uk_full)
add_column("C(religion, Treatment(reference='Not applicable'))[T.Roman Catholic]", uk_full)
add_column("Intercept", uk_full)
# ------------------------------

uk_full["geometry"] = uk_full["geometry"].simplify(tolerance=500, preserve_topology=True)

m = folium.Map(
    location=[54, -2],
    zoom_start=5,
    tiles=None,
    max_bounds=True
)

folium.TileLayer(
    tiles="cartodbpositron",
    name="Base map",
    control=False
    
).add_to(m)




# --------------------------------

# coef_min, coef_max = uk_full[variable].min(), uk_full[variable].max()
# coef_cmap = cm.LinearColormap(
#     colors=["blue", "white", "red"],
#     vmin=coef_min,
#     vmax=coef_max,
#     caption="Regression coefficient"
# )

def coef_style(feature, coef_cmap, variable_):
    val = feature["properties"][variable_]
    return {
        "fillColor": coef_cmap(val) if val is not None else "#cccccc",
        "color": "black",
        "weight": 0.5,
        "fillOpacity": 0.7
    }

def add_variable_layer(m, variable, caption):
    coef_cmap = cm.linear.viridis.scale(
        # uk_full[variable].min(),
        # uk_full[variable].max()
        -0.3,
        0.3
    )
    coef_cmap.caption = caption 
    # "Coefficient for emotional attachment to Country"

    coef_layer = folium.FeatureGroup(name=caption, overlay=False, control=True)
    
    folium.GeoJson(
        uk_full,
        style_function=lambda feature: coef_style(feature, coef_cmap, variable),
        tooltip=folium.GeoJsonTooltip(
            fields=["RGN23NM", variable],
            aliases=["Region:", "Coefficient:"]
        )
    ).add_to(coef_layer)
    
    coef_layer.add_to(m)
    # coef_cmap.add_to(m)
    
    return m

coef_cmap = cm.linear.viridis.scale(
    # uk_full[variable].min(),
    # uk_full[variable].max()
    -0.3,
    0.3
)
coef_cmap.caption = "Colourmap scaling used (results beyond this range take a max/min value)"
coef_cmap.add_to(m)
# print(uk_full[variable].describe())

add_variable_layer(m, "emotional_country", "Coefficient for emotional attachment to Country")
add_variable_layer(m, "emotional_europe", "Coefficient for emotional attachment to Europe")
add_variable_layer(m, "log_news", "Coefficient for log(news consumption, in minutes)")
add_variable_layer(m, "C(religion, Treatment(reference='Not applicable'))[T.Church of England / Anglican]", "Coefficient for belonging to Church of England")
add_variable_layer(m, "C(religion, Treatment(reference='Not applicable'))[T.Islam / Muslim]", "Coefficient for belonging to Islam")
add_variable_layer(m, "C(religion, Treatment(reference='Not applicable'))[T.Other]", "Coefficient for belonging to an 'other' religion")
add_variable_layer(m, "C(religion, Treatment(reference='Not applicable'))[T.Roman Catholic]", "Coefficient for being Roman Catholic")
# ----------------------------

# pop_cmap = cm.linear.viridis.scale(
#     uk_full["pop_density"].min(),
#     uk_full["pop_density"].max()
# )
# pop_cmap.caption = "Population density"

# def pop_style(feature):
#     v = feature["properties"]["pop_density"]
#     return {
#         "fillColor": pop_cmap(v) if v is not None else "#cccccc",
#         "color": "black",
#         "weight": 0.5,
#         "fillOpacity": 0.5
#     }

# pop_layer = folium.FeatureGroup(name="Population density")

# folium.GeoJson(
#     uk_full,
#     style_function=pop_style,
#     tooltip=folium.GeoJsonTooltip(
#         fields=["RGN23NM", "pop_density"],
#         aliases=["Region:", "Pop. density:"]
#     )
# ).add_to(pop_layer)

# pop_layer.add_to(m)
# pop_cmap.add_to(m)
folium.LayerControl(collapsed=False).add_to(m)


m.save("uk_multivariable_map.html")
# html_str = m.get_root().render()

# print(html_str)
