import requests
import json

url = "http://localhost:8000/sales/upload-history"

# Prepare the form data
data = {
    "date": "2025-07-06"
}

# Prepare the file
with open("data/rekaphari_produk_2025-07-06.csv", "rb") as f:
    files = {
        "file": ("rekaphari_produk_2025-07-06.csv", f, "text/csv")
    }
    
    response = requests.post(url, data=data, files=files)

print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

if response.status_code == 200:
    try:
        print(f"Response JSON: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print("Response is not valid JSON")
else:
    print("Error occurred during upload")

# Close the file properly
if 'file' in locals():
    try:
        files['file'][1].close()
    except:
        pass