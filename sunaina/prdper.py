import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('preprocessed_dataset.csv')

# Step 1: User Input for Sub-Category
selected_subcategory = input("Enter the Sub-Category to analyze : ").strip()

# Step 2: Filter Dataset for Selected Sub-Category
filtered_data = data[data['Sub Category'] == selected_subcategory]

# Step 3: Group by City to Aggregate Metrics
city_performance = (
    filtered_data.groupby('City')
    .agg({'Sales': 'sum', 'Profit': 'sum', 'Order ID': 'count'})
    .rename(columns={'Order ID': 'Frequency'})
    .reset_index()
)

# Step 4: Sort Data by Profit
city_performance = city_performance.sort_values(by='Profit', ascending=False)

# Step 5: Create a Graphical Representation
plt.figure(figsize=(15, 8))

# Plot city performance
sns.barplot(
    data=city_performance,
    x='City',
    y='Profit',
    palette='viridis'
)

# Add labels and title
plt.title(f'City-Wise Performance for Sub Category: {selected_subcategory}', fontsize=16)
plt.xlabel('City', fontsize=12)
plt.ylabel('Profit', fontsize=12)
plt.xticks(rotation=45, fontsize=10)

# Show the plot
plt.tight_layout()
plt.show()
