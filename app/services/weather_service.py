import requests
import pandas as pd
import io
from datetime import datetime
from typing import Dict, Any, Tuple
from fastapi import HTTPException


class WeatherService:
    """Service for fetching weather data from Visual Crossing API"""
    
    BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    
    def __init__(self):
        pass
    
    def validate_dates(self, start_date: str, end_date: str) -> None:
        """Validate date format"""
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    def fetch_weather_data(self, location: str, start_date: str, end_date: str, 
                          api_key: str, include_current: bool = False) -> Dict[str, Any]:
        """
        Fetch weather data from Visual Crossing API
        
        Args:
            location: Location (city, address, or coordinates)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            api_key: Visual Crossing API key
            include_current: Whether to include current conditions
            
        Returns:
            Dictionary containing weather data
        """
        self.validate_dates(start_date, end_date)
        
        url = f"{self.BASE_URL}/{location}/{start_date}/{end_date}"
        
        params = {
            "key": api_key,
            "include": "days,hours" if include_current else "days",
            "elements": "datetime,tempmax,tempmin,temp,humidity,precip,windspeed,winddir,pressure,cloudcover,visibility,conditions,description"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=400, detail=f"Error fetching weather data: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def convert_to_csv(self, weather_data: Dict[str, Any], location: str, 
                      start_date: str, end_date: str) -> Tuple[str, str]:
        """
        Convert weather data to CSV format
        
        Returns:
            Tuple of (csv_content, filename)
        """
        if 'days' not in weather_data:
            raise HTTPException(status_code=404, detail="No weather data found for the specified location and date range")
        
        df = pd.DataFrame(weather_data['days'])
        
        # Add location info
        df['location'] = weather_data.get('address', location)
        df['latitude'] = weather_data.get('latitude', '')
        df['longitude'] = weather_data.get('longitude', '')
        
        # Reorder columns for better readability
        columns_order = ['location', 'latitude', 'longitude', 'datetime'] + [
            col for col in df.columns if col not in ['location', 'latitude', 'longitude', 'datetime']
        ]
        df = df.reindex(columns=columns_order)
        
        # Convert DataFrame to CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()
        
        # Create filename
        safe_location = location.replace(',', '_').replace(' ', '_')
        filename = f"weather_forecast_{safe_location}_{start_date}_to_{end_date}.csv"
        
        return csv_content, filename
    
    def get_weather_forecast(self, location: str, start_date: str, end_date: str, 
                           api_key: str, format_type: str = "json", 
                           include_current: bool = False) -> Dict[str, Any]:
        """
        Get weather forecast in specified format
        
        Args:
            location: Location string
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            api_key: Visual Crossing API key
            format_type: Output format ("json" or "csv")
            include_current: Include current conditions
            
        Returns:
            Weather data in requested format
        """
        weather_data = self.fetch_weather_data(location, start_date, end_date, api_key, include_current)
        
        if format_type.lower() == "csv":
            csv_content, filename = self.convert_to_csv(weather_data, location, start_date, end_date)
            return {
                "content": csv_content,
                "filename": filename,
                "media_type": "text/csv"
            }
        else:
            return weather_data
