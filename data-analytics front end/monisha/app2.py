import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import json

# Load the dataset
df = pd.read_csv('monisha/sorted_csv_file.csv')

# Filter for the West region only
west_region_df = df[df['Region'] == 'West'].copy()  # Use .copy() to avoid SettingWithCopyWarning

# Convert 'Order Date' to datetime and extract Year
west_region_df['Order Date'] = pd.to_datetime(west_region_df['Order Date'], errors='coerce')
west_region_df['Year'] = west_region_df['Order Date'].dt.year

# Aggregate sales data by Year
sales_per_year = west_region_df.groupby('Year')['Sales'].sum()

# Build ARIMA model
model = ARIMA(sales_per_year, order=(5, 1, 0))  # (p,d,q) can be tuned based on analysis
model_fit = model.fit()

# Forecast for the next 3 years
forecast_steps = 3
forecast = model_fit.forecast(steps=forecast_steps)

# Prepare results for JSON output
forecast_years = [int(sales_per_year.index[-1] + i + 1) for i in range(forecast_steps)]
forecast_results = [{"Year": int(year), "Sales": float(sales)} for year, sales in zip(forecast_years, forecast)]

# Save forecast results to a JSON file
with open('west_sales_forecast.json', 'w') as json_file:
    json.dump(forecast_results, json_file, indent=4)

print("Forecast saved to 'west_sales_forecast.json'.")
