import csv
import json
import os
import itertools 

def load_config(filePath):
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"'{filePath}' not found.")
    with open(filePath, 'r') as file:
        return json.load(file) #returns the json as dictionary

def processRow(row, years):
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
            return 
            {
                'Country Name': country,
                'Region': region, 
                'Year': int(year),     
                'Value': float(value_str)  
            }
        except ValueError:
            return None
    return list(filter(None, map(extractYears, years)))

def load_gdp_data(filePath):
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"'{filePath}' not found.")

    with open(filePath, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        allHeaders = reader.fieldnames
        years = list(filter(lambda h: h.isdigit(), allHeaders)) #isolating year columns 

        if not years:
            raise ValueError("Could not find any Year columns in the CSV.")

        nestedData = map(lambda row: processRow(row, years), reader)
        flatData = list(itertools.chain.from_iterable(nestedData))
    return flatData