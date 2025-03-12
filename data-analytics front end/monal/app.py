import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

# Specify the local CSV file path
file_path = "monisha/sorted_csv_file.csv"

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Data Cleaning
df['Order Date'] = pd.to_datetime(df['Order Date'])  # Convert Order Date to datetime

# Check for missing values
print("Missing Values:\n", df.isnull().sum())

# Drop duplicates if any
df.drop_duplicates(inplace=True)

# Sales Analysis
total_sales = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False)
avg_sales = df.groupby('Customer Name')['Sales'].mean()
sales_trend = df.groupby(['Customer Name', df['Order Date'].dt.year])['Sales'].sum().unstack()
total_profit = df.groupby('Customer Name')['Profit'].sum().sort_values(ascending=False)
df['Profit Margin'] = (df['Profit'] / df['Sales']) * 100
profit_margin = df.groupby('Customer Name')['Profit Margin'].mean()
avg_discount = df.groupby('Customer Name')['Discount'].mean()
order_frequency = df['Customer Name'].value_counts()

# Days Between Orders
df = df.sort_values(by=['Customer Name', 'Order Date'])
df['Days Between Orders'] = df.groupby('Customer Name')['Order Date'].diff().dt.days
avg_days_between_orders = df.groupby('Customer Name')['Days Between Orders'].mean()

# City Preference and Cross-Selling
city_preference = df.groupby('City')['Sales'].sum().sort_values(ascending=False)
cross_sell = df.groupby(['Customer Name', 'Category', 'Sub Category']).size()

# High Margin Products and Retention
high_margin_products = df[df['Profit'] > df['Profit'].mean()]
retention = df.groupby('Customer Name')['Order Date'].nunique()
loyal_customers = retention[retention > 1]  # Example threshold for loyalty

# Rankings
rank_sales = df.groupby('Customer Name')['Sales'].sum().rank(ascending=False)
rank_profit = df.groupby('Customer Name')['Profit'].sum().rank(ascending=False)
sales_rank_by_category = df.groupby(['Category', 'Customer Name'])['Sales'].sum().groupby(level=0, group_keys=False).rank(ascending=False)

# Inactive Customers
latest_date = df['Order Date'].max()
df['Days Since Last Order'] = (latest_date - df['Order Date']).dt.days
inactive_customers = df[df['Days Since Last Order'] > 180]  # Example threshold

# High-Value Customers and Frequent Buyers
high_value = total_sales[total_sales > 1000]  # Example threshold
frequent_buyers = df['Customer Name'].value_counts()

# Consolidating Results
results = {
    'Total Sales': total_sales,
    'Average Sales': avg_sales,
    'Sales Growth': sales_trend,
    'Total Profit': total_profit,
    'Profit Margin': profit_margin,
    'Average Discount': avg_discount,
    'High Value Customers': high_value,
    'Frequent Buyers': frequent_buyers,
    'Number of Orders': order_frequency,
    'Avg Days Between Orders': avg_days_between_orders,
    'City Preference': city_preference,
    'Cross Selling': cross_sell,
    'Upselling Potential': high_margin_products,
    'Customer Retention': retention,
    'Loyal Customers': loyal_customers,
    'Rank by Sales': rank_sales,
    'Rank by Profit': rank_profit,
    'Sales Rank by Category': sales_rank_by_category,
    'Inactive Customers': inactive_customers
}

# Save all results to an Excel file
# with pd.ExcelWriter('Customer_Analysis_Results.xlsx', engine='openpyxl') as writer:
#     for sheet_name, data in results.items():
#         if isinstance(data, pd.Series):
#             data = data.to_frame()
#         data.to_excel(writer, sheet_name=sheet_name[:31])  # Sheet names max length is 31 characters

# Ensure seaborn style
sns.set(style="whitegrid")

# Total Sales - Bar Chart
plt.figure(figsize=(12, 6))
sns.barplot(x=total_sales.index, y=total_sales.values, palette="Blues_d")
plt.title("Total Sales by Customer", fontsize=16)
plt.xlabel("Customer", fontsize=12)
plt.ylabel("Total Sales", fontsize=12)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Save all results to a JSON file
results_json = {key: data.to_dict() if isinstance(data, (pd.Series, pd.DataFrame)) else data for key, data in results.items()}
with open('customer_analysis_results.json', 'w') as f:
    json.dump(results_json, f, indent=4)

print("Analysis completed. Results saved to 'Customer_Analysis_Results.xlsx' and 'customer_analysis_results.json'.")
