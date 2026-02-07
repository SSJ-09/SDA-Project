
import matplotlib.pyplot as plt

print("="*60)
print("  TESTING VISUALIZATION  ")
print("="*60)
print()

# 1: CREATE A PIE CHART

# Estimate data - GDP by region (in billions)
regions = ['Asia', 'Europe', 'North America', 'South America', 'Africa', 'Oceania']
gdp_values = [6300, 2900, 8400, 850, 390, 850]

# Figuring
plt.figure(figsize=(10, 8))

# Color Slicing
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0']

# Create pie chart
plt.pie(gdp_values, 
        labels=regions, 
        autopct='%1.1f%%',        # Show percentages
        colors=colors,
        explode=[0.05]*6,         # Separation Between Parts
        shadow=True,
        startangle=90)

plt.title('GDP Distribution by Region (Estimating Data)', fontsize=16, fontweight='bold')
plt.axis('equal')

# Saving Chart
plt.savefig('test_pie_chart.png', dpi=100)
print("Pie chart saved as: test_pie_chart.png")

plt.show(block=False)  # Display Chart
plt.pause(6)  # Timer in Seconds


# 2: CREATE A LINE GRAPH

# Estimate data - GDP over years (in billions)
years = [2018, 2019, 2020, 2021, 2022]
avg_gdp = [3362, 3421, 3342, 3784, 3914]

# Figuring
plt.figure(figsize=(10, 6))

# Making line graph
plt.plot(years, avg_gdp, 
         marker='o',              
         linewidth=2.5,           
         markersize=8,           
         color='#2E86AB',        
         markerfacecolor='#A23B72',
         markeredgewidth=2,
         markeredgecolor='white')

# Add value labeling
for year, gdp in zip(years, avg_gdp):
    plt.text(year, gdp + 50, f'${gdp}B', ha='center', fontsize=10, fontweight='bold')

# Formatting
plt.title('Average Global GDP Trend (Estimate Data)', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=12, fontweight='bold')
plt.ylabel('Average GDP (Billions USD)', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3, linestyle='--')

# Saving
plt.savefig('test_line_graph.png', dpi=100)
print("Line graph saved as: test_line_graph.png")

plt.show(block=False)  # Display Chart
plt.pause(6)  # Timer in Seconds

print()
print("PIE and LINE Chart Created")