import csv
import json
import os

def load_config(filePath):
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"'{filePath}' not found.")
    with open(filePath, 'r') as file:
        return json.load(file)

def processRow(row, years):
    """
    Extracts data for each year from a CSV row.
    """
    country = row.get('Country Name')
    region = row.get('Continent') 
    
    # Validation
    if not country or not region: 
        return []
    
    country = country.strip()
    region = region.strip()
    
    extracted_data = []
    
    for year in years:
        value_str = row.get(year)
        if not value_str:
            continue
            
        try:
            # Create the dictionary on one line or inside specific brackets to avoid syntax errors
            record = {
                'Country Name': country,
                'Region': region, 
                'Year': int(year),     
                'Value': float(value_str)  
            }
            extracted_data.append(record)
        except ValueError:
            continue
            
    return extracted_data

def load_gdp_data(filePath):
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"'{filePath}' not found.")

    with open(filePath, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        allHeaders = reader.fieldnames
        # Isolate year columns (headers that are digits)
        years = list(filter(lambda h: h.isdigit(), allHeaders)) 

        if not years:
            raise ValueError("Could not find any Year columns in CSV.")

        all_records = []
        for row in reader:
            # Extend the main list with the results from this row
            all_records.extend(processRow(row, years))
            
        return all_records