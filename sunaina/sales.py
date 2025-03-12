# Sales Analysis for Each Region

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the preprocessed dataset
file_path = 'preprocessed_dataset.csv'
data = pd.read_csv(file_path)

# Group the data by 'Region' and calculate sales metrics
region_sales = data.groupby('Region').agg(
    total_sales=('Sales', 'sum'),
    average_sales=('Sales', 'mean'),
    num_orders=('Sales', 'count')
).reset_index()

# Print the analysis
print("Sales analysis by region:\n", region_sales)

# Visualization: Total Sales by Region
plt.figure(figsize=(8, 6))
sns.barplot(x='Region', y='total_sales', data=region_sales, palette='viridis')
plt.title('Total Sales by Region')
plt.xlabel('Region')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Visualization: Average Sales by Region
plt.figure(figsize=(8, 6))
sns.barplot(x='Region', y='average_sales', data=region_sales, palette='coolwarm')
plt.title('Average Sales by Region')
plt.xlabel('Region')
plt.ylabel('Average Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Visualization: Number of Orders by Region
plt.figure(figsize=(8, 6))
sns.barplot(x='Region', y='num_orders', data=region_sales, palette='magma')
plt.title('Number of Orders by Region')
plt.xlabel('Region')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Optional: Save the results to a CSV file
sales_analysis_file_path = 'sales_analysis_by_region.csv'
region_sales.to_csv(sales_analysis_file_path, index=False)
print(f"Sales analysis saved to {sales_analysis_file_path}.")
    