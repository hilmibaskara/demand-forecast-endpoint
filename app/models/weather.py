from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class WeatherForecastRequest(BaseModel):
    location: str = Field(..., description="Location (city, address, or coordinates lat,lon)")
    start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: str = Field(..., description="End date in YYYY-MM-DD format")
    api_key: str = Field(..., description="Visual Crossing Weather API key")
    include_current: bool = Field(False, description="Include current conditions")


class WeatherForecastResponse(BaseModel):
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    start_date: str
    end_date: str
    forecast_data: dict
