from fastapi import FastAPI, HTTPException, Depends, Query, Body, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
import uuid
from datetime import datetime
import base64
from dotenv import load_dotenv
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/ukraine_experts")
client = AsyncIOMotorClient(MONGO_URL)
db = client.ukraine_experts

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database connection and seed data if needed
    try:
        # Check if we need to seed data
        count = await db.experts.count_documents({})
        if count == 0:
            logger.info("Seeding initial data...")
            
            # Create sample cities
            cities = [
                {
                    "id": str(uuid.uuid4()),
                    "name": "Berlin",
                    "country": "Germany",
                    "coordinates": {"lat": 52.5200, "lng": 13.4050}
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "Paris",
                    "country": "France",
                    "coordinates": {"lat": 48.8566, "lng": 2.3522}
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "Warsaw",
                    "country": "Poland",
                    "coordinates": {"lat": 52.2297, "lng": 21.0122}
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "London",
                    "country": "United Kingdom",
                    "coordinates": {"lat": 51.5074, "lng": -0.1278}
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "Prague",
                    "country": "Czech Republic",
                    "coordinates": {"lat": 50.0755, "lng": 14.4378}
                }
            ]
            
            await db.cities.insert_many(cities)
            
            # Sample expertise areas
            expertise_areas = [
                "Political Science", "Economics", "International Relations", 
                "Humanitarian Aid", "Journalism", "Legal", "Culture", 
                "Education", "Technology", "Medicine", "Agriculture"
            ]
            
            # Create sample experts
            experts = []
            
            # Individual experts
            for i in range(15):
                city = cities[i % len(cities)]
                expert = {
                    "id": str(uuid.uuid4()),
                    "name": f"Ukrainian Expert {i+1}",
                    "type": "individual",
                    "expertise": [expertise_areas[i % len(expertise_areas)], expertise_areas[(i+2) % len(expertise_areas)]],
                    "is_diaspora": i % 3 == 0,
                    "image": None,
                    "title": f"Researcher in {expertise_areas[i % len(expertise_areas)]}",
                    "affiliation": f"University of {city['name']}",
                    "description": f"Expert on Ukrainian issues related to {expertise_areas[i % len(expertise_areas)]} and {expertise_areas[(i+2) % len(expertise_areas)]}.",
                    "city_id": city["id"],
                    "country": city["country"],
                    "contact_email": f"expert{i+1}@example.com",
                    "website": f"https://expert{i+1}.example.com",
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
                experts.append(expert)
            
            # Organizations
            for i in range(10):
                city = cities[i % len(cities)]
                org = {
                    "id": str(uuid.uuid4()),
                    "name": f"Ukraine Organization {i+1}",
                    "type": "organization",
                    "expertise": [expertise_areas[i % len(expertise_areas)], expertise_areas[(i+1) % len(expertise_areas)]],
                    "is_diaspora": i % 2 == 0,
                    "image": None,
                    "description": f"Organization focused on {expertise_areas[i % len(expertise_areas)]} and {expertise_areas[(i+1) % len(expertise_areas)]} in Ukraine and Europe.",
                    "city_id": city["id"],
                    "country": city["country"],
                    "contact_email": f"org{i+1}@example.com",
                    "website": f"https://org{i+1}.example.com",
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
                experts.append(org)
            
            await db.experts.insert_many(experts)
            logger.info(f"Seeded {len(cities)} cities and {len(experts)} experts")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
    
    yield
    # Shutdown: Clean up resources if needed
    pass

# Initialize FastAPI app with lifespan
app = FastAPI(title="Ukraine Experts API", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ExpertBase(BaseModel):
    name: str
    type: str = "individual"  # individual or organization
    expertise: List[str] = []
    is_diaspora: bool = False
    image: Optional[str] = None
    title: Optional[str] = None
    affiliation: Optional[str] = None
    description: Optional[str] = None
    city_id: Optional[str] = None
    country: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    social_media: Optional[Dict[str, str]] = None

class ExpertCreate(ExpertBase):
    pass

class ExpertUpdate(ExpertBase):
    name: Optional[str] = None
    type: Optional[str] = None
    expertise: Optional[List[str]] = None
    is_diaspora: Optional[bool] = None

class ExpertInDB(ExpertBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class City(BaseModel):
    id: str
    name: str
    country: str
    coordinates: Optional[Dict[str, float]] = None

class Statistics(BaseModel):
    total_entries: int
    by_type: Dict[str, int] 
    by_city: List[Dict[str, Any]]
    by_expertise: List[Dict[str, int]]

# Helper functions
async def get_expert_by_id(expert_id: str):
    expert = await db.experts.find_one({"id": expert_id})
    if expert:
        return expert
    raise HTTPException(status_code=404, detail=f"Expert with ID {expert_id} not found")



# API Routes
@app.get("/api/experts", response_model=List[dict])
async def get_experts(
    type: Optional[str] = None,
    city_id: Optional[str] = None,
    expertise: Optional[str] = None,
    is_diaspora: Optional[bool] = None,
    search: Optional[str] = None,
    limit: int = Query(100, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    """Get all experts with optional filtering"""
    query = {}
    
    if type:
        query["type"] = type
    
    if city_id:
        query["city_id"] = city_id
    
    if expertise:
        query["expertise"] = {"$in": [expertise]}
    
    if is_diaspora is not None:
        query["is_diaspora"] = is_diaspora
    
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"expertise": {"$regex": search, "$options": "i"}}
        ]
    
    cursor = db.experts.find(query).skip(skip).limit(limit)
    experts = await cursor.to_list(length=limit)
    
    # Convert MongoDB ObjectId to string for JSON serialization
    for expert in experts:
        if "_id" in expert:
            del expert["_id"]
    
    return experts

@app.get("/api/experts/{expert_id}", response_model=dict)
async def get_expert(expert_id: str):
    """Get expert by ID"""
    expert = await get_expert_by_id(expert_id)
    
    # Convert MongoDB ObjectId to string for JSON serialization
    if "_id" in expert:
        del expert["_id"]
    
    return expert

@app.post("/api/experts", response_model=dict)
async def create_expert(expert: ExpertCreate):
    """Create a new expert"""
    expert_dict = expert.model_dump()
    
    # Add additional fields
    expert_dict["id"] = str(uuid.uuid4())
    expert_dict["created_at"] = datetime.now()
    expert_dict["updated_at"] = datetime.now()
    
    # Insert into database
    await db.experts.insert_one(expert_dict)
    
    # Remove MongoDB ObjectId for JSON serialization
    if "_id" in expert_dict:
        del expert_dict["_id"]
    
    return expert_dict

@app.put("/api/experts/{expert_id}", response_model=dict)
async def update_expert(expert_id: str, expert_update: ExpertUpdate):
    """Update an expert by ID"""
    # Check if expert exists
    await get_expert_by_id(expert_id)
    
    # Prepare update dictionary (only non-None fields)
    update_data = {
        k: v for k, v in expert_update.model_dump(exclude_unset=True).items() 
        if v is not None
    }
    
    # Add updated timestamp
    update_data["updated_at"] = datetime.now()
    
    # Update in database
    await db.experts.update_one(
        {"id": expert_id},
        {"$set": update_data}
    )
    
    # Return updated expert
    updated_expert = await get_expert_by_id(expert_id)
    if "_id" in updated_expert:
        del updated_expert["_id"]
    
    return updated_expert

@app.delete("/api/experts/{expert_id}", response_model=dict)
async def delete_expert(expert_id: str):
    """Delete an expert by ID"""
    # Check if expert exists
    await get_expert_by_id(expert_id)
    
    # Delete from database
    await db.experts.delete_one({"id": expert_id})
    
    return {"message": f"Expert with ID {expert_id} deleted successfully"}

@app.post("/api/experts/{expert_id}/image", response_model=dict)
async def upload_expert_image(
    expert_id: str, 
    image: UploadFile = File(...),
):
    """Upload an image for an expert"""
    # Check if expert exists
    await get_expert_by_id(expert_id)
    
    # Read and encode image to base64
    image_content = await image.read()
    base64_image = base64.b64encode(image_content).decode('utf-8')
    image_data = f"data:{image.content_type};base64,{base64_image}"
    
    # Update expert with image
    await db.experts.update_one(
        {"id": expert_id},
        {
            "$set": {
                "image": image_data,
                "updated_at": datetime.now()
            }
        }
    )
    
    return {"message": "Image uploaded successfully"}

@app.get("/api/cities", response_model=List[dict])
async def get_cities():
    """Get all cities"""
    cities = await db.cities.find().to_list(length=100)
    
    # Convert MongoDB ObjectId to string for JSON serialization
    for city in cities:
        if "_id" in city:
            del city["_id"]
    
    return cities

@app.get("/api/statistics", response_model=dict)
async def get_statistics():
    """Get database statistics"""
    # Total entries
    total_entries = await db.experts.count_documents({})
    
    # By type
    individual_count = await db.experts.count_documents({"type": "individual"})
    organization_count = await db.experts.count_documents({"type": "organization"})
    
    # By city
    pipeline = [
        {"$group": {"_id": "$city_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    by_city_results = await db.experts.aggregate(pipeline).to_list(length=100)
    
    city_stats = []
    for result in by_city_results:
        if result["_id"]:
            city = await db.cities.find_one({"id": result["_id"]})
            if city:
                city_stats.append({
                    "city_id": result["_id"],
                    "name": city["name"],
                    "country": city["country"],
                    "count": result["count"]
                })
    
    # By expertise (get top 10)
    pipeline = [
        {"$unwind": "$expertise"},
        {"$group": {"_id": "$expertise", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    by_expertise_results = await db.experts.aggregate(pipeline).to_list(length=10)
    
    expertise_stats = [
        {"expertise": result["_id"], "count": result["count"]}
        for result in by_expertise_results
    ]
    
    return {
        "total_entries": total_entries,
        "by_type": {
            "individual": individual_count,
            "organization": organization_count
        },
        "by_city": city_stats,
        "by_expertise": expertise_stats
    }

# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
