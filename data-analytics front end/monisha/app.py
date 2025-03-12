import pandas as pd

# Load your dataset
df = pd.read_csv('monisha/sorted_csv_file.csv')

# Calculate city-level correlations
city_correlation = (
    df.groupby('City')
    .apply(lambda group: group['Sales'].corr(group['Discount']))
    .reset_index(name='Correlation')
)

# Save as JSON
city_correlation.to_json('city_correlation.json', orient='records')
