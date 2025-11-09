from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/api/organizations", tags=["Organizations"])


@router.post("/", response_model=schemas.OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(
    organization: schemas.OrganizationCreate,
    db: Session = Depends(get_db)
):
    """Create a new organization"""
    return crud.create_organization(db, organization)


@router.get("/", response_model=List[schemas.OrganizationResponse])
def get_organizations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all organizations"""
    return crud.get_organizations(db, skip=skip, limit=limit)


@router.get("/{organization_id}", response_model=schemas.OrganizationWithSuppliers)
def get_organization(
    organization_id: int,
    db: Session = Depends(get_db)
):
    """Get organization by ID with suppliers"""
    org = crud.get_organization(db, organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.put("/{organization_id}", response_model=schemas.OrganizationResponse)
def update_organization(
    organization_id: int,
    organization: schemas.OrganizationUpdate,
    db: Session = Depends(get_db)
):
    """Update organization"""
    updated_org = crud.update_organization(db, organization_id, organization)
    if not updated_org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return updated_org


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db)
):
    """Delete organization"""
    success = crud.delete_organization(db, organization_id)
    if not success:
        raise HTTPException(status_code=404, detail="Organization not found")
    return None