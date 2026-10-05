import json
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.schema import Area, ServiceHistory, DiseaseRisk, MobilityPattern
from app.models.pydantic_models import AreaDetail

router = APIRouter(prefix="/areas", tags=["Areas"])

@router.get("", response_model=List[AreaDetail])
def list_areas(db: Session = Depends(get_db)):
    areas = db.query(Area).all()
    result = []
    
    for area in areas:
        # Fetch latest service history, risk, mobility
        hist = db.query(ServiceHistory).filter(ServiceHistory.area_id == area.area_id).first()
        risk = db.query(DiseaseRisk).filter(DiseaseRisk.area_id == area.area_id).first()
        mobility = db.query(MobilityPattern).filter(MobilityPattern.area_id == area.area_id).first()

        vaccinated = hist.vaccinated_count if hist else 0
        elig = area.eligible_population
        coverage = (vaccinated / elig * 100) if elig > 0 else 0.0
        gap_ratio = (1.0 - (vaccinated / elig)) if elig > 0 else 0.0

        result.append(AreaDetail(
            area_id=area.area_id,
            area_name=area.area_name,
            zone_type=area.zone_type,
            population=area.population,
            eligible_population=area.eligible_population,
            accessibility_index=area.accessibility_index,
            latitude=area.latitude,
            longitude=area.longitude,
            distance_from_base_km=area.distance_from_base_km,
            vaccinated_count=vaccinated,
            vaccination_coverage=round(coverage, 1),
            service_gap_ratio=round(gap_ratio, 3),
            historical_demand=hist.historical_demand if hist else 0,
            seasonal_risk=risk.seasonal_risk if risk else 0.0,
            emerging_risk=risk.emerging_risk if risk else 0.0,
            mobility_index=mobility.mobility_index if mobility else 0.0,
            inflow_index=mobility.inflow_index if mobility else 0.0,
            outflow_index=mobility.outflow_index if mobility else 0.0
        ))
    return result

@router.get("/geojson")
def get_areas_geojson(db: Session = Depends(get_db)):
    """
    Returns valid GeoJSON FeatureCollection representing synthetic city zone boundaries
    enriched with live database risk, coverage, and demographic indicators.
    """
    geojson_path = os.path.join(os.path.dirname(__file__), "..", "data", "city_zones.geojson")
    if not os.path.exists(geojson_path):
        raise HTTPException(status_code=404, detail="City zones GeoJSON file not found.")

    with open(geojson_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Enrich GeoJSON feature properties with live DB indicators
    areas_list = list_areas(db)
    area_dict = {a.area_id: a for a in areas_list}

    for feature in data.get("features", []):
        aid = feature.get("properties", {}).get("area_id")
        if aid in area_dict:
            a = area_dict[aid]
            feature["properties"].update({
                "population": a.population,
                "eligible_population": a.eligible_population,
                "accessibility_index": a.accessibility_index,
                "vaccinated_count": a.vaccinated_count,
                "vaccination_coverage": a.vaccination_coverage,
                "seasonal_risk": a.seasonal_risk,
                "emerging_risk": a.emerging_risk,
                "mobility_index": a.mobility_index
            })

    return data

@router.get("/{area_id}", response_model=AreaDetail)
def get_area(area_id: str, db: Session = Depends(get_db)):
    area = db.query(Area).filter(Area.area_id == area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    
    hist = db.query(ServiceHistory).filter(ServiceHistory.area_id == area.area_id).first()
    risk = db.query(DiseaseRisk).filter(DiseaseRisk.area_id == area.area_id).first()
    mobility = db.query(MobilityPattern).filter(MobilityPattern.area_id == area.area_id).first()

    vaccinated = hist.vaccinated_count if hist else 0
    elig = area.eligible_population
    coverage = (vaccinated / elig * 100) if elig > 0 else 0.0
    gap_ratio = (1.0 - (vaccinated / elig)) if elig > 0 else 0.0

    return AreaDetail(
        area_id=area.area_id,
        area_name=area.area_name,
        zone_type=area.zone_type,
        population=area.population,
        eligible_population=area.eligible_population,
        accessibility_index=area.accessibility_index,
        latitude=area.latitude,
        longitude=area.longitude,
        distance_from_base_km=area.distance_from_base_km,
        vaccinated_count=vaccinated,
        vaccination_coverage=round(coverage, 1),
        service_gap_ratio=round(gap_ratio, 3),
        historical_demand=hist.historical_demand if hist else 0,
        seasonal_risk=risk.seasonal_risk if risk else 0.0,
        emerging_risk=risk.emerging_risk if risk else 0.0,
        mobility_index=mobility.mobility_index if mobility else 0.0,
        inflow_index=mobility.inflow_index if mobility else 0.0,
        outflow_index=mobility.outflow_index if mobility else 0.0
    )
