# Seasonal Spikes for food items
import pandas as pd
import json 
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

# Step 3: Aggregate total sales by City, Subcategory, and Season
city_subcategory_season_sales = (
    df.groupby(['City', 'Sub Category', 'Season'])['Sales']
    .sum()
    .reset_index()
)

# Step 4: Find the season with the highest sales for each city and subcategory
city_subcategory_season_sales['Max_Sales_Season'] = city_subcategory_season_sales.groupby(['City', 'Sub Category'])['Sales'].transform('max')
city_subcategory_season_sales['Demand_Increase'] = city_subcategory_season_sales['Sales'] == city_subcategory_season_sales['Max_Sales_Season']

# Step 5: Output the city, subcategory, season with the highest sales (increase in demand)
demand_increase_sales = city_subcategory_season_sales[city_subcategory_season_sales['Demand_Increase']].sort_values(by=['City', 'Sales'], ascending=False)

# Step 6: Limit the output to 2 results per city
# Create an empty list to store the results
final_output = []

# Loop over each city and select the top 2 subcategories with the highest demand
for city in demand_increase_sales['City'].unique():
    city_data = demand_increase_sales[demand_increase_sales['City'] == city]
    # Get the top 2 results for the city
    top_2 = city_data.head(2)
    for index, row in top_2.iterrows():
        final_output.append(f"Increase in demand for subcategory {row['Sub Category']} in city {row['City']} during season {row['Season']}")

# Print the final output
print("Increase in Demand Analysis by City, Subcategory, and Season (Top 2 per City):")
for output in final_output:
    print(output)

# Convert the result to JSON format
demand_increase_sales_json = demand_increase_sales[['City', 'Sub Category', 'Season', 'Sales']].to_dict(orient='records')


with open('demand_increase_sales.json', 'w') as f:
    json.dump(demand_increase_sales_json, f, indent=4)
