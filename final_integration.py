import dataLoader
from dashboard import Dashboard

def calculate_average_stats(raw_data):
    """
    Calculates Averages (AVG) instead of SUMs.
    Returns:
      1. region_avg_2020: {Region: AvgGDP} for 2020
      2. year_avg: {Year: AvgGDP} for all years
      3. countries_2020: {Country: GDP} for 2020 (for contribution chart)
    """
    # 1. Region Average in 2020
    region_sums_2020 = {}
    region_counts_2020 = {}
    
    # 2. Year Average (All Regions/Countries combined)
    year_sums = {}
    year_counts = {}
    
    # 3. Country Data for 2020
    countries_2020 = {}

    for row in raw_data:
        region = row['Region']
        year = row['Year']
        val = row['Value']
        country = row['Country Name']

        # --- LOGIC 1: Average GDP per Year (Trend) ---
        if year not in year_sums:
            year_sums[year] = 0
            year_counts[year] = 0
        year_sums[year] += val
        year_counts[year] += 1

        # --- LOGIC 2: Average GDP per Region (Only for 2020) ---
        if year == 2020:
            if region not in region_sums_2020:
                region_sums_2020[region] = 0
                region_counts_2020[region] = 0
            region_sums_2020[region] += val
            region_counts_2020[region] += 1
            
            # Store country data for the contribution chart
            countries_2020[country] = val

    # Final Calculation: Divide Sum by Count to get Average
    region_avg_2020 = {r: region_sums_2020[r]/region_counts_2020[r] for r in region_sums_2020}
    year_avg = {y: year_sums[y]/year_counts[y] for y in year_sums}
    
    return region_avg_2020, year_avg, countries_2020

def main():
    print("\n" + "="*60)
    print("      FINAL GDP ANALYSIS (AVERAGE BASED)")
    print("="*60 + "\n")

    # 1. Load Data
    try:
        csv_file = "Copy of gdp_with_continent_filled.csv"
        raw_data = dataLoader.load_gdp_data(csv_file) 
        print(f" [Success] Loaded {len(raw_data)} records from {csv_file}")
    except Exception as e:
        print(f" [Error] Could not load data: {e}")
        return

    # 2. Process Data (Calculate Averages)
    print(" [Processing] Calculating Region and Year Averages...")
    region_avg_2020, year_avg, countries_2020 = calculate_average_stats(raw_data)

    # 3. Initialize Dashboard
    # NOTE: Output folder will be 'assets'
    dash = Dashboard(output_folder='assets')

    # --- GENERATING THE 5 REQUIRED GRAPHS ---

    print("\n [Visualization] Generating Graphs...")

    # Set 1: Region Avg in 2020 vs Others (Bar & Pie)
    dash.create_bar_chart(
        region_avg_2020,
        "Region Average GDP in 2020",
        "Region",
        "Average GDP",
        "1_region_avg_2020_bar.png"
    )
    
    dash.create_pie_chart(
        region_avg_2020,
        "Region Average GDP Share (2020)",
        "2_region_avg_2020_pie.png"
    )

    # Set 2: Region/Global Avg during other years (Line & Histogram)
    dash.create_line_graph(
        year_avg,
        "Average Global GDP Trend (2018-2022)",
        "Year",
        "Average GDP",
        "3_year_avg_trend_line.png"
    )

    dash.create_histogram(
        list(year_avg.values()),
        "Distribution of Yearly Average GDP",
        "GDP Value",
        "Frequency",
        "4_year_avg_hist.png",
        bins=5
    )

    # Set 3: Countries Contribution (Pie)
    # Get top 8 countries to make the chart readable
    top_countries = dict(sorted(countries_2020.items(), key=lambda x: x[1], reverse=True)[:8])
    dash.create_pie_chart(
        top_countries,
        "Top Countries Contribution (2020)",
        "5_countries_2020_pie.png"
    )

    # 4. Show All
    dash.show_all()
    print("\n [Done] Analysis Complete. Graphs saved to 'assets/' folder.")

if __name__ == "__main__":
    main()