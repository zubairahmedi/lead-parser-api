from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Lead Parser API")

# Flexible input model - all fields optional
class LeadInput(BaseModel):
    lead_id: Optional[str] = None
    date_posted: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    best_time_to_contact: Optional[str] = None
    collection: Optional[str] = None
    franchise_coordinator: Optional[str] = None
    timeframe: Optional[str] = None
    liquid_capital: Optional[str] = None
    net_worth: Optional[str] = None
    comments: Optional[str] = None

# POST /parse endpoint
@app.post("/parse")
def parse_lead(data: LeadInput):
    # Return only non-null fields
    result = {k: v for k, v in data.dict().items() if v is not None}
    return result if result else {"error": "No data provided"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}
