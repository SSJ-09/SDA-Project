import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from datetime import datetime


class Dashboard:
    
    def __init__(self, config=None, output_folder='assets'):
        """
        Initialize dashboard
        
        Args:
            config: Configuration dictionary (from Partner A)
            output_folder: Folder for output files
        """
        self.config = config or {}
        self.output_folder = output_folder
        self.results = {}
        self.chart_files = []
        
        # Create output folder
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"Created output folder: {self.output_folder}/")
    
   # VISUALIZATION FUNCTIONS
   
    def create_pie_chart(self, data_dict, title, filename):
        print(f"  Creating pie chart: {filename}...")
        
        plt.figure(figsize=(10, 8))
        
        labels = list(data_dict.keys())
        values = list(data_dict.values())
        
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0']
        
        wedges, texts, autotexts = plt.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
            colors=colors[:len(labels)],
            explode=[0.05] * len(labels),
            shadow=True,
            startangle=90,
            textprops={'fontsize': 10, 'fontweight': 'bold'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.axis('equal')
        
        filepath = os.path.join(self.output_folder, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        self.chart_files.append(filepath)
        print(f" Saved: {filepath}")
        return filepath
    
    def create_line_graph(self, data_dict, title, xlabel, ylabel, filename):
        print(f"  Creating line graph: {filename}...")
        
        plt.figure(figsize=(12, 6))
        
        sorted_data = dict(sorted(data_dict.items()))
        x_values = list(sorted_data.keys())
        y_values = list(sorted_data.values())
        
        if max(y_values) > 1000000000:
            y_values = [v / 1e9 for v in y_values]
            ylabel = f"{ylabel} (Billions USD)"
        
        plt.plot(x_values, y_values,
                marker='o', linewidth=2.5, markersize=8,
                color='#2E86AB', markerfacecolor='#A23B72',
                markeredgewidth=2, markeredgecolor='white')
        
        for x, y in zip(x_values, y_values):
            plt.text(x, y, f'${y:.1f}B',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.xlabel(xlabel, fontsize=12, fontweight='bold')
        plt.ylabel(ylabel, fontsize=12, fontweight='bold')
        plt.grid(True, alpha=0.3, linestyle='--')
        
        filepath = os.path.join(self.output_folder, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        self.chart_files.append(filepath)
        print(f" Saved: {filepath}")
        return filepath
    
    def create_bar_chart(self, data_dict, title, xlabel, ylabel, filename):
        print(f"  Creating bar chart: {filename}...")
        
        plt.figure(figsize=(12, 6))
        
        sorted_data = dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True))
        labels = list(sorted_data.keys())
        values = list(sorted_data.values())
        
        if max(values) > 1000000000:
            values = [v / 1e9 for v in values]
            ylabel = f"{ylabel} (Billions USD)"
        
        import numpy as np
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(labels)))
        
        bars = plt.bar(labels, values, color=colors, edgecolor='black', linewidth=1.2)
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:.1f}B',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.xlabel(xlabel, fontsize=12, fontweight='bold')
        plt.ylabel(ylabel, fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()
        
        filepath = os.path.join(self.output_folder, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        self.chart_files.append(filepath)
        print(f"  Saved: {filepath}")
        return filepath
    
    # CONSOLE DISPLAY FUNCTIONS
    
    def display_header(self):
        print("\n")
        print("  GDP ANALYSIS DASHBOARD  ".center(80))
        print("\n")
        print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n")
    
    def display_configuration(self):
        print(" CONFIGURATION")
        print("-" * 80)
        
        filters = self.config.get('filters', {})
        operations = self.config.get('operations', {})
        
        print(f"  Region Filter:     {filters.get('region', 'All')}")
        print(f"  Year Filter:       {filters.get('year', 'All')}")
        print(f"  Country Filter:    {filters.get('country', 'All')}")
        print(f"  Operation Type:    {operations.get('region_operation', 'average')}")
        print("\n")
    
    def display_statistics(self):
        print(" STATISTICAL RESULTS")
        print("-" * 80)
        
        if 'region_stats' in self.results:
            print("\n  Region-wise Statistics:")
            for region, value in sorted(self.results['region_stats'].items(), 
                                       key=lambda x: x[1], reverse=True):
                print(f"    {region:20s}: ${value:,.2f}")
        
        if 'year_stats' in self.results:
            print("\n  Year-wise Statistics:")
            for year, value in sorted(self.results['year_stats'].items()):
                print(f"    {year:20d}: ${value:,.2f}")
        
        if 'country_stats' in self.results:
            print("\n  Country Statistics (Top 10):")
            sorted_countries = sorted(self.results['country_stats'].items(), 
                                    key=lambda x: x[1], reverse=True)[:10]
            for country, value in sorted_countries:
                print(f"    {country:20s}: ${value:,.2f}")
        
        print("\n")
    
    def display_visualizations(self):
        print(" VISUALIZATIONS GENERATED")
        print("-" * 80)
        
        if not self.chart_files:
            print("  No visualizations generated yet.")
        else:
            for i, chart in enumerate(self.chart_files, 1):
                print(f"  {i}. {chart}")
        
    
    def display_summary(self):
        print("SUMMARY")
        print("-" * 80)
        
        print(f"  Total Records:        {self.results.get('total_records', 0):,}")
        print(f"  Filtered Records:     {self.results.get('filtered_count', 0):,}")
        print(f"  Regions Analyzed:     {len(self.results.get('region_stats', {}))}")
        print(f"  Countries Analyzed:   {len(self.results.get('country_stats', {}))}")
        print(f"  Charts Created:       {len(self.chart_files)}")
        
        print(" " + "\n")
    
    def display_footer(self):
        print(" ")
        print(" Analysis Complete!".center(80))
    
    # MAIN RENDER FUNCTION
    
    def render(self, results):
      
        self.results = results
        
        self.display_header()
        self.display_configuration()
        self.display_statistics()
        self.display_visualizations()
        self.display_summary()
        self.display_footer()
    
    def set_results(self, results):
        self.results = results


# FUNCTION

def test_complete_dashboard():
    
    print("\n")
    print("  TESTING DASHBOARD MODULE  ")
    print(" " + "\n")
    
    # Mock configuration
    mock_config = {
        'filters': {
            'region': 'Asia',
            'year': 2022,
            'country': ''
        },
        'operations': {
            'region_operation': 'average',
            'country_operation': 'average'
        }
    }
    
    # Creating dashboard
    dashboard = Dashboard(config=mock_config, output_folder='test_dashboard_output')
    
    # Mocking data 
    region_data = {
        'Asia': 6306477100000,
        'Europe': 2933565950000,
        'North America': 8449515984786,
        'South America': 852279000000,
        'Africa': 389211533333,
        'Oceania': 851170400000
    }
    
    year_data = {
        2018: 3362102339831,
        2019: 3421799069210,
        2020: 3342422736842,
        2021: 3784344368421,
        2022: 3914471631579
    }
    
    country_data = {
        'United States': 22255573154358,
        'China': 15718946000000,
        'Japan': 4853987400000,
        'Germany': 4012773800000,
        'India': 2955770800000
    }
    
    # Creating Visualizations
    print("Creating visualizations\n")
    
    dashboard.create_pie_chart(
        region_data,
        'GDP Distribution by Region',
        'region_pie.png'
    )
    
    dashboard.create_line_graph(
        year_data,
        'GDP Trend Over Years',
        'Year',
        'Average GDP',
        'year_line.png'
    )
    
    dashboard.create_bar_chart(
        country_data,
        'Top Countries by GDP',
        'Country',
        'GDP',
        'country_bar.png'
    )
    
    # Mocking Results
    mock_results = {
        'total_records': 95,
        'filtered_count': 20,
        'region_stats': region_data,
        'year_stats': year_data,
        'country_stats': country_data
    }
    
    # Rendering Dashboard
    print()
    dashboard.render(mock_results)


if __name__ == "main":
    test_complete_dashboard()