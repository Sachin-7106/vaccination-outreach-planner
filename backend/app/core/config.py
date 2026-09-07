import os

class Settings:
    PROJECT_NAME: str = "Vaccination Outreach Planner"
    VERSION: str = "1.0.0-phase1"
    API_PREFIX: str = "/api"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./city_health.db")

settings = Settings()
