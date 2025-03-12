
#Seasonal Spikes in Sales

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset (replace 'data.csv' with your file path)
df = pd.read_csv('monisha/sorted_csv_file.csv')

# Step 1: Convert 'Order Date' to datetime format and extract the month
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Month'] = df['Order Date'].dt.month

# Step 2: Define a function to classify months into seasons
def get_season(month):
    if month in [3, 4, 5]:  # March to May = Summer
        return 'Summer'
    elif month in [6, 7, 8, 9]:  # June to September = Monsoon
        return 'Monsoon'
    elif month in [10, 11]:  # October to November = Autumn
        return 'Autumn'
    elif month in [12, 1, 2]:  # December to February = Winter
        return 'Winter'

# Apply the function to create a 'Season' column
df['Season'] = df['Month'].apply(get_season)

# Step 3: Aggregate total sales by City and Season
city_sales_by_season = (
    df.groupby(['City', 'Season'])['Sales']
    .sum()
    .reset_index()
)

# Step 4: Identify the season with the highest sales for each city
city_sales_by_season['Max_Sales_Season'] = city_sales_by_season.groupby('City')['Sales'].transform('max')
city_sales_by_season['Spike_Season'] = city_sales_by_season['Sales'] == city_sales_by_season['Max_Sales_Season']

# Step 5: Output the city and its season with the highest sales
city_spike_sales = city_sales_by_season[city_sales_by_season['Spike_Season']].sort_values(by='City')

# Print the result for all 24 cities
print("Sales Spike Analysis by City and Season:")
for index, row in city_spike_sales.iterrows():
    print(f"{row['City']} faces spike in sales in season {row['Season']}")
# Convert the result to JSON format
city_spike_sales_json = city_spike_sales[['City', 'Season', 'Sales']].to_dict(orient='records')

# Save the JSON data to a file
import json
with open('sales_spike_analysis.json', 'w') as f:
    json.dump(city_spike_sales_json, f, indent=4)
