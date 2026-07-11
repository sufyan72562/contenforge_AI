class RepositoryError(Exception):
    """Base exception for repository operations."""


class ProductKnowledgeRepositoryError(RepositoryError):
    """Raised when product knowledge cannot be loaded."""