from pydantic import BaseModel, Field
from typing import List, Dict, Any


class SalesUploadResponse(BaseModel):
    message: str
    sales_date: str
    filename: str
    status: str


class SalesHistoryResponse(BaseModel):
    message: str
    available_dates: List[str]


class SalesDataResponse(BaseModel):
    message: str
    sales_date: str
    data: Dict[str, Any]


class PredictDemandResponse(BaseModel):
    message: str
    sales_date: str
    prediction: Dict[str, Any]
