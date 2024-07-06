import json
import pandas as pd

# Read data from JSON file with explicit encoding specification
with open('filtered_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Convert data to DataFrame
df = pd.DataFrame(data)

# Convert 'price' to numerical values
df['price'] = df['price'].str.replace(',', '').astype(float)

# Convert 'neighborhood' to categorical type
df['neighborhood'] = df['neighborhood'].astype('category')

# Group by neighborhood and calculate mean, mode, median, and count
neighborhood_groups = df.groupby('neighborhood')
for neighborhood, group_df in neighborhood_groups:
    mean_price = group_df['price'].mean()
    mode_price = group_df['price'].mode().iloc[0]
    median_price = group_df['price'].median()
    count = group_df.shape[0]

    print(f'{neighborhood}')
    print(f'Number of Apartments: {count}')
    print(f'Mean Price: {mean_price}')
    print(f'Mode Price: {mode_price}')
    print(f'Median Price: {median_price}')
    print()
