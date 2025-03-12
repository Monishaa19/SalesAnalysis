import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from mlxtend.frequent_patterns import apriori, association_rules

# Load the dataset
file_path = 'sunaina/preprocessed_dataset.csv'
data = pd.read_csv(file_path)

# Prepare transactional data for Apriori Algorithm
transaction_data = data.groupby(['City', 'Category']).size().unstack(fill_value=0)
transaction_data = transaction_data.applymap(lambda x: 1 if x > 0 else 0)

# Top-selling categories by city
top_selling_categories = data.groupby(['City', 'Category'])['Sales'].sum().reset_index()
top_selling_categories = top_selling_categories.sort_values(by=['City', 'Sales'], ascending=[True, False])

# Get the top category for each city
top_category_by_city = top_selling_categories.groupby('City').first().reset_index()

# Print top-selling categories
print("\nTop-Selling Categories by City:\n")
for _, row in top_category_by_city.iterrows():
    print(f"{row['City']}: {row['Category']} (Sales: {row['Sales']})")

# Generate plot filename
plot_dir = 'static'
os.makedirs(plot_dir, exist_ok=True)

# Visualize top categories
fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(top_category_by_city['City'], top_category_by_city['Sales'], color='skyblue')
ax.set_xlabel('Total Sales')
ax.set_ylabel('Cities')
ax.set_title('Top-Selling Categories by City')

# Annotate each bar with the category name
for bar, category in zip(bars, top_category_by_city['Category']):
    ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height() / 2, category, va='center', fontsize=9)

# Save the plot
top_categories_plot_path = os.path.join(plot_dir, 'top_selling_categories_by_city.png')
plt.tight_layout()
plt.savefig(top_categories_plot_path)
plt.close()

# Step 4: Create JSON Output
json_output = {
    'plot': f'/{top_categories_plot_path}',
    'top_categories_by_city': top_category_by_city.to_dict(orient='records')
}

# Save the JSON output
json_file_path = 'top_selling_categories_by_city.json'
with open(json_file_path, 'w') as json_file:
    json.dump(json_output, json_file)

print(f"Analysis and plot saved to {json_file_path}")
