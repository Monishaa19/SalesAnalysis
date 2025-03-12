import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('sunaina/preprocessed_dataset.csv')

# Preprocess the Date feature
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month

# Aggregate data month-wise
monthly_data = df.groupby(['Category', 'City', 'Year', 'Month', 'Discount'])[['Sales']].mean().reset_index()

# Encode categorical columns
from sklearn.preprocessing import LabelEncoder
label_encoders = {}
categorical_columns = ['Category', 'City']
for col in categorical_columns:
    le = LabelEncoder()
    monthly_data[col] = le.fit_transform(monthly_data[col])
    label_encoders[col] = le

# Define features and target for sales prediction
X_sales = monthly_data[['Category', 'City', 'Year', 'Month', 'Discount']]
y_sales = monthly_data['Sales']

# Train a Random Forest Regressor
sales_model = RandomForestRegressor(random_state=42)
sales_model.fit(X_sales, y_sales)

# Get feature importances
feature_importances = sales_model.feature_importances_

# Create a dataframe to view the feature importances
importance_df = pd.DataFrame({
    'Feature': X_sales.columns,
    'Importance': feature_importances
})

# Sort features by importance
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# Plot the feature importances
plt.figure(figsize=(10, 6))
plt.barh(importance_df['Feature'], importance_df['Importance'])
plt.xlabel('Importance')
plt.title('Feature Importance for Sales Prediction')
plt.show()

# Display feature importance
importance_df

plot_path = 'feature_importance_plot.png'
plt.figure(figsize=(10, 6))
plt.barh(importance_df['Feature'], importance_df['Importance'])
plt.xlabel('Importance')
plt.title('Feature Importance for Sales Prediction')
plt.savefig(plot_path)  # Save plot as an image
plt.close()