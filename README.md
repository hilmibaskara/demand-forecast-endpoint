# Demand Forecast Endpoint

A FastAPI-based weather forecasting API that integrates with Visual Crossing Weather API to provide historical and forecast weather data in CSV and JSON formats.

## Features

- 🌤️ **Weather Forecast API** - Get weather forecasts for any location and date range
- 📊 **CSV Export** - Download weather data as CSV files
- 🔗 **JSON API** - RESTful JSON endpoints for integration
- 🌍 **Global Coverage** - Support for worldwide locations
- ⚡ **Fast API** - Built with FastAPI for high performance

## Setup

### 1. Virtual Environment
```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Visual Crossing API Key
1. Sign up at [Visual Crossing Weather](https://www.visualcrossing.com/sign-up)
2. Get your free API key from the dashboard

### 4. Start the Server
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Weather Forecast (CSV)
**GET** `/weather/forecast/csv`

Download weather forecast data as a CSV file.

**Parameters:**
- `location` (required): Location name, address, or coordinates (lat,lon)
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format  
- `api_key` (required): Your Visual Crossing Weather API key
- `include_current` (optional): Include current conditions (default: false)

**Example:**
```
GET /weather/forecast/csv?location=New York,NY&start_date=2025-07-15&end_date=2025-07-22&api_key=YOUR_API_KEY
```

### Weather Forecast (JSON)
**GET** `/weather/forecast/json`

Get weather forecast data in JSON format.

**Parameters:**
- `location` (required): Location name, address, or coordinates (lat,lon)
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `api_key` (required): Your Visual Crossing Weather API key

**Example:**
```
GET /weather/forecast/json?location=Jakarta,Indonesia&start_date=2025-07-15&end_date=2025-07-22&api_key=YOUR_API_KEY
```

## Usage Examples

### Python Example
```python
import requests

# Get CSV data
response = requests.get(
    "http://localhost:8000/weather/forecast/csv",
    params={
        "location": "Jakarta, Indonesia",
        "start_date": "2025-07-15", 
        "end_date": "2025-07-22",
        "api_key": "YOUR_API_KEY"
    }
)

if response.status_code == 200:
    with open("weather_forecast.csv", "w") as f:
        f.write(response.text)
```

### cURL Example
```bash
curl -X GET "http://localhost:8000/weather/forecast/csv?location=Singapore&start_date=2025-07-15&end_date=2025-07-22&api_key=YOUR_API_KEY" -o weather_forecast.csv
```

## Testing

Run the test script to verify the API is working:

```bash
python test_api.py
```

Make sure to update the `API_KEY` variable in `test_api.py` with your actual Visual Crossing API key.

## Data Fields

The weather forecast includes the following fields:
- **datetime**: Date of the forecast
- **tempmax**: Maximum temperature
- **tempmin**: Minimum temperature  
- **temp**: Average temperature
- **humidity**: Relative humidity percentage
- **precip**: Precipitation amount
- **windspeed**: Wind speed
- **winddir**: Wind direction (degrees)
- **pressure**: Atmospheric pressure
- **cloudcover**: Cloud cover percentage
- **visibility**: Visibility distance
- **conditions**: Weather conditions summary
- **description**: Detailed weather description

## Interactive Documentation

When the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Error Handling

The API includes comprehensive error handling:
- **400 Bad Request**: Invalid parameters or API key issues
- **404 Not Found**: Location not found or no data available
- **500 Internal Server Error**: Server-side errors

## License

This project is open source and available under the MIT License.

### To reload the server app
```
uvicorn main:app --reload
```