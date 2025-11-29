from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class IndustryType(str, enum.Enum):
    PHARMACEUTICAL = "Pharmaceutical"
    AUTOMOTIVE = "Automotive"
    ELECTRONICS = "Electronics"
    FOOD_BEVERAGE = "Food & Beverage"
    OTHER = "Other"


class CriticalityLevel(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class SupplierTier(int, enum.Enum):
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3


class SupplierCategory(str, enum.Enum):
    RAW_MATERIALS = "Raw Materials"
    COMPONENTS = "Components"
    FINISHED_GOODS = "Finished Goods"
    LOGISTICS = "Logistics"
    SERVICES = "Services"


class EventType(str, enum.Enum):
    NATURAL_DISASTER = "Natural Disaster"
    GEOPOLITICAL = "Geopolitical"
    LABOR_STRIKE = "Labor Strike"
    LOGISTICS = "Logistics"
    ECONOMIC = "Economic"
    CYBER_SECURITY = "Cyber Security"
    REGULATORY = "Regulatory"
    OTHER = "Other"


class ProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    industry = Column(Enum(IndustryType), nullable=False)
    headquarters_location = Column(String(200))
    description = Column(Text)
    shipping_route = Column(JSON)  # Store onboarding route data: {origin: {...}, destination: {...}}
    current_risk_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    suppliers = relationship("Supplier", back_populates="organization", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="organization", cascade="all, delete-orphan")
    risk_history = relationship("RiskHistory", back_populates="organization", cascade="all, delete-orphan")
    future_predictions = relationship("FutureRiskPrediction", back_populates="organization", cascade="all, delete-orphan")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(200), nullable=False)
    country = Column(String(100), nullable=False)
    city = Column(String(100))
    category = Column(Enum(SupplierCategory), nullable=False)
    criticality = Column(Enum(CriticalityLevel), nullable=False)
    tier = Column(Enum(SupplierTier), nullable=False, default=SupplierTier.TIER_1)
    lead_time_days = Column(Integer, default=30)
    reliability_score = Column(Float, default=85.0)  # 0-100
    capacity_utilization = Column(Float, default=70.0)  # 0-100 percentage
    contact_info = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="suppliers")
    dependencies = relationship(
        "SupplierDependency",
        foreign_keys="SupplierDependency.supplier_id",
        back_populates="supplier",
        cascade="all, delete-orphan"
    )
    dependent_on = relationship(
        "SupplierDependency",
        foreign_keys="SupplierDependency.depends_on_supplier_id",
        back_populates="depends_on_supplier",
        cascade="all, delete-orphan"
    )


class SupplierDependency(Base):
    __tablename__ = "supplier_dependencies"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    depends_on_supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    dependency_type = Column(String(50), default="important")  # critical, important, minor
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    supplier = relationship("Supplier", foreign_keys=[supplier_id], back_populates="dependencies")
    depends_on_supplier = relationship("Supplier", foreign_keys=[depends_on_supplier_id], back_populates="dependent_on")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    # User Input
    event_input = Column(Text, nullable=False)
    severity_level = Column(Integer, default=3)  # 1-5
    
    # Parsed Event Details
    title = Column(String(300))  # Event title for historical display
    event_type = Column(Enum(EventType))
    location = Column(String(200))
    description = Column(Text)
    latitude = Column(Float)  # Geographic coordinates for historical matching
    longitude = Column(Float)
    event_date = Column(DateTime)  # When the event occurred
    impact_assessment = Column(Text)  # Impact severity assessment
    
    # Analysis Results
    affected_supplier_count = Column(Integer, default=0)
    overall_risk_score = Column(Float, default=0.0)
    
    # Agent Outputs (stored as JSON)
    parsed_event = Column(JSON)
    affected_suppliers = Column(JSON)
    risk_analysis = Column(JSON)
    recommendations = Column(JSON)
    alternative_suppliers = Column(JSON)
    playbook = Column(JSON)
    
    # Agent Processing Info
    agent_logs = Column(JSON)  # Track agent workflow
    
    # Metadata
    processing_status = Column(Enum(ProcessingStatus), default=ProcessingStatus.PENDING)
    processing_time_seconds = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    # Relationships
    organization = relationship("Organization", back_populates="events")


class RiskHistory(Base):
    __tablename__ = "risk_history"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    risk_score = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)
    notes = Column(Text)

    # Relationships
    organization = relationship("Organization", back_populates="risk_history")


class FutureRiskPrediction(Base):
    __tablename__ = "future_risk_predictions"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    prediction_period_days = Column(Integer)  # 30, 60, 90
    predicted_risk_score = Column(Float)
    risk_factors = Column(JSON)  # List of identified risk factors
    recommendations = Column(JSON)
    confidence_level = Column(Float)  # 0-100
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="future_predictions")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)