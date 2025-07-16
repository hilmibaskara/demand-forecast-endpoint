# ETL Sales Process Integration

## Overview
The upload-history endpoint has been updated to use the enhanced ETL process from `etl-sales.py`. This provides a more robust and comprehensive approach to processing sales history data.

## Key Changes Made

### 1. Updated Sales Service (`app/services/sales_service.py`)

#### Enhanced Data Processing:
- **Better Data Cleaning**: Filters out non-product entries like payment records, discounts, etc.
- **Improved Perishable Detection**: Uses keywords ['ayam', 'katsu', 'cumi', 'sapi', 'daging', 'tempe', 'tahu']
- **More Accurate Portion Calculations**: Updated ingredient portions (chicken: 125g, beef: 100g, squid: 80g, tempe: 50g, tofu: 50g)

#### Enhanced Menu Mapping:
- **Expanded Menu Coverage**: Added more menu items including Bolognese dishes, various chicken preparations
- **Better Portion Control**: Different multipliers for different dish types (e.g., 0.75 for fried rice, 0.5 for additional katsu)
- **Improved Fallback Detection**: Better ingredient detection for unlisted menu items

#### Historical Data Management:
- **Automatic Historical Tracking**: Updates `ingredients_historical.csv` with cumulative data
- **Daily Summaries**: Creates `ingredients_needed_YYYY-MM-DD.csv` for each upload
- **Structured Output**: Consistent format with columns: TANGGAL, chicken, beef, squid, tempe, tahu

### 2. Updated Response Model (`app/models/sales.py`)

Added new fields to `SalesUploadResponse`:
- `historical_file`: Path to the cumulative historical data file
- `ingredients_needed`: Dictionary with calculated ingredient requirements for the date

### 3. Enhanced API Endpoint (`app/api/sales.py`)

- **Better Documentation**: Updated endpoint description explaining the ETL process
- **Enhanced Response**: Returns additional information about historical tracking and ingredient calculations

## New Process Flow

1. **Data Upload**: User uploads CSV file with sales data
2. **Data Cleaning**: Remove non-product entries, standardize format
3. **Perishable Filtering**: Identify items requiring fresh ingredients
4. **Ingredient Mapping**: Map menu items to ingredient requirements
5. **Calculation**: Calculate total ingredients needed based on portions and servings
6. **Historical Update**: Append to cumulative historical data
7. **Daily Summary**: Create date-specific ingredient summary
8. **Response**: Return comprehensive processing results

## Benefits of the New Process

1. **More Accurate Calculations**: Better portion control and ingredient mapping
2. **Historical Tracking**: Maintains cumulative data for trend analysis
3. **Better Data Quality**: Enhanced filtering and cleaning
4. **Comprehensive Coverage**: More menu items and better fallback detection
5. **Structured Output**: Consistent format suitable for ML model training

## Files Generated

- `ingredients_historical.csv`: Cumulative historical data
- `ingredients_needed_YYYY-MM-DD.csv`: Daily ingredient requirements
- `data/rekaphari_produk_YYYY-MM-DD.csv`: Original uploaded data (if saved)

## Testing

Use the updated `upload-sales.py` script to test the new functionality:

```bash
python upload-sales.py
```

The script will now display the full response including ingredient calculations and file paths.

## Migration Notes

- The old `ingredient_summary_` files are replaced with `ingredients_needed_` files
- Historical data is now tracked in a single cumulative file
- Response format includes additional fields for better integration with prediction models
