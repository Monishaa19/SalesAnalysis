!pip install apyori
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
dataset = pd.read_csv('association2.csv', header = None)
transactions = []
for i in range(0, 8899):
  transactions.append([str(dataset.values[i,j]) for j in range(0, 3)])
from apyori import apriori
rules = apriori(transactions = transactions, min_support = 0.0000001, min_confidence = 0.00001, min_lift = 0.000001, min_length = 2, max_length=2)
results = list(rules)
# Function to format results and sort by highest support
def format_and_sort_results_by_support(results):
    rows = []  # Store rows to be formatted

    for result in results:
        for ordered_stat in result.ordered_statistics:
            # Ensure both LHS and RHS are non-empty and not NaN
            if ordered_stat.items_base and ordered_stat.items_add:
                lhs_set = ordered_stat.items_base
                rhs_set = ordered_stat.items_add

                # Check for NaN in LHS and RHS
                if not any(pd.isna(item) for item in lhs_set.union(rhs_set)):
                    lhs_str = ', '.join(lhs_set)
                    rhs_str = ', '.join(rhs_set)
                    support = result.support
                    confidence = ordered_stat.confidence
                    lift = ordered_stat.lift
                    rows.append((lhs_str, rhs_str, support, confidence, lift))

    # Create DataFrame from rows
    results_df = pd.DataFrame(rows, columns=['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift'])

    # Sort by Support in descending order
    # results_df = results_df.sort_values(by='Lift', ascending=False).reset_index(drop=True)
    results_df = results_df.query("`Left Hand Side` != 'nan' and `Right Hand Side` != 'nan'").sort_values(by='Lift', ascending=False).reset_index(drop=True)

    return results_df

# Apply the function and sort
sorted_results = format_and_sort_results_by_support(results)

# Display the sorted results
print(sorted_results.head(100))  # Display the top 10 rows
# Add a unique identifier for each pair by sorting LHS and RHS alphabetically
sorted_results['Pair'] = sorted_results.apply(lambda row: tuple(sorted([row['Left Hand Side'], row['Right Hand Side']])), axis=1)

# Drop duplicates based on the Pair column
sorted_results = sorted_results.drop_duplicates(subset='Pair').drop(columns='Pair').reset_index(drop=True)
# Set the option to display all rows
pd.set_option('display.max_rows', 50)

# Print the entire DataFrame
print(sorted_results.head(20))

# Reset the option if needed later
pd.reset_option('display.max_rows')
