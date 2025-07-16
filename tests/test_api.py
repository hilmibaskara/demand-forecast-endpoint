# Example usage of the Weather Forecast API

import requests
import json

# API base URL (adjust if running on different host/port)
BASE_URL = "http://localhost:8000"

# Example parameters
LOCATION = "New York, NY"  # Can be city name, address, or coordinates "40.7128,-74.0060"
START_DATE = "2025-07-15"
END_DATE = "2025-07-22"
API_KEY = "YKNS6FHVN4DXKBP8T8TUSXQFP"  # Replace with your actual API key

def test_weather_forecast(format_type="json"):
    """Test the unified weather forecast endpoint"""
    print(f"Testing weather forecast endpoint (format: {format_type})...")
    
    params = {
        "location": LOCATION,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "api_key": API_KEY,
        "format_type": format_type,
        "include_current": False
    }
    
    response = requests.get(f"{BASE_URL}/weather/forecast", params=params)
    
    if response.status_code == 200:
        if format_type == "csv":
            # Save CSV file
            filename = f"weather_forecast_{LOCATION.replace(',', '_').replace(' ', '_')}_{START_DATE}_to_{END_DATE}.csv"
            with open(filename, 'w') as f:
                f.write(response.text)
            print(f"✅ CSV saved as: {filename}")
        else:
            data = response.json()
            print("✅ JSON response received:")
            print(json.dumps(data, indent=2)[:500] + "..." if len(str(data)) > 500 else json.dumps(data, indent=2))
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

# Backward compatibility test functions
def test_csv_endpoint():
    """Test the CSV weather forecast endpoint (backward compatibility)"""
    print("Testing CSV endpoint (backward compatibility)...")
    
    params = {
        "location": LOCATION,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "api_key": API_KEY,
        "include_current": False
    }
    
    response = requests.get(f"{BASE_URL}/weather/forecast/csv", params=params)
    
    if response.status_code == 200:
        # Save CSV file
        filename = f"weather_forecast_{LOCATION.replace(',', '_').replace(' ', '_')}_{START_DATE}_to_{END_DATE}.csv"
        with open(filename, 'w') as f:
            f.write(response.text)
        print(f"✅ CSV saved as: {filename}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def test_json_endpoint():
    """Test the JSON weather forecast endpoint (backward compatibility)"""
    print("Testing JSON endpoint (backward compatibility)...")
    
    params = {
        "location": LOCATION,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "api_key": API_KEY
    }
    
    response = requests.get(f"{BASE_URL}/weather/forecast/json", params=params)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ JSON response received:")
        print(json.dumps(data, indent=2)[:500] + "..." if len(str(data)) > 500 else json.dumps(data, indent=2))
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("Weather Forecast API Test")
    print("=" * 30)
    print(f"Location: {LOCATION}")
    print(f"Date range: {START_DATE} to {END_DATE}")
    print(f"API Key: {'Set' if API_KEY != 'YOUR_VISUAL_CROSSING_API_KEY' else 'NOT SET - Please update API_KEY variable'}")
    print()
    
    if API_KEY == "YOUR_VISUAL_CROSSING_API_KEY":
        print("⚠️  Please set your Visual Crossing API key in the API_KEY variable")
        print("   You can get a free API key at: https://www.visualcrossing.com/sign-up")
    else:
        # Test the new unified endpoint
        print("🚀 Testing New Unified Endpoint:")
        test_weather_forecast("json")
        print()
        test_weather_forecast("csv")
        print()
        
        # Test backward compatibility
        print("🔄 Testing Backward Compatibility:")
        test_json_endpoint()
        print()
        test_csv_endpoint()
