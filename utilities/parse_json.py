#%%
import pandas as pd
import json

# Load JSON data from file
with open('data.json', 'r') as file:
    json_data = json.load(file)

# Function to parse JSON data into a list of dictionaries
def parse_items(items, parent_name=None):
    rows = []
    for item in items:
        row = {
            'account_id': item.get('account_id'),
            'name': item.get('name'),
            'value': item.get('value'),
            'parent_name': parent_name
        }
        rows.append(row)
        if 'items' in item:
            rows.extend(parse_items(item['items'], item.get('name')))
    return rows

# Parse assets
assets_data = parse_items(json_data['assets']['items'], json_data['assets']['name'])
assets_df = pd.DataFrame(assets_data)

# Parse liabilities
liabilities_data = parse_items(json_data['liabilities']['items'], json_data['liabilities']['name'])
liabilities_df = pd.DataFrame(liabilities_data)

# Parse equity
equity_data = parse_items(json_data['equity']['items'], json_data['equity']['name'])
equity_df = pd.DataFrame(equity_data)

# Print dataframes
print("Assets DataFrame:")
print(assets_df)

print("\nLiabilities DataFrame:")
print(liabilities_df)
liabilities_df

print("\nEquity DataFrame:")
print(equity_df)
equity_df

#%%
assets_df.describe()
#%%
equity_df.describe()
#%%
liabilities_df.describe()

# %%
assets_df.parent_name.value_counts()
#%%
equity_df.parent_name.value_counts()
#%%
liabilities_df.parent_name.value_counts()
# %%
