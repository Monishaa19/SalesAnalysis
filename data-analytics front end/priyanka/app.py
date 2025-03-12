import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import json

# Load the dataset
file_path = 'C:\\Users\\rprar\\Projects\\static web page\\priyanka\\sorted_csv_file.csv'
data = pd.read_csv(file_path)

# Correctly parse the Date column
data['Order Date'] = pd.to_datetime(data['Order Date'], format='%Y-%m-%d', errors='coerce')  # Adjust format if needed
data.set_index('Order Date', inplace=True)

# Forecast sales for each sub-category
subcategories = data['Sub Category'].unique()
forecast_results = {}

for subcategory in subcategories:
    # Filter data for the sub-category
    sub_data = data[data['Sub Category'] == subcategory]
    
    # Check if there is enough data to forecast
    if sub_data.empty:
        print(f"Skipping sub-category '{subcategory}' due to lack of data.")
        continue
    
    # Fit ARIMA model
    model = ARIMA(sub_data['Sales'], order=(5, 1, 0))  # Adjust (p, d, q) as needed
    try:
        model_fit = model.fit()
    except Exception as e:
        print(f"Could not fit ARIMA for sub-category '{subcategory}': {e}")
        continue

    # Forecast for the next 3 years (365 * 3 days)
    forecast_steps = 365 * 3
    forecast = model_fit.forecast(steps=forecast_steps)
    
    # Check if the last date in sub_data is a valid timestamp
    if pd.isna(sub_data.index[-1]):
        print(f"Skipping sub-category '{subcategory}' due to invalid last date.")
        continue
    
    forecast_index = pd.date_range(start=sub_data.index[-1], periods=forecast_steps + 1, freq='D')[1:]

    # Prepare forecast DataFrame
    forecast_df = pd.DataFrame({'Date': forecast_index, 'Forecasted Sales': forecast})

    # Filter the forecasted sales between 2019 and 2021
    forecast_df = forecast_df[forecast_df['Date'].dt.year.isin([2019, 2020, 2021])]

    # Summarize forecasted sales by year
    forecast_summary = forecast_df.groupby(forecast_df['Date'].dt.year)['Forecasted Sales'].sum().to_dict()
    forecast_results[subcategory] = forecast_summary

# Save the forecast results to a JSON file
forecast_json_path = 'C:\\Users\\rprar\\Projects\\static web page\\forecast_results.json'
with open(forecast_json_path, 'w') as json_file:
    json.dump(forecast_results, json_file)

print(f"Forecast results saved to {forecast_json_path}")
