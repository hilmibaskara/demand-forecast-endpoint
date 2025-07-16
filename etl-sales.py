import os
import pandas as pd

# === CONFIG ===
base_dir = "data"
date_str = "2025-07-11"
rekap_file = os.path.join(base_dir, f"rekaphari_produk_{date_str}.csv")
historical_file = "ingredients_historical.csv"

# === 1) Load & Clean ===
if os.path.exists(rekap_file):
    df = pd.read_csv(rekap_file, skiprows=2, names=["PRODUK", "JUMLAH", "HARGA"])
    df["TANGGAL"] = date_str

    df = df[["TANGGAL", "PRODUK", "JUMLAH"]]
    df = df[~df["PRODUK"].str.contains("HARGA|Diskon|PEMBAYARAN|BAYAR|HUTANG|Cash|HARGA JUAL|LABA|PRODUK", na=False)]
    df = df[df["PRODUK"] != ""].dropna(subset=["PRODUK"])
    df["TANGGAL"] = pd.to_datetime(df["TANGGAL"]).dt.strftime("%Y-%m-%d")
    df = df.sort_values("TANGGAL")
else:
    raise FileNotFoundError(f"File not found: {rekap_file}")

# === 2) Filter only perishable ===
perishable_keywords = ['ayam', 'katsu', 'cumi', 'sapi', 'daging', 'tempe', 'tahu']
df['is_perishable'] = df['PRODUK'].str.lower().str.contains('|'.join(perishable_keywords))
df_perishable = df[df['is_perishable']].copy()

# === 3) Ingredient portions ===
ingredient_portions = {
    'chicken': 125, 'beef': 100, 'squid': 80,
    'tempe': 50, 'tofu': 50
}

# === 4) Menu mapping ===
menu_ingredients = {
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

# === 5) Fallback detection ===
def detect_ingredients(menu_name):
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

# === 6) Calculate total ingredients ===
total_ingredients = {}

for _, row in df_perishable.iterrows():
    menu_item = row['PRODUK']
    servings = int(row['JUMLAH'])

    if menu_item in menu_ingredients:
        ingredients = menu_ingredients[menu_item]
    else:
        ingredients = detect_ingredients(menu_item)

    for ingredient, portion_multiplier in ingredients.items():
        qty = portion_multiplier * servings * ingredient_portions.get(ingredient, 0)
        total_ingredients[ingredient] = total_ingredients.get(ingredient, 0) + qty

# === 7) Build pivot row ===
pivot_row = {
    'TANGGAL': date_str,
    'chicken': round(total_ingredients.get('chicken', 0), 2),
    'beef': round(total_ingredients.get('beef', 0), 2),
    'squid': round(total_ingredients.get('squid', 0), 2),
    'tempe': round(total_ingredients.get('tempe', 0), 2),
    'tahu': round(total_ingredients.get('tofu', 0), 2)
}

# === 8) Append or create ===
pivot_df = pd.DataFrame([pivot_row])

if not os.path.exists(historical_file):
    pivot_df.to_csv(historical_file, index=False)
    print(f"✅ Created new historical file: {historical_file}")
else:
    pivot_df.to_csv(historical_file, mode='a', header=False, index=False)
    print(f"✅ Appended to existing historical file: {historical_file}")

print(pivot_df)
