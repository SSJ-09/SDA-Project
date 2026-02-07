
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

