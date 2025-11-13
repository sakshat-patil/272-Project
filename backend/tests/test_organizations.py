"""
Tests for organization CRUD operations
"""
import pytest
from fastapi import status

from app.models import IndustryType, CriticalityLevel
from app.crud import (
    create_organization,
    get_organization,
    get_organizations,
    update_organization,
    delete_organization
)


class TestOrganizationCRUD:
    """Test organization CRUD functions"""
    
    def test_create_organization(self, db_session, test_user):
        """Test creating an organization"""
        from app.schemas import OrganizationCreate
        
        org_data = OrganizationCreate(
            name="New Corp",
            industry=IndustryType.AUTOMOTIVE,
            headquarters_location="Chicago, IL",
            description="A new test organization"
        )
        
        org = create_organization(db_session, org_data)
        
        assert org.id is not None
        assert org.name == "New Corp"
        assert org.industry == IndustryType.AUTOMOTIVE
    
    def test_get_organization(self, db_session, test_organization):
        """Test retrieving an organization by ID"""
        org = get_organization(db_session, test_organization.id)
        
        assert org is not None
        assert org.id == test_organization.id
        assert org.name == test_organization.name
    
    def test_get_organization_not_found(self, db_session):
        """Test retrieving non-existent organization"""
        org = get_organization(db_session, 99999)
        assert org is None
    
    def test_get_organizations(self, db_session, test_organization):
        """Test retrieving all organizations"""
        orgs = get_organizations(db_session)
        
        assert len(orgs) >= 1
        assert any(o.id == test_organization.id for o in orgs)
    
    def test_update_organization(self, db_session, test_organization):
        """Test updating an organization"""
        update_data = {"name": "Updated Corp", "description": "Updated description"}
        
        updated_org = update_organization(db_session, test_organization.id, update_data)
        
        assert updated_org is not None
        assert updated_org.name == "Updated Corp"
        assert updated_org.description == "Updated description"
    
    def test_delete_organization(self, db_session, test_organization):
        """Test deleting an organization"""
        result = delete_organization(db_session, test_organization.id)
        
        assert result is True
        assert get_organization(db_session, test_organization.id) is None


class TestOrganizationEndpoints:
    """Test organization API endpoints"""
    
    def test_list_organizations(self, client, auth_headers, test_organization):
        """Test listing organizations"""
        response = client.get("/api/organizations/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_create_organization_endpoint(self, client, auth_headers):
        """Test creating organization via API"""
        response = client.post(
            "/api/organizations/",
            headers=auth_headers,
            json={
                "name": "API Test Corp",
                "industry": "Electronics",
                "headquarters_location": "Austin, TX",
                "description": "Created via API"
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "API Test Corp"
        assert data["industry"] == "Electronics"
    
    def test_get_organization_endpoint(self, client, auth_headers, test_organization):
        """Test getting organization by ID via API"""
        response = client.get(
            f"/api/organizations/{test_organization.id}",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_organization.id
        assert data["name"] == test_organization.name
    
    def test_get_organization_not_found(self, client, auth_headers):
        """Test getting non-existent organization"""
        response = client.get("/api/organizations/99999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_organization_endpoint(self, client, auth_headers, test_organization):
        """Test updating organization via API"""
        response = client.put(
            f"/api/organizations/{test_organization.id}",
            headers=auth_headers,
            json={"name": "Updated via API"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated via API"
    
    def test_delete_organization_endpoint(self, client, auth_headers, test_organization):
        """Test deleting organization via API"""
        response = client.delete(
            f"/api/organizations/{test_organization.id}",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's deleted
        response = client.get(
            f"/api/organizations/{test_organization.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_organization_endpoints_unauthorized(self, client):
        """Test that organization endpoints work without authentication (no auth required currently)"""
        response = client.get("/api/organizations/")
        # Currently these endpoints don't require auth, so they return 200
        assert response.status_code == status.HTTP_200_OK
