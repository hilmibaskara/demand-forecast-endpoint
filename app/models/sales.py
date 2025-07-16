from pydantic import BaseModel, Field
from typing import List, Dict, Any


class SalesUploadResponse(BaseModel):
    message: str
    sales_date: str
    filename: str
    status: str
    unique_products: List[str] = Field(default_factory=list)
    num_unique_products: int = 0
    perishable_products: List[str] = Field(default_factory=list)
    non_perishable_products: List[str] = Field(default_factory=list)
    # ingredient_summary_file: str = ""
    historical_file: str = ""
    ingredients_needed: Dict[str, Any] = Field(default_factory=dict)


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
