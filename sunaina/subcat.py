import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('preprocessed_dataset.csv')

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

# Step 3: Create Graphical Representation
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

# Show plot
plt.tight_layout()
plt.show()
