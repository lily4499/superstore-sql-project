import pandas as pd

# Load original CSV
df = pd.read_csv('data/superstore_orders.csv')

# ✅ 1. Fix date format (MM/DD/YYYY → YYYY-MM-DD)
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y')

# ✅ 2. Strip whitespace
df.columns = [col.strip() for col in df.columns]
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# ✅ 3. Remove duplicates (optional)
df = df.drop_duplicates()

# ✅ 4. Handle NaNs: fill with zeros or drop
df = df.fillna({
    'Sales': 0,
    'Quantity': 0,
    'Discount': 0,
    'Profit': 0
})

# ✅ 5. Save cleaned version
df.to_csv('data/superstore_orders_cleaned.csv', index=False)
print("✅ Clean CSV saved as: data/superstore_orders_cleaned.csv")

