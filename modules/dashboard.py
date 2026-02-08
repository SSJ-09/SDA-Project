import os
import numpy as np

import matplotlib
matplotlib.use('Agg') # prevents conflict with veiwer window 
import matplotlib.pyplot as plt


# application details based ui monlith class
class Dashboard:
    
    def __init__(self, output_folder='output_charts'):
        self.output_folder = output_folder
        self.chart_files = []
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def create_pie_chart(self, data_dict, title, filename, highlight_key=None):
        print(f"  Generating pie chart: {title}...")
        
        plt.figure(filename, figsize=(10, 8))
        
        if len(data_dict) > 8:
            sorted_items = sorted(data_dict.items(), key=lambda x: x[1], reverse=True)
            top_7 = sorted_items[:7]
            others_value = sum(item[1] for item in sorted_items[7:])
            labels = [item[0] for item in top_7] + ['Others']
            values = [item[1] for item in top_7] + [others_value]
        else:
            labels = list(data_dict.keys())
            values = list(data_dict.values())

        explode = []
        colors = []
        standard_colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0', '#ffb3e6', '#c4c4c4']
        
        for i, label in enumerate(labels):
            if highlight_key and label == highlight_key:
                explode.append(0.15)
                colors.append('#E74C3C')
            else:
                explode.append(0.05)
                colors.append(standard_colors[i % len(standard_colors)])

        wedges, texts, autotexts = plt.pie(
            values, labels=labels, autopct='%1.1f%%', 
            colors=colors, explode=explode, shadow=True, startangle=90,
            textprops={'fontsize': 9, 'fontweight': 'bold'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(8)
            autotext.set_fontweight('bold')
        
        plt.title(title, fontsize=15, fontweight='bold', pad=20)
        plt.axis('equal')
        
        save_path = os.path.join(self.output_folder, filename)
        plt.savefig(save_path)
        plt.close()
        self.chart_files.append(filename)
        return filename

    def create_bar_chart(self, data_dict, title, xlabel, ylabel, filename, highlight_key=None):
        print(f"  Generating bar chart: {title}...")
        
        plt.figure(filename, figsize=(12, 6))
        
        sorted_data = dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True))
        labels = list(sorted_data.keys())
        values = list(sorted_data.values())
        
        if values and max(values) > 1e9:
            values = [v / 1e9 for v in values]
            ylabel = f"{ylabel} (Billions USD)"
        
        bar_colors = []
        for label in labels:
            if highlight_key and label == highlight_key:
                bar_colors.append('#E74C3C')
            else:
                bar_colors.append('#2E86AB')
        
        if highlight_key is None:
             bar_colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(labels)))

        bars = plt.bar(labels, values, color=bar_colors, edgecolor='black', linewidth=1)
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}B', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.title(title, fontsize=15, fontweight='bold', pad=20)
        plt.xlabel(xlabel, fontsize=12, fontweight='bold')
        plt.ylabel(ylabel, fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()
        
        save_path = os.path.join(self.output_folder, filename)
        plt.savefig(save_path)
        plt.close()
        self.chart_files.append(filename)
        return filename

    def create_line_graph(self, data_dict, title, xlabel, ylabel, filename, highlight_key=None):
        print(f"  Generating line graph: {title}...")
        
        plt.figure(filename, figsize=(12, 6))
        
        sorted_data = dict(sorted(data_dict.items()))
        x_values = list(sorted_data.keys())
        y_values = list(sorted_data.values())
        
        if y_values and max(y_values) > 1e9:
            y_values = [v / 1e9 for v in y_values]
            ylabel = f"{ylabel} (Billions USD)"
        
        plt.plot(x_values, y_values, linewidth=3, color='#2E86AB', zorder=1)
        plt.scatter(x_values, y_values, color='#2E86AB', s=30, zorder=2)
        
        
        if highlight_key:
            
            str_key = str(highlight_key)
            for x, y in zip(x_values, y_values):
                if str(x) == str_key:
                    plt.scatter([x], [y], color='#E74C3C', s=150, zorder=3, edgecolors='white', linewidth=2)
                    plt.text(x, y + (max(y_values)*0.05), f"{x}", 
                             ha='center', fontsize=10, fontweight='bold', color='#E74C3C')

        
        max_val = max(y_values)
        max_year = x_values[y_values.index(max_val)]
        plt.text(max_year, max_val + (max_val*0.02), f'Peak: {max_val:.1f}B',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='black')

        plt.title(title, fontsize=15, fontweight='bold', pad=20)
        plt.xlabel(xlabel, fontsize=12, fontweight='bold')
        plt.ylabel(ylabel, fontsize=12, fontweight='bold')
        plt.xticks(x_values[::5], rotation=45)
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.tight_layout()
        
        save_path = os.path.join(self.output_folder, filename)
        plt.savefig(save_path)
        plt.close()
        self.chart_files.append(filename)
        return filename

    def create_histogram(self, values, title, xlabel, ylabel, filename, highlight_val=None):
        print(f"  Generating histogram: {title}...")
        
        plt.figure(filename, figsize=(12, 6))
        
        if values and max(values) > 1e9:
            values = [v / 1e9 for v in values]
            if highlight_val: highlight_val = highlight_val / 1e9 
            xlabel = f"{xlabel} (Billions USD)"
            
        plt.hist(values, bins=15, color='#66b3ff', edgecolor='black', alpha=0.7)
        
        
        if highlight_val is not None:
            plt.axvline(highlight_val, color='#E74C3C', linestyle='dashed', linewidth=2)
            plt.text(highlight_val*1.05, plt.ylim()[1]*0.8, 'You Are Here', 
                     color='#E74C3C', fontweight='bold', rotation=90)
        
        plt.title(title, fontsize=15, fontweight='bold', pad=20)
        plt.xlabel(xlabel, fontsize=12, fontweight='bold')
        plt.ylabel(ylabel, fontsize=12, fontweight='bold')
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        save_path = os.path.join(self.output_folder, filename)
        plt.savefig(save_path)
        plt.close()
        self.chart_files.append(filename)
        return filename