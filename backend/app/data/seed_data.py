import uuid
from app.core.database import SessionLocal, engine, Base
from app.models.schema import Area, ServiceHistory, DiseaseRisk, MobilityPattern, OutreachSession, Recommendation, Review

SEED_AREAS = [
    {
        "area_id": "AREA-01",
        "area_name": "Metro Central Corridor",
        "zone_type": "High-Density Urban",
        "population": 18500,
        "eligible_population": 4200,
        "accessibility_index": 0.95,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "distance_from_base_km": 3.2,
        "vaccinated_count": 3100,
        "service_visits": 450,
        "historical_demand": 410,
        "seasonal_risk": 0.45,
        "emerging_risk": 0.38,
        "mobility_index": 0.85,
        "inflow_index": 0.90,
        "outflow_index": 0.80
    },
    {
        "area_id": "AREA-02",
        "area_name": "Northwood Hills Suburb",
        "zone_type": "Suburban Low-Density",
        "population": 12000,
        "eligible_population": 2100,
        "accessibility_index": 0.88,
        "latitude": 40.7484,
        "longitude": -73.9857,
        "distance_from_base_km": 6.5,
        "vaccinated_count": 1820,
        "service_visits": 310,
        "historical_demand": 290,
        "seasonal_risk": 0.25,
        "emerging_risk": 0.20,
        "mobility_index": 0.40,
        "inflow_index": 0.35,
        "outflow_index": 0.45
    },
    {
        "area_id": "AREA-03",
        "area_name": "Riverside Industrial Dock",
        "zone_type": "Industrial Worker Zone",
        "population": 9400,
        "eligible_population": 3600,
        "accessibility_index": 0.65,
        "latitude": 40.6892,
        "longitude": -74.0445,
        "distance_from_base_km": 9.1,
        "vaccinated_count": 1400,
        "service_visits": 210,
        "historical_demand": 195,
        "seasonal_risk": 0.60,
        "emerging_risk": 0.55,
        "mobility_index": 0.72,
        "inflow_index": 0.78,
        "outflow_index": 0.66
    },
    {
        "area_id": "AREA-04",
        "area_name": "Southside informal Settlement",
        "zone_type": "Under-Served Settlement",
        "population": 15800,
        "eligible_population": 5100,
        "accessibility_index": 0.42,
        "latitude": 40.6501,
        "longitude": -73.9496,
        "distance_from_base_km": 11.4,
        "vaccinated_count": 1250,
        "service_visits": 180,
        "historical_demand": 160,
        "seasonal_risk": 0.82,
        "emerging_risk": 0.89,
        "mobility_index": 0.78,
        "inflow_index": 0.75,
        "outflow_index": 0.81
    },
    {
        "area_id": "AREA-05",
        "area_name": "West Valley Transit Hub",
        "zone_type": "Transit Corridor",
        "population": 11200,
        "eligible_population": 3900,
        "accessibility_index": 0.91,
        "latitude": 40.7282,
        "longitude": -74.0776,
        "distance_from_base_km": 5.8,
        "vaccinated_count": 2100,
        "service_visits": 340,
        "historical_demand": 320,
        "seasonal_risk": 0.58,
        "emerging_risk": 0.64,
        "mobility_index": 0.94,
        "inflow_index": 0.96,
        "outflow_index": 0.92
    },
    {
        "area_id": "AREA-06",
        "area_name": "Highland Park Residential",
        "zone_type": "Suburban Residential",
        "population": 8900,
        "eligible_population": 1600,
        "accessibility_index": 0.82,
        "latitude": 40.7831,
        "longitude": -73.9712,
        "distance_from_base_km": 8.0,
        "vaccinated_count": 1350,
        "service_visits": 240,
        "historical_demand": 225,
        "seasonal_risk": 0.30,
        "emerging_risk": 0.22,
        "mobility_index": 0.32,
        "inflow_index": 0.30,
        "outflow_index": 0.34
    },
    {
        "area_id": "AREA-07",
        "area_name": "Eastside Railway Market",
        "zone_type": "Mobile Vendor Settlement",
        "population": 14200,
        "eligible_population": 4800,
        "accessibility_index": 0.55,
        "latitude": 40.7061,
        "longitude": -73.9210,
        "distance_from_base_km": 7.8,
        "vaccinated_count": 980,  # Low coverage!
        "service_visits": 110,  # Low historical visits!
        "historical_demand": 95,   # Low historical demand!
        "seasonal_risk": 0.88,  # HIGH seasonal risk!
        "emerging_risk": 0.96,  # CRITICAL EMERGING RISK SPIKE!
        "mobility_index": 0.91,
        "inflow_index": 0.94,
        "outflow_index": 0.88
    },
    {
        "area_id": "AREA-08",
        "area_name": "Old Town Commercial District",
        "zone_type": "Urban Commercial",
        "population": 16500,
        "eligible_population": 2900,
        "accessibility_index": 0.96,
        "latitude": 40.7190,
        "longitude": -74.0000,
        "distance_from_base_km": 2.1,
        "vaccinated_count": 2350,
        "service_visits": 380,
        "historical_demand": 360,
        "seasonal_risk": 0.40,
        "emerging_risk": 0.35,
        "mobility_index": 0.82,
        "inflow_index": 0.88,
        "outflow_index": 0.76
    },
    {
        "area_id": "AREA-09",
        "area_name": "Pine Ridge Seasonal Camp",
        "zone_type": "Migrant / Temporary Housing",
        "population": 7300,
        "eligible_population": 3100,
        "accessibility_index": 0.38,
        "latitude": 40.6120,
        "longitude": -74.1200,
        "distance_from_base_km": 16.5,  # Exceeds standard 12km travel limit!
        "vaccinated_count": 620,
        "service_visits": 85,
        "historical_demand": 70,
        "seasonal_risk": 0.75,
        "emerging_risk": 0.84,
        "mobility_index": 0.85,
        "inflow_index": 0.89,
        "outflow_index": 0.81
    },
    {
        "area_id": "AREA-10",
        "area_name": "Sunset District Waterfront",
        "zone_type": "Mixed Residential/Tourism",
        "population": 10500,
        "eligible_population": 2200,
        "accessibility_index": 0.79,
        "latitude": 40.7600,
        "longitude": -73.9900,
        "distance_from_base_km": 4.9,
        "vaccinated_count": 1780,
        "service_visits": 270,
        "historical_demand": 250,
        "seasonal_risk": 0.35,
        "emerging_risk": 0.30,
        "mobility_index": 0.65,
        "inflow_index": 0.70,
        "outflow_index": 0.60
    },
    {
        "area_id": "AREA-11",
        "area_name": "College Heights Campus",
        "zone_type": "Student / High Mobility",
        "population": 19800,
        "eligible_population": 4500,
        "accessibility_index": 0.92,
        "latitude": 40.8075,
        "longitude": -73.9626,
        "distance_from_base_km": 14.2,  # Travel flag (14.2km > 12km)
        "vaccinated_count": 2900,
        "service_visits": 410,
        "historical_demand": 380,
        "seasonal_risk": 0.52,
        "emerging_risk": 0.68,
        "mobility_index": 0.96,
        "inflow_index": 0.98,
        "outflow_index": 0.94
    },
    {
        "area_id": "AREA-12",
        "area_name": "Harbor View Agricultural Edge",
        "zone_type": "Peri-Urban Agricultural",
        "population": 6100,
        "eligible_population": 2400,
        "accessibility_index": 0.45,
        "latitude": 40.5800,
        "longitude": -74.1600,
        "distance_from_base_km": 18.8,  # Remote area
        "vaccinated_count": 710,
        "service_visits": 95,
        "historical_demand": 80,
        "seasonal_risk": 0.68,
        "emerging_risk": 0.72,
        "mobility_index": 0.52,
        "inflow_index": 0.48,
        "outflow_index": 0.56
    }
]

