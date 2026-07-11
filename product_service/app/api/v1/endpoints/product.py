from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.schemas.response import ResponseModel
from app.db.deps import get_db
from app.core.security import get_current_user
from app.core.pagination import get_pagination_params
from app.services.productservices import (
    get_all_products,
    get_product,
    create_product,
    update_product,
    delete_product,
    search_products
)

router = APIRouter()


@router.get("/", response_model=ResponseModel)
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Get all products for current user with pagination"""
    skip, limit = get_pagination_params(skip, limit)
    products, total = get_all_products(db, current_user_id, skip=skip, limit=limit)
    
    return ResponseModel(
        success=True,
        message="Products retrieved successfully",
        data=[ProductResponse.model_validate(product) for product in products],
        error=None
    )


@router.get("/search", response_model=ResponseModel)
def search_product(
    query: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Search products by name (current user only)"""
    skip, limit = get_pagination_params(skip, limit)
    products, total = search_products(db, current_user_id, query=query, skip=skip, limit=limit)
    
    return ResponseModel(
        success=True,
        message="Search results retrieved",
        data=[ProductResponse.model_validate(product) for product in products],
        error=None
    )


@router.get("/{product_id}", response_model=ResponseModel)
def get_product_details(
    product_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Get product by ID (current user only)"""
    product = get_product(db, product_id, current_user_id)
    
    return ResponseModel(
        success=True,
        message="Product retrieved successfully",
        data=ProductResponse.model_validate(product),
        error=None
    )


@router.post("/", response_model=ResponseModel)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Create a new product (authenticated users only)"""
    created_product = create_product(db, product, current_user_id)
    
    return ResponseModel(
        success=True,
        message="Product created successfully",
        data=ProductResponse.model_validate(created_product),
        error=None
    )


@router.put("/{product_id}", response_model=ResponseModel)
def update_existing_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Update product (current user only)"""
    updated_product = update_product(db, product_id, product_data, current_user_id)
    
    return ResponseModel(
        success=True,
        message="Product updated successfully",
        data=ProductResponse.model_validate(updated_product),
        error=None
    )


@router.delete("/{product_id}", response_model=ResponseModel)
def delete_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Delete product (current user only)"""
    deleted_product = delete_product(db, product_id, current_user_id)
    
    return ResponseModel(
        success=True,
        message="Product deleted successfully",
        data=ProductResponse.model_validate(deleted_product),
        error=None
    )
