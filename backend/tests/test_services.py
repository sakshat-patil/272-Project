"""
Tests for service modules: dependency_analyzer, risk_calculator, supplier_scoring
"""
import pytest
from app.services import dependency_analyzer, risk_calculator, supplier_scoring
from app.models import Supplier, Organization, IndustryType, SupplierCategory, CriticalityLevel, SupplierTier


class TestDependencyAnalyzer:
    """Test dependency analysis service"""
    
    def test_build_dependency_graph_empty(self, db_session, test_organization):
        """Test building dependency graph with no suppliers"""
        graph = dependency_analyzer.build_dependency_graph(db_session, test_organization.id)
        
        assert isinstance(graph, dict)
    
    def test_build_dependency_graph_with_suppliers(self, db_session, test_organization):
        """Test building dependency graph with suppliers"""
        # Create suppliers
        supplier1 = Supplier(
            name="Supplier 1",
            country="USA",
            city="New York",
            organization_id=test_organization.id,
            category=SupplierCategory.COMPONENTS,
            criticality=CriticalityLevel.HIGH,
            tier=SupplierTier.TIER_1,
            reliability_score=90.0
        )
        supplier2 = Supplier(
            name="Supplier 2",
            country="China",
            city="Shanghai",
            organization_id=test_organization.id,
            category=SupplierCategory.RAW_MATERIALS,
            criticality=CriticalityLevel.MEDIUM,
            tier=SupplierTier.TIER_2,
            reliability_score=85.0
        )
        db_session.add(supplier1)
        db_session.add(supplier2)
        db_session.commit()
        
        graph = dependency_analyzer.build_dependency_graph(db_session, test_organization.id)
        
        assert isinstance(graph, dict)
        assert len(graph) >= 2
    
    def test_find_downstream_impact(self):
        """Test finding downstream impact"""
        graph = {
            1: [2, 3],
            2: [4],
            3: [4],
            4: [],
            5: [1]
        }
        
        affected = {1}
        downstream = dependency_analyzer.find_downstream_impact(affected, graph)
        
        assert isinstance(downstream, set)


class TestRiskCalculator:
    """Test risk calculation service"""
    
    def test_calculate_supplier_impact_score(self, test_supplier):
        """Test supplier impact score calculation"""
        score = risk_calculator.calculate_supplier_impact_score(
            supplier=test_supplier,
            severity_level=4,
            proximity_score=0.8
        )
        
        assert 0 <= score <= 100
    
    def test_calculate_supplier_impact_score_high_severity(self, test_supplier):
        """Test impact score with high severity"""
        score = risk_calculator.calculate_supplier_impact_score(
            supplier=test_supplier,
            severity_level=5,
            proximity_score=1.0
        )
        
        assert score > 0
    
    def test_calculate_supplier_impact_score_low_severity(self, test_supplier):
        """Test impact score with low severity"""
        score = risk_calculator.calculate_supplier_impact_score(
            supplier=test_supplier,
            severity_level=1,
            proximity_score=0.2
        )
        
        assert score >= 0


class TestSupplierScorer:
    """Test supplier scoring service"""
    
    def test_calculate_distance(self):
        """Test geographic distance calculation"""
        # New York to Los Angeles
        distance = supplier_scoring.calculate_distance(
            lat1=40.7128,
            lon1=-74.0060,
            lat2=34.0522,
            lon2=-118.2437
        )
        
        assert distance > 0
        assert distance < 10000  # Reasonable bound
    
    def test_calculate_distance_same_location(self):
        """Test distance calculation for same location"""
        distance = supplier_scoring.calculate_distance(
            lat1=40.0,
            lon1=-70.0,
            lat2=40.0,
            lon2=-70.0
        )
        
        assert distance == 0.0 or distance < 0.1  # Negligible
    
    def test_score_alternative_supplier(self, test_supplier):
        """Test scoring alternative supplier"""
        # Create another supplier as alternative
        alternative = Supplier(
            name="Alternative Supplier",
            country="USA",
            city="Seattle",
            organization_id=test_supplier.organization_id,
            category=test_supplier.category,
            criticality=CriticalityLevel.MEDIUM,
            tier=SupplierTier.TIER_2,
            reliability_score=85.0,
            latitude=47.6062,
            longitude=-122.3321
        )
        
        score = supplier_scoring.score_alternative_supplier(
            alternative=alternative,
            affected_supplier=test_supplier,
            event_location=(35.0, 100.0)
        )
        
        assert isinstance(score, dict)
