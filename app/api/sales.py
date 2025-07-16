import pandas as pd
import io
from fastapi import APIRouter, UploadFile, File, Form
from app.models.sales import (
    SalesUploadResponse, 
    SalesHistoryResponse, 
    SalesDataResponse, 
    PredictDemandResponse
)

from app.services.sales_service import SalesService

router = APIRouter(prefix="/sales", tags=["sales"])
sales_service = SalesService()

@router.get("/history", response_model=SalesHistoryResponse)
async def get_sales_history():
    """
    Get list of available sales history dates
    """
    return SalesHistoryResponse(
        message="Sales history endpoint - placeholder",
        available_dates=["2025-07-06", "2025-07-05", "2025-07-04"]  # Mock data
    )


@router.get("/data/{date}", response_model=SalesDataResponse)
async def get_sales_data(date: str):
    """
    Get sales data for a specific date
    
    Parameters:
    - date: Date in YYYY-MM-DD format
    """
    return SalesDataResponse(
        message=f"Sales data for {date} - placeholder",
        sales_date=date,
        data={"placeholder": "This will contain actual sales data"}
    )


@router.post("/predict-demand", response_model=PredictDemandResponse)
async def predict_demand(date: str = Form(..., description="Date for demand prediction in YYYY-MM-DD format")):
    """
    Predict demand for a specific date
    
    Parameters:
    - date: Date for prediction in YYYY-MM-DD format
    """
    return PredictDemandResponse(
        message=f"Demand prediction for {date} - placeholder",
        sales_date=date,
        prediction={"placeholder": "This will contain AI prediction results"}
    )


@router.post("/upload-history", response_model=SalesUploadResponse)
async def upload_sales_history(
    date: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Upload and process sales history using ETL logic
    
    This endpoint now uses the enhanced ETL process that:
    - Cleans and filters the sales data
    - Identifies perishable vs non-perishable products
    - Maps menu items to ingredient requirements
    - Updates historical ingredient tracking
    - Creates daily ingredient summaries
    """
    content = await file.read()
    
    # Read CSV with proper handling of the format (skip header rows, set column names)
    df = pd.read_csv(io.BytesIO(content), skiprows=2, names=["PRODUK", "JUMLAH", "HARGA"])
    
    # Remove the first row if it contains the column headers
    if len(df) > 0 and str(df.iloc[0]['PRODUK']).upper() == 'PRODUK':
        df = df.iloc[1:].reset_index(drop=True)

    result = sales_service.process_sales_history(date, df)

    return SalesUploadResponse(
        message=f"Sales history uploaded and processed for {date} using ETL logic",
        sales_date=date,
        filename=file.filename,
        status="success",
        unique_products=result["unique_products"],
        num_unique_products=result["num_unique_products"],
        perishable_products=result["perishable_products"],
        non_perishable_products=result["non_perishable_products"],
        # ingredient_summary_file=result["ingredient_summary_file"],
        historical_file=result["historical_file"],
        ingredients_needed=result["ingredients_needed"]
    )