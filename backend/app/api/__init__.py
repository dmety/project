from fastapi import APIRouter
from app.api import auth, profile, resource, path, tutor, evaluation, permission

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(profile.router)
api_router.include_router(resource.router)
api_router.include_router(path.router)
api_router.include_router(tutor.router)
api_router.include_router(evaluation.router)
api_router.include_router(permission.router)

__all__ = ["api_router"]
