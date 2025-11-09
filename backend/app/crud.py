from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from typing import List, Optional
from datetime import datetime, timedelta

from app import models, schemas


# ============ Organization CRUD ============

def create_organization(db: Session, org: schemas.OrganizationCreate) -> models.Organization:
    db_org = models.Organization(**org.model_dump())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org


def get_organization(db: Session, org_id: int) -> Optional[models.Organization]:
    return db.query(models.Organization).filter(models.Organization.id == org_id).first()


def get_organizations(db: Session, skip: int = 0, limit: int = 100) -> List[models.Organization]:
    return db.query(models.Organization).offset(skip).limit(limit).all()


# def update_organization(db: Session, org_id: int, org_update: schemas.OrganizationUpdate) -> Optional[models.Organization]:
#     db_org = get_organization(db, org_id)
#     if db_org:
#         update_data = org_update.model_dump(exclude_unset=True)
#         for field, value in update_data.items():
#             setattr(db_org, field, value)
#         db_org.updated_at = datetime.utcnow()
#         db.commit()
#         db.refresh(db_org)
#     return db_org

def update_organization(db: Session, org_id: int, org_update) -> Optional[models.Organization]:
    db_org = get_organization(db, org_id)
    if db_org:
        # Handle both dict and Pydantic model
        if hasattr(org_update, 'model_dump'):
            # It's a Pydantic model
            update_data = org_update.model_dump(exclude_unset=True)
        else:
            # It's already a dict
            update_data = org_update
        
        for field, value in update_data.items():
            setattr(db_org, field, value)
        db_org.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_org)
    return db_org


def delete_organization(db: Session, org_id: int) -> bool:
    db_org = get_organization(db, org_id)
    if db_org:
        db.delete(db_org)
        db.commit()
        return True
    return False


# ============ Supplier CRUD ============

def create_supplier(db: Session, supplier: schemas.SupplierCreate) -> models.Supplier:
    db_supplier = models.Supplier(**supplier.model_dump())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


def get_supplier(db: Session, supplier_id: int) -> Optional[models.Supplier]:
    return db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()


def get_suppliers_by_organization(db: Session, org_id: int) -> List[models.Supplier]:
    return db.query(models.Supplier).filter(models.Supplier.organization_id == org_id).all()


def get_suppliers_by_tier(db: Session, org_id: int, tier: models.SupplierTier) -> List[models.Supplier]:
    return db.query(models.Supplier).filter(
        and_(models.Supplier.organization_id == org_id, models.Supplier.tier == tier)
    ).all()


def update_supplier(db: Session, supplier_id: int, supplier_update: schemas.SupplierUpdate) -> Optional[models.Supplier]:
    db_supplier = get_supplier(db, supplier_id)
    if db_supplier:
        update_data = supplier_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_supplier, field, value)
        db_supplier.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_supplier)
    return db_supplier


def delete_supplier(db: Session, supplier_id: int) -> bool:
    db_supplier = get_supplier(db, supplier_id)
    if db_supplier:
        db.delete(db_supplier)
        db.commit()
        return True
    return False


# ============ Supplier Dependency CRUD ============

def create_supplier_dependency(db: Session, dependency: schemas.SupplierDependencyCreate) -> models.SupplierDependency:
    db_dependency = models.SupplierDependency(**dependency.model_dump())
    db.add(db_dependency)
    db.commit()
    db.refresh(db_dependency)
    return db_dependency


def get_supplier_dependencies(db: Session, supplier_id: int) -> List[models.SupplierDependency]:
    return db.query(models.SupplierDependency).filter(
        models.SupplierDependency.supplier_id == supplier_id
    ).all()


def get_dependent_suppliers(db: Session, supplier_id: int) -> List[models.Supplier]:
    """Get all suppliers that depend on the given supplier"""
    dependencies = db.query(models.SupplierDependency).filter(
        models.SupplierDependency.depends_on_supplier_id == supplier_id
    ).all()
    return [dep.supplier for dep in dependencies]


# ============ Event CRUD ============

def create_event(db: Session, event: schemas.EventCreate) -> models.Event:
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event(db: Session, event_id: int) -> Optional[models.Event]:
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def get_events_by_organization(db: Session, org_id: int, skip: int = 0, limit: int = 50) -> List[models.Event]:
    return db.query(models.Event).filter(
        models.Event.organization_id == org_id
    ).order_by(desc(models.Event.created_at)).offset(skip).limit(limit).all()


def update_event(db: Session, event_id: int, **kwargs) -> Optional[models.Event]:
    db_event = get_event(db, event_id)
    if db_event:
        for field, value in kwargs.items():
            setattr(db_event, field, value)
        db.commit()
        db.refresh(db_event)
    return db_event


# ============ Risk History CRUD ============

def create_risk_history(db: Session, risk_history: schemas.RiskHistoryCreate) -> models.RiskHistory:
    db_risk = models.RiskHistory(**risk_history.model_dump())
    db.add(db_risk)
    db.commit()
    db.refresh(db_risk)
    return db_risk


def get_risk_history(db: Session, org_id: int, days: int = 30) -> List[models.RiskHistory]:
    since_date = datetime.utcnow() - timedelta(days=days)
    return db.query(models.RiskHistory).filter(
        and_(
            models.RiskHistory.organization_id == org_id,
            models.RiskHistory.recorded_at >= since_date
        )
    ).order_by(models.RiskHistory.recorded_at).all()


# ============ Future Risk Prediction CRUD ============

def create_future_prediction(db: Session, prediction_data: dict) -> models.FutureRiskPrediction:
    db_prediction = models.FutureRiskPrediction(**prediction_data)
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction


def get_latest_prediction(db: Session, org_id: int, period_days: int) -> Optional[models.FutureRiskPrediction]:
    return db.query(models.FutureRiskPrediction).filter(
        and_(
            models.FutureRiskPrediction.organization_id == org_id,
            models.FutureRiskPrediction.prediction_period_days == period_days
        )
    ).order_by(desc(models.FutureRiskPrediction.created_at)).first()