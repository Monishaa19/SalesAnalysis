# Import necessary libraries
import pandas as pd

# Load the dataset
file_path = 'dataset2.csv'
data = pd.read_csv(file_path)

# Step 1: Check for missing values
missing_values = data.isnull().sum()
print("Missing values per column:\n", missing_values)

# Step 2: Check for duplicates
duplicates = data.duplicated().sum()
print("Number of duplicate rows:", duplicates)

if duplicates > 0:
    data = data.drop_duplicates()
    print("Duplicates removed.")

# Step 3: Standardize column names (strip extra spaces)
data.columns = data.columns.str.strip()

# Step 4: Convert 'Order Date' to datetime format
if 'Order Date' in data.columns:
    data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d-%m-%Y', errors='coerce')
    print("Order Date column converted to datetime.")

# Step 5: Verify data types
data_types = data.dtypes
print("Data types after conversion:\n", data_types)

# Step 6: Identify outliers in numerical columns (e.g., Sales, Discount, Profit)
def detect_outliers(column):
    q1 = column.quantile(0.25)
    q3 = column.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return column[(column < lower_bound) | (column > upper_bound)]

numerical_columns = ['Sales', 'Discount', 'Profit']
outliers = {col: detect_outliers(data[col]) for col in numerical_columns}
for col, outlier_values in outliers.items():
    print(f"Outliers in {col}:", outlier_values.shape[0])

# Final dataset ready for analysis
print("Dataset is preprocessed and ready for analysis.")
# Save the preprocessed data if necessary
preprocessed_file_path = 'preprocessed_dataset.csv'
data.to_csv(preprocessed_file_path, index=False)
print(f"Preprocessed dataset saved to {preprocessed_file_path}.")
