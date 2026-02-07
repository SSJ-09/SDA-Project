"""
Final Integration
Loads GDP data, applies configuration filters,
computes statistics, and generates a visualization dashboard
"""

import dataLoader
from modules.dashboard import Dashboard

print("\n" + "="*80)
print("  FINAL INTEGRATION - COMPLETE GDP ANALYSIS SYSTEM")
print("="*80 + "\n")

# Load configuration file and GDP dataset

print("STEP 1: Loading configuration (Partner A)...")
try:
    config = dataLoader.load_config("config.json")
    print(" Configuration loaded successfully")
    print(f"  Filters: {config.get('filters', {})}")
    print(f"  Operations: {config.get('operations', {})}\n")
except FileNotFoundError as e:
    print(f" Error: {e}")
    exit(1)

print("STEP 2: Loading GDP data (Partner A)...")
try:
    csv_file = "Copy of gdp_with_continent_filled.csv"
    raw_data = dataLoader.load_gdp_data(csv_file)
    print(f" Successfully loaded {len(raw_data)} records from CSV")
    print(f"  Sample record: {raw_data[0] if raw_data else 'No data'}\n")
except FileNotFoundError as e:
    print(f" Error: {e}")
    exit(1)

# Filter GDP data based on configuration values

print("STEP 3: Processing data using functional programming...")

filters = config.get('filters', {})
filter_region = filters.get('region', '')
filter_year = filters.get('year', 0)
filter_country = filters.get('country', '')

filtered_data = raw_data

if filter_region:
    filtered_data = list(filter(lambda x: x['Region'] == filter_region, filtered_data))
    print(f" Filtered by region '{filter_region}': {len(filtered_data)} records")

if filter_year:
    filtered_data = list(filter(lambda x: x['Year'] == filter_year, filtered_data))
    print(f" Filtered by year {filter_year}: {len(filtered_data)} records")

if filter_country:
    filtered_data = list(filter(lambda x: x['Country Name'] == filter_country, filtered_data))
    print(f" Filtered by country '{filter_country}': {len(filtered_data)} records")

print(f" Total filtered records: {len(filtered_data)}\n")

# Compute GDP statistics using functional programming

print("STEP 4: Computing statistics using functional programming...")

operation_type = config.get('operations', {}).get('region_operation', 'average')

def compute_average(values):
    """Returns the average of a numeric list"""
    if not values:
        return 0.0
    from functools import reduce
    total = reduce(lambda x, y: x + y, values, 0)
    return total / len(values)

def compute_sum(values):
    """Returns the sum of a numeric list"""
    if not values:
        return 0.0
    from functools import reduce
    return reduce(lambda x, y: x + y, values, 0)

def group_by_field(data, field):
    """Groups records by a given dictionary key"""
    unique_values = set(map(lambda x: x[field], data))
    return {
        value: list(filter(lambda x: x[field] == value, data))
        for value in unique_values
    }

regions_grouped = group_by_field(filtered_data, 'Region')
region_stats = {}

for region, records in regions_grouped.items():
    values = list(map(lambda x: x['Value'], records))
    if operation_type == 'sum':
        region_stats[region] = compute_sum(values)
    else:
        region_stats[region] = compute_average(values)

print(f" Computed {operation_type} for {len(region_stats)} regions")

years_grouped = group_by_field(filtered_data, 'Year')
year_stats = {}

for year, records in years_grouped.items():
    values = list(map(lambda x: x['Value'], records))
    year_stats[year] = compute_average(values)

print(f" Computed statistics for {len(year_stats)} years")

countries_grouped = group_by_field(filtered_data, 'Country Name')
country_stats = {}

for country, records in countries_grouped.items():
    values = list(map(lambda x: x['Value'], records))
    country_stats[country] = compute_average(values)

print(f" Computed statistics for {len(country_stats)} countries\n")

# Generate dashboard and visual charts

print("STEP 5: Creating dashboard and visualizations (Partner B - YOUR MODULE!)...\n")

dashboard = Dashboard(config=config, output_folder='final_output')

print("Generating charts with REAL GDP data...\n")

if region_stats:
    dashboard.create_pie_chart(
        region_stats,
        f'GDP Distribution by Region ({operation_type.capitalize()})',
        'region_gdp_pie.png'
    )

if year_stats:
    dashboard.create_line_graph(
        year_stats,
        'GDP Trend Over Years (Average)',
        'Year',
        'GDP',
        'year_gdp_trend.png'
    )

if country_stats:
    top_10_countries = dict(sorted(
        country_stats.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10])

    dashboard.create_bar_chart(
        top_10_countries,
        'Top 10 Countries by GDP (Average)',
        'Country',
        'GDP',
        'top_countries_bar.png'
    )

results = {
    'total_records': len(raw_data),
    'filtered_count': len(filtered_data),
    'region_stats': region_stats,
    'year_stats': year_stats,
    'country_stats': country_stats
}

dashboard.render(results)

print("-"*80)
print("COMPLETE INTEGRATION SUCCESSFUL!")
print("-"*80)
print()
print("What happened:")
print("  1. Partner A: Loaded config.json")
print("  2. Partner A: Loaded GDP data from CSV")
print("  3. Partner A: Filtered data based on config")
print("  4. Partner A: Computed statistics using functional programming")
print("  5. Partner B: Created 3 professional visualizations")
print("  6. Partner B: Displayed complete dashboard")
print()
print("Output files saved to: final_output/")
print("  - region_gdp_pie.png")
print("  - year_gdp_trend.png")
print("  - top_countries_bar.png")
print("-"*80 + "\n")
