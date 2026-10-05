from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Area(Base):
    __tablename__ = "areas"

    area_id = Column(String(20), primary_key=True, index=True)
    area_name = Column(String(100), nullable=False)
    zone_type = Column(String(50), nullable=False)
    population = Column(Integer, nullable=False)
    eligible_population = Column(Integer, nullable=False)
    accessibility_index = Column(Float, nullable=False)  # 0.0 to 1.0
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    distance_from_base_km = Column(Float, nullable=False)

    service_histories = relationship("ServiceHistory", back_populates="area")
    disease_risks = relationship("DiseaseRisk", back_populates="area")
    mobility_patterns = relationship("MobilityPattern", back_populates="area")
    outreach_sessions = relationship("OutreachSession", back_populates="area")
    recommendations = relationship("Recommendation", back_populates="area")


class ServiceHistory(Base):
    __tablename__ = "service_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    area_id = Column(String(20), ForeignKey("areas.area_id"), nullable=False)
    time_period = Column(String(20), nullable=False)
    eligible_population = Column(Integer, nullable=False)
    vaccinated_count = Column(Integer, nullable=False)
    service_visits = Column(Integer, nullable=False)
    historical_demand = Column(Integer, nullable=False)

    area = relationship("Area", back_populates="service_histories")


class DiseaseRisk(Base):
    __tablename__ = "disease_risk"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    area_id = Column(String(20), ForeignKey("areas.area_id"), nullable=False)
    time_period = Column(String(20), nullable=False)
    seasonal_risk = Column(Float, nullable=False)  # 0.0 to 1.0
    emerging_risk = Column(Float, nullable=False)  # 0.0 to 1.0
    surveillance_signal_date = Column(String(10), nullable=False)

    area = relationship("Area", back_populates="disease_risks")


class MobilityPattern(Base):
    __tablename__ = "mobility_patterns"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    area_id = Column(String(20), ForeignKey("areas.area_id"), nullable=False)
    time_period = Column(String(20), nullable=False)
    mobility_index = Column(Float, nullable=False)  # 0.0 to 1.0
    inflow_index = Column(Float, nullable=False)
    outflow_index = Column(Float, nullable=False)

    area = relationship("Area", back_populates="mobility_patterns")


class OutreachSession(Base):
    __tablename__ = "outreach_sessions"

    session_id = Column(String(36), primary_key=True, index=True)
    area_id = Column(String(20), ForeignKey("areas.area_id"), nullable=False)
    planning_period = Column(String(20), nullable=False)
    scheduled_date = Column(String(10), nullable=False)
    capacity = Column(Integer, nullable=False)
    planned_reach = Column(Integer, nullable=False)
    actual_reach = Column(Integer, default=0)
    travel_distance_km = Column(Float, nullable=False)
    status = Column(String(30), default="PLANNED")

    area = relationship("Area", back_populates="outreach_sessions")


class Recommendation(Base):
    __tablename__ = "recommendations"

    recommendation_id = Column(String(36), primary_key=True, index=True)
    area_id = Column(String(20), ForeignKey("areas.area_id"), nullable=False)
    planning_period = Column(String(20), nullable=False)
    objective = Column(String(50), nullable=False)  # MAX_REACH, RISK_REDUCTION, HISTORICAL_BASELINE
    priority_score = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)
    expected_reach = Column(Integer, nullable=False)
    reason = Column(Text, nullable=False)  # JSON string breakdown
    hard_constraint_passed = Column(Boolean, nullable=False, default=True)
    constraint_flags = Column(Text, nullable=True)  # JSON string array of flags
    status = Column(String(30), default="PENDING")  # PENDING, ACCEPTED, MODIFIED, REJECTED, OVERRIDDEN

    area = relationship("Area", back_populates="recommendations")
    reviews = relationship("Review", back_populates="recommendation")


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(String(36), primary_key=True, index=True)
    recommendation_id = Column(String(36), ForeignKey("recommendations.recommendation_id"), nullable=False)
    reviewer_id = Column(String(50), nullable=False)
    reviewer_role = Column(String(50), nullable=False)
    decision = Column(String(30), nullable=False)  # ACCEPTED, MODIFIED, REJECTED, OVERRIDDEN
    override_reason = Column(Text, nullable=True)
    modified_capacity = Column(Integer, nullable=True)
    modified_travel_km = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    recommendation = relationship("Recommendation", back_populates="reviews")


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False)  # ADMIN, CLINICIAN
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

