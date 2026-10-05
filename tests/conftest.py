import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.models.schema import Area, ServiceHistory, DiseaseRisk, MobilityPattern
from app.data.seed_data import SEED_AREAS
from main import app

# In-memory SQLite DB engine using StaticPool for isolated unit testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_engine():
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    
    # Populate test database with standard synthetic seed areas
    time_period = "2026-Q4"
    for area_data in SEED_AREAS:
        area = Area(
            area_id=area_data["area_id"],
            area_name=area_data["area_name"],
            zone_type=area_data["zone_type"],
            population=area_data["population"],
            eligible_population=area_data["eligible_population"],
            accessibility_index=area_data["accessibility_index"],
            latitude=area_data["latitude"],
            longitude=area_data["longitude"],
            distance_from_base_km=area_data["distance_from_base_km"]
        )
        session.add(area)

        history = ServiceHistory(
            area_id=area_data["area_id"],
            time_period=time_period,
            eligible_population=area_data["eligible_population"],
            vaccinated_count=area_data["vaccinated_count"],
            service_visits=area_data["service_visits"],
            historical_demand=area_data["historical_demand"]
        )
        session.add(history)

        risk = DiseaseRisk(
            area_id=area_data["area_id"],
            time_period=time_period,
            seasonal_risk=area_data["seasonal_risk"],
            emerging_risk=area_data["emerging_risk"],
            surveillance_signal_date="2026-09-01"
        )
        session.add(risk)

        mobility = MobilityPattern(
            area_id=area_data["area_id"],
            time_period=time_period,
            mobility_index=area_data["mobility_index"],
            inflow_index=area_data["inflow_index"],
            outflow_index=area_data["outflow_index"]
        )
        session.add(mobility)

    # Seed demo users for auth testing
    from app.models.schema import User
    from app.core.auth import get_password_hash
    session.add(User(
        user_id="usr-admin-test",
        username="admin",
        hashed_password=get_password_hash("AdminPass123!"),
        role="ADMIN",
        full_name="System Administrator",
        is_active=True
    ))
    session.add(User(
        user_id="usr-clinician-test",
        username="clinician",
        hashed_password=get_password_hash("ClinicianPass123!"),
        role="CLINICIAN",
        full_name="Dr. Sarah Chen",
        is_active=True
    ))

    session.commit()

    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def admin_headers(client):
    res = client.post("/api/auth/login", json={"username": "admin", "password": "AdminPass123!"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def clinician_headers(client):
    res = client.post("/api/auth/login", json={"username": "clinician", "password": "ClinicianPass123!"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

