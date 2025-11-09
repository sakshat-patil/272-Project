from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/api/suppliers", tags=["Suppliers"])


@router.post("/", response_model=schemas.SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    supplier: schemas.SupplierCreate,
    db: Session = Depends(get_db)
):
    """Create a new supplier"""
    return crud.create_supplier(db, supplier)


@router.get("/organization/{organization_id}", response_model=List[schemas.SupplierResponse])
def get_suppliers_by_organization(
    organization_id: int,
    db: Session = Depends(get_db)
):
    """Get all suppliers for an organization"""
    return crud.get_suppliers_by_organization(db, organization_id)


@router.get("/{supplier_id}", response_model=schemas.SupplierResponse)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    """Get supplier by ID"""
    supplier = crud.get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.put("/{supplier_id}", response_model=schemas.SupplierResponse)
def update_supplier(
    supplier_id: int,
    supplier: schemas.SupplierUpdate,
    db: Session = Depends(get_db)
):
    """Update supplier"""
    updated_supplier = crud.update_supplier(db, supplier_id, supplier)
    if not updated_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return updated_supplier


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    """Delete supplier"""
    success = crud.delete_supplier(db, supplier_id)
    if not success:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return None


@router.post("/dependencies", response_model=schemas.SupplierDependencyResponse, status_code=status.HTTP_201_CREATED)
def create_supplier_dependency(
    dependency: schemas.SupplierDependencyCreate,
    db: Session = Depends(get_db)
):
    """Create a supplier dependency relationship"""
    return crud.create_supplier_dependency(db, dependency)


@router.get("/{supplier_id}/dependencies", response_model=List[schemas.SupplierDependencyResponse])
def get_supplier_dependencies(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    """Get all dependencies for a supplier"""
    return crud.get_supplier_dependencies(db, supplier_id)