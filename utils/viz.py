# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 10:10:48 2020

@author: AubertSigouin-Lebel
"""

import plotly
import geopandas as gpd


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


def map_city_count(city_value_counts_df, geojson_path):

    df = gpd.read_file(geojson_path)
    
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
        

    x = city_value_counts_df['mean_x']
    y = city_value_counts_df['mean_y']
    
    city_scatter = dict(
        type = 'scatter',
        showlegend = False,
        x=x,
        y=y,
        mode = 'markers',
        marker = dict(
            size =city_value_counts_df['count_scaled']*100
            ),
        fillcolor = 'purple',
        opacity = 0.8
    )
    plot_data.append(city_scatter)
    
    
    fig = dict(data=plot_data, layout=layout)
    
    return(plotly.offline.iplot(fig, filename='county_text.html'))

    
