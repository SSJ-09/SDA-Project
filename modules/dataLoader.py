import csv
import json
import os
import itertools 

def load_config(filePath):
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"'{filePath}' not found.")
    with open(filePath, 'r') as file:
        return json.load(file) #returns the json as dictionary

def normalizeRow(row, years):
    """
    Converts a single CSV row (wide format) into a list of yearly records (long format).
    Example:
        Input: {'Country': 'China', '2015': '100', '2016': '110'}
        Output: [{'Country': 'China', 'Year': 2015, 'Value': 100}, 
                 {'Country': 'China', 'Year': 2016, 'Value': 110}]
    Args:
        row (dict): A dictionary representing one row from the CSV.
        years (list): A list of column names that represent years (e.g., ['2015', '2016']).
    Returns:
        list: A list of dictionaries, where each dictionary represents one specific year's data.
    """
    country = row.get('Country Name')
    region = row.get('Continent') 
    if not country or not region: #discarding any row with no country or continent name
        return []
    country = country.strip()
    region = region.strip()
    def extractYears(year):
        value_str = row.get(year)     
        if not value_str:
            return None
        try:   
            return {
                'Country Name': country,
                'Region': region, 
                'Year': int(year),     
                'Value': float(value_str)  
            }
        except ValueError:
            return None
    return list(filter(None, map(extractYears, years)))

def load_gdp_data(filePath):
    """
    Reads the entire GDP CSV file and converts it into a clean list of records.
    Args:
        filePath (str): The path to the CSV file.
    Returns:
        list: A flat list of dictionaries containing Country, Region, Year, and Value(GDP).
    """
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"'{filePath}' not found.")

    with open(filePath, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        allHeaders = reader.fieldnames
        years = list(filter(lambda h: h.isdigit(), allHeaders)) #isolating year columns 

        if not years:
            raise ValueError("Could not find any Year columns in the CSV.")

        nestedData = map(lambda row: normalizeRow(row, years), reader)
        flatData = list(itertools.chain.from_iterable(nestedData))
    return flatData