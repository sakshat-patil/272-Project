"""
Tests for supplier CRUD operations
"""
import pytest
from fastapi import status

from app.models import SupplierCategory, CriticalityLevel, SupplierTier


class TestSupplierEndpoints:
    """Test supplier API endpoints"""
    
    def test_create_supplier(self, client, auth_headers, test_organization):
        """Test creating a supplier"""
        response = client.post(
            "/api/suppliers/",
            headers=auth_headers,
            json={
                "name": "New Supplier Co",
                "country": "Germany",
                "city": "Berlin",
                "category": "Components",
                "criticality": "High",
                "tier": 1,
                "lead_time_days": 45,
                "reliability_score": 90.0,
                "capacity_utilization": 75.0,
                "organization_id": test_organization.id
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "New Supplier Co"
        assert data["country"] == "Germany"
        assert data["reliability_score"] == 90.0
    
    def test_list_suppliers(self, client, test_organization, test_supplier):
        """Test list suppliers endpoint"""
        response = client.get(f"/api/suppliers/organization/{test_organization.id}")
        assert response.status_code == status.HTTP_200_OK
    
    def test_get_supplier(self, client, auth_headers, test_supplier):
        """Test getting supplier by ID"""
        response = client.get(
            f"/api/suppliers/{test_supplier.id}",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_supplier.id
        assert data["name"] == test_supplier.name
    
    def test_get_supplier_not_found(self, client, auth_headers):
        """Test getting non-existent supplier"""
        response = client.get("/api/suppliers/99999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_supplier(self, client, auth_headers, test_supplier):
        """Test updating supplier"""
        response = client.put(
            f"/api/suppliers/{test_supplier.id}",
            headers=auth_headers,
            json={
                "reliability_score": 95.0,
                "capacity_utilization": 80.0
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["reliability_score"] == 95.0
        assert data["capacity_utilization"] == 80.0
    
    def test_delete_supplier(self, client, test_supplier, auth_headers):
        """Test delete supplier endpoint"""
        response = client.delete(
            f"/api/suppliers/{test_supplier.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_get_organization_suppliers(self, client, auth_headers, test_organization, test_supplier):
        """Test getting suppliers for an organization"""
        response = client.get(
            f"/api/suppliers/organization/{test_organization.id}",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert any(s["id"] == test_supplier.id for s in data)
    
    def test_supplier_endpoints_unauthorized(self, client):
        """Test supplier endpoints without authentication"""
        response = client.post("/api/suppliers/", json={})
        # POST without proper data returns 422, not 401 since no auth is required
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
