import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import os

# Load the preprocessed dataset
file_path = 'sunaina/preprocessed_dataset.csv'
data = pd.read_csv(file_path)

# Group the data by 'Region' and calculate sales metrics
region_sales = data.groupby('Region').agg(
    total_sales=('Sales', 'sum'),
    average_sales=('Sales', 'mean'),
    num_orders=('Sales', 'count')
).reset_index()

# Print the analysis
print("Sales analysis by region:\n", region_sales)

# Generate plot filenames
plot_dir = 'static'
os.makedirs(plot_dir, exist_ok=True)

# Visualization: Total Sales by Region
total_sales_plot_path = os.path.join(plot_dir, 'total_sales_by_region.png')
plt.figure(figsize=(8, 6))
sns.barplot(x='Region', y='total_sales', data=region_sales, palette='viridis')
plt.title('Total Sales by Region')
plt.xlabel('Region')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(total_sales_plot_path)
plt.close()

# Visualization: Average Sales by Region
average_sales_plot_path = os.path.join(plot_dir, 'average_sales_by_region.png')
plt.figure(figsize=(8, 6))
sns.barplot(x='Region', y='average_sales', data=region_sales, palette='coolwarm')
plt.title('Average Sales by Region')
plt.xlabel('Region')
plt.ylabel('Average Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(average_sales_plot_path)
plt.close()

# Visualization: Number of Orders by Region
num_orders_plot_path = os.path.join(plot_dir, 'num_orders_by_region.png')
plt.figure(figsize=(8, 6))
sns.barplot(x='Region', y='num_orders', data=region_sales, palette='magma')
plt.title('Number of Orders by Region')
plt.xlabel('Region')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(num_orders_plot_path)
plt.close()

# Step 2: Create JSON output
json_output = {
    'plots': {
        'total_sales': f'/{total_sales_plot_path}',
        'average_sales': f'/{average_sales_plot_path}',
        'num_orders': f'/{num_orders_plot_path}'
    },
    'region_sales': region_sales.to_dict(orient='records')
}

# Save the JSON output
json_file_path = 'region_sales_analysis.json'
with open(json_file_path, 'w') as json_file:
    json.dump(json_output, json_file)

print(f"Sales analysis and plots saved to {json_file_path}")
