# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 10:10:48 2020

@author: AubertSigouin-Lebel
"""

import plotly
import geopandas as gpd
import pandas as pd
from sklearn import preprocessing


def hist_plot(series, title):
    
    fig = plotly.offline.iplot(
        {
            'data':[
                {
                    'type' : 'histogram',
                    'x' : series,
                    'nbinsx' : len(series),
                    'marker' : {
                        'line' : {
                            'color' : '#000000',
                            'width' : 2
                        }
                    },
                    'opacity' : 0.5,
                }
            ],
            'layout':{
                'xaxis' : {
                    'tickangle' : 45
                },
                'title' :  title,
                'legend' : {
                    'x' : 1,
                    'xanchor' : 'center'
                },
                'font' : {
                    'size' : 10,
                    'family' : "Open Sans, sans-serif"
                }
            }
        }
    )
    
    return fig


def map_city_count(city_value_counts_df, cx = 'longitude', cy = 'latitude', r = 'count_scaled'):

    df = gpd.read_file('../data/geojson/region_admin_poly.shp')
    
    layout = dict(
        hovermode = 'closest',
        dragmode = 'zoom',
        plot_bgcolor = 'white',
        xaxis = dict(
            autorange = False,
            range = [-80, -55],
            showgrid = False,
            zeroline = False,
            visible = False,
            fixedrange = True
        ),
        yaxis = dict(
            autorange = False,
            range = [40, 64],
            showgrid = False,
            visible = False,
            zeroline = False,
            fixedrange = True
        ),
        width = 1000,
        height= 800,
        margin = dict(
            l = 150,
            t=0
            )
        
        
    )
    
    
    plot_data = []
    for index,row in df.iterrows():

        x = list(row.geometry.exterior.xy[0])
        y = list(row.geometry.exterior.xy[1])

        
        county_outline = dict(
                type = 'scatter',
                showlegend = False,
                legendgroup = "shapes",
                line = dict(width=1, color='white'),
                x=x,
                y=y,
                fill='toself',
                fillcolor = 'orange',
                opacity = 0.2,
                hoverinfo='none'
        )
        
        plot_data.append(county_outline)
        

    cx = city_value_counts_df[cx]
    cy = city_value_counts_df[cy]
    
    city_scatter = dict(
        type = 'scatter',
        showlegend = False,
        x=cx,
        y=cy,
        mode = 'markers',
        marker = dict(
            size =city_value_counts_df[r]*100
            ),
        fillcolor = 'purple',
        opacity = 0.8
    )
    plot_data.append(city_scatter)
    
    
    fig = dict(data=plot_data, layout=layout)
    
    return(plotly.offline.iplot(fig, filename='county_text.html'))


def city_postings(df, city_label_cols='city_name', longitude_cols = 'longitude',
                  latitude_cols = 'latitude', scaler='MinMaxScaler'):
    
    city_count = pd.DataFrame(df[city_label_cols].value_counts())

    scaler = getattr(preprocessing, scaler)(feature_range=(0.1,0.9))
    scaled_count = scaler.fit_transform(city_count.values.reshape(-1,1))

    city_count['count_scaled'] = scaled_count
    city_count['latitude'] = [df[df[city_label_cols]==city][latitude_cols].mean() for city in city_count.index]
    city_count['longitude'] = [df[df[city_label_cols]==city][longitude_cols].mean() for city in city_count.index]

    return(city_count.drop('Unavailable'))
