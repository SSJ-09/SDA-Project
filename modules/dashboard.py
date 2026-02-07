import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import os


class Dashboard:
    
    def __init__(self, output_folder='assets'):
        
        self.output_folder = output_folder
        
        # Create output folder if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"✓ Created output folder: {self.output_folder}/")
        else:
            print(f"✓ Using output folder: {self.output_folder}/")
    
    
    def create_pie_chart(self, data_dict, title, filename):
       
        print(f"  Creating pie chart: {filename}...")
        
        # Figure
        plt.figure(figsize=(10, 8))
        
        labels = list(data_dict.keys())
        values = list(data_dict.values())
        
        # Coloring
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0']
        
        # Creating Pie chart
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
        
        # Make percentage text white and bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.axis('equal')
        
        # Save
        filepath = os.path.join(self.output_folder, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f" Saved: {filepath}")
        return filepath
    
    
    def create_line_graph(self, data_dict, title, xlabel, ylabel, filename):
       
        print(f"  Creating line graph: {filename}...")
        
        # Figuring
        plt.figure(figsize=(12, 6))
        
        # Sorting
        sorted_data = dict(sorted(data_dict.items()))
        
        x_values = list(sorted_data.keys())
        y_values = list(sorted_data.values())
        
        # Conversion
        if max(y_values) > 1000000000:
            y_values = [v / 1e9 for v in y_values]
            ylabel = f"{ylabel} (Billions USD)"
        
        # Creating line graph
        plt.plot(x_values, y_values,
                marker='o',
                linewidth=2.5,
                markersize=8,
                color='#2E86AB',
                markerfacecolor='#A23B72',
                markeredgewidth=2,
                markeredgecolor='white')
        
        # Add value labelING
        for x, y in zip(x_values, y_values):
            plt.text(x, y, f'${y:.1f}B',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Formatting
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.xlabel(xlabel, fontsize=12, fontweight='bold')
        plt.ylabel(ylabel, fontsize=12, fontweight='bold')
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Save
        filepath = os.path.join(self.output_folder, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f" Saved: {filepath}")
        return filepath
    
    
    def create_bar_chart(self, data_dict, title, xlabel, ylabel, filename):
       
        print(f"  Creating bar chart: {filename}...")
        
        # Figuring
        plt.figure(figsize=(12, 6))
        
        # Sorting (descending)
        sorted_data = dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True))
        
        labels = list(sorted_data.keys())
        values = list(sorted_data.values())
        
        # Conversion
        if max(values) > 1000000000:
            values = [v / 1e9 for v in values]
            ylabel = f"{ylabel} (Billions USD)"
        
        # Coloring
        import numpy as np
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(labels)))
        
        # Creating bar chart
        bars = plt.bar(labels, values, color=colors, edgecolor='black', linewidth=1.2)
        
        # Add value labeling on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:.1f}B',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Formatting
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.xlabel(xlabel, fontsize=12, fontweight='bold')
        plt.ylabel(ylabel, fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()
        
        # Saving
        filepath = os.path.join(self.output_folder, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"Saved: {filepath}")
        return filepath
    
    
    def display_summary(self, summary_dict):
        
        """
        Display statistical summary in console
        
        """
        
        print("\n")
        print("DASHBOARD SUMMARY")
        print("\n")
        
        for key, value in summary_dict.items():
            if isinstance(value, dict):
                print(f"\n{key}:")
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, float):
                        print(f"  {sub_key:20s}: ${sub_value:,.2f}")
                    else:
                        print(f"  {sub_key:20s}: {sub_value}")
            elif isinstance(value, float):
                print(f"{key:25s}: ${value:,.2f}")
            else:
                print(f"{key:25s}: {value}")
        
        print("\n")

def test_dashboard():

    print("  TESTING DASHBOARD MODULE")
  
    
    # Creating Dashboard
    dashboard = Dashboard(output_folder='test_output')
    
    # Estimated data
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
        'India': 2955770800000,
        'United Kingdom': 2929536400000,
        'France': 2772831200000,
        'Brazil': 1747227000000,
        'Canada': 1844270400000,
        'Italy': 2019122400000
    }
    
    print("Creating Visualizations\n")
    
    # Create charts
    dashboard.create_pie_chart(
        region_data,
        'GDP Distribution by Region',
        'region_pie_chart.png'
    )
    
    dashboard.create_line_graph(
        year_data,
        'GDP Trend Over Years',
        'Year',
        'Average GDP',
        'year_line_chart.png'
    )
    
    dashboard.create_bar_chart(
        country_data,
        'Top 10 Countries by GDP',
        'Country',
        'GDP',
        'country_bar_chart.png'
    )
    
    # Display summary
    summary = {
        'Total Regions': len(region_data),
        'Years Analyzed': f"{min(year_data.keys())}-{max(year_data.keys())}",
        'Countries Shown': len(country_data),
        'Charts Generated': 3,
        'Output Folder': 'test_output/'
    }
    
    dashboard.display_summary(summary)

if __name__ == "__main__":
    test_dashboard()