import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'sunaina/preprocessed_dataset.csv'
data = pd.read_csv(file_path)

# Step 1: Preprocess Data for Clustering
# Aggregate data at the customer level
customer_data = data.groupby('Customer Name').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'count'
}).rename(columns={'Order ID': 'Order Frequency'})

# Step 2: Normalize the Data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(customer_data)

# Step 3: Apply K-Means Clustering
kmeans = KMeans(n_clusters=4, random_state=42)
customer_data['Cluster'] = kmeans.fit_predict(scaled_data)

# Step 4: Visualize the Clusters
plt.figure(figsize=(8, 6))
plt.scatter(customer_data['Sales'], customer_data['Profit'], c=customer_data['Cluster'], cmap='viridis', alpha=0.7)
plt.title("Customer Segmentation")
plt.xlabel("Total Sales")
plt.ylabel("Total Profit")
plt.colorbar(label="Cluster")
plt.grid()
plt.show()

# Save the results
customer_data.to_csv('customer_segments.csv', index=True)
print("Customer segments saved to 'customer_segments.csv'.")

# Save the plot to a file
plot_path = 'customer_segmentation_plot.png'
plt.figure(figsize=(8, 6))
plt.scatter(customer_data['Sales'], customer_data['Profit'], c=customer_data['Cluster'], cmap='viridis', alpha=0.7)
plt.title("Customer Segmentation")
plt.xlabel("Total Sales")
plt.ylabel("Total Profit")
plt.colorbar(label="Cluster")
plt.grid()
plt.savefig(plot_path)  # Save plot as an image
plt.close()
