from fastapi import FastAPI
from app.api.weather import router as weather_router

# Initialize FastAPI app
app = FastAPI(
    title="Demand Forecast Endpoint",
    description="API for weather forecasting and AI inference",
    version="1.0.0"
)

# Include routers
app.include_router(weather_router)

@app.get("/")
async def root():
    return {
        "message": "Demand Forecast API - Weather & AI Inference Service",
        "version": "1.0.0",
        "endpoints": {
            "weather_forecast": "/weather/forecast",
            "weather_forecast_json": "/weather/forecast/json",
            "weather_forecast_csv": "/weather/forecast/csv"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "demand-forecast-endpoint"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
