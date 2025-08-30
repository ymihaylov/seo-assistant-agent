# Routers package

"""
API endpoints package initialization.
"""
from fastapi import APIRouter


from .home import router as home_router

# Create main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(home_router)

# Export for easy import
__all__ = ["api_router"]
