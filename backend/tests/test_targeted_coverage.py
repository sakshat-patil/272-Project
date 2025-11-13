"""
Tests specifically targeting uncovered lines to reach 80%+
"""
import pytest
from app import crud, schemas, models
from app.models import Supplier, SupplierDependency, SupplierCategory, CriticalityLevel, SupplierTier


class TestSupplierDependencyCRUD:
    """Test supplier dependency CRUD operations"""
    
    def test_create_supplier_dependency(self, db_session, test_organization):
        """Test creating a supplier dependency"""
        # Create two suppliers
        supplier1 = Supplier(
            name="Main Supplier",
            country="USA",
            city="NYC",
            organization_id=test_organization.id,
            category=SupplierCategory.FINISHED_GOODS,
            criticality=CriticalityLevel.HIGH,
            tier=SupplierTier.TIER_1,
            reliability_score=90.0
        )
        supplier2 = Supplier(
            name="Component Supplier",
            country="China",
            city="Shanghai",
            organization_id=test_organization.id,
            category=SupplierCategory.COMPONENTS,
            criticality=CriticalityLevel.MEDIUM,
            tier=SupplierTier.TIER_2,
            reliability_score=85.0
        )
        db_session.add(supplier1)
        db_session.add(supplier2)
        db_session.commit()
        
        # Create dependency
        dep_data = schemas.SupplierDependencyCreate(
            supplier_id=supplier1.id,
            depends_on_supplier_id=supplier2.id,
            dependency_type="Component Supply",
            criticality_level=3
        )
        dependency = crud.create_supplier_dependency(db_session, dep_data)
        
        assert dependency.id is not None
        assert dependency.supplier_id == supplier1.id
        assert dependency.depends_on_supplier_id == supplier2.id
    
    def test_get_supplier_dependencies(self, db_session, test_organization):
        """Test getting dependencies for a supplier"""
        # Create suppliers
        supplier1 = Supplier(
            name="Main",
            country="USA",
            city="NYC",
            organization_id=test_organization.id,
            category=SupplierCategory.FINISHED_GOODS,
            criticality=CriticalityLevel.HIGH,
            tier=SupplierTier.TIER_1,
            reliability_score=90.0
        )
        supplier2 = Supplier(
            name="Component",
            country="China",
            city="Shanghai",
            organization_id=test_organization.id,
            category=SupplierCategory.COMPONENTS,
            criticality=CriticalityLevel.MEDIUM,
            tier=SupplierTier.TIER_2,
            reliability_score=85.0
        )
        db_session.add(supplier1)
        db_session.add(supplier2)
        db_session.commit()
        
        # Create dependency
        dependency = SupplierDependency(
            supplier_id=supplier1.id,
            depends_on_supplier_id=supplier2.id,
            dependency_type="Component Supply",
            criticality_level=3
        )
        db_session.add(dependency)
        db_session.commit()
        
        # Get dependencies
        deps = crud.get_supplier_dependencies(db_session, supplier1.id)
        assert len(deps) >= 1
        assert deps[0].supplier_id == supplier1.id
    
    def test_get_dependent_suppliers(self, db_session, test_organization):
        """Test getting suppliers that depend on a given supplier"""
        # Create suppliers
        supplier1 = Supplier(
            name="Component Supplier",
            country="Japan",
            city="Tokyo",
            organization_id=test_organization.id,
            category=SupplierCategory.COMPONENTS,
            criticality=CriticalityLevel.HIGH,
            tier=SupplierTier.TIER_1,
            reliability_score=95.0
        )
        supplier2 = Supplier(
            name="Manufacturer",
            country="USA",
            city="Detroit",
            organization_id=test_organization.id,
            category=SupplierCategory.FINISHED_GOODS,
            criticality=CriticalityLevel.CRITICAL,
            tier=SupplierTier.TIER_1,
            reliability_score=90.0
        )
        db_session.add(supplier1)
        db_session.add(supplier2)
        db_session.commit()
        
        # Create dependency (supplier2 depends on supplier1)
        dependency = SupplierDependency(
            supplier_id=supplier2.id,
            depends_on_supplier_id=supplier1.id,
            dependency_type="Critical Component",
            criticality_level=5
        )
        db_session.add(dependency)
        db_session.commit()
        
        # Get dependent suppliers
        dependents = crud.get_dependent_suppliers(db_session, supplier1.id)
        assert len(dependents) >= 1


class TestEventCRUD:
    """Test event CRUD operations"""
    
    def test_create_event(self, db_session, test_organization):
        """Test creating an event"""
        event_data = schemas.EventCreate(
            organization_id=test_organization.id,
            event_type=models.EventType.NATURAL_DISASTER,
            description="Earthquake in supplier region",
            event_date="2024-01-15",
            location="California",
            severity_level=4
        )
        
        event = crud.create_event(db_session, event_data)
        assert event.id is not None
        assert event.organization_id == test_organization.id
        assert event.event_type == models.EventType.NATURAL_DISASTER


class TestRiskHistoryCRUD:
    """Test risk history CRUD operations"""
    
    def test_create_risk_history(self, db_session, test_organization):
        """Test creating risk history entry"""
        risk_data = schemas.RiskHistoryCreate(
            organization_id=test_organization.id,
            risk_score=62.5,
            contributing_factors=["Market volatility", "Supply delays"]
        )
        
        risk = crud.create_risk_history(db_session, risk_data)
        assert risk.id is not None
        assert risk.organization_id == test_organization.id
        assert risk.risk_score == 62.5
    
    def test_get_risk_history(self, db_session, test_organization):
        """Test getting risk history for organization"""
        # Create risk entry
        risk = models.RiskHistory(
            organization_id=test_organization.id,
            risk_score=55.0,
            contributing_factors=["Factor 1"]
        )
        db_session.add(risk)
        db_session.commit()
        
        # Get history
        history = crud.get_risk_history_by_organization(db_session, test_organization.id, limit=10)
        assert len(history) >= 1
