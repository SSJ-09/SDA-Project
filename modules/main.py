import dataLoader
import dataProcessor
from dashboard import Dashboard
import dashboardViewer  

def main():
    try:
       
        config = dataLoader.load_config("config.json")
        rawData = dataLoader.load_gdp_data("Copy of gdp_with_continent_filled.csv")
       
        
        
        allRegions = set(row['Region'] for row in rawData)
        allYears = set(row['Year'] for row in rawData)
        ops = {'sum', 'avg', 'average'}

        
        regionValid = config.get('region') in allRegions
        yearValid = config.get('year') in allYears
        opValid = config.get('operation', '').lower() in ops

       
        if not (regionValid and yearValid and opValid):
            print("\nInvalid Configuration.Switching to default : Asia,2018,sum.")
            config['region'] = 'Asia'
            config['year'] = 2015
            config['operation'] = 'sum'
        
        results = dataProcessor.process_data(rawData, config)

        
        dash = Dashboard(output_folder="output_charts")
        
        dash.create_bar_chart(
            results['graph_1_bar'], 
            f"Global Comparison ({config['year']})", 
            "Region", "GDP", "1_global_comparison_bar.png",
            highlight_key=config['region']  
        )

        
        dash.create_pie_chart(
            results['graph_2_pie'], 
            f"Global Share ({config['year']})", "2_global_comparison_pie.png",
            highlight_key=config['region'] 
        )

        
        dash.create_line_graph(
            results['graph_3_line'], 
            f"Historical Trend: {config['region']}", 
            "Year", "GDP", "3_historical_trend_line.png",
            highlight_key=config['year']    
        )

        
        current_val = results['graph_3_line'].get(config['year'])
        dash.create_histogram(
            results['graph_4_hist'], 
            f"GDP Distribution: {config['region']}", 
            "GDP Range", "Freq", "4_historical_dist_hist.png",
            highlight_val=current_val      
        )

        app = dashboardViewer.DashboardViewer("output_charts", results)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()