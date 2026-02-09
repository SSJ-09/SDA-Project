import functools
from itertools import groupby
#Helper functions

def Filter(data, key, value):
    """
Filters a list of dictionaries based on a specific key-value match.
Args:
    data (list): A list of dictionaries containing dataset records.
    key (str): The key to check in each dictionary.
    value: The value that the key must match.
Returns:
    list: A filtered list of dictionaries where key equals value.
"""
    return list(filter(lambda x: x.get(key) == value, data))

def calculate(values, operation):
    """
Performs aggregation (sum or average) on a list of numeric values.
Args:
    values (list): A list of numeric values.
    operation (str): The aggregation type ('sum' or 'avg').
Returns:
    float: The calculated result based on the operation.
"""
    if not values:
        return 0.0
    
    total = functools.reduce(lambda a, b: a + b, values)
    
    if operation.lower() == 'avg':
        return total / len(values)
    return total 

def keyAggregation(data, group_key, value_key, operation):
    """
Groups data by a specific key and performs aggregation on another key.
Args:
    data (list): A list of dictionaries representing dataset records.
    group_key (str): The key used to group the data.
    value_key (str): The key whose values will be aggregated.
    operation (str): The aggregation type ('sum' or 'avg').
Returns:
    dict: A dictionary with group_key values as keys and aggregated results as values.
"""

    sorted_data = sorted(data, key=lambda x: x[group_key])
    grouped_iter = groupby(sorted_data, key=lambda x: x[group_key])
    return {
        key: calculate(list(map(lambda x: x[value_key], group)), operation)
        for key, group in grouped_iter
    }



def process_data(data, config):
    """
Processes dataset according to user configuration to prepare data for the graphs
Args:
    data (list): A list of dictionaries representing dataset records.
    config (dict): Configuration containing 'region', 'year', and 'operation'.
Returns:
    dict: A dictionary with processed results for the graphs
"""

    region = config['region'] 
    year = config['year']     
    operation = config['operation'] 
    
    data_in_year = Filter(data, 'Year', year)
    data_in_region = Filter(data, 'Region', region)
   
    data_specific = Filter(data_in_region, 'Year', year)
    
    global_comp_data = keyAggregation(data_in_year, 'Region', 'Value', operation)
    trend_data = keyAggregation(data_in_region, 'Year', 'Value', operation)
    hist_data = list(trend_data.values())

    country_map = {item['Country Name']: item['Value'] for item in data_specific}
    
    sorted_countries = sorted(country_map.items(), key=lambda x: x[1], reverse=True)
    
    top_10 = dict(sorted_countries[:10])
    
    if len(sorted_countries) > 10:
        others_value = sum(item[1] for item in sorted_countries[10:])
        top_10['Others'] = others_value

    return {
        "config": config,
        "graph_1_bar": global_comp_data,   
        "graph_2_pie": global_comp_data,   
        "graph_3_line": trend_data,        
        "graph_4_hist": hist_data,
        "graph_5_top10": top_10  
    }