from fastapi import APIRouter

from app.router.v1_router import api_v1_router
from app.router.admin_router import api_admin_router

api_router = APIRouter(prefix='/api')
api_router.include_router(api_v1_router)
api_router.include_router(api_admin_router)
