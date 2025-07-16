import pandas as pd
import io
from app.services.sales_service import SalesService

# Test the service directly
sales_service = SalesService()

# Read the CSV file as the API would
with open("data/rekaphari_produk_2025-07-06.csv", "rb") as f:
    content = f.read()

print("Reading CSV with skiprows=2...")
df = pd.read_csv(io.BytesIO(content), skiprows=2, names=["PRODUK", "JUMLAH", "HARGA"])

# Remove the first row if it contains the column headers
if len(df) > 0 and str(df.iloc[0]['PRODUK']).upper() == 'PRODUK':
    print("Removing header row from data...")
    df = df.iloc[1:].reset_index(drop=True)

print(f"DataFrame shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print("First few rows:")
print(df.head())

print("\nTesting process_sales_history...")
try:
    result = sales_service.process_sales_history("2025-07-16", df)
    print("Success!")
    print(f"Unique products: {len(result['unique_products'])}")
    print(f"Perishable products: {len(result['perishable_products'])}")
    print(f"Ingredients needed: {result['ingredients_needed']}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
