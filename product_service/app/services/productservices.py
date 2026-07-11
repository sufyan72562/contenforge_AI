from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.core.exceptions import AppException

# GET ALL PRODUCTS FOR CURRENT USER
def get_all_products(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    """Get all products for the current user with pagination"""
    query = db.query(Product).filter(Product.user_id == user_id)
    total = query.count()
    products = query.offset(skip).limit(limit).all()
    return products, total

# GET PRODUCT BY ID (with ownership check)
def get_product(db: Session, product_id: int, user_id: int):
    """Get product by ID, ensure it belongs to current user"""
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.user_id == user_id
    ).first()
    
    if not product:
        raise AppException("Product not found", 404)
    return product

# GET PRODUCT BY PRODUCT_ID (with ownership check)
def get_product_by_product_id(db: Session, product_id: str, user_id: int):
    """Get product by custom product_id, ensure it belongs to current user"""
    product = db.query(Product).filter(
        Product.product_id == product_id,
        Product.user_id == user_id
    ).first()
    
    if not product:
        raise AppException("Product not found", 404)
    return product

# CREATE PRODUCT
def create_product(db: Session, product: ProductCreate, user_id: int):
    """Create a new product for the current user"""
    # Check if product_id already exists for this user
    existing_product = db.query(Product).filter(
        Product.product_id == product.product_id,
        Product.user_id == user_id
    ).first()
    
    if existing_product:
        raise AppException("Product with this ID already exists for your account", 400)
    
    db_product = Product(
        product_id=product.product_id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        user_id=user_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# UPDATE PRODUCT
def update_product(db: Session, product_id: int, product_data: ProductUpdate, user_id: int):
    """Update product, only current user can update their products"""
    product = get_product(db, product_id, user_id)
    
    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

# DELETE PRODUCT
def delete_product(db: Session, product_id: int, user_id: int):
    """Delete product, only current user can delete their products"""
    product = get_product(db, product_id, user_id)
    
    db.delete(product)
    db.commit()
    return product

# SEARCH PRODUCTS BY NAME (current user only)
def search_products(db: Session, user_id: int, query: str, skip: int = 0, limit: int = 10):
    """Search products by name for current user"""
    q = db.query(Product).filter(
        Product.user_id == user_id,
        Product.name.ilike(f"%{query}%")
    )
    total = q.count()
    products = q.offset(skip).limit(limit).all()
    return products, total
