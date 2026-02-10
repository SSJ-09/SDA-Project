import functools
from itertools import groupby
import pandas as pd

def process_data(data, config):
    
    df = pd.DataFrame(data)
    
    region = config['region']
    year = config['year']
    rawOp = config['operation'].lower()
    operation = 'mean' if rawOp in ['avg', 'average'] else rawOp
    
    #Filtering
    df_year = df[df['Year'] == year]
    df_region = df[df['Region'] == region]
    df_specific = df_region[df_region['Year'] == year]

    #Key Aggregation 
    global_comp_data = df_year.groupby('Region')['Value'].agg(operation).to_dict()
    trend_data = df_region.groupby('Year')['Value'].agg(operation).to_dict()
    
    country_series = df_specific.set_index('Country Name')['Value'].sort_values(ascending=False)
    
    top_10 = country_series.head(10).to_dict()
    if len(country_series) > 10:
        top_10['Others'] = country_series.iloc[10:].sum()

    return {
        "config": config,
        "graph_1_bar": global_comp_data,
        "graph_2_pie": global_comp_data,
        "graph_3_line": trend_data,
        "graph_4_hist": list(trend_data.values()),
        "graph_5_top10": top_10
    }