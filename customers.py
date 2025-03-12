!pip install pandas matplotlib seaborn
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import files  #add file
uploaded=files.upload()
df=pd.read_excel('dataset2.xlsx')
#data cleaning
# Convert Order Date to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Check for missing values
print(df.isnull().sum())

# Drop duplicates if any
df.drop_duplicates(inplace=True)
#sales
total_sales = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False)
print(total_sales)
avg_sales = df.groupby('Customer Name')['Sales'].mean()
print(avg_sales)
sales_trend = df.groupby(['Customer Name', df['Order Date'].dt.year])['Sales'].sum().unstack()
print(sales_trend)
total_profit = df.groupby('Customer Name')['Profit'].sum().sort_values(ascending=False)
print(total_profit)
df['Profit Margin'] = (df['Profit'] / df['Sales']) * 100
profit_margin = df.groupby('Customer Name')['Profit Margin'].mean()
print(profit_margin)
avg_discount = df.groupby('Customer Name')['Discount'].mean()
print(avg_discount)
order_frequency = df['Customer Name'].value_counts()
print(order_frequency)
df = df.sort_values(by=['Customer Name', 'Order Date'])
df['Days Between Orders'] = df.groupby('Customer Name')['Order Date'].diff().dt.days
avg_days_between_orders = df.groupby('Customer Name')['Days Between Orders'].mean()
print(avg_days_between_orders)
city_preference = df.groupby('City')['Sales'].sum().sort_values(ascending=False)
print(city_preference)
cross_sell = df.groupby(['Customer Name', 'Category', 'Sub Category']).size()
print(cross_sell)
high_margin_products = df[df['Profit'] > df['Profit'].mean()]
print(high_margin_products.groupby('Customer Name')['Sub Category'].unique())
retention = df.groupby('Customer Name')['Order Date'].nunique()
print(retention)
loyal_customers = retention[retention > 1]  # Example threshold
print(loyal_customers)
rank_sales = df.groupby('Customer Name')['Sales'].sum().rank(ascending=False)
rank_profit = df.groupby('Customer Name')['Profit'].sum().rank(ascending=False)
print(rank_sales, rank_profit)
sales_rank_by_category = df.groupby(['Category', 'Customer Name'])['Sales'].sum().groupby(level=0, group_keys=False).rank(ascending=False)
print(sales_rank_by_category)
latest_date = df['Order Date'].max()
df['Days Since Last Order'] = (latest_date - df['Order Date']).dt.days
inactive_customers = df[df['Days Since Last Order'] > 180]  # Example threshold
print(inactive_customers)

high_value = total_sales[total_sales > 1000]  # Example threshold
print(high_value)
frequent_buyers = df['Customer Name'].value_counts()
print(frequent_buyers)


# Assuming the analyses have been performed and the results are stored in the following variables:
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
   

# Export all results to an Excel file
with pd.ExcelWriter('Customer_Analysis_Results.xlsx', engine='openpyxl') as writer:
    for sheet_name, data in results.items():
        # Convert Series to DataFrame for consistency
        if isinstance(data, pd.Series):
            data = data.to_frame()
        
        # Export each analysis to its own sheet
        data.to_excel(writer, sheet_name=sheet_name[:31])  # Sheet names max length is 31 characters

# Download the Excel file
files.download('Customer_Analysis_Results.xlsx')

# Ensure seaborn style
sns.set(style="whitegrid")

# 1. Total Sales - Bar Chart
plt.figure(figsize=(12, 6))
sns.barplot(x=total_sales.index, y=total_sales.values, palette="Blues_d")
plt.title("Total Sales by Customer", fontsize=16)
plt.xlabel("Customer", fontsize=12)
plt.ylabel("Total Sales", fontsize=12)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 2. Avg Sales - Bar Chart
plt.figure(figsize=(12, 6))
sns.barplot(x=avg_sales.index, y=avg_sales.values, palette="Oranges_d")
plt.title("Average Sales by Customer", fontsize=16)
plt.xlabel("Customer", fontsize=12)
plt.ylabel("Average Sales", fontsize=12)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 3. Sales Trend - Line Chart
plt.figure(figsize=(12, 6))
for customer in sales_trend.columns[:5]:  # Visualize top 5 customers
    plt.plot(sales_trend.index, sales_trend[customer], label=customer)
plt.title("Sales Trend Over Time", fontsize=16)
plt.xlabel("Order Date", fontsize=12)
plt.ylabel("Sales", fontsize=12)
plt.legend(title="Customer", fontsize=10)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 4. Total Profit - Bar Chart
plt.figure(figsize=(12, 6))
sns.barplot(x=total_profit.index, y=total_profit.values, palette="Greens_d")
plt.title("Total Profit by Customer", fontsize=16)
plt.xlabel("Customer", fontsize=12)
plt.ylabel("Total Profit", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Profit Margin - Bar Chart
plt.figure(figsize=(12, 6))
sns.barplot(x=profit_margin.index, y=profit_margin.values, palette="Purples_d")
plt.title("Profit Margin by Customer", fontsize=16)
plt.xlabel("Customer", fontsize=12)
plt.ylabel("Profit Margin (%)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# # 6. High-Value Customers - Pie Chart
# plt.figure(figsize=(8, 8))
# plt.pie(high_value.values, labels=high_value.index, autopct="%1.1f%%", colors=sns.color_palette("pastel"))
# plt.title("High-Value Customers Share", fontsize=16)
# plt.tight_layout()
# plt.show()

# 7. Frequent Buyers - Horizontal Bar Chart
plt.figure(figsize=(12, 10))  # Increased height to reduce overlap
sns.barplot(y=frequent_buyers.index, x=frequent_buyers.values, palette="coolwarm")
plt.title("Frequent Buyers by Number of Orders", fontsize=16)
plt.xlabel("Number of Orders", fontsize=12)
plt.ylabel("Customer", fontsize=12)
plt.yticks(fontsize=8)  # Reduce font size of y-axis labels
plt.tight_layout()
plt.show()


# 8. Order Frequency - Histogram
plt.figure(figsize=(12, 6))
plt.hist(order_frequency.values, bins=20, color="skyblue", edgecolor="black")
plt.title("Order Frequency Distribution", fontsize=16)
plt.xlabel("Days Between Orders", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.tight_layout()
plt.show()

# 9. City Preference - Bar Chart
plt.figure(figsize=(12, 6))
sns.barplot(x=city_preference.index, y=city_preference.values, palette="Set2")
plt.title("City Preference by Sales", fontsize=16)
plt.xlabel("City", fontsize=12)
plt.ylabel("Total Sales", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
