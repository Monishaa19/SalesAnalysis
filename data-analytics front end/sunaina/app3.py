import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# Load the dataset
data = pd.read_csv('sunaina/preprocessed_dataset.csv')

# Step 1: Group by City and Subcategory to Aggregate Metrics
city_subcategory = (
    data.groupby(['City', 'Sub Category'])
    .agg({'Sales': 'sum', 'Profit': 'sum', 'Order ID': 'count'})
    .rename(columns={'Order ID': 'Frequency'})
    .reset_index()
)

# Step 2: Identify Top Subcategories per City Based on Profit or Sales
top_subcategories = (
    city_subcategory.sort_values(['City', 'Profit'], ascending=[True, False])
    .groupby('City')
    .head(3)  # Select top 3 subcategories per city
)

# Print top subcategories for each city
print("Top Subcategories by Profit for Each City:\n", top_subcategories)

# Generate plot filename
plot_dir = 'static'
os.makedirs(plot_dir, exist_ok=True)

# Step 3: Create Graphical Representation (Top Subcategories by Profit)
top_subcategories_plot_path = os.path.join(plot_dir, 'top_subcategories_by_profit.png')
plt.figure(figsize=(15, 8))

# Plot each city's data as a grouped bar chart
sns.barplot(
    data=top_subcategories,
    x='City',
    y='Profit',
    hue='Sub Category',
    palette='viridis'
)

# Add labels and title
plt.title('Top Subcategories by Profit for Each City', fontsize=16)
plt.xlabel('City', fontsize=12)
plt.ylabel('Profit', fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.legend(title='Sub Category', bbox_to_anchor=(1.05, 1), loc='upper left')

# Save the plot
plt.tight_layout()
plt.savefig(top_subcategories_plot_path)
plt.close()

# Step 4: Create JSON Output
json_output = {
    'plot': f'/{top_subcategories_plot_path}',
    'city_subcategory': top_subcategories.to_dict(orient='records')
}

# Save the JSON output
json_file_path = 'top_subcategories_by_city.json'
with open(json_file_path, 'w') as json_file:
    json.dump(json_output, json_file)

print(f"Analysis and plot saved to {json_file_path}")
