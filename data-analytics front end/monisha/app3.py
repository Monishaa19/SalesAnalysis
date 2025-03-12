import pandas as pd

# Load the dataset (replace 'dataset4.csv' with your file path)
df = pd.read_csv('monisha/sorted_csv_file.csv')

# Define the high-spending threshold
high_spending_threshold = 5000 # Example threshold

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

# Check if there's any data to save
if branch_high_spending_counts.empty:
    print("No high-spending customers found.")
    data_to_save = []
else:
    data_to_save = branch_high_spending_counts.to_dict(orient='records')

# Save the results to a JSON file
import json

with open('high_spending_data.json', 'w') as json_file:
    json.dump(data_to_save, json_file, indent=4)

print("JSON file generated successfully.")
