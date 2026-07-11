# Pagination Utility Usage Guide

The `app/core/pagination.py` module provides a reusable pagination system that can be used across all modules.

## Components

### 1. `get_pagination_params(skip: int, limit: int) -> tuple`
Validates and normalizes pagination parameters
```python
from app.core.pagination import get_pagination_params

skip, limit = get_pagination_params(skip=request.skip, limit=request.limit)
# Ensures: skip >= 0, 1 <= limit <= 100
```

### 2. `PaginatedResponse` - Generic Response Wrapper
```python
from app.core.pagination import PaginatedResponse
from app.schemas.product import ProductResponse

response = PaginatedResponse(
    success=True,
    message="Products retrieved",
    data=products,
    skip=0,
    limit=10,
    total=50
)
# Returns pagination metadata automatically
```

## Example: Usage in Other Service Modules

```python
# In another service - e.g., order_service
from sqlalchemy.orm import Session
from app.core.pagination import get_pagination_params

def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    skip, limit = get_pagination_params(skip, limit)
    
    query = db.query(Order).filter(Order.user_id == user_id)
    total = query.count()
    orders = query.offset(skip).limit(limit).all()
    
    return orders, total
```

## Pagination Response Format

When using `PaginatedResponse` with total count, the response includes metadata:

```json
{
  "success": true,
  "message": "Products retrieved successfully",
  "data": [...],
  "pagination": {
    "skip": 0,
    "limit": 10,
    "total": 50,
    "pages": 5
  }
}
```

## Best Practices

1. Always validate pagination params using `get_pagination_params()`
2. Return both items AND total count from service functions
3. Let `PaginatedResponse` handle metadata generation
4. Keep pagination logic consistent across all modules
