from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.core.database import get_db, engine
from app.data.seed_data import init_db_and_seed
from app.api import areas, planner, reviews, eval as eval_api, auth, forecast

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Vaccination Outreach Planner API...")
    init_db_and_seed()
    yield
    print("Shutting down Vaccination Outreach Planner API...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="City Health Department Seasonal Infectious Disease Vaccination Outreach Planner API",
    lifespan=lifespan
)

# Configure CORS using environment-configured origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(areas.router, prefix=settings.API_PREFIX)
app.include_router(planner.router, prefix=settings.API_PREFIX)
app.include_router(reviews.router, prefix=settings.API_PREFIX)
app.include_router(eval_api.router, prefix=settings.API_PREFIX)
app.include_router(forecast.router, prefix=settings.API_PREFIX)

@app.get("/")
def root():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """
    Liveness probe endpoint returning basic operational status.
    """
    return {
        "status": "UP",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }

@app.get("/readiness", status_code=status.HTTP_200_OK)
def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness probe verifying database connectivity.
    """
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "READY",
            "database": "CONNECTED",
            "service": settings.PROJECT_NAME
        }
    except Exception as e:
        return {
            "status": "NOT_READY",
            "database": f"DISCONNECTED: {str(e)}",
            "service": settings.PROJECT_NAME
        }, status.HTTP_503_SERVICE_UNAVAILABLE

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
