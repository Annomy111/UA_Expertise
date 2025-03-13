from fastapi import FastAPI, HTTPException, Query, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import uvicorn
from enum import Enum
import uuid

import db_utils

app = FastAPI(
    title="Ukraine Experts Database API",
    description="API for accessing and managing the database of Ukrainian experts and organizations in Europe",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint for Render
@app.get("/health")
def health_check():
    return {"status": "OK"}

# Enums for validation
class ExpertType(str, Enum):
    individual = "individual"
    organization = "organization"

class FocusArea(str, Enum):
    advocacy = "advocacy"
    humanitarian = "humanitarian"
    cultural_diplomacy = "cultural_diplomacy"
    political_mobilization = "political_mobilization"
    research = "research"
    policy_analysis = "policy_analysis"
    community_support = "community_support"
    integration = "integration"
    education = "education"
    media = "media"

# Models
class City(BaseModel):
    id: int
    name: str
    country: str
    description: Optional[str] = None

class Contact(BaseModel):
    type: str
    value: str
    is_primary: bool = False

class KeyFigure(BaseModel):
    name: str
    role: Optional[str] = None
    description: Optional[str] = None

class ExpertCreate(BaseModel):
    name: str
    type: ExpertType
    title: Optional[str] = None
    affiliation: Optional[str] = None
    city_id: int
    description: Optional[str] = None
    founding_year: Optional[int] = None
    is_diaspora: bool = False
    focus_areas: List[FocusArea] = []
    contacts: List[Contact] = []
    key_figures: List[KeyFigure] = []
    tags: List[str] = []

class ExpertUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    affiliation: Optional[str] = None
    city_id: Optional[int] = None
    description: Optional[str] = None
    founding_year: Optional[int] = None
    is_diaspora: Optional[bool] = None
    image: Optional[str] = None
    focus_areas: Optional[List[FocusArea]] = None
    contacts: Optional[List[Contact]] = None
    key_figures: Optional[List[KeyFigure]] = None
    tags: Optional[List[str]] = None

# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to the Ukraine Experts Database API"}

@app.get("/cities", response_model=List[City])
def get_cities():
    """Get all cities in the database."""
    return db_utils.get_all_cities()

@app.get("/experts/city/{city_id}")
def get_experts_by_city(city_id: int = Path(..., description="The ID of the city")):
    """Get all experts for a specific city."""
    return db_utils.get_experts_by_city(city_id)

@app.get("/organizations")
def get_organizations(city_id: Optional[int] = Query(None, description="Filter by city ID")):
    """Get organizations with their key figures, optionally filtered by city."""
    return db_utils.get_organizations_with_key_figures(city_id)

@app.get("/experts/{expert_id}")
def get_expert_details(expert_id: str = Path(..., description="The ID of the expert")):
    """Get detailed information about an expert or organization."""
    expert = db_utils.get_expert_details(expert_id)
    if not expert:
        raise HTTPException(status_code=404, detail="Expert not found")
    return expert

@app.get("/search")
def search_experts(q: str = Query(..., description="Search term")):
    """Search for experts by name, description, or tags."""
    return db_utils.search_experts(q)

@app.get("/experts/focus/{focus_area}")
def get_experts_by_focus(focus_area: FocusArea = Path(..., description="The focus area to filter by")):
    """Get experts by focus area."""
    return db_utils.get_experts_by_focus_area(focus_area)

@app.get("/diaspora/organizations")
def get_diaspora_organizations():
    """Get all diaspora organizations."""
    return db_utils.get_diaspora_organizations()

@app.post("/experts", status_code=201)
def create_expert(expert: ExpertCreate = Body(...)):
    """Add a new expert or organization to the database."""
    try:
        expert_id = db_utils.add_expert(expert.dict())
        return {"id": expert_id, "message": "Expert created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/experts/{expert_id}")
def update_expert(
    expert_id: str = Path(..., description="The ID of the expert to update"),
    expert_data: ExpertUpdate = Body(...)
):
    """Update an existing expert or organization."""
    # First check if expert exists
    existing = db_utils.get_expert_details(expert_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Expert not found")
    
    # Filter out None values
    update_data = {k: v for k, v in expert_data.dict().items() if v is not None}
    
    try:
        success = db_utils.update_expert(expert_id, update_data)
        if success:
            return {"message": "Expert updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to update expert")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/experts/{expert_id}")
def delete_expert(expert_id: str = Path(..., description="The ID of the expert to delete")):
    """Delete an expert or organization."""
    # First check if expert exists
    existing = db_utils.get_expert_details(expert_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Expert not found")
    
    success = db_utils.delete_expert(expert_id)
    if success:
        return {"message": "Expert deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to delete expert")

@app.get("/statistics")
def get_statistics():
    """Get database statistics."""
    return db_utils.get_statistics()

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True) 