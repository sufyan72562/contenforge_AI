from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class PaginationParams(BaseModel):
    """Global pagination parameters"""
    skip: int = 0
    limit: int = 10
    
    class Config:
        ge = 0


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper"""
    success: bool = True
    message: str
    data: List[T]
    pagination: Optional[dict] = None
    
    def __init__(self, 
                 success: bool = True,
                 message: str = "Data retrieved successfully",
                 data: List[T] = None,
                 skip: int = 0,
                 limit: int = 10,
                 total: int = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.success = success
        self.message = message
        self.data = data or []
        
        # Add pagination metadata if total count is provided
        if total is not None:
            self.pagination = {
                "skip": skip,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit  # Ceiling division
            }


def get_pagination_params(skip: int = 0, limit: int = 10) -> tuple:
    """
    Validate and return pagination parameters
    
    Args:
        skip: Number of records to skip (default: 0)
        limit: Number of records to return (default: 10, max: 100)
    
    Returns:
        tuple: (skip, limit)
    """
    if skip < 0:
        skip = 0
    if limit < 1:
        limit = 1
    if limit > 100:
        limit = 100
    
    return skip, limit
