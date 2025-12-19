from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI(title="Lead Parser API")

# Input model
class LeadInput(BaseModel):
    text: str

# Regex to extract lead fields
pattern = re.compile(
    r"Lead ID:\s*(\d+)\s*"
    r"Date Posted:\s*([0-9\/:\s]+)\s*"
    r"First Name:\s*([^\r\n]+)\s*"
    r"Last Name:\s*([^\r\n]+)\s*"
    r"Address:\s*([^\r\n]+)\s*"
    r"City:\s*([^\r\n]+)\s*"
    r"State:\s*([A-Z]{2})\s*"
    r"Zip:\s*(\d{5})\s*"
    r"Email:\s*([^\s]+)\s*"
    r"Phone:\s*(\d+)\s*"
    r"Best Time to Contact:\s*([^\r\n]+)\s*"
    r"Collection:\s*([^\r\n]+)\s*"
    r"Franchise Coordinator:\s*([^\r\n]+)\s*"
    r"Timeframe to Start Business:\s*([^\r\n]+)\s*"
    r"Liquid Capital to Invest:\s*([^\r\n]+)\s*"
    r"Net Worth.*:\s*([^\r\n]+)\s*"
    r"Comments:\s*([\s\S]*?)(?=\n\n(?:On\s|zubair|>)|\Z)",
    re.MULTILINE
)

keys = [
    "lead_id",
    "date_posted",
    "first_name",
    "last_name",
    "address",
    "city",
    "state",
    "zip",
    "email",
    "phone",
    "best_time_to_contact",
    "collection",
    "franchise_coordinator",
    "timeframe",
    "liquid_capital",
    "net_worth",
    "comments"
]

# POST /parse endpoint
@app.post("/parse")
def parse_lead(data: LeadInput):
    # Match regex
    match = pattern.search(data.text)
    if not match:
        return {"error": "Invalid lead format"}

    # Convert to JSON
    result = dict(zip(keys, match.groups()))
    
    # Strip trailing whitespace from comments
    if 'comments' in result:
        result['comments'] = result['comments'].strip()
    
    return result

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}
