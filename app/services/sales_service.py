import pandas as pd
import os

class SalesService:
    """Service for processing sales history CSV using ETL logic"""

    # Updated perishable keywords from etl-sales.py
    PERISHABLE_KEYWORDS = ['ayam', 'katsu', 'cumi', 'sapi', 'daging', 'tempe', 'tahu']

    # Updated ingredient portions from etl-sales.py
    INGREDIENT_PORTIONS = {
        'chicken': 125, 
        'beef': 100, 
        'squid': 80,
        'tempe': 50, 
        'tofu': 50
    }

    # Enhanced menu mapping from etl-sales.py
    MENU_INGREDIENTS = {
        # Bolognese dishes
        'Spaghetti Bolognese katsu keju': {'chicken': 1},
        'Spagetti bolognese katsu': {'chicken': 1},
        'Spagetti Kari Katsu': {'chicken': 1},
        'French Fries Bolognese': {'ground_meat': 0.75},
        'French Fries Bolognese keju': {'ground_meat': 0.75},
        'Kentang Bolognese keju': {'ground_meat': 0.75},
        
        # Chicken dishes
        'Katsu': {'chicken': 1},
        'Nasi Kari Chicken Katsu': {'chicken': 1},
        'Nasi Katsu Bumbu Bali': {'chicken': 1},
        'Nasi katsu + saos': {'chicken': 1},
        'Nasi katsu lada hitam': {'chicken': 1},
        'Katsu + bumbu TANPA NASI': {'chicken': 1},
        'Nasi + katsu TANPA BUMBU': {'chicken': 1},
        'Tambahan katsu': {'chicken': 0.5},
        'Indomie telur katsu': {'chicken': 0.75},
        'Indomie telur katsu keju (Tidak Pedas )': {'chicken': 0.75},
        'Indomie Telur Kari Katsu (Tidak Pedas)': {'chicken': 0.75},
        'Indomie kari katsu keju': {'chicken': 0.75},
        'Mie tek tek katsu  (Tidak pedas)': {'chicken': 0.75},
        
        # Ayam dishes
        'Nasi Rempah Ayam': {'chicken': 1},
        'Nasi Siram Ayam (Bumbu bali)': {'chicken': 1},
        'Nasi Siram Ayam (Kari)': {'chicken': 1},
        'Nasi Siram Ayam (Lada hitam)': {'chicken': 1},
        'Nasi Goreng Ayam (Tidak pedas)': {'chicken': 0.75},
        
        # Beef dishes
        'Nasi Rempah Daging': {'beef': 1},
        'Nasi Siram Daging (Bumbu bali)': {'beef': 1},
        'Nasi Siram Daging (Kari)': {'beef': 1},
        'Nasi Siram Daging (Lada hitam )': {'beef': 1},
        'Nasi goreng daging (Tidak pedas)': {'beef': 0.75},
        'Mie tek tek sapi (Tidak Pedas )': {'beef': 0.75},
        
        # Squid dishes
        'Cumi': {'squid': 1},
        'Cumi Bumbu Bali Tanpa Nasi': {'squid': 1},
        'Nasi rempah cumi': {'squid': 1},
        'Nasi siram cumi ': {'squid': 1},
        'Nasi goreng cumi ': {'squid': 0.75},
    }

    def __init__(self):
        """Initialize the sales service"""
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        self.historical_file = os.path.join(BASE_DIR, "data", "ingredients_historical.csv")


    def detect_ingredients(self, menu_name: str):
        """Enhanced ingredient detection from etl-sales.py"""
        menu_lower = menu_name.lower()
        ingredients = {}

        if 'bolognese' in menu_lower:
            ingredients['ground_meat'] = ingredients.get('ground_meat', 0) + 0.75
            ingredients['tomato'] = ingredients.get('tomato', 0) + 0.75
        if 'katsu' in menu_lower or 'ayam' in menu_lower:
            ingredients['chicken'] = ingredients.get('chicken', 0) + 1
        if any(word in menu_lower for word in ['daging', 'sapi']):
            ingredients['beef'] = ingredients.get('beef', 0) + 1
        if 'cumi' in menu_lower:
            ingredients['squid'] = ingredients.get('squid', 0) + 1
        if 'tempe' in menu_lower:
            ingredients['tempe'] = ingredients.get('tempe', 0) + 1
        if 'tahu' in menu_lower:
            ingredients['tofu'] = ingredients.get('tofu', 0) + 1
        return ingredients

    def clean_and_filter_data(self, df: pd.DataFrame, date: str) -> pd.DataFrame:
        """Clean and filter data using ETL logic"""
        # Add date column
        df["TANGGAL"] = date
        
        # Select and reorder columns
        df = df[["TANGGAL", "PRODUK", "JUMLAH"]]
        
        # Filter out unwanted rows using ETL logic
        df = df[~df["PRODUK"].str.contains("HARGA|Diskon|PEMBAYARAN|BAYAR|HUTANG|Cash|HARGA JUAL|LABA|PRODUK", na=False)]
        df = df[df["PRODUK"] != ""].dropna(subset=["PRODUK"])
        
        # Convert JUMLAH to numeric, handling any non-numeric values
        df["JUMLAH"] = pd.to_numeric(df["JUMLAH"], errors='coerce')
        df = df.dropna(subset=["JUMLAH"])  # Remove rows where JUMLAH couldn't be converted
        
        # Format date
        df["TANGGAL"] = pd.to_datetime(df["TANGGAL"]).dt.strftime("%Y-%m-%d")
        df = df.sort_values("TANGGAL")
        
        return df

    def calculate_ingredients_from_sales(self, df_perishable: pd.DataFrame, date: str) -> dict:
        """Calculate total ingredients needed using ETL logic"""
        total_ingredients = {}

        for _, row in df_perishable.iterrows():
            menu_item = row['PRODUK']
            servings = int(row['JUMLAH'])

            if menu_item in self.MENU_INGREDIENTS:
                ingredients = self.MENU_INGREDIENTS[menu_item]
            else:
                ingredients = self.detect_ingredients(menu_item)

            for ingredient, portion_multiplier in ingredients.items():
                qty = portion_multiplier * servings * self.INGREDIENT_PORTIONS.get(ingredient, 0)
                total_ingredients[ingredient] = total_ingredients.get(ingredient, 0) + qty

        # Build pivot row similar to ETL
        pivot_row = {
            'TANGGAL': date,
            'chicken': round(total_ingredients.get('chicken', 0), 2),
            'beef': round(total_ingredients.get('beef', 0), 2),
            'squid': round(total_ingredients.get('squid', 0), 2),
            'tempe': round(total_ingredients.get('tempe', 0), 2),
            'tahu': round(total_ingredients.get('tofu', 0), 2)
        }

        return pivot_row

    def update_historical_data(self, pivot_row: dict):
        """Upsert (overwrite) pivot row for the same date"""
        pivot_df = pd.DataFrame([pivot_row])

        if os.path.exists(self.historical_file):
            # Load existing CSV
            df_existing = pd.read_csv(self.historical_file)

            # Drop rows with same date
            df_existing = df_existing[df_existing['TANGGAL'] != pivot_row['TANGGAL']]

            # Append the new pivot row
            df_updated = pd.concat([df_existing, pivot_df], ignore_index=True)

            # Sort by date in descending order (newest first)
            df_updated = df_updated.sort_values('TANGGAL')

            # Write back to CSV
            df_updated.to_csv(self.historical_file, index=False)
            print(f"✅ Overwrote existing date and saved: {self.historical_file}")

        else:
            # No file yet: create new one
            pivot_df.to_csv(self.historical_file, index=False)
            print(f"✅ Created new historical file: {self.historical_file}")


    def process_sales_history(self, date: str, df: pd.DataFrame) -> dict:
        """Main processing function using ETL logic"""
        # Clean and filter the data using ETL approach
        df_cleaned = self.clean_and_filter_data(df, date)
        
        # Get unique products before filtering
        unique_products = sorted(df_cleaned['PRODUK'].dropna().unique())
        num_unique_products = len(unique_products)

        # Filter only perishable items using ETL logic
        df_cleaned['is_perishable'] = df_cleaned['PRODUK'].str.lower().str.contains('|'.join(self.PERISHABLE_KEYWORDS))
        df_perishable = df_cleaned[df_cleaned['is_perishable']].copy()

        # Calculate ingredients using ETL logic
        pivot_row = self.calculate_ingredients_from_sales(df_perishable, date)
        
        # Update historical data
        self.update_historical_data(pivot_row)
        
        # Create ingredient summary for the specific date
        # data_dir = "data"
        # os.makedirs(data_dir, exist_ok=True)
        # output_file = os.path.join(data_dir, f"ingredients_needed_{date}.csv")
        
        # Save the ingredients needed for this date
        # ingredient_df = pd.DataFrame([pivot_row])
        # ingredient_df.to_csv(output_file, index=False)

        return {
            "unique_products": unique_products,
            "num_unique_products": num_unique_products,
            "perishable_products": sorted(df_perishable['PRODUK'].unique()),
            "non_perishable_products": sorted(df_cleaned[~df_cleaned['is_perishable']]['PRODUK'].unique()),
            # "ingredient_summary_file": output_file,
            "historical_file": self.historical_file,
            "ingredients_needed": pivot_row
        }