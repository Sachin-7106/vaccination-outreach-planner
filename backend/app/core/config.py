import os

class Settings:
    PROJECT_NAME: str = "Vaccination Outreach Planner"
    VERSION: str = "1.0.0-final"
    API_PREFIX: str = "/api"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./city_health.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "city_health_super_secret_jwt_key_2026_change_in_prod")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    @property
    def cors_origins(self):
        raw = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:8000")
        return [origin.strip() for origin in raw.split(",") if origin.strip()]

settings = Settings()
