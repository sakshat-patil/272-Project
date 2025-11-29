from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models import (
    IndustryType, CriticalityLevel, SupplierTier, 
    SupplierCategory, EventType, ProcessingStatus
)


# ============ Organization Schemas ============

class ShippingRouteLocation(BaseModel):
    port: str
    country: str
    latitude: float
    longitude: float


class ShippingRoute(BaseModel):
    origin: ShippingRouteLocation
    destination: ShippingRouteLocation


class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    industry: IndustryType
    headquarters_location: Optional[str] = None
    description: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    shipping_route: Optional[ShippingRoute] = None


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[IndustryType] = None
    headquarters_location: Optional[str] = None
    description: Optional[str] = None
    shipping_route: Optional[ShippingRoute] = None
    current_risk_score: Optional[float] = None


class OrganizationResponse(OrganizationBase):
    id: int
    shipping_route: Optional[Dict[str, Any]] = None
    current_risk_score: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrganizationWithSuppliers(OrganizationResponse):
    suppliers: List['SupplierResponse'] = []

    class Config:
        from_attributes = True


# ============ Supplier Schemas ============

class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    country: str = Field(..., min_length=1, max_length=100)
    city: Optional[str] = None
    category: SupplierCategory
    criticality: CriticalityLevel
    tier: SupplierTier = SupplierTier.TIER_1
    lead_time_days: int = Field(default=30, ge=1)
    reliability_score: float = Field(default=85.0, ge=0, le=100)
    capacity_utilization: float = Field(default=70.0, ge=0, le=100)
    contact_info: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)


class SupplierCreate(SupplierBase):
    organization_id: int


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    category: Optional[SupplierCategory] = None
    criticality: Optional[CriticalityLevel] = None
    tier: Optional[SupplierTier] = None
    lead_time_days: Optional[int] = None
    reliability_score: Optional[float] = None
    capacity_utilization: Optional[float] = None
    contact_info: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class SupplierResponse(SupplierBase):
    id: int
    organization_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SupplierDependencyCreate(BaseModel):
    supplier_id: int
    depends_on_supplier_id: int
    dependency_type: str = "important"


class SupplierDependencyResponse(BaseModel):
    id: int
    supplier_id: int
    depends_on_supplier_id: int
    dependency_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Event Schemas ============

class EventCreate(BaseModel):
    organization_id: int
    event_input: str = Field(..., min_length=10)
    severity_level: int = Field(default=3, ge=1, le=5)


class EventResponse(BaseModel):
    id: int
    organization_id: int
    event_input: str
    severity_level: int
    event_type: Optional[EventType] = None
    location: Optional[str] = None
    description: Optional[str] = None
    affected_supplier_count: int
    overall_risk_score: float
    processing_status: ProcessingStatus
    processing_time_seconds: Optional[float] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EventDetailResponse(EventResponse):
    parsed_event: Optional[Dict[str, Any]] = None
    affected_suppliers: Optional[List[Dict[str, Any]]] = None
    risk_analysis: Optional[Dict[str, Any]] = None
    recommendations: Optional[Dict[str, Any]] = None
    alternative_suppliers: Optional[List[Dict[str, Any]]] = None
    playbook: Optional[Dict[str, Any]] = None
    agent_logs: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True


# ============ Risk History Schemas ============

class RiskHistoryCreate(BaseModel):
    organization_id: int
    risk_score: float
    event_id: Optional[int] = None
    notes: Optional[str] = None


class RiskHistoryResponse(BaseModel):
    id: int
    organization_id: int
    risk_score: float
    recorded_at: datetime
    event_id: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


# ============ Future Risk Prediction Schemas ============

class FutureRiskPredictionCreate(BaseModel):
    organization_id: int
    prediction_period_days: int = Field(..., ge=1)


class FutureRiskPredictionResponse(BaseModel):
    id: int
    organization_id: int
    prediction_period_days: int
    predicted_risk_score: float
    risk_factors: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    confidence_level: float
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Comparison Schemas ============

class ComparisonRequest(BaseModel):
    organization_id: int
    events: List[str] = Field(..., min_items=2, max_items=3)
    severity_levels: Optional[List[int]] = None

    @validator('severity_levels')
    def validate_severity_levels(cls, v, values):
        if v is not None:
            if len(v) != len(values.get('events', [])):
                raise ValueError('severity_levels must match the number of events')
        return v


class ComparisonResponse(BaseModel):
    comparison_id: str
    events: List[EventDetailResponse]
    priority_recommendation: str
    comparative_analysis: Dict[str, Any]


# ============ User/Auth Schemas ============
import re

class UserBase(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None