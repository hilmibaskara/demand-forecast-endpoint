# Test script for Sales API placeholder endpoints

import requests
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_get_sales_history():
    """Test getting sales history"""
    print("Testing GET /sales/history...")
    
    response = requests.get(f"{BASE_URL}/sales/history")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Success!")
        print(f"   Message: {result['message']}")
        print(f"   Available dates: {result['available_dates']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def test_get_sales_data():
    """Test getting sales data for specific date"""
    print("\nTesting GET /sales/data/{date}...")
    
    test_date = "2025-07-06"
    response = requests.get(f"{BASE_URL}/sales/data/{test_date}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Success!")
        print(f"   Message: {result['message']}")
        print(f"   Sales date: {result['sales_date']}")
        print(f"   Data: {result['data']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def test_predict_demand():
    """Test demand prediction"""
    print("\nTesting POST /sales/predict-demand...")
    
    data = {'date': '2025-07-07'}
    response = requests.post(f"{BASE_URL}/sales/predict-demand", data=data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Success!")
        print(f"   Message: {result['message']}")
        print(f"   Sales date: {result['sales_date']}")
        print(f"   Prediction: {result['prediction']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def test_upload_sales_history():
    """Test uploading sales history"""
    print("\nTesting POST /sales/upload-history...")
    
    # Create a dummy CSV content for testing
    csv_content = "PRODUK,JUMLAH,HARGA\nTest Product,5,50000\n"
    
    # Create temp file for testing
    with open("temp_test.csv", "w") as f:
        f.write(csv_content)
    
    try:
        with open("temp_test.csv", 'rb') as f:
            files = {'file': ('test_sales.csv', f, 'text/csv')}
            data = {'date': '2025-07-06'}
            
            response = requests.post(f"{BASE_URL}/sales/upload-history", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"   Message: {result['message']}")
            print(f"   Sales date: {result['sales_date']}")
            print(f"   Filename: {result['filename']}")
            print(f"   Status: {result['status']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    
    finally:
        # Cleanup temp file
        Path("temp_test.csv").unlink(missing_ok=True)

if __name__ == "__main__":
    print("Sales API Placeholder Test")
    print("=" * 40)
    
    # Test all placeholder endpoints
    test_get_sales_history()
    test_get_sales_data()
    test_predict_demand()
    test_upload_sales_history()
    
    print("\n" + "=" * 40)
    print("🚀 All placeholder endpoints tested!")
    print("📖 Check http://localhost:8000/docs for interactive API documentation.")
