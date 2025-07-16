import pandas as pd

class SalesService:
    """Service for processing sales history CSV"""

    PERISHABLE_KEYWORDS = [
        'cumi', 'katsu', 'ayam', 'daging', 'sapi', 'tempe', 'tahu'
    ]

    SHELF_STABLE_ITEMS = [
        'dancow', 'air mineral', 'air putih', 'americano', 'aqua/summit', 'kopi', 'pisang',
        'es coklat', 'es teh manis', 'kopi butter', 'kopi pisang',
        'kopi vanilla', 'kopi tiramisu', 'rujak cireng', 'otak otak',
        'leci tea', 'lemon tea', 'milo machiato', 'ovaltine machiato', 'nasi putih',
        'teh manis', 'teh tarik', 'teh tawar', 'wedang jahe', 'wedang sereh',
        'wedang susu', 'telur', 'sosis', 'kentang goreng'
    ]

    INGREDIENT_PORTIONS = {
        'chicken': 125,
        'beef': 100,
        'squid': 80,
        'tempe': 100,
        'tahu': 100
    }

    MENU_INGREDIENTS = {
        # tambahkan mapping sesuai milikmu
        'Spaghetti Bolognese katsu keju': {'chicken': 1},
        # dst...
    }

    def __init__(self):
        """Optional: Inisialisasi resource, kalau nanti ada DB connection, config, dsb."""
        pass

    def detect_ingredients(self, menu_name: str):
        menu_lower = menu_name.lower()
        ingredients = {}

        if 'katsu' in menu_lower:
            ingredients['chicken'] = ingredients.get('chicken', 0) + 1
        if any(word in menu_lower for word in ['daging', 'sapi']):
            ingredients['beef'] = ingredients.get('beef', 0) + 1
        if 'ayam' in menu_lower:
            ingredients['chicken'] = ingredients.get('chicken', 0) + 1
        if 'cumi' in menu_lower:
            ingredients['squid'] = ingredients.get('squid', 0) + 1
        if 'tempe' in menu_lower:
            ingredients['tempe'] = ingredients.get('tempe', 0) + 1
        if 'tahu' in menu_lower:
            ingredients['tahu'] = ingredients.get('tahu', 0) + 1
        return ingredients

    def standardize_product_names(self, df: pd.DataFrame) -> pd.DataFrame:
        name_mapping = {
            'spaghetti katsu keju': 'Spaghetti Bolognese katsu keju'
        }
        df['PRODUK'] = df['PRODUK'].apply(
            lambda x: name_mapping.get(x.lower(), x) if isinstance(x, str) else x
        )
        return df

    def map_menu_to_ingredients(self, df: pd.DataFrame) -> pd.DataFrame:
        df['TANGGAL'] = pd.to_datetime(df['TANGGAL'])
        df['JUMLAH'] = pd.to_numeric(df['JUMLAH'], errors='coerce')

        all_dates = df['TANGGAL'].unique()
        ingredients = list(self.INGREDIENT_PORTIONS.keys())

        result_df = pd.DataFrame(0, index=pd.DatetimeIndex(all_dates), columns=ingredients)

        for _, row in df.iterrows():
            menu_item = row['PRODUK']
            qty = row['JUMLAH']
            date = row['TANGGAL']

            if menu_item in self.MENU_INGREDIENTS:
                for ing, mult in self.MENU_INGREDIENTS[menu_item].items():
                    result_df.at[date, ing] += qty * mult * self.INGREDIENT_PORTIONS[ing]
            else:
                detected = self.detect_ingredients(menu_item)
                for ing, mult in detected.items():
                    result_df.at[date, ing] += qty * mult * self.INGREDIENT_PORTIONS[ing]

        result_df.reset_index(inplace=True)
        result_df.rename(columns={'index': 'TANGGAL'}, inplace=True)
        return result_df

    def process_sales_history(self, date: str, df: pd.DataFrame) -> dict:
        unique_products = sorted(df['PRODUK'].dropna().unique())
        num_unique_products = len(unique_products)

        df['lower_produk'] = df['PRODUK'].str.lower()
        df['is_perishable'] = df['lower_produk'].apply(
            lambda x: int(any(k in x for k in self.PERISHABLE_KEYWORDS)) if isinstance(x, str) else 0
        )

        df.loc[
            df['lower_produk'].apply(
                lambda x: any(item in x for item in self.SHELF_STABLE_ITEMS) if isinstance(x, str) else False
            ),
            'is_perishable'
        ] = 0

        df = self.standardize_product_names(df)
        df_perishable = df[df['is_perishable'] == 1].copy()

        ingredient_summary = self.map_menu_to_ingredients(df_perishable)
        output_file = f"ingredient_summary_{date}.csv"
        ingredient_summary.to_csv(output_file, index=False)

        return {
            "unique_products": unique_products,
            "num_unique_products": num_unique_products,
            "perishable_products": sorted(df_perishable['PRODUK'].unique()),
            "non_perishable_products": sorted(df[df['is_perishable'] == 0]['PRODUK'].unique()),
            "ingredient_summary_file": output_file
        }
