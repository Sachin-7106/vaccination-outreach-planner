from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.data.seed_data import init_db_and_seed
from app.api import areas, planner, reviews, eval as eval_api

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="City Health Department Seasonal Infectious Disease Vaccination Outreach Planner API"
)

# Configure CORS for local React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("Starting Vaccination Outreach Planner API...")
    init_db_and_seed()

# Include Routers
app.include_router(areas.router, prefix=settings.API_PREFIX)
app.include_router(planner.router, prefix=settings.API_PREFIX)
app.include_router(reviews.router, prefix=settings.API_PREFIX)
app.include_router(eval_api.router, prefix=settings.API_PREFIX)

@app.get("/")
def root():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