def init_db_and_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(Area).count() > 0:
            print("Database already contains seed data.")
            return

        print("Seeding database with synthetic public health datasets...")
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
            db.add(area)

            history = ServiceHistory(
                area_id=area_data["area_id"],
                time_period=time_period,
                eligible_population=area_data["eligible_population"],
                vaccinated_count=area_data["vaccinated_count"],
                service_visits=area_data["service_visits"],
                historical_demand=area_data["historical_demand"]
            )
            db.add(history)

            risk = DiseaseRisk(
                area_id=area_data["area_id"],
                time_period=time_period,
                seasonal_risk=area_data["seasonal_risk"],
                emerging_risk=area_data["emerging_risk"],
                surveillance_signal_date="2026-09-01"
            )
            db.add(risk)

            mobility = MobilityPattern(
                area_id=area_data["area_id"],
                time_period=time_period,
                mobility_index=area_data["mobility_index"],
                inflow_index=area_data["inflow_index"],
                outflow_index=area_data["outflow_index"]
            )
            db.add(mobility)

        db.commit()

        # Seed sample past completed outreach sessions for baseline calculation
        sample_sessions = [
            OutreachSession(
                session_id=str(uuid.uuid4()),
                area_id="AREA-01",
                planning_period="2026-Q3",
                scheduled_date="2026-08-10",
                capacity=300,
                planned_reach=300,
                actual_reach=285,
                travel_distance_km=3.2,
                status="COMPLETED"
            ),
            OutreachSession(
                session_id=str(uuid.uuid4()),
                area_id="AREA-08",
                planning_period="2026-Q3",
                scheduled_date="2026-08-14",
                capacity=300,
                planned_reach=300,
                actual_reach=290,
                travel_distance_km=2.1,
                status="COMPLETED"
            ),
            OutreachSession(
                session_id=str(uuid.uuid4()),
                area_id="AREA-05",
                planning_period="2026-Q3",
                scheduled_date="2026-08-18",
                capacity=300,
                planned_reach=300,
                actual_reach=270,
                travel_distance_km=5.8,
                status="COMPLETED"
            )
        ]
        for sess in sample_sessions:
            db.add(sess)
        db.commit()

        print("Database seeding completed successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    init_db_and_seed()
