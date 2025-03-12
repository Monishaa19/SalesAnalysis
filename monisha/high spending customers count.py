#High spending customers count

import pandas as pd

# Load the dataset (replace 'data.csv' with your file path)
df = pd.read_csv('dataset4.csv')

# Define the high-spending threshold
high_spending_threshold = 10000  # Example threshold

# Step 1: Calculate total sales for each customer
customer_sales = (
    df.groupby(['City', 'Region', 'Customer Name'])['Sales']
    .sum()
    .reset_index(name='TotalSales')
)

# Step 2: Filter customers whose total sales exceed the threshold
high_spending_customers = customer_sales[customer_sales['TotalSales'] > high_spending_threshold]

# Step 3: Count high-spending customers by city and region
branch_high_spending_counts = (
    high_spending_customers
    .groupby(['City', 'Region'])
    .size()
    .reset_index(name='HighSpendingCustomerCount')
)

# Step 4: Sort the regions by the count of high-spending customers
sorted_branches = branch_high_spending_counts.sort_values(by='HighSpendingCustomerCount', ascending=False)

# Display results
print("Regions with the highest number of high-spending customers:")
print(sorted_branches)
import matplotlib.pyplot as plt

# Plot the high-spending customer counts
plt.figure(figsize=(12, 6))
plt.bar(sorted_branches['City'] + " - " + sorted_branches['Region'], sorted_branches['HighSpendingCustomerCount'], color='pink')
plt.xticks(rotation=45, ha='right')
plt.title('High-Spending Customers by Region')
plt.xlabel('City - Region')
plt.ylabel('High-Spending Customer Count')
plt.tight_layout()
plt.show()
