from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
import io
from app.services.weather_service import WeatherService
from app.models.weather import WeatherForecastRequest


router = APIRouter(prefix="/weather", tags=["weather"])
weather_service = WeatherService()


@router.get("/forecast")
async def get_weather_forecast(
    location: str = Query(..., description="Location (city, address, or coordinates lat,lon)"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    api_key: str = Query(..., description="Visual Crossing Weather API key"),
    format_type: str = Query("json", description="Output format: 'json' or 'csv'"),
    include_current: bool = Query(False, description="Include current conditions")
):
    """
    Get weather forecast data for a specific location and date range.
    
    Parameters:
    - location: City name, address, or coordinates (lat,lon)
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - api_key: Your Visual Crossing Weather API key
    - format_type: Output format ('json' or 'csv')
    - include_current: Whether to include current weather conditions
    """
    
    result = weather_service.get_weather_forecast(
        location=location,
        start_date=start_date,
        end_date=end_date,
        api_key=api_key,
        format_type=format_type,
        include_current=include_current
    )
    
    if format_type.lower() == "csv":
        return StreamingResponse(
            io.StringIO(result["content"]),
            media_type=result["media_type"],
            headers={"Content-Disposition": f"attachment; filename={result['filename']}"}
        )
    else:
        return result


# Backward compatibility endpoints
@router.get("/forecast/json")
async def get_weather_forecast_json(
    location: str = Query(..., description="Location (city, address, or coordinates lat,lon)"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    api_key: str = Query(..., description="Visual Crossing Weather API key")
):
    """Get weather forecast data in JSON format (backward compatibility)"""
    return await get_weather_forecast(location, start_date, end_date, api_key, "json", False)


@router.get("/forecast/csv")
async def get_weather_forecast_csv(
    location: str = Query(..., description="Location (city, address, or coordinates lat,lon)"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    api_key: str = Query(..., description="Visual Crossing Weather API key"),
    include_current: bool = Query(False, description="Include current conditions")
):
    """Get weather forecast data in CSV format (backward compatibility)"""
    return await get_weather_forecast(location, start_date, end_date, api_key, "csv", include_current)
